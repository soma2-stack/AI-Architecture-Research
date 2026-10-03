"""Center norm with the ACTUAL archived dense R:
   R = (R0 + J/(1e8 n^3)) * a / ||R0 + J/(1e8 n^3)||_op.
(i) float64 dense matrix, direct evaluation of PROOF eq (1) and a forward tanh
    simulation of the whole center history (h_T=0 check, past-cube check);
(ii) high-precision closed form for the same R using the exact structure
    (raw = R0 + eps*11^T, top singular value from a rank-2 secular equation),
    so E_R - E0 is resolved far below Delta_n.
"""
import numpy as np
import mpmath as mp

mp.mp.dps = 60


def build(n):
    k, l, d = n // 2, n - n // 2, n // 4
    a = 1 - 1 / n
    w = -np.ones(k) / np.sqrt(k)
    w[0] += 1
    U = np.eye(k) - 2 * np.outer(w, w) / (w @ w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)  # (Pv)(i) = v(i-1)
    O = U @ P @ U
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O
    R0[k:, k:] = np.eye(l) / (100 * n)
    raw = R0 + np.ones((n, n)) / (1e8 * n**3)
    R = raw * (a / np.linalg.norm(raw, 2))
    return k, l, d, a, w, U, P, O, R0, R


def closed_form_highprec(n):
    nn = mp.mpf(n)
    k, l, d = n // 2, n - n // 2, n // 4
    a, lam = 1 - 1 / nn, 1 / (100 * nn)
    eps = 1 / (mp.mpf(10)**8 * nn**3)
    b0, s, z0 = mp.mpf(1) / 20, mp.mpf(2) / 5, mp.mpf(3) / 20
    beta = mp.sqrt(z0 / nn)
    A, B = mp.atanh(s), mp.atanh(beta)
    N = int(mp.ceil(4 * nn * mp.log(nn))) + 1

    # top eigenvalue mu of raw^T raw = D + eps(g1^T+1g^T) + eps^2 n 11^T,
    # D = diag(a^2 I_k, lam^2 I_l), g = R0^T 1 = (a O^T 1_k, lam 1_l), 1_k^T O^T 1_k = 0.
    # Q maps into V=span{(1_k,0),(O^T1_k,0),(0,1_l)} which D preserves; orthonormal basis u1,u2,u3.
    one = mp.matrix([mp.sqrt(k), 0, mp.sqrt(l)])
    gg = mp.matrix([0, a * mp.sqrt(k), lam * mp.sqrt(l)])
    MV = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            MV[i, j] = eps * (gg[i] * one[j] + one[i] * gg[j]) + eps**2 * nn * one[i] * one[j]
    MV[0, 0] += a**2; MV[1, 1] += a**2; MV[2, 2] += lam**2
    ev = mp.eigsy(MV)[0]
    mu = max(max(ev[i] for i in range(3)), a**2)
    sig = mp.sqrt(mu)
    c = a / sig
    # actual R = c (R0 + eps J)
    # R p, R v; p=(0_k, s 1_l), v=(beta 1_k, s 1_l)
    mp_ = s * l                      # 1^T p
    mv = beta * k + s * l            # 1^T v
    # term1: atanh(p) - b0
    t1 = k * b0**2 + l * (A - b0)**2
    # term2: q - R p ; memory: (B-b0 - c eps mp_) 1_k ; source: (A-b0 - c lam s - c eps mp_) 1_l
    t2 = k * (B - b0 - c * eps * mp_)**2 + l * (A - b0 - c * lam * s - c * eps * mp_)**2
    # term3: q - R v ; memory (B-b0-c eps mv)1_k - c a beta O1_k (orthogonal pieces, ||O1_k||^2=k)
    t3 = k * ((B - b0 - c * eps * mv)**2 + (c * a * beta)**2) + l * (A - b0 - c * lam * s - c * eps * mv)**2
    # term4: R v + b0 1 ; memory (c eps mv + b0) 1_k + c a beta O1_k
    t4 = k * ((c * eps * mv + b0)**2 + (c * a * beta)**2) + l * (c * lam * s + c * eps * mv + b0)**2
    ER = mp.sqrt(t1 + t2 + (N - 1) * t3 + t4)
    E0 = mp.sqrt(k * (2 * b0**2 + N * ((B - b0)**2 + a**2 * beta**2)) +
                 l * ((A - b0)**2 + N * (A - b0 - lam * s)**2 + (b0 + lam * s)**2))
    en = 4 / (mp.mpf(10)**8 * nn**2)
    Delta = en * mp.sqrt(s**2 * l + N * (beta**2 * k + s**2 * l))
    # ||R - R0||_op <= |c-1| a + c eps n  (R0 has norm a, J has norm n)
    RmR0_bound = abs(c - 1) * a + c * eps * nn
    return dict(N=N, sig=sig, c=c, ER=ER, E0=E0, Delta=Delta, RmR0_bound=RmR0_bound, en=en)


