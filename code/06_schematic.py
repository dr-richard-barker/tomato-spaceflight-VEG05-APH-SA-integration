"""Module 6 — Figure 1 concept schematic: spaceflight resembles the SA-deficient state.
Hand-built matplotlib schematic (graphical abstract)."""
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
                     'pdf.fonttype': 42, 'svg.fonttype': 'none'})
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
F = os.path.join(ROOT, 'results', 'figures')
C_OSD, C_APH, C_HI, C_DK, C_BG = '#2E6F95', '#C24B3A', '#E8A33D', '#222222', '#F4F1EA'

fig, ax = plt.subplots(figsize=(10.5, 5.6)); ax.set_xlim(0, 105); ax.set_ylim(0, 56); ax.axis('off')

def box(x, y, w, h, fc, ec, title, lines, tcol='white', fs=8.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.4,rounding_size=1.6',
                                facecolor=fc, edgecolor=ec, linewidth=1.4))
    ax.text(x + w / 2, y + h - 3.2, title, ha='center', va='top', fontsize=fs + 1.0, fontweight='bold', color=tcol)
    ax.text(x + w / 2, y + h - 7.4, lines, ha='center', va='top', fontsize=fs, color=tcol, linespacing=1.45)

def arrow(x1, y1, x2, y2, col=C_DK, lw=2.0, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=18,
                                 lw=lw, color=col, shrinkA=2, shrinkB=2))

# --- two missions (left) ---
box(1.5, 33, 27, 18, C_OSD, '#1d4e6b', 'OSD-767  (VEG-05)',
    'Light × Spaceflight\nLeaf + Root\nNo SA manipulation')
box(1.5, 5, 27, 18, C_APH, '#8f3327', 'APH  (Adv. Plant Habitat)',
    'MoneyMaker vs NahG\n± SA × Spaceflight\nLeaf')

# --- PhysioSpace convergence (center) ---
box(38, 19, 22, 18, C_BG, C_DK, 'Plant PhysioSpace', '15 shared\nstress axes', tcol=C_DK)
arrow(28.5, 39, 41, 33, C_OSD); arrow(28.5, 16, 41, 23, C_APH)

# --- result (right) ---
box(68, 19.5, 35, 19, C_DK, '#000000', 'Spaceflight ≈ SA-deficient state',
    'OSD-767 spaceflight signature\nmatches APH NahG (no SA)\n\nPearson r = 0.78  (p = 0.001)', fs=8.6)
arrow(60.5, 28, 67.5, 28, C_DK, lw=2.6)

# --- bottom: SA-tone dial / buffer model ---
ax.text(2, 1.0, 'Model:', fontsize=9, fontweight='bold', color=C_DK)
# SA-tone bar
bx0, bx1, by = 16, 95, 1.8
for i, (frac, col) in enumerate([(0.0, C_HI), (1.0, C_OSD)]):
    pass
ax.add_patch(FancyBboxPatch((bx0, by - 0.2), bx1 - bx0, 2.4, boxstyle='round,pad=0.1,rounding_size=1.0',
                            facecolor='none', edgecolor=C_DK, lw=1.0))
# gradient fill (left = high SA buffered, right = low SA primed)
import numpy as np
grad = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(grad, extent=[bx0, bx1, by, by + 2.0], aspect='auto', cmap='RdYlBu_r', zorder=0, alpha=0.9)
ax.text(bx0, by + 3.3, '◀ high SA  ·  buffered  (MM, +SA:  r ≈ −0.2)', ha='left', fontsize=7.4, color=C_DK)
ax.text(bx1, by + 3.3, 'low SA  ·  defense-primed  (NahG:  r = +0.78) ▶', ha='right', fontsize=7.4, color=C_DK)
ax.scatter([bx1 - 3], [by + 1.0], s=160, color=C_HI, edgecolor='white', zorder=5)
ax.text(bx1 - 3, by + 1.0, '★', ha='center', va='center', fontsize=10, color='white', zorder=6)
ax.annotate('spaceflight\nsits here', (bx1 - 3, by + 1.0), xytext=(bx1 - 18, by + 6.5), fontsize=7.6,
            color=C_DK, ha='center', arrowprops=dict(arrowstyle='-|>', color=C_DK, lw=1.2))

ax.text(52, 53.5, 'Spaceflight drives tomato into a salicylic-acid–deficient, defense-primed state',
        ha='center', fontsize=12.5, fontweight='bold', color=C_DK)

for ext in ('png', 'svg'):
    fig.savefig(os.path.join(F, f'Fig1_concept_schematic.{ext}'), bbox_inches='tight', dpi=300)
plt.close(fig)
print('Fig1_concept_schematic written')
