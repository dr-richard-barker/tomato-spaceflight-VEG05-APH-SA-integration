"""Module 2 — Joint PhysioSpace: project BOTH studies' leaf data into the identical
15-axis AT_Stress_Space_Meta and test whether the spaceflight STRESS-PATTERN response
is conserved across studies (even though gene-level FCs are not — see Module 1).
"""
import os, re, numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr
import physiospace as ps

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables'); os.makedirs(T, exist_ok=True)
space, s2at = ps.load_reference(os.path.join(ROOT, 'data/reference/at_stress_space.csv'),
                                os.path.join(ROOT, 'data/reference/solyc_to_at_entrez.json'))
AXES = list(space.columns)

# ===== APH (MoneyMaker + NahG, leaf) =====
aph = pd.read_csv(os.path.join(ROOT, 'data/aph/aph_log2cpm_filtered.csv'), index_col=0)
cond = pd.read_csv(os.path.join(ROOT, 'data/aph/aph_conditions.csv'), index_col=0).T  # samples x factors
ag = [s for s in aph.columns if cond.loc[s, 'Treatment'] == 'Ground']
aph_fc = ps.fc_vs_ground(aph, ag)
aph_at = ps.map_to_at(aph_fc, s2at)
aph_ps, n_aph = ps.calculate_physio_map(aph_at, space)

def delta(ps_df, samples_f, samples_g):
    return ps_df[samples_f].mean(axis=1) - ps_df[samples_g].mean(axis=1)

def sel(mask):
    idx = cond.index[mask]
    return ([s for s in idx if cond.loc[s, 'Treatment'] == 'Flight'],
            [s for s in idx if cond.loc[s, 'Treatment'] == 'Ground'])

aph_eff = {}
for label, mask in {'APH_Main': pd.Series(True, index=cond.index),
                    'APH_MM': cond['Genotype'] == 'MM', 'APH_NahG': cond['Genotype'] == 'NahG',
                    'APH_SA': cond['Hormonal_addition'] == 'SA', 'APH_Mock': cond['Hormonal_addition'] == 'Mock'}.items():
    f, g = sel(mask)
    aph_eff[label] = delta(aph_ps, f, g)

# ===== OSD-767 (VEG-05, leaf) =====
osd = pd.read_csv(os.path.join(ROOT, 'data/osd767/osd767_leaf_VST_counts.csv'), index_col=0)
def meta_osd(s):
    return ('Flight' if '-Flt-' in s else 'Ground', 'Blue' if s.endswith('Blue') else 'Red')
omd = {s: meta_osd(s) for s in osd.columns}
og = [s for s in osd.columns if omd[s][0] == 'Ground']
osd_fc = ps.fc_vs_ground(osd, og)
osd_at = ps.map_to_at(osd_fc, s2at)
osd_ps, n_osd = ps.calculate_physio_map(osd_at, space)

osd_eff = {}
for label, light in {'OSD_Main': None, 'OSD_Red': 'Red', 'OSD_Blue': 'Blue'}.items():
    f = [s for s in osd.columns if omd[s][0] == 'Flight' and (light is None or omd[s][1] == light)]
    g = [s for s in osd.columns if omd[s][0] == 'Ground' and (light is None or omd[s][1] == light)]
    osd_eff[label] = delta(osd_ps, f, g)

# ===== assemble joint flight-effect matrix (15 axes x condition groups) =====
joint = pd.DataFrame({**osd_eff, **aph_eff}).reindex(AXES)
joint.to_csv(os.path.join(T, 'joint_physiospace_flight_effects.csv'))

# ===== cross-study PATTERN concordance (the decisive test) =====
rows = []
for o_lab in ['OSD_Main', 'OSD_Red', 'OSD_Blue']:
    for a_lab in ['APH_Main', 'APH_MM', 'APH_NahG', 'APH_SA', 'APH_Mock']:
        r, p = pearsonr(joint[o_lab], joint[a_lab])
        rho, _ = spearmanr(joint[o_lab], joint[a_lab])
        rows.append({'OSD': o_lab, 'APH': a_lab, 'pearson_r': round(r, 3),
                     'p': round(p, 4), 'spearman': round(rho, 3)})
conc = pd.DataFrame(rows)
conc.to_csv(os.path.join(T, 'physiospace_crossstudy_concordance.csv'), index=False)

print(f"genes mapped: OSD={n_osd}, APH={n_aph}  | axes={len(AXES)}")
print('\n=== Joint flight-effect (PhysioScore Flight-Ground) ===')
print(joint.round(1).to_string())
print('\n=== Cross-study PATTERN concordance (15-axis vectors) ===')
print(conc.to_string(index=False))
print('\nMain-vs-Main Pearson r =', conc[(conc.OSD=='OSD_Main')&(conc.APH=='APH_Main')]['pearson_r'].values)
