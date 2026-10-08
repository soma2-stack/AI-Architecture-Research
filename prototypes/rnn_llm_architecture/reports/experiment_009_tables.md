Status: **complete**; runs 75; elapsed 2256 s; torch 2.14.1+cu130; Python 3.13.16; 4 workers × 1 thread.

### Primary: A≠B both-correct, mean over seeds (solved seeds ≥90%)

| Arm | Params | State floats | 32 | 64 | 128 | 256 | 512 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `protected_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 94.4% (4/5) | 84.2% (2/5) |
| `protected_no_retain_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.9% (5/5) | 96.5% (5/5) |
| `protected_shift_w32` | 8,016 | 128 | 100.0% (5/5) | 100.0% (5/5) | 99.9% (5/5) | 83.6% (1/5) | 67.1% (1/5) |
| `protected_hard_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.0% (5/5) |
| `protected_hard_shift_w32` | 8,016 | 128 | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) |
| `tanh_w32` | 4,864 | 64 | 0.1% (0/5) | 0.2% (0/5) | 0.1% (0/5) | 0.0% (0/5) | 0.1% (0/5) |
| `gru_w32` | 13,376 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.5% (5/5) | 92.1% (4/5) |
| `lstm_w32` | 17,600 | 128 | 80.2% (4/5) | 80.6% (4/5) | 80.6% (4/5) | 70.7% (2/5) | 51.8% (1/5) |
| `gru_w24` | 7,728 | 48 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 99.1% (5/5) | 90.0% (3/5) |
| `lstm_w20` | 7,160 | 80 | 90.6% (4/5) | 90.5% (4/5) | 90.0% (4/5) | 83.9% (3/5) | 70.9% (1/5) |
| `gru_keep3_w32` | 13,376 | 64 | 80.0% (4/5) | 80.0% (4/5) | 80.0% (4/5) | 79.8% (4/5) | 72.3% (2/5) |
| `gru_hard_w32` | 13,376 | 64 | 3.0% (0/5) | 1.7% (0/5) | 2.2% (0/5) | 1.8% (0/5) | 1.3% (0/5) |

Oracle upper-bound diagnostic (not an architecture):

| Arm | Params | State floats | 32 | 64 | 128 | 256 | 512 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `oracle_tag_protected_w32` | 7,504 | 64 | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) | 100.0% (5/5) |

### Rule baselines on the same held-out histories (A≠B both-correct)

| Rule (no learning) | 32 | 64 | 128 | 256 | 512 |
|---|---:|---:|---:|---:|---:|
| random | 24.9% | 23.5% | 25.4% | 24.7% | 25.6% |
| last_marked_write | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| last_bit_token | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| initial_values_only | 38.3% | 40.2% | 38.3% | 37.4% | 39.3% |
| sticky_address | 46.1% | 39.9% | 38.9% | 34.2% | 32.8% |

### Per-seed A≠B both-correct

| Arm | Delay | 17 | 29 | 43 | 59 | 71 |
|---|---:|---:|---:|---:|---:|---:|
| `protected_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `protected_w32` | 256 | 100.0% | 72.5% | 100.0% | 100.0% | 99.6% |
| `protected_w32` | 512 | 100.0% | 57.7% | 100.0% | 83.3% | 79.8% |
| `protected_no_retain_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `protected_no_retain_w32` | 256 | 100.0% | 100.0% | 100.0% | 99.6% | 100.0% |
| `protected_no_retain_w32` | 512 | 100.0% | 96.0% | 99.6% | 94.6% | 92.1% |
| `protected_shift_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `protected_shift_w32` | 256 | 72.9% | 83.4% | 100.0% | 76.9% | 84.6% |
| `protected_shift_w32` | 512 | 57.7% | 61.4% | 100.0% | 45.3% | 71.2% |
| `protected_hard_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `protected_hard_w32` | 256 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `protected_hard_w32` | 512 | 100.0% | 95.2% | 100.0% | 100.0% | 100.0% |
| `protected_hard_shift_w32` | 64 | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `protected_hard_shift_w32` | 256 | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `protected_hard_shift_w32` | 512 | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `tanh_w32` | 64 | 0.0% | 0.0% | 0.0% | 0.8% | 0.0% |
| `tanh_w32` | 256 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `tanh_w32` | 512 | 0.0% | 0.0% | 0.0% | 0.4% | 0.0% |
| `gru_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `gru_w32` | 256 | 100.0% | 100.0% | 97.3% | 100.0% | 100.0% |
| `gru_w32` | 512 | 96.6% | 100.0% | 74.6% | 95.3% | 94.0% |
| `lstm_w32` | 64 | 3.2% | 100.0% | 100.0% | 100.0% | 100.0% |
| `lstm_w32` | 256 | 1.2% | 72.1% | 99.6% | 100.0% | 80.4% |
| `lstm_w32` | 512 | 0.4% | 33.1% | 91.9% | 80.2% | 53.6% |
| `gru_w24` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `gru_w24` | 256 | 100.0% | 100.0% | 96.2% | 100.0% | 99.2% |
| `gru_w24` | 512 | 100.0% | 100.0% | 70.4% | 100.0% | 79.4% |
| `lstm_w20` | 64 | 100.0% | 100.0% | 100.0% | 52.6% | 100.0% |
| `lstm_w20` | 256 | 100.0% | 81.9% | 91.6% | 47.0% | 98.8% |
| `lstm_w20` | 512 | 98.7% | 68.4% | 70.0% | 40.3% | 77.2% |
| `gru_keep3_w32` | 64 | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `gru_keep3_w32` | 256 | 99.2% | 0.0% | 100.0% | 100.0% | 100.0% |
| `gru_keep3_w32` | 512 | 76.9% | 0.0% | 89.6% | 100.0% | 95.1% |
| `gru_hard_w32` | 64 | 3.2% | 0.4% | 4.1% | 0.8% | 0.0% |
| `gru_hard_w32` | 256 | 1.6% | 1.1% | 6.5% | 0.0% | 0.0% |
| `gru_hard_w32` | 512 | 2.1% | 0.4% | 4.2% | 0.0% | 0.0% |
| `oracle_tag_protected_w32` | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `oracle_tag_protected_w32` | 256 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `oracle_tag_protected_w32` | 512 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

