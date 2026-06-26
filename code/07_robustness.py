"""Module 7 — Robustness of the headline cross-study concordance.
A Pearson r on 15 PhysioSpace axes invites the question "is this just chance with n=15?".
We add (a) a label-permutation test (exact-style empirical p) and (b) a bootstrap 95% CI,
for the key correlations, plus a monotonic-trend test for the SA-status gradient.
"""
import os, numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables')
rng = np.random.default_rng(0)
N_PERM, N_BOOT = 20000, 20000

joint = pd.read_csv(os.path.join(T, 'pattern_joint_flight_effects.csv'), index_col=0)

def robust_pair(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    r = pearsonr(x, y)[0]
    # permutation: shuffle y labels, recompute r -> two-sided empirical p
    perm = np.array([pearsonr(x, rng.permutation(y))[0] for _ in range(N_PERM)])
    p_perm = (np.sum(np.abs(perm) >= abs(r)) + 1) / (N_PERM + 1)
    # bootstrap over axes (paired resample) -> 95% CI
    n = len(x)
    boot = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, n)
        if np.std(x[idx]) == 0 or np.std(y[idx]) == 0:
            continue
        boot.append(pearsonr(x[idx], y[idx])[0])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return r, p_perm, lo, hi

pairs = [('OSD_root', 'APH_NahG'), ('OSD_root', 'APH_MM'),
         ('OSD_leaf', 'APH_NahG'), ('OSD_root', 'APH_Mock')]
rows = []
for a, b in pairs:
    r, p, lo, hi = robust_pair(joint[a], joint[b])
    rows.append({'pair': f'{a} vs {b}', 'n_axes': len(joint), 'pearson_r': round(r, 3),
                 'perm_p_2sided': round(p, 4), 'boot95_lo': round(lo, 3), 'boot95_hi': round(hi, 3)})
rob = pd.DataFrame(rows)
rob.to_csv(os.path.join(T, 'robustness_concordance.csv'), index=False)

# SA-status gradient monotonic trend (SA tone decreasing: SA > MM > Mock > NahG)
grad = pd.read_csv(os.path.join(T, 'SA_status_gradient.csv'), index_col=0)['pearson_r']
order = [g for g in ['SA', 'MM', 'Mock', 'NahG'] if g in grad.index]
vals = grad.loc[order].values
rho, p_trend = spearmanr(np.arange(len(order)), vals)  # rank of decreasing-SA vs similarity
trend = pd.DataFrame([{'gradient_order': '>'.join(order),
                       'values': ','.join(f'{v:+.2f}' for v in vals),
                       'spearman_trend': round(rho, 3), 'trend_p': round(p_trend, 4),
                       'n_groups': len(order)}])
trend.to_csv(os.path.join(T, 'robustness_SA_gradient_trend.csv'), index=False)

print(rob.to_string(index=False))
print('\nSA-tone gradient (decreasing SA):', '>'.join(order))
print('  values:', ', '.join(f'{v:+.2f}' for v in vals),
      f'| Spearman trend = {rho:+.2f}, p = {p_trend:.3f}')
