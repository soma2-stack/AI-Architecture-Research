"""Matrix-free, equation-faithful frozen R0 reference and controlled histories.

Sources: unpaired-corridor PROOF §§1-5,8-10; holding-cost PROOF §4;
linear-frontier PROOF §§3,4,6,8-10; Route-7A PROOF §11.1.
Small-width algebra is executable; asymptotic robust sections are NOT certified.
R0 and an optional caller-supplied R_actual remain separately identified.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import NamedTuple

import torch
from torch import Tensor, nn


def positive_integer(value, name, minimum=1):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def finite_tensor(x, shape, reference, name):
    if (not isinstance(x, Tensor) or tuple(x.shape) != tuple(shape)
            or x.dtype != reference.dtype or x.device != reference.device
            or not torch.isfinite(x).all()):
        raise ValueError(f"{name} must match shape {shape}, dtype/device and be finite")


class CorridorOperator(nn.Module):
    """Exact O*=C+1u^T+e1 v_H^T, O(r*p) arithmetic and O(r) constants.

Input coordinate axis is FIRST, including matrix responses [r,p].
Physical coordinate j=1 is tensor row 0; physical d-1 is row d-2.
"""
    def __init__(self, n: int, *, dtype=torch.float64):
        super().__init__()
        positive_integer(n, "n", 16)
        if dtype not in (torch.float32, torch.float64):
            raise ValueError("reference requires float32 or float64")
        self.n, self.k, self.d, self.r = n, n//2, n//4, n//2-1
        self.a = 1-1/n
        self.gamma = gamma = 1/(1-1/math.sqrt(self.k))
        u = torch.full((self.r,), -gamma**2/self.k, dtype=dtype)
        u[self.d-2] += gamma/math.sqrt(self.k)
        self.register_buffer("u", u)
        self.register_buffer("v_h", torch.full_like(u, gamma/math.sqrt(self.k)))

    def local(self, x: Tensor, *, transpose=False):
        z = torch.zeros_like(x)
        if transpose:
            z[:self.d-2] = x[1:self.d-1]
        else:
            z[1:self.d-1] = x[:self.d-2]
        z[self.d-1:] = x[self.d-1:]
        return z

    def forward(self, x: Tensor, *, transpose=False):
        if (x.ndim < 1 or x.shape[0] != self.r or x.dtype != self.u.dtype
                or x.device != self.u.device):
            raise ValueError("operator input must have coordinate axis first and matching dtype/device")
        expand = (self.r,)+(1,)*(x.ndim-1)
        if transpose:
            return self.local(x, transpose=True)+self.u.reshape(expand)*x.sum(0)+self.v_h.reshape(expand)*x[0]
        j = torch.tensordot(self.u, x, dims=1)
        b = torch.tensordot(self.v_h, x, dims=1)
        z = self.local(x)+j
        # Avoid a mutation of a graph value used by another branch.
        e = torch.zeros_like(self.u); e[0] = 1
        return z+e.reshape(expand)*b


class RenewalState(NamedTuple):
    local: Tensor
    feedback: Tensor
    steps: int

    @property
    def response(self):
        return self.local+self.feedback


class CorridorCreditEngine(nn.Module):
    """Exact streaming L/H renewal; all J and B parameter columns retained.

