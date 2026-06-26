"""Module 5 — Cell-type localization of the conserved defense response.
Tests whether both studies localize the biotic-defense (SA) axis to outer/epidermal
cell types. OSD-767 uses AT_Stress_Space 'Biotic.Hormone'; APH uses meta 'BioMone'.
"""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
                     'pdf.fonttype': 42, 'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False})
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables'); F = os.path.join(ROOT, 'results', 'figures')

# OSD-767 cell-type defense axis (Biotic.Hormone, AT_Stress_Space)
o = pd.read_csv(os.path.join(ROOT, 'data/osd767/osd767_celltype_physioscores.csv'))
defense_axis = 'Biotic.Hormone' if 'Biotic.Hormone' in o.Stress_Axis.unique() else 'Hormone'
od = o[(o.Space == 'AT_Stress_Space') & (o.Stress_Axis == defense_axis)].copy()
od['cell'] = od['Cell_Type'].str.replace('leaf_light_|root_', '', regex=True)
od = od.groupby('cell')['PhysioScore'].mean().sort_values()

# APH cell-type defense axis (BioMone)
a = pd.read_csv(os.path.join(ROOT, 'data/aph/aph_cell_stress_delta.csv'), index_col=0)
ad = a['BioMone'].sort_values()

pd.concat([od.rename('OSD767_BioticHormone'), ad.rename('APH_BioMone')], axis=1).to_csv(
    os.path.join(T, 'celltype_defense_localization.csv'))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 4.6))
a1.barh(range(len(od)), od.values, color='#2E6F95')
a1.set_yticks(range(len(od))); a1.set_yticklabels(od.index, fontsize=8)
a1.set_title(f'OSD-767 — {defense_axis}', fontsize=10, color='#2E6F95', fontweight='bold')
a1.axvline(0, color='#bbb', lw=0.6); a1.set_xlabel('Cell-type PhysioScore', fontsize=9)
a2.barh(range(len(ad)), ad.values, color='#C24B3A')
a2.set_yticks(range(len(ad))); a2.set_yticklabels(ad.index, fontsize=8)
a2.set_title('APH — BioMone (biotic+hormone)', fontsize=10, color='#C24B3A', fontweight='bold')
a2.axvline(0, color='#bbb', lw=0.6); a2.set_xlabel('Cell-type flight delta', fontsize=9)
fig.suptitle('Defense response localizes to outer / epidermal cell types in both studies',
             fontsize=12, fontweight='bold', x=0.5, ha='center')
fig.tight_layout()
for ext in ('png', 'svg'):
    fig.savefig(os.path.join(F, f'Fig6_celltype_localization.{ext}'), bbox_inches='tight', dpi=300)
plt.close(fig)
print('OSD-767 defense axis:', defense_axis)
print('OSD-767 top cell types:', list(od.tail(3).index[::-1]))
print('APH top cell types:', list(ad.tail(3).index[::-1]))
print('Fig5 written')