### Learning speed and stability

| Arm | A≠B at 250 updates (per seed) | First checkpoint ≥90% (per seed) | Median | Final loss (mean) | Max pre-clip grad norm |
|---|---|---|---:|---:|---:|
| `protected_w32` | 0.9% / 0.0% / 3.9% / 0.8% / 1.5% | 750 / 750 / 750 / 500 / 750 | 750 | 0.0001 | 22.7 |
| `protected_no_retain_w32` | 4.3% / 12.6% / 0.0% / 0.8% / 0.7% | 1250 / 1500 / 500 / 750 / 750 | 750 | 0.0004 | 17.7 |
| `protected_shift_w32` | 0.0% / 0.8% / 3.9% / 4.7% / 7.4% | 750 / 750 / 750 / 500 / 500 | 750 | 0.0002 | 22.7 |
| `protected_hard_w32` | 6.0% / 0.0% / 2.3% / 0.0% / 0.7% | 500 / 1000 / 1000 / 1250 / 1750 | 1000 | 0.0002 | 27.4 |
| `protected_hard_shift_w32` | 1.7% / 2.4% / 4.7% / 0.0% / 2.2% | 500 / never / 1750 / 750 / 1000 | 875.0 | 0.1107 | 35.8 |
| `tanh_w32` | 17.9% / 0.0% / 0.0% / 0.0% / 5.2% | never / never / never / never / never | — | 0.7006 | 7.47 |
| `gru_w32` | 12.8% / 0.8% / 0.8% / 0.8% / 7.4% | 750 / 500 / 500 / 500 / 500 | 500 | 0.0001 | 8.45 |
| `lstm_w32` | 32.5% / 9.4% / 2.3% / 0.0% / 8.9% | never / 1750 / 1750 / 1250 / 1250 | 1500.0 | 0.1141 | 206 |
| `gru_w24` | 23.1% / 2.4% / 2.3% / 0.0% / 11.9% | 750 / 750 / 750 / 750 / 500 | 750 | 0.0001 | 9.51 |
| `lstm_w20` | 29.9% / 7.1% / 14.1% / 0.8% / 17.8% | 1750 / 1250 / 1500 / never / 1500 | 1500.0 | 0.0598 | 67.9 |
| `gru_keep3_w32` | 0.0% / 0.0% / 1.6% / 0.0% / 0.0% | 2000 / never / 1250 / 2000 / 1500 | 1750.0 | 0.1140 | 7.76 |
| `gru_hard_w32` | 0.0% / 0.0% / 0.0% / 0.0% / 0.0% | never / never / never / never / never | — | 0.7129 | 1.35e+07 |
| `oracle_tag_protected_w32` | 96.6% / 5.5% / 100.0% / 4.7% / 5.9% | 250 / 500 / 250 / 500 / 500 | 500 | 0.0001 | 18.3 |

