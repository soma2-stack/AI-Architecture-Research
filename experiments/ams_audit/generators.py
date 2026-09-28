"""
Benchmark Task Generators for Automated Mechanism Search (AMS) Audit.
Fulfills Stage 0 and Stage 1 verification under AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md.

Tasks implemented:
- Task B: Catastrophic Interference & Orthogonal Subspace Retention
- Task C*: Recurring-Regime Adaptation (no explicit boundary signal)
- Task F: Discrete Structural Commitment (3-bit parity with 90% train / 10% OOD shortcut)
- Task D: Optimization Conditioning Diagnostic (anisotropic Hessian ravines)
- Task A (Reserved): Long-Range Credit Transport (delayed bit-memorization)
- Task E (Reserved): Fast/Slow State & Multi-Timescale Binding
"""

import numpy as np
import torch
from typing import Tuple, Dict, Any, List, Optional


class TaskBGenerator:
    """
    Task B: Sequential regression on orthogonal subspaces with conflicting shared projection.
    Ambient dimension D=32, Subspace 1 has dims 0:16, Subspace 2 has dims 16:32.
    """
    def __init__(self, dim: int = 32, out_dim: int = 4, seed: int = 42):
        self.dim = dim
        self.half_dim = dim // 2
        self.out_dim = out_dim
        self.seed = seed
        self.rng = np.random.RandomState(seed)

        # Fixed random ground truth projections for Task 1 and Task 2
        self.W1 = self.rng.randn(self.half_dim, self.out_dim) / np.sqrt(self.half_dim)
        self.W2 = self.rng.randn(self.half_dim, self.out_dim) / np.sqrt(self.half_dim)

    def generate_task1_data(self, n_samples: int = 500) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate data for Task 1 (non-zero only in first half_dim)."""
        x_sub = self.rng.randn(n_samples, self.half_dim).astype(np.float32)
        y = x_sub @ self.W1.astype(np.float32)
        
        x = np.zeros((n_samples, self.dim), dtype=np.float32)
        x[:, :self.half_dim] = x_sub
        return torch.from_numpy(x), torch.from_numpy(y)

    def generate_task2_data(self, n_samples: int = 500) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate data for Task 2 (non-zero only in second half_dim)."""
        x_sub = self.rng.randn(n_samples, self.half_dim).astype(np.float32)
        y = x_sub @ self.W2.astype(np.float32)

        x = np.zeros((n_samples, self.dim), dtype=np.float32)
        x[:, self.half_dim:] = x_sub
        return torch.from_numpy(x), torch.from_numpy(y)


class TaskCStarGenerator:
    """
    Task C*: Recurring-Regime Adaptation without explicit boundary signals.
    Generates a stream of non-stationary regression problems where regimes recur.
    Regime 0: y = sin(w0 * x + phi0)
    Regime 1: y = sin(w1 * x + phi1)
    Pattern: Regime 0 -> Regime 1 -> Regime 0 (recurrence).
    No boundary signal or regime indicator is present in input x!
    """
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.RandomState(seed)
        
        self.w0, self.phi0 = 1.0, 0.0
        self.w1, self.phi1 = 2.5, np.pi / 3.0

    def generate_stream(self, n_phase0_a: int = 100, n_phase1: int = 50, n_phase0_b: int = 100
                        ) -> Dict[str, Any]:
        """
        Generates the sequential stream:
        Phase 0a (Regime 0) -> Phase 1 (Regime 1) -> Phase 0b (Regime 0 recurring).
        """
        # Phase 0a
        x_0a = self.rng.uniform(-1.0, 1.0, size=(n_phase0_a, 1)).astype(np.float32)
        y_0a = np.sin(self.w0 * x_0a + self.phi0).astype(np.float32)

        # Phase 1
        x_1 = self.rng.uniform(-1.0, 1.0, size=(n_phase1, 1)).astype(np.float32)
        y_1 = np.sin(self.w1 * x_1 + self.phi1).astype(np.float32)

        # Phase 0b (Regime 0 recurrence)
        x_0b = self.rng.uniform(-1.0, 1.0, size=(n_phase0_b, 1)).astype(np.float32)
        y_0b = np.sin(self.w0 * x_0b + self.phi0).astype(np.float32)

        # Held-out evaluation sets for measuring adaptation and recovery
        eval_x0 = self.rng.uniform(-1.0, 1.0, size=(200, 1)).astype(np.float32)
        eval_y0 = np.sin(self.w0 * eval_x0 + self.phi0).astype(np.float32)

        eval_x1 = self.rng.uniform(-1.0, 1.0, size=(200, 1)).astype(np.float32)
        eval_y1 = np.sin(self.w1 * eval_x1 + self.phi1).astype(np.float32)

        return {
            "stream_x": torch.from_numpy(np.vstack([x_0a, x_1, x_0b])),
            "stream_y": torch.from_numpy(np.vstack([y_0a, y_1, y_0b])),
            "phase_slices": {
                "phase_0a": slice(0, n_phase0_a),
                "phase_1": slice(n_phase0_a, n_phase0_a + n_phase1),
                "phase_0b": slice(n_phase0_a + n_phase1, n_phase0_a + n_phase1 + n_phase0_b)
            },
            "eval_regime0": (torch.from_numpy(eval_x0), torch.from_numpy(eval_y0)),
            "eval_regime1": (torch.from_numpy(eval_x1), torch.from_numpy(eval_y1))
        }


