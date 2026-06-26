"""CI reproducibility check: assert the two headline results survive a fresh pipeline run.
Run after run_pipeline.py. Exits non-zero (fails the build) if either claim drifts."""
import sys, pandas as pd, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, 'results', 'tables')

rob = pd.read_csv(os.path.join(T, 'robustness_concordance.csv'))
r = float(rob.loc[rob['pair'] == 'OSD_root vs APH_NahG', 'pearson_r'].iloc[0])
con = pd.read_csv(os.path.join(T, 'concordance_summary.csv'))
sp = float(con['spearman_all'].iloc[0])

ok = True
# 1. pattern-level convergence: spaceflight matches the SA-deficient (NahG) state
if not (0.70 <= r <= 0.85):
    print(f'FAIL: OSD_root vs APH_NahG Pearson r = {r} (expected ~0.78)'); ok = False
# 2. gene-level non-replication
if not (abs(sp) < 0.15):
    print(f'FAIL: gene-level Spearman = {sp} (expected ~0.05, non-replication)'); ok = False

if ok:
    print(f'Reproducibility check PASSED  |  pattern r = {r:.3f}  |  gene-level rho = {sp:.3f}')
    sys.exit(0)
sys.exit(1)