Mean held-out A≠B both-correct at the training length by update (checkpoint histories):

| Arm | 250 | 500 | 750 | 1000 | 1250 | 1500 | 1750 | 2000 | same answer to A and B at 250 → final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `protected_w32` | 1.4% | 39.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 98.0% → 50.5% |
| `protected_no_retain_w32` | 3.7% | 38.8% | 60.2% | 60.7% | 96.5% | 100.0% | 100.0% | 100.0% | 91.1% → 50.5% |
| `protected_shift_w32` | 3.4% | 78.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 95.1% → 50.5% |
| `protected_hard_w32` | 1.8% | 21.2% | 33.6% | 71.5% | 80.7% | 80.1% | 100.0% | 100.0% | 97.1% → 50.5% |
| `protected_hard_shift_w32` | 2.2% | 20.1% | 41.0% | 60.0% | 60.0% | 65.3% | 80.0% | 80.0% | 95.8% → 60.4% |
| `tanh_w32` | 4.6% | 2.6% | 0.0% | 0.0% | 2.5% | 0.0% | 0.0% | 0.3% | 86.4% → 99.8% |
| `gru_w32` | 4.5% | 87.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 92.3% → 50.5% |
| `lstm_w32` | 10.6% | 7.1% | 1.1% | 14.2% | 40.8% | 51.5% | 79.2% | 80.2% | 76.3% → 59.3% |
| `gru_w24` | 7.9% | 25.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 81.8% → 50.5% |
| `lstm_w20` | 13.9% | 12.3% | 1.4% | 18.2% | 35.2% | 60.6% | 80.1% | 89.4% | 69.7% → 55.7% |
| `gru_keep3_w32` | 0.3% | 1.2% | 0.2% | 0.8% | 34.5% | 40.2% | 41.8% | 80.0% | 98.8% → 60.4% |
| `gru_hard_w32` | 0.0% | 0.0% | 0.0% | 0.5% | 0.5% | 1.2% | 0.3% | 1.4% | 100.0% → 96.3% |
| `oracle_tag_protected_w32` | 42.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 77.7% → 50.5% |

### Legacy task (Experiments 004–008 generator)

| Model | Trained on | legacy 64 | legacy 128 | legacy 256 | two-slot 64 | two-slot 256 |
|---|---|---:|---:|---:|---:|---:|
| `protected_w32` | two_slot (5/5 seeds) | 100.0% | 100.0% | 91.8% | 100.0% | 94.4% |
| `protected_w32` | legacy (5/5 seeds) | 100.0% | 42.0% | 30.3% | 11.3% | 11.1% |
| `gru_w32` | two_slot (5/5 seeds) | 100.0% | 100.0% | 100.0% | 100.0% | 99.5% |
| `gru_w32` | legacy (5/5 seeds) | 80.7% | 80.8% | 73.1% | 33.2% | 18.5% |

### Gate usage

