"""Module 3 (definitive) — Cross-study stress-pattern convergence using each study's
PUBLISHED full-reference PhysioScores (AT_Stress_Meta). Tests the thesis:
spaceflight drives an SA-deficient-like, biotic-defense-primed state that SA buffers.
"""
import os, numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables'); os.makedirs(T, exist_ok=True)

# ---- OSD-767 published meta-space flight effects (root + leaf, by light) ----
g = pd.read_csv(os.path.join(ROOT, 'data/osd767/osd767_physio_group_means.csv'))
meta = g[g.Space == 'AT_Stress_Meta']
def osd_vec(organ, contrasts):
    s = meta[(meta.Organ == organ) & (meta.Contrast.isin(contrasts))]
    return s.groupby('Stress_Axis')['PhysioScore'].mean()
osd = pd.DataFrame({
    'OSD_root': osd_vec('Root', ['Flight_Effect_Red', 'Flight_Effect_Blue']),
    'OSD_root_Red': osd_vec('Root', ['Flight_Effect_Red']),
    'OSD_root_Blue': osd_vec('Root', ['Flight_Effect_Blue']),
    'OSD_leaf': osd_vec('Leaf', ['Flight_Effect_Red', 'Flight_Effect_Blue']),
})

# ---- APH published per-axis flight effects (Main / MM / NahG / SA / Mock) ----
aph = pd.read_csv(os.path.join(ROOT, 'data/aph/aph_physio_interaction.csv'), index_col=0)
axes = [a for a in osd.index if a in aph.index]
osd, aph = osd.reindex(axes), aph.reindex(axes)

joint = pd.concat([osd, aph.add_prefix('APH_')], axis=1)
joint.to_csv(os.path.join(T, 'pattern_joint_flight_effects.csv'))

# ---- cross-study concordance matrix ----
rows = []
for o in osd.columns:
    for a in [c for c in aph.columns]:
        r, p = pearsonr(osd[o], aph[a]); rho, _ = spearmanr(osd[o], aph[a])
        rows.append({'OSD': o, 'APH': a, 'pearson_r': round(r, 3), 'p': round(p, 4), 'spearman': round(rho, 3)})
conc = pd.DataFrame(rows)
conc.to_csv(os.path.join(T, 'pattern_concordance_matrix.csv'), index=False)

# ---- SA-status gradient: does OSD spaceflight signature track SA-deficiency? ----
# APH groups ordered by approximate SA tone (high -> low): SA, MM, Main, Mock, NahG
order = ['SA', 'MM', 'Main', 'Mock', 'NahG']  # high -> low SA tone
grad = conc[(conc.OSD == 'OSD_root')].set_index('APH').reindex(order)['pearson_r']
grad.to_csv(os.path.join(T, 'SA_status_gradient.csv'))

# ---- axes driving the convergence (OSD_root & APH_NahG same-sign, both notable) ----
drv = joint[['OSD_root', 'APH_NahG']].copy()
drv['same_sign'] = np.sign(drv['OSD_root']) == np.sign(drv['APH_NahG'])
drv['conserved'] = drv['same_sign'] & (drv['OSD_root'].abs() > 3) & (drv['APH_NahG'].abs() > 0.5)
drv.sort_values('OSD_root', ascending=False).to_csv(os.path.join(T, 'conserved_axes.csv'))

print('=== Joint flight-effect (published meta scores) ===')
print(joint.round(1).to_string())
print('\n=== Headline concordances ===')
for o, a in [('OSD_root', 'NahG'), ('OSD_root', 'MM'), ('OSD_leaf', 'NahG'), ('OSD_root', 'SA')]:
    row = conc[(conc.OSD == o) & (conc.APH == a)].iloc[0]
    print(f"  {o:9s} vs {a:9s}:  r={row.pearson_r:+.2f}  p={row.p:.3f}  rho={row.spearman:+.2f}")
print('\n=== SA-status gradient (OSD_root vs APH groups, high->low SA tone) ===')
print(grad.round(2).to_string())
print('\n=== Conserved axes (OSD_root & APH_NahG same sign) ===')
print(drv[drv.conserved].round(2).to_string())