if __name__ == "__main__":
  for n in (200, 256, 400):
      k, l, d, a, w, U, P, O, R0, R = build(n)
      ones = np.ones(k)
      gam = 2 / (w @ w)
      e = np.eye(k)
      # identities (2) and the explicit forms of O 1_k and O^T 1_k
      id_orth = ones @ O @ ones
      id_norm = np.linalg.norm(O @ ones)**2 - k
      O1_form = np.linalg.norm(O @ ones - (np.sqrt(k) * e[1] + gam * w))
      OT1_form = np.linalg.norm(O.T @ ones - (np.sqrt(k) * e[d - 1] + gam * w))
      Oe0 = np.linalg.norm(O @ e[0] - e[0])
      s, b0 = 0.4, 0.05
      beta = np.sqrt(0.15 / n)
      N = int(np.ceil(4 * n * np.log(n))) + 1
      p = np.r_[np.zeros(k), np.full(l, s)]
      v = np.r_[np.full(k, beta), np.full(l, s)]
      q = np.arctanh(v) - b0

      def E1(Rm):
          return np.sqrt(np.linalg.norm(np.arctanh(p) - b0)**2 + np.linalg.norm(q - Rm @ p)**2
                         + (N - 1) * np.linalg.norm(q - Rm @ v)**2 + np.linalg.norm(Rm @ v + b0)**2)

      ER_f = E1(R)
      E0_f = E1(R0)
      eR_f = np.linalg.norm(R - R0, 2)
      # forward simulation of the whole center history with the actual R
      h = np.zeros(n)
      tot = 0.0
      maxabs = 0.0
      targets = [p] + [v] * N + [np.zeros(n)]
      for tgt in targets:
          x = np.arctanh(tgt) - R @ h - b0
          maxabs = max(maxabs, np.max(np.abs(x)))
          tot += x @ x
          h = np.tanh(R @ h + x + b0)
      hT = np.max(np.abs(h))
      HP = closed_form_highprec(n)
      print(f"n={n} N={N} T={len(targets)}")
      print(f"  identities: 1^T O 1={id_orth:.2e}  ||O1||^2-k={id_norm:.2e}  O1=sqrt(k)e1+gam w err={O1_form:.2e}"
            f"  O^T1=sqrt(k)e_(d-1)+gam w err={OT1_form:.2e}  ||Oe0-e0||={Oe0:.2e}")
      print(f"  float64: E(R0)={E0_f:.12f}  E(R)={ER_f:.12f}  E(R)-E(R0)={ER_f - E0_f:.3e}  ||R-R0||op={eR_f:.3e}  e_n={4e-8 / n**2:.3e}")
      print(f"  forward sim: sqrt(sum x^2)={np.sqrt(tot):.12f}  max|h_T|={hT:.2e}  max|x_i|={maxabs:.4f} (<0.5?)")
      print(f"  high-prec: E0={mp.nstr(HP['E0'], 25)}  E_R={mp.nstr(HP['ER'], 25)}")
      print(f"     E_R-E0={mp.nstr(HP['ER'] - HP['E0'], 6)}  Delta_n={mp.nstr(HP['Delta'], 6)}  ratio={mp.nstr((HP['ER'] - HP['E0']) / HP['Delta'], 6)}")
      print(f"     ||raw||-a={mp.nstr(HP['sig'] - (1 - mp.mpf(1) / n), 6)} (float64: {np.linalg.norm(R0 + np.ones((n, n)) / (1e8 * n**3), 2) - (1 - 1 / n):.3e})"
            f"  ||R-R0|| upper={mp.nstr(HP['RmR0_bound'], 6)} vs e_n={mp.nstr(HP['en'], 6)}")