class TaskFGenerator:
    """
    Task F: Discrete Structural Commitment vs Continuous Spurious Shortcut.
    Input: Binary string x in {0, 1}^20.
    True invariant rule: y = x[0] ^ x[1] ^ x[2] (3-bit parity).
    Spurious shortcut feature: x[3].
      - In training set: P(x[3] == y) = 0.90 exactly.
      - In OOD test set: P(x[3] == y) = 0.10 exactly.
    Distractor features: x[4:20] ~ Bernoulli(0.5).
    """
    def __init__(self, dim: int = 20, seed: int = 42):
        self.dim = dim
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    def generate_data(self, n_samples: int, shortcut_prob: float) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Generate samples with exact shortcut_prob correlation for x[3] with y.
        """
        # Step 1: Generate independent random bits for the 3 structural features
        bits_structural = self.rng.randint(0, 2, size=(n_samples, 3))
        # Ground truth 3-bit parity
        y = bits_structural[:, 0] ^ bits_structural[:, 1] ^ bits_structural[:, 2]

        # Step 2: Construct the shortcut feature x[3] with exact ratio
        n_matching = int(round(n_samples * shortcut_prob))
        n_flipped = n_samples - n_matching

        match_mask = np.zeros(n_samples, dtype=bool)
        match_mask[:n_matching] = True
        self.rng.shuffle(match_mask)

        shortcut_feature = np.where(match_mask, y, 1 - y)

        # Step 3: Distractor features x[4:dim]
        n_distractors = self.dim - 4
        distractors = self.rng.randint(0, 2, size=(n_samples, n_distractors))

        # Assemble input x
        x = np.column_stack([bits_structural, shortcut_feature, distractors]).astype(np.float32)
        y = y.astype(np.float32)[:, None]

        return torch.from_numpy(x), torch.from_numpy(y)

    def generate_train_and_ood(self, n_train: int = 100, n_ood: int = 1000
                               ) -> Tuple[Tuple[torch.Tensor, torch.Tensor], Tuple[torch.Tensor, torch.Tensor]]:
        """
        Generates standard train set (shortcut_prob=0.90) and OOD test set (shortcut_prob=0.10).
        """
        train_x, train_y = self.generate_data(n_train, shortcut_prob=0.90)
        ood_x, ood_y = self.generate_data(n_ood, shortcut_prob=0.10)
        return (train_x, train_y), (ood_x, ood_y)


class TaskDGenerator:
    """
    Task D: Optimization Conditioning Diagnostic.
    Synthesizes ill-conditioned quadratic ravines with condition number kappa in [10^2, 10^8].
    Loss: L(theta) = 0.5 * (theta - theta^*)^T H (theta - theta^*)
    where H = Q Lambda Q^T with lambda_min = 1.0, lambda_max = kappa.
    """
    def __init__(self, dim: int = 32, kappa: float = 1e4, seed: int = 42):
        self.dim = dim
        self.kappa = kappa
        self.seed = seed
        self.rng = np.random.RandomState(seed)

        # Generate random orthogonal matrix Q via QR decomposition
        A = self.rng.randn(dim, dim)
        Q, _ = np.linalg.qr(A)
        self.Q = Q.astype(np.float32)

        # Logarithmically spaced eigenvalues from 1.0 to kappa
        eigenvalues = np.logspace(0, np.log10(kappa), num=dim).astype(np.float32)
        self.eigenvalues = eigenvalues
        self.H = (self.Q @ np.diag(eigenvalues) @ self.Q.T).astype(np.float32)
        self.theta_star = self.rng.randn(dim, 1).astype(np.float32)

    def loss(self, theta: torch.Tensor) -> torch.Tensor:
        """Computes 0.5 * (theta - theta_star)^T H (theta - theta_star)."""
        diff = theta - torch.from_numpy(self.theta_star)
        H_tensor = torch.from_numpy(self.H)
        return 0.5 * torch.sum(diff * (H_tensor @ diff))

    def grad(self, theta: torch.Tensor) -> torch.Tensor:
        """Computes exact gradient H (theta - theta_star)."""
        diff = theta - torch.from_numpy(self.theta_star)
        H_tensor = torch.from_numpy(self.H)
        return H_tensor @ diff


class ReservedTaskAGenerator:
    """
    Reserved Task A: Long-Range Credit Transport (Delayed Bit-Memorization).
    Sequence length T in {100, 250, 500, 1000}.
    At step t1 in [1, 5], 4-bit random trigger s in {-1, +1}^4 is presented with flag bit x[0]=1.0.
    Intermediate steps: Gaussian noise with x[0]=0.0.
    At step T: query token x[1]=1.0.
    Target: y = s at step T.
    """
    def __init__(self, dim: int = 16, k_bits: int = 4, seed: int = 42):
        self.dim = dim
        self.k_bits = k_bits
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    def generate_sequence(self, T: int = 250, t1: int = 2) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.rng.randn(T, self.dim).astype(np.float32) * 0.1
        # Set flags to 0 by default
        x[:, 0] = 0.0
        x[:, 1] = 0.0

        # Trigger step t1
        s = self.rng.choice([-1.0, 1.0], size=self.k_bits).astype(np.float32)
        x[t1, 0] = 1.0  # trigger flag
        x[t1, 2:2+self.k_bits] = s

        # Query step T-1 (0-indexed)
        x[T - 1, 1] = 1.0  # query flag

        target = torch.from_numpy(s)
        return torch.from_numpy(x), target


class ReservedTaskEGenerator:
    """
    Reserved Task E: Fast/Slow State & Multi-Timescale Binding.
    Episode reveals 3 temporary bindings {key_i -> value_i}.
    Interleaves L distractor steps.
    Queries one key; model must output corresponding value.
    """
    def __init__(self, key_dim: int = 4, val_dim: int = 4, seed: int = 42):
        self.key_dim = key_dim
        self.val_dim = val_dim
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    def generate_episode(self, n_bindings: int = 3, distractor_steps: int = 50
                          ) -> Dict[str, Any]:
        keys = self.rng.randn(n_bindings, self.key_dim).astype(np.float32)
        values = self.rng.randn(n_bindings, self.val_dim).astype(np.float32)

        # Distractor tokens
        distractors = self.rng.randn(distractor_steps, self.key_dim + self.val_dim).astype(np.float32)

        # Pick random query
        query_idx = self.rng.randint(0, n_bindings)
        query_key = keys[query_idx]
        target_val = values[query_idx]

        return {
            "keys": torch.from_numpy(keys),
            "values": torch.from_numpy(values),
            "distractors": torch.from_numpy(distractors),
            "query_key": torch.from_numpy(query_key),
            "target_value": torch.from_numpy(target_val),
            "query_idx": query_idx
        }
