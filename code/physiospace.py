"""Shared PhysioSpace engine (faithful port of the APH study's calculate_physio_map,
itself a port of PhysioSpaceMethods::calculatePhysioMap). Used to project BOTH studies
into the identical 15-axis AT_Stress_Space_Meta reference.
"""
import json, numpy as np, pandas as pd
from collections import defaultdict
from scipy.stats import mannwhitneyu

GENES_RATIO = 0.05  # matches OSD-767 + APH (GenesRatio=0.05)

def strip_ver(s):
    return str(s).rsplit('.', 1)[0]

def load_reference(ref_csv, map_json):
    space = pd.read_csv(ref_csv, index_col=0)
    space.index = space.index.astype(str)
    with open(map_json) as f:
        solyc_to_at = json.load(f)
    return space, solyc_to_at

def fc_vs_ground(expr, ground_cols):
    """FC(gene,sample) = expr - mean(expr over ground samples). expr is log-scale."""
    return expr.subtract(expr[ground_cols].mean(axis=1), axis=0)

def map_to_at(fc, solyc_to_at):
    at = defaultdict(list)
    for g in fc.index:
        aid = solyc_to_at.get(strip_ver(g))
        if aid is not None:
            at[aid].append(fc.loc[g].values)
    ids = sorted(at.keys())
    out = pd.DataFrame(np.array([np.mean(at[k], axis=0) for k in ids]),
                       index=[str(i) for i in ids], columns=fc.columns)
    return out

def calculate_physio_map(input_fc, space, genes_ratio=GENES_RATIO):
    common = space.index.intersection(input_fc.index)
    if len(common) < 10:
        raise ValueError(f"Only {len(common)} common genes")
    Space = space.loc[common].values.astype(float)
    Input = input_fc.loc[common].values.astype(float)
    n_genes, n_stress = Space.shape
    n_samples = Input.shape[1]
    n_top = max(2, round(n_genes * genes_ratio))
    PS = np.zeros((n_stress, n_samples))
    for s in range(n_samples):
        order = np.argsort(Input[:, s])
        ll, lh = order[:n_top], order[-n_top:]
        for k in range(n_stress):
            ref = Space[:, k]; vlh, vll = ref[lh], ref[ll]
            if vlh.std() == 0 and vll.std() == 0:
                continue
            try:
                _, pv = mannwhitneyu(vlh, vll, alternative='two-sided')
                sign = -1.0 if np.mean(vlh) >= np.mean(vll) else 1.0
                PS[k, s] = np.log2(max(pv, 1e-300)) * sign
            except ValueError:
                pass
    return pd.DataFrame(PS, index=space.columns, columns=input_fc.columns), len(common)