Persistent credit: 2*r*p values plus one public step count. No low-dimensional
compression is claimed. Forward hidden memory is a separate n values.
"""
    def __init__(self, n, *, dtype=torch.float64):
        super().__init__()
        self.op = CorridorOperator(n, dtype=dtype)

    def initial_state(self, probes: Tensor):
        if not isinstance(probes, Tensor) or probes.ndim != 2 or probes.shape[1] < 1:
            raise ValueError("probes must be [r,positive p]")
        finite_tensor(probes, (self.op.r,probes.shape[1]), self.op.u, "probes")
        return RenewalState(torch.zeros_like(probes), torch.zeros_like(probes), 0)

    def scan(self, gates: Tensor, probes: Tensor, state=None, *, return_history=False):
        if not isinstance(probes, Tensor) or probes.ndim != 2 or probes.shape[1] < 1:
            raise ValueError("probes must be [r,positive p]")
        finite_tensor(probes, (self.op.r,probes.shape[1]), self.op.u, "probes")
        if not isinstance(gates, Tensor) or gates.ndim != 2:
            raise ValueError("gates must be [time,r]")
        finite_tensor(gates, (gates.shape[0],self.op.r), self.op.u, "gates")
        if ((gates < 0) | (gates > 1)).any():
            raise ValueError("gates must lie in [0,1]")
        state = self.initial_state(probes) if state is None else state
        for x in (state.local,state.feedback):
            finite_tensor(x, probes.shape, self.op.u, "credit state")
        history = [state.response] if return_history else None
        for g in gates:
            j = self.op.u @ state.response
            b = self.op.v_h @ state.response
            e = torch.zeros_like(self.op.u); e[0] = 1
            local = g[:,None]*(self.op.a*self.op.local(state.local)+probes)
            feedback = self.op.a*g[:,None]*(self.op.local(state.feedback)+j[None,:]+e[:,None]*b[None,:])
            state = RenewalState(local,feedback,state.steps+1)
            if history is not None:
                history.append(state.response)
        return (state,torch.stack(history)) if return_history else state


class FrozenTanhReference(nn.Module):
    """h'=tanh(R h+x+.05), R0=diag(a U P U,lambda I), W=I.

Every R,W,b entry may be independently differentiated by direction probes.
Base parameters are frozen buffers. The inverse controller is never part of
the fixed-input derivative. Dense R_actual must be supplied and validated;
we do not invent a missing dense realization. Default is explicitly R0.
"""
    def __init__(self, n: int, *, actual_recurrent: Tensor | None = None, dtype=torch.float64):
        super().__init__()
        self.op = CorridorOperator(n, dtype=dtype)
        self.n, self.k, self.r, self.l = n, n//2, n//2-1, n-n//2
        self.a, self.lam, self.b0 = self.op.a, 1/(100*n), .05
        sigma = math.tanh(self.b0)
        for _ in range(32):  # fixed scalar contraction solve, not learning
            sigma = math.tanh(self.lam*sigma+self.b0)
        self.sigma = sigma
        self.register_buffer("bias", torch.full((n,), self.b0, dtype=dtype))
        self.register_buffer("actual", None)
        if actual_recurrent is not None:
            finite_tensor(actual_recurrent, (n,n), self.bias, "R_actual")
            base = self.dense_recurrent()
            discrepancy = torch.linalg.matrix_norm(actual_recurrent-base, ord=2).item()
            norm = torch.linalg.matrix_norm(actual_recurrent, ord=2).item()
            tolerance = 32*torch.finfo(dtype).eps
            if discrepancy > 4/(1e8*n*n)+tolerance or abs(norm-self.a) > tolerance:
                raise ValueError("R_actual must meet the source operator-norm and perturbation bounds")
            self.actual = actual_recurrent.detach().clone()

    @property
    def realization(self):
        return "R0_reference" if self.actual is None else "caller_supplied_R_actual"

    def reference_apply(self, x: Tensor, *, transpose=False):
        return torch.cat((self.a*x[:1],self.a*self.op(x[1:self.k],transpose=transpose),self.lam*x[self.k:]),dim=0)

    def apply_recurrent(self, x: Tensor, *, transpose=False):
        if self.actual is None:
            return self.reference_apply(x,transpose=transpose)
        return (self.actual.T if transpose else self.actual) @ x

    def dense_recurrent(self):
        """O(n^2) allocation, only for small audit or explicit dense realization."""
        return self.apply_recurrent(torch.eye(self.n,dtype=self.bias.dtype,device=self.bias.device))

    def recurrent_normalization(self):
        norm_f = (math.sqrt(self.k*self.a**2+self.l*self.lam**2) if self.actual is None
                  else torch.linalg.vector_norm(self.actual).item())
        beta = max(1.,norm_f)
        return {"R_group_RMS":norm_f/self.n,"loss_divisor":beta,
                "R_group_over_loss":norm_f/(self.n*beta),
                "independently_differentiated_R_W_b_entries":2*self.n**2+self.n,
                "normalizers_are_differentiated":False}

    def initial_state(self):
        return torch.zeros_like(self.bias)

    def step(self, x: Tensor, h: Tensor):
        finite_tensor(x, (self.n,), self.bias, "input")
        finite_tensor(h, (self.n,), self.bias, "state")
        return torch.tanh(self.apply_recurrent(h)+x+self.bias)

    def scan(self, inputs: Tensor, state=None, *, return_history=False):
        if not isinstance(inputs, Tensor) or inputs.ndim != 2:
            raise ValueError("inputs must be [time,n]")
        finite_tensor(inputs, (inputs.shape[0],self.n), self.bias, "inputs")
        h = self.initial_state() if state is None else state
        finite_tensor(h, (self.n,), self.bias, "state")
        history = [h] if return_history else None
        for x in inputs:
            h = self.step(x,h)
            if history is not None:
                history.append(h)
        return (h,torch.stack(history)) if return_history else h

    def fixed_source_scan(self, inputs: Tensor, probes: Tensor, *, state=None, sensitivity=None):
        """Complete physical [n,p] sensitivity for delta R=V_full f_s^T.

        Probes [r,p] are embedded with E; probes [n,p] include every row,
        including public source/e0 directions and their dense coupling.
        Includes preparation, all feedback, and source/e0 leakage if R_actual is used.
