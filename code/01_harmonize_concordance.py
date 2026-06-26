"""Module 1 — Harmonize the two studies' leaf Flight-vs-Ground contrasts and
quantify the conserved core (cross-study concordance of fold-changes + shared DEGs).

OSD-767 (VEG-05, light x spaceflight, leaf)  vs  APH (MoneyMaker WT, SA x spaceflight, leaf).
Integration is on FOLD-CHANGES (batch/cultivar/chamber-resistant), per the locked meta plan.
"""
import os, numpy as np, pandas as pd
from scipy.stats import spearmanr, pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, 'results', 'tables'); os.makedirs(T, exist_ok=True)

def strip_ver(s):
    return str(s).split('.')[0]

# --- OSD-767 leaf Flight vs Ground (deposited DESeq2 table) ---
o = pd.read_csv(os.path.join(ROOT, 'data/osd767/osd767_leaf_Flight_vs_Ground.csv'))
ocol = 'shrunk_log2FoldChange' if 'shrunk_log2FoldChange' in o.columns else 'log2FoldChange'
o['gene'] = o['gene_id'].map(strip_ver)
o = o.dropna(subset=[ocol]).groupby('gene').first()
o_sig = set(o.index[(o['padj'] < 0.05) & (o[ocol].abs() >= 1)])

# --- APH leaf Flight vs Ground (MoneyMaker WT = closest to OSD-767 WT leaf) ---
a = pd.read_csv(os.path.join(ROOT, 'data/aph/aph_leaf_Flight_vs_Ground_MM.csv'))
a['gene'] = a['GeneID'].map(strip_ver)
a = a.dropna(subset=['log2FC']).groupby('gene').first()
if 'significant' in a.columns:
    a_sig = set(a.index[a['significant'].astype(str).str.lower().isin(['true', '1', 'yes'])])
else:
    a_sig = set(a.index[(a['padj'] < 0.05) & (a['log2FC'].abs() >= 1)])

# --- harmonize on shared gene universe ---
shared = sorted(set(o.index) & set(a.index))
m = pd.DataFrame({'osd767_lfc': o.loc[shared, ocol].values,
                  'aph_lfc': a.loc[shared, 'log2FC'].values}, index=shared)
m.to_csv(os.path.join(T, 'leaf_FvG_merged_lfc.csv'))

rho, p_rho = spearmanr(m['osd767_lfc'], m['aph_lfc'])
r, p_r = pearsonr(m['osd767_lfc'], m['aph_lfc'])
sign_conc = float((np.sign(m['osd767_lfc']) == np.sign(m['aph_lfc'])).mean())

# concordance among union of DEGs (where signal is real)
deg_union = sorted((o_sig | a_sig) & set(shared))
md = m.loc[deg_union]
rho_deg, _ = spearmanr(md['osd767_lfc'], md['aph_lfc']) if len(md) > 2 else (np.nan, np.nan)
sign_conc_deg = float((np.sign(md['osd767_lfc']) == np.sign(md['aph_lfc'])).mean()) if len(md) else np.nan

shared_degs = sorted(o_sig & a_sig)
# directional shared core: significant in both AND same sign
core = [g for g in shared_degs if np.sign(o.loc[g, ocol]) == np.sign(a.loc[g, 'log2FC'])]
pd.Series(core, name='gene').to_csv(os.path.join(T, 'conserved_core_DEGs.csv'), index=False)

summary = pd.DataFrame([{
    'shared_genes': len(shared),
    'osd767_DEGs': len(o_sig), 'aph_MM_DEGs': len(a_sig),
    'spearman_all': round(rho, 3), 'spearman_all_p': p_rho,
    'pearson_all': round(r, 3),
    'sign_concordance_all': round(sign_conc, 3),
    'spearman_DEGunion': round(rho_deg, 3) if rho_deg == rho_deg else None,
    'sign_concordance_DEGunion': round(sign_conc_deg, 3) if sign_conc_deg == sign_conc_deg else None,
    'shared_DEGs_bothsig': len(shared_degs),
    'conserved_core_samesign': len(core),
}])
summary.to_csv(os.path.join(T, 'concordance_summary.csv'), index=False)
print(summary.T.to_string(header=False))
print('\nTop conserved-core genes (sig both, same sign):', core[:15])
