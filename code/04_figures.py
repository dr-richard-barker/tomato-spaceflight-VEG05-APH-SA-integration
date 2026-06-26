"""Module 4 — Integration figures (publication-quality, matplotlib).
Reads result tables from Modules 1 & 3."""
import os, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
                     'pdf.fonttype': 42, 'svg.fonttype': 'none', 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.dpi': 120})
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables'); F = os.path.join(ROOT, 'results', 'figures')
os.makedirs(F, exist_ok=True)
C_OSD, C_APH, C_HI = '#2E6F95', '#C24B3A', '#E8A33D'

def save(fig, name):
    for ext in ('png', 'svg'):
        fig.savefig(os.path.join(F, f'{name}.{ext}'), bbox_inches='tight', dpi=300)
    plt.close(fig)

# ===== Fig 1 — SA-status gradient (headline) =====
grad = pd.read_csv(os.path.join(T, 'SA_status_gradient.csv'), index_col=0)['pearson_r']
labels = {'SA': 'SA\n(+SA)', 'MM': 'MM\n(WT)', 'Main': 'All\n(pooled)', 'Mock': 'Mock\n(−SA)', 'NahG': 'NahG\n(SA-deficient)'}
fig, ax = plt.subplots(figsize=(6.4, 4.3))
x = range(len(grad))
ax.plot(x, grad.values, '-', color='#888', lw=1.5, zorder=1)
ax.scatter(x, grad.values, s=160, c=[C_HI if g == 'NahG' else C_OSD for g in grad.index], zorder=3, edgecolor='white')
for i, (g, v) in enumerate(grad.items()):
    ax.annotate(f'{v:+.2f}', (i, v), textcoords='offset points', xytext=(0, 12 if v >= 0 else -16), ha='center', fontsize=9, fontweight='bold')
ax.axhline(0, color='#bbb', lw=0.8, ls=':')
ax.set_xticks(list(x)); ax.set_xticklabels([labels[g] for g in grad.index], fontsize=9)
ax.set_ylabel("Similarity to OSD-767 spaceflight\nsignature (Pearson r, 15 stress axes)", fontsize=10)
ax.set_xlabel('APH genotype / SA treatment  (decreasing SA tone →)', fontsize=10)
ax.set_title('Spaceflight resembles the SA-deficient state', fontsize=12, fontweight='bold', loc='left')
ax.set_ylim(-0.45, 0.95)
save(fig, 'Fig2_SA_status_gradient')

# ===== Fig 2 — joint flight-effect heatmap (z-scored within each column) =====
joint = pd.read_csv(os.path.join(T, 'pattern_joint_flight_effects.csv'), index_col=0)
cols = ['OSD_root', 'OSD_leaf', 'APH_MM', 'APH_Mock', 'APH_SA', 'APH_NahG']
M = joint[cols]
Z = (M - M.mean()) / M.std(ddof=0)  # within-study standardization so patterns compare
order = joint['OSD_root'].sort_values(ascending=False).index
Z = Z.reindex(order)
fig, ax = plt.subplots(figsize=(6.6, 6.2))
im = ax.imshow(Z.values, aspect='auto', cmap='RdBu_r', norm=TwoSlopeNorm(0, -2.2, 2.2))
ax.set_xticks(range(len(cols)))
ax.set_xticklabels(['OSD-767\nroot', 'OSD-767\nleaf', 'APH\nMM', 'APH\nMock', 'APH\nSA', 'APH\nNahG'], fontsize=8.5)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order, fontsize=8.5)
ax.axvline(1.5, color='k', lw=1.2)
cb = fig.colorbar(im, ax=ax, shrink=0.55, aspect=18, pad=0.02); cb.set_label('Flight effect (z within study)', fontsize=8)
ax.set_title('Conserved spaceflight stress-pattern axes', fontsize=12, fontweight='bold', loc='left', pad=8)
save(fig, 'Fig3_joint_physiospace_heatmap')

# ===== Fig 3 — gene-level non-replication (rigor contrast) =====
m = pd.read_csv(os.path.join(T, 'leaf_FvG_merged_lfc.csv'), index_col=0)
fig, ax = plt.subplots(figsize=(4.8, 4.6))
ax.scatter(m['osd767_lfc'], m['aph_lfc'], s=4, alpha=0.18, color='#666', edgecolor='none')
ax.axhline(0, color='#ccc', lw=0.6); ax.axvline(0, color='#ccc', lw=0.6)
lim = 6; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
ax.set_xlabel('OSD-767 leaf Flight-vs-Ground log2FC', fontsize=9)
ax.set_ylabel('APH leaf Flight-vs-Ground log2FC', fontsize=9)
ax.set_title('Gene level does NOT replicate\n(Spearman ρ = 0.05)', fontsize=11, fontweight='bold', loc='left')
save(fig, 'Fig4_genelevel_nonreplication')

# ===== Fig 4 — conserved-axis profile (OSD_root vs APH_NahG) =====
ca = joint.loc[order, ['OSD_root', 'APH_NahG']]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 5.2), sharey=True)
y = range(len(ca))
a1.barh(y, ca['OSD_root'], color=C_OSD); a1.set_yticks(y); a1.set_yticklabels(ca.index, fontsize=8.5)
a1.set_title('OSD-767 spaceflight (root)', fontsize=10, color=C_OSD, fontweight='bold'); a1.axvline(0, color='#bbb', lw=0.6); a1.invert_yaxis()
a2.barh(y, ca['APH_NahG'], color=C_HI); a2.set_title('APH SA-deficient (NahG)', fontsize=10, color=C_HI, fontweight='bold'); a2.axvline(0, color='#bbb', lw=0.6)
a1.set_xlabel('PhysioScore flight effect', fontsize=9); a2.set_xlabel('PhysioScore flight effect', fontsize=9)
fig.suptitle('Same biotic-defense axes activated (r = 0.78)', fontsize=12, fontweight='bold', x=0.12, ha='left')
save(fig, 'Fig5_conserved_axis_profile')

print('Figures written to', F)
for fn in sorted(os.listdir(F)):
    if fn.endswith('.png'): print('  ', fn)