State/sensitivity may resume streaming; inputs must already be realized.
"""
        if not isinstance(probes, Tensor) or probes.ndim != 2 or probes.shape[1] < 1:
            raise ValueError("probes must be [r or n,positive p]")
        if probes.shape[0] not in (self.r,self.n):
            raise ValueError("probe row count must be r or n")
        finite_tensor(probes,probes.shape,self.bias,"probes")
        if inputs.ndim != 2:
            raise ValueError("inputs must be [time,n]")
        finite_tensor(inputs,(inputs.shape[0],self.n),self.bias,"inputs")
        h = self.initial_state() if state is None else state
        s = self.bias.new_zeros(self.n,probes.shape[1]) if sensitivity is None else sensitivity
        finite_tensor(h,(self.n,),self.bias,"state")
        finite_tensor(s,(self.n,probes.shape[1]),self.bias,"sensitivity")
        for x in inputs:
            forcing = probes*(h[self.k:].sum()/math.sqrt(self.l))
            if probes.shape[0]==self.r:
                forcing = torch.cat((torch.zeros_like(s[:1]),forcing,torch.zeros_like(s[self.k:])))
            hn = self.step(x,h)
            s = (1-hn.square())[:,None]*(self.apply_recurrent(s)+forcing)
            h = hn
        return h,s

    def directional_scan(self, inputs: Tensor, dR: Tensor, dW: Tensor, db: Tensor):
        """Equation (1) for arbitrary independent R/W/b directions, raw units.