| Arm | Layer | mean gate: marked value | unmarked bit | WRITE marker | benign distractor | exact-zero fraction on distractors | implied retention after 512 non-write tokens (median over seeds) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `protected_w32` | 0 | 0.049 | 0.049 | 0.055 | 0.046 | 0.00 | 1.3e-11 |
| `protected_w32` | 1 | 0.176 | 0.102 | 0.219 | 0.107 | 0.00 | 6.4e-31 |
| `protected_no_retain_w32` | 0 | 0.048 | 0.048 | 0.052 | 0.048 | 0.00 | 1.1e-11 |
| `protected_no_retain_w32` | 1 | 0.083 | 0.071 | 0.108 | 0.072 | 0.00 | 2.9e-20 |
| `protected_shift_w32` | 0 | 0.122 | 0.040 | 0.053 | 0.038 | 0.00 | 9.3e-10 |
| `protected_shift_w32` | 1 | 0.271 | 0.116 | 0.249 | 0.119 | 0.00 | 1.2e-56 |
| `protected_hard_w32` | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 1.00 | 1 |
| `protected_hard_w32` | 1 | 0.205 | 0.384 | 0.162 | 0.434 | 0.57 | 0 |
| `protected_hard_shift_w32` | 0 | 0.075 | 0.000 | 0.000 | 0.000 | 1.00 | 1 |
| `protected_hard_shift_w32` | 1 | 0.369 | 0.511 | 0.357 | 0.511 | 0.49 | 0 |
| `gru_w32` | 0 | 0.563 | 0.555 | 0.614 | 0.533 | 0.00 | 9.5e-179 |
| `gru_w32` | 1 | 0.515 | 0.392 | 0.543 | 0.387 | 0.00 | 1.2e-201 |
| `gru_w24` | 0 | 0.585 | 0.562 | 0.636 | 0.534 | 0.00 | 3.3e-187 |
| `gru_w24` | 1 | 0.547 | 0.434 | 0.569 | 0.439 | 0.00 | 3e-232 |
| `gru_keep3_w32` | 0 | 0.227 | 0.114 | 0.184 | 0.086 | 0.00 | 1.6e-30 |
| `gru_keep3_w32` | 1 | 0.269 | 0.134 | 0.323 | 0.133 | 0.00 | 2.4e-46 |
| `gru_hard_w32` | 0 | 0.139 | 0.176 | 0.053 | 0.057 | 0.94 | 9.9e-230 |
| `gru_hard_w32` | 1 | 0.355 | 0.418 | 0.279 | 0.421 | 0.58 | 0 |
| `oracle_tag_protected_w32` | 0 | 0.071 | 0.000 | 0.000 | 0.000 | 1.00 | 1 |
| `oracle_tag_protected_w32` | 1 | 0.193 | 0.000 | 0.000 | 0.000 | 1.00 | 1 |

### State-perturbation recovery (seeds that solve 64)

| Arm | Seeds solving 64 | clean, immediate | clean, +64 tail | noise 0.5, immediate | noise 0.5, +64 tail | noise 1.0, immediate | noise 1.0, +64 tail |
|---|---:|---:|---:|---:|---:|---:|---:|
| `protected_w32` | 5 | 100.0% | 100.0% | 100.0% | 99.8% | 92.7% | 91.7% |
| `protected_no_retain_w32` | 5 | 100.0% | 100.0% | 99.9% | 99.3% | 83.8% | 83.8% |
| `protected_shift_w32` | 5 | 100.0% | 99.5% | 100.0% | 98.8% | 91.2% | 92.2% |
| `protected_hard_w32` | 5 | 100.0% | 100.0% | 99.6% | 99.8% | 88.2% | 88.4% |
| `protected_hard_shift_w32` | 4 | 100.0% | 100.0% | 99.9% | 99.8% | 86.3% | 87.8% |
| `tanh_w32` | 0 | — | — | — | — | — | — |
| `gru_w32` | 5 | 100.0% | 100.0% | 100.0% | 98.3% | 93.4% | 86.9% |
| `lstm_w32` | 4 | 100.0% | 99.9% | 92.1% | 87.8% | 72.1% | 68.3% |
| `gru_w24` | 5 | 100.0% | 100.0% | 98.7% | 98.2% | 85.6% | 84.1% |
| `lstm_w20` | 4 | 100.0% | 100.0% | 96.9% | 92.0% | 75.9% | 70.3% |
| `gru_keep3_w32` | 4 | 100.0% | 100.0% | 98.9% | 98.0% | 82.3% | 83.6% |
| `gru_hard_w32` | 0 | — | — | — | — | — | — |
| `oracle_tag_protected_w32` | 5 | 100.0% | 100.0% | 99.8% | 99.7% | 90.5% | 90.2% |