Direction axis FIRST: dR,dW [p,n,n], db [p,n]. No group scaling for
W/b is invented here; the fixed-source recurrent query uses its exact scale.
"""
        p = db.shape[0]
        for x,shape,name in ((dR,(p,self.n,self.n),"dR"),(dW,(p,self.n,self.n),"dW"),(db,(p,self.n),"db")):
            finite_tensor(x,shape,self.bias,name)
        finite_tensor(inputs,(inputs.shape[0],self.n),self.bias,"inputs")
        h, s = self.initial_state(), self.bias.new_zeros(self.n,p)
        for x in inputs:
            injection = (torch.einsum('pij,j->ip',dR,h)+torch.einsum('pij,j->ip',dW,x)+db.T)
            hn = self.step(x,h)
            s = (1-hn.square())[:,None]*(self.apply_recurrent(s)+injection)
            h = hn
        return h,s

    def realize_query(self, endpoint: Tensor, preactivations: Tensor):
        """Legal future raw inputs; detach before any parameter differentiation."""
        self.validate_query(preactivations)
        finite_tensor(endpoint,(self.n,),self.bias,"endpoint")
        h, inputs = endpoint.detach(), []
        for z in preactivations.detach():
            inputs.append(z-self.apply_recurrent(h)-self.bias)
            h = torch.tanh(z)
        return torch.stack(inputs).detach()

    def validate_query(self, preactivations: Tensor):
        if not isinstance(preactivations, Tensor) or preactivations.ndim != 2 or preactivations.shape[0] < 1:
            raise ValueError("query must have at least one future step")
        finite_tensor(preactivations,(preactivations.shape[0],self.n),self.bias,"query")
        if ((preactivations < .25) | (preactivations > .75)).any():
            raise ValueError("legal query preactivations must lie in [.25,.75]")

    def query_adjoint(self, preactivations: Tensor):
        """Unnormalized head pullback through every future chronological step."""
        self.validate_query(preactivations)
        c = torch.ones_like(self.bias)/math.sqrt(self.n)
        for z in reversed(preactivations.unbind()):
            c = self.apply_recurrent((1-torch.tanh(z).square())*c,transpose=True)
        return c

    def normalized_past_answer(self, sensitivity: Tensor, preactivations: Tensor):
        """Selected recurrent-group past contribution: S^T c / n.

Future direct terms cancel only for histories with the SAME actual endpoint.
This is one supplied legal query, a lower witness for a supremum, never D.
"""
        finite_tensor(sensitivity,(self.n,sensitivity.shape[1]),self.bias,"sensitivity")
        return sensitivity.T @ self.query_adjoint(preactivations)/self.n


@dataclass(frozen=True)
class FourSiteGeometry:
    n: int
    tuples: int
    interior_steps: int
    require_proof_margin: bool = False

    def __post_init__(self):
        positive_integer(self.n,"n",16)
        positive_integer(self.tuples,"tuples")
        positive_integer(self.interior_steps,"interior_steps")
        s = self.tuples+self.interior_steps+4
        if 5*s+self.tuples+self.interior_steps+1 >= self.n//4:
            raise ValueError("corridor tracks must not wrap or reach terminal/front")
        if 2*self.tuples >= self.n//2-self.n//4-1:
            raise ValueError("insufficient stationary compensator and bath sites")
        if self.require_proof_margin and (self.n < 10**6 or s > (self.n//4)/100):
            raise ValueError("source lift premises require n>=10^6 and S<=d/100")

    @property
    def proof_lift_premises_met(self):
        return self.n >= 10**6 and self.tuples+self.interior_steps+4 <= (self.n//4)/100

    def sites(self, time: int, *, device=None):
        if not isinstance(time,int) or not 0 <= time <= self.interior_steps+1:
            raise ValueError("time outside prepared/interior/reset geometry")
        s, m = self.tuples+self.interior_steps+4, self.tuples
        i = torch.arange(1,m+1,device=device)
        return torch.stack((2*s+i+time,5*s+i+time,self.n//4+2*(i-1),self.n//4+2*(i-1)+1),dim=1)


@dataclass
class RealizedHistory:
    inputs: Tensor          # prep, T interiors, reset; every correction counted
    states: Tensor          # includes zero start
    gates: Tensor           # all full-state gates, including prep/reset
    geometry: FourSiteGeometry
    phases: tuple[str,...]

    def cost(self):
        return {"n":self.geometry.n,"m":self.geometry.tuples,"T":self.geometry.interior_steps,
                "mT":self.geometry.tuples*self.geometry.interior_steps,
                "raw_history_l2_measured":self.inputs.norm().item(),
                "max_abs_raw_input_measured":self.inputs.abs().max().item(),
                "past_cube_valid_measured":bool((self.inputs.abs()<.5).all()),
                "source_lift_premises_met":self.geometry.proof_lift_premises_met,
                "history_storage_bytes":sum(x.numel()*x.element_size() for x in (self.inputs,self.states,self.gates)),
                "robust_dimension":"NOT CERTIFIED"}


def realize_four_site_history(model: FrozenTanhReference, geometry: FourSiteGeometry,
                              tuple_gates: Tensor, *, phases=None, preparation_beta=.05):
    """Zero-start balanced lift, autonomous bath/front/source, common reset.

Nondriven saturated front states are advanced with tanh, never inverse tanh.
Controls are detached once realized. Preparation/source and actual dense
correction at EVERY coordinate are included in absolute raw-input costs.
"""
    if geometry.n != model.n:
        raise ValueError("model and geometry widths differ")
    finite_tensor(tuple_gates,(geometry.interior_steps,geometry.tuples),model.bias,"tuple gates")
    if ((tuple_gates <= .99) | (tuple_gates >= 1)).any():
        raise ValueError("balanced lift requires tuple gates strictly in (.99,1)")
    if not math.isfinite(preparation_beta) or not 0 < preparation_beta < .1:
        raise ValueError("preparation_beta must be in (0,.1)")
    phases = tuple(phases) if phases is not None else ("interior",)*geometry.interior_steps
    if len(phases) != geometry.interior_steps:
        raise ValueError("one phase per interior step is required")
    h, raw, states, gates = model.initial_state(), [], [model.initial_state()], []
    signs = model.bias.new_tensor((1.,1.,-1.,-1.))
    for time in range(geometry.interior_steps+2):
        zref = model.reference_apply(h)+model.bias
        target = torch.tanh(zref)
        xref = torch.zeros_like(h)
        sites = geometry.sites(time,device=h.device)
        if time == 0:
            values = preparation_beta*signs.expand(geometry.tuples,4)
            target[model.k:] = model.sigma
            xref[model.k:] = model.lam*model.sigma
        elif time <= geometry.interior_steps:
            values = torch.sqrt(1-tuple_gates[time-1])[:,None]*signs
        else:
            # An untouched stationary ordinary bath site supplies the public reset.
            values = target[model.k-1].expand(geometry.tuples,4)
        target[sites] = values
        xref[sites] = torch.atanh(values)-zref[sites]
        x = xref+model.reference_apply(h)-model.apply_recurrent(h)
        raw.append(x)
        h = target
        states.append(h)
        gates.append(1-h.square())
    return RealizedHistory(torch.stack(raw).detach(),torch.stack(states).detach(),
                           torch.stack(gates).detach(),geometry,("prepare",*phases,"reset"))


def orthonormal_probe_bank(geometry: FourSiteGeometry, groups: int, *, dtype=torch.float64):
    """Stationary donor/survivor bank V=W[I-(1-1/sqrt(2))11^T/K]."""
    m, r = geometry.tuples, geometry.n//2-1
    positive_integer(groups,"groups")
    if m%2 or (m//2)%groups:
        raise ValueError("half the tuples must divide evenly into donor groups")
    sites = geometry.sites(0)[:,2:]-1
    donors, survivors = sites[:m//2], sites[m//2:]
    s = torch.zeros(r,dtype=dtype); s[survivors.flatten()] = 1/math.sqrt(m)
    w = torch.zeros(r,groups,dtype=dtype)
    for j,block in enumerate(donors.chunk(groups)):
        w[block.flatten(),j] = 1/math.sqrt(m/groups)
    w -= s[:,None]/math.sqrt(groups)
    h = torch.eye(groups,dtype=dtype)-(1-1/math.sqrt(2))*torch.ones(groups,groups,dtype=dtype)/groups
    return w @ h


def survivor_walsh(geometry: FourSiteGeometry, labels: tuple[int,...], time: int, *, dtype=torch.float64):
    """Characters repeated on all four sites of each survivor tuple."""
    count = geometry.tuples//2
    if geometry.tuples%2 or count&(count-1):
        raise ValueError("survivor tuple count must be a power of two")
    if len(set(labels)) != len(labels) or any(not isinstance(j,int) or j <= 0 or j >= count for j in labels):
        raise ValueError("distinct nonzero Walsh labels below survivor tuple count required")
    rows = torch.zeros(len(labels),geometry.n//2-1,dtype=dtype)
    sites = geometry.sites(time)[count:]-1
    for e,label in enumerate(labels):
        signs = torch.tensor([1 if (label&i).bit_count()%2==0 else -1 for i in range(count)],dtype=dtype)
        rows[e,sites] = signs[:,None]/math.sqrt(4*count)
    return rows


def trace_neutral_triple(tau: Tensor, control: Tensor, a: float, g_high: float,
                         *, center=.9975, amplitude=1e-4):
    """Route-7A equation (25): exact local trace correction, not feedback reset."""
    if (tau.shape != control.shape or tau.dtype != control.dtype or tau.device != control.device
            or not torch.isfinite(tau).all() or not torch.isfinite(control).all()
            or (tau < 0).any() or (control.abs()>1).any()
            or not 0<a<1 or not .99<g_high<1
            or not math.isfinite(center) or not math.isfinite(amplitude)
            or amplitude<=0 or not .99<center-amplitude<center+amplitude<1):
        raise ValueError("invalid trace-neutral parameters")
    d1 = center+amplitude*control
    target = center*(1+a*g_high*(1+a*center*(1+a*tau)))
    d3 = target/(1+a*g_high*(1+a*d1*(1+a*tau)))
    schedule = torch.stack((d1,torch.full_like(d1,g_high),d3))
    if ((schedule <= .99) | (schedule >= 1)).any():
        raise ValueError("trace-neutral correction outside admitted gate interval")
    return schedule,target


def early_capture_schedule(n: int, tuples: int, controls: Tensor, labels: tuple[int,...],
                            *, write_steps: int, tail_steps: int, clear_steps: int):
    """Executable chronology: write -> ONE capture -> tail/repair -> clear.