### Frozen-state linear probe

| Arm | Native 64 | Probe 64 (held-out) | Native 256 | Probe fit at 64, applied at 256 | Probe features |
|---|---:|---:|---:|---:|---:|
| `protected_w32` | 100.0% | 100.0% | 94.4% | 90.6% | 64 |
| `protected_no_retain_w32` | 100.0% | 100.0% | 99.9% | 99.9% | 64 |
| `protected_shift_w32` | 100.0% | 100.0% | 83.6% | 90.5% | 128 |
| `protected_hard_w32` | 100.0% | 100.0% | 100.0% | 100.0% | 64 |
| `protected_hard_shift_w32` | 80.0% | 83.4% | 80.0% | 83.0% | 128 |
| `tanh_w32` | 0.2% | 23.2% | 0.0% | 22.6% | 64 |
| `gru_w32` | 100.0% | 100.0% | 99.5% | 99.0% | 64 |
| `lstm_w32` | 80.6% | 84.3% | 70.7% | 78.8% | 128 |
| `gru_w24` | 100.0% | 100.0% | 99.1% | 98.5% | 48 |
| `lstm_w20` | 90.5% | 93.1% | 83.9% | 87.0% | 80 |
| `gru_keep3_w32` | 80.0% | 83.5% | 79.8% | 83.2% | 64 |
| `gru_hard_w32` | 1.7% | 14.8% | 1.8% | 12.9% | 64 |
| `oracle_tag_protected_w32` | 100.0% | 100.0% | 100.0% | 100.0% | 64 |

### Resources

| Arm | Params | State floats | Median train s | Median eval s | Statuses |
|---|---:|---:|---:|---:|---|
| `protected_w32` | 7,504 | 64 | 132 | 6 | complete |
| `protected_no_retain_w32` | 7,504 | 64 | 126 | 5 | complete |
| `protected_shift_w32` | 8,016 | 128 | 134 | 6 | complete |
| `protected_hard_w32` | 7,504 | 64 | 135 | 5 | complete |
| `protected_hard_shift_w32` | 8,016 | 128 | 136 | 6 | complete |
| `tanh_w32` | 4,864 | 64 | 46 | 3 | complete |
| `gru_w32` | 13,376 | 64 | 91 | 4 | complete |
| `lstm_w32` | 17,600 | 128 | 91 | 5 | complete |
| `gru_w24` | 7,728 | 48 | 90 | 4 | complete |
| `lstm_w20` | 7,160 | 80 | 86 | 5 | complete |
| `gru_keep3_w32` | 13,376 | 64 | 104 | 5 | complete |
| `gru_hard_w32` | 13,376 | 64 | 112 | 6 | complete |
| `oracle_tag_protected_w32` | 7,504 | 64 | 152 | 7 | complete |
| `protected_w32` (legacy-trained) | 7,504 | 64 | 129 | 5 | complete |
| `gru_w32` (legacy-trained) | 13,376 | 64 | 87 | 4 | complete |

### Preregistered decisions