Durations are finite diagnostic inputs, NOT the asymptotic theorem calibration.
Retains public donor traces between stages. Rejects illegal finite corrections.
"""
    positive_integer(n,"n",16)
    positive_integer(tuples,"tuples",2)
    for value,name in ((write_steps,"write_steps"),(tail_steps,"tail_steps"),(clear_steps,"clear_steps")):
        positive_integer(value,name)
    if (controls.ndim != 2 or controls.shape[0] != len(labels) or controls.shape[1] < 1
            or not torch.isfinite(controls).all() or (controls.abs()>1).any()):
        raise ValueError("controls must be finite [stages,groups] in [-1,1]")
    groups, count = controls.shape[1], tuples//2
    if tuples%2 or count%groups or count&(count-1):
        raise ValueError("equal donor groups and power-of-two survivor count required")
    if len(set(labels)) != len(labels) or any(j<=0 or j>=count for j in labels):
        raise ValueError("invalid capture labels")
    a, gh, gl = 1-1/n, 1-1/(n*n), .995
    tau = torch.zeros(groups,dtype=controls.dtype,device=controls.device)
    public_tau = torch.zeros_like(tau)
    rows, phases, corrections = [], [], []
    def append(donor_gate, survivor_gate, phase):
        nonlocal tau,public_tau
        rows.append(torch.cat((donor_gate.repeat_interleave(count//groups),survivor_gate)))
        phases.append(phase)
        tau = donor_gate*(1+a*tau)
        public_tau = gl*(1+a*public_tau)
    high_survivors = torch.full((count,),gh,dtype=controls.dtype,device=controls.device)
    low_donors = torch.full_like(tau,gl)
    for control,label in zip(controls,labels):
        donor = gl+(control+1)*(gh-gl)/2
        for _ in range(write_steps):
            append(donor,high_survivors,"write")
        chi = torch.tensor([1 if (label&i).bit_count()%2==0 else -1 for i in range(count)],device=controls.device)
        append(low_donors,torch.where(chi>0,high_survivors,torch.full_like(high_survivors,gl)),"capture")
        for _ in range(tail_steps-1):
            append(low_donors,high_survivors,"trace_tail")
        correction = gl*(1+a*public_tau)/(1+a*tau)
        if ((correction<=.99) | (correction>=1)).any():
            raise ValueError("finite tail too short for a legal trace correction")
        append(correction,high_survivors,"trace_correction")
        corrections.append((tau-public_tau).abs().max().item())
        for _ in range(clear_steps):
            append(low_donors,high_survivors,"clear")
    return torch.stack(rows),tuple(phases),{"donor_trace_match_errors":corrections,
            "calibration":"finite diagnostic durations; asymptotic margin NOT CERTIFIED"}


def trace_neutral_schedule(n: int, tuples: int, controls: Tensor, labels: tuple[int,...],
                           *, precharge_steps: int, release_steps=0):
    """Exact Route-7A local protocol with high-donor capture and NO final clear.