- **H1 (budget/plateau): SUPPORTED.** `protected_w32` solves 64 in 5/5 seeds; A≠B at 250 updates per seed: 0.9%, 0.0%, 3.9%, 0.8%, 1.5%.
- **H2 (fixed-timing task): SUPPORTED.** Legacy-eval A≠B, two-slot-trained minus legacy-trained `protected_w32`: 128 → +58.0 pp (5/5 seeds positive); 256 → +61.5 pp (5/5 positive).
- **H3 (protected retention unused): SUPPORTED.** no-retain solves 64 in 5/5 vs protected 5/5; max implied 512-token retention over solved protected runs and layers: 4.3e-11.
- **H4 (error-correcting memory) for `protected_w32`: SUPPORTED** (3/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `protected_no_retain_w32`: NOT SUPPORTED** (2/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `protected_shift_w32`: NOT SUPPORTED** (2/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `protected_hard_w32`: SUPPORTED** (5/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `protected_hard_shift_w32`: SUPPORTED** (3/4 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `gru_w32`: NOT SUPPORTED** (0/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `lstm_w32`: NOT SUPPORTED** (1/4 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `gru_w24`: SUPPORTED** (3/5 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `lstm_w20`: NOT SUPPORTED** (0/4 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `gru_keep3_w32`: NOT SUPPORTED** (2/4 solved seeds recover from 0.5×RMS noise).
- **H4 (error-correcting memory) for `oracle_tag_protected_w32`: SUPPORTED** (4/5 solved seeds recover from 0.5×RMS noise).
- **H5 (learned exact closure ≈ oracle) for `protected_hard_w32`: FALSIFIED.** Reached 90% by oracle median + 250 (= 750) in 1/5 seeds; solves 512 in 5/5.
- **H5 (learned exact closure ≈ oracle) for `protected_hard_shift_w32`: FALSIFIED.** Reached 90% by oracle median + 250 (= 750) in 2/5 seeds; solves 512 in 4/5.
- **H6 (descriptive) solved seeds at 64 / 512:** `protected_w32` 5/2; `protected_no_retain_w32` 5/5; `protected_shift_w32` 5/1; `protected_hard_w32` 5/5; `protected_hard_shift_w32` 4/4; `tanh_w32` 0/0; `gru_w32` 5/4; `lstm_w32` 4/1; `gru_w24` 5/3; `lstm_w20` 4/1; `gru_keep3_w32` 4/2; `gru_hard_w32` 0/0.

### Hosted GitHub Actions replication (torch 2.14.1+cpu wheel)

| Arm | Trained on | Seed pairs | Solved 64 local / hosted | Solved 512 local / hosted | Mean abs. diff (all delays) | Seed-runs whose solved/unsolved status differs at any delay |
|---|---|---:|---:|---:|---:|---:|
| `protected_w32` | two_slot | 5 | 5 / 5 | 2 / 2 | 0.0 pp | 0 |
| `protected_no_retain_w32` | two_slot | 5 | 5 / 5 | 5 / 5 | 0.2 pp | 0 |
| `protected_shift_w32` | two_slot | 5 | 5 / 5 | 1 / 1 | 0.0 pp | 0 |
| `protected_hard_w32` | two_slot | 5 | 5 / 5 | 5 / 5 | 0.2 pp | 0 |
| `protected_hard_shift_w32` | two_slot | 5 | 4 / 5 | 4 / 4 | 19.1 pp | 1 |
| `tanh_w32` | two_slot | 5 | 0 / 0 | 0 / 0 | 0.1 pp | 0 |
| `gru_w32` | two_slot | 5 | 5 / 5 | 4 / 4 | 0.0 pp | 0 |
| `lstm_w32` | two_slot | 5 | 4 / 4 | 1 / 1 | 1.9 pp | 1 |
| `gru_w24` | two_slot | 5 | 5 / 5 | 3 / 3 | 0.0 pp | 0 |
| `lstm_w20` | two_slot | 5 | 4 / 3 | 1 / 1 | 17.0 pp | 2 |
| `gru_keep3_w32` | two_slot | 5 | 4 / 4 | 2 / 2 | 0.0 pp | 0 |
| `gru_hard_w32` | two_slot | 5 | 0 / 0 | 0 / 0 | 1.1 pp | 0 |
| `oracle_tag_protected_w32` | two_slot | 5 | 5 / 5 | 5 / 5 | 0.0 pp | 0 |
| `protected_w32` | legacy | 5 | 0 / 0 | 0 / 0 | 1.8 pp | 0 |
| `gru_w32` | legacy | 5 | 0 / 0 | 0 / 0 | 0.4 pp | 0 |