Every precharge/release step is counted. Complete donor feedback survives;
the missing robust-margin theorem remains an OPEN_MECHANISMS obligation.
"""
    positive_integer(n,"n",16)
    positive_integer(tuples,"tuples",2)
    positive_integer(precharge_steps,"precharge_steps")
    positive_integer(release_steps,"release_steps",0)
    if (not isinstance(controls,Tensor) or controls.ndim!=2 or controls.shape[0]!=len(labels)
            or controls.shape[1]<1 or not torch.isfinite(controls).all() or (controls.abs()>1).any()):
        raise ValueError("controls must be finite [stages,groups] in [-1,1]")
    groups,count=controls.shape[1],tuples//2
    if tuples%2 or count%groups or count&(count-1):
        raise ValueError("equal donor groups and power-of-two survivor count required")
    if len(set(labels))!=len(labels) or any(j<=0 or j>=count for j in labels):
        raise ValueError("invalid capture labels")
    a,gh,gl=1-1/n,1-1/n**2,.995
    tau=torch.zeros(groups,dtype=controls.dtype,device=controls.device)
    high=torch.full((tuples,),gh,dtype=controls.dtype,device=controls.device)
    rows,phases,errors=[],[],[]
    for _ in range(precharge_steps):
        rows.append(high);phases.append("precharge");tau=gh*(1+a*tau)
    for control,label in zip(controls,labels):
        triple,target=trace_neutral_triple(tau,control,a,gh)
        for step,g in enumerate(triple):
            survivor=high[count:]
            if step==1:
                chi=torch.tensor([1 if (label&i).bit_count()%2==0 else -1 for i in range(count)],device=controls.device)
                survivor=torch.where(chi>0,survivor,torch.full_like(survivor,gl))
            rows.append(torch.cat((g.repeat_interleave(count//groups),survivor)))
            phases.append(("imprint","high_donor_capture","trace_correction")[step])
            tau=g*(1+a*tau)
        errors.append((tau-target).abs().max().item())
        for _ in range(release_steps):
            rows.append(high);phases.append("public_release");tau=gh*(1+a*tau)
    return torch.stack(rows),tuple(phases),{"local_trace_errors":errors,"final_clear":False,
               "robust_margin_status":"OPEN; feedback is not reset by local trace matching"}


@dataclass(frozen=True)
class ResearchGap:
    name: str
    missing_obligation: str

    def require_implementation(self):
        raise NotImplementedError(f"{self.name}: {self.missing_obligation}")


OPEN_MECHANISMS = (
    ResearchGap("strict_budget_linear_dimension","joint continuous robust section with D=Omega(n), mT=o(n^(3/2))"),
    ResearchGap("uncleared_route7a_feedback","robust joint margin or finite-error code for retained donor feedback"),
    ResearchGap("route6_complete_contract","consistent reader, chronological mass and full-query error allocation"),
    ResearchGap("exact_token_adapter","arbitrary-token transition preserving the specified mathematical invariants"),
)
