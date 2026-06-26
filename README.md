# Tomato Spaceflight Integration — OSD-767 × APH (SA signalling)

**Cross-mission meta-integration of two ISS tomato RNA-seq studies, establishing that the
spaceflight transcriptome resembles a salicylic-acid–deficient state.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

## Summary

This repository integrates two independent ISS tomato spaceflight RNA-seq experiments:

- **OSD-767** — VEG-05 chamber, light quality (red/blue) × spaceflight, leaf + root.
- **APH** — Advanced Plant Habitat, MoneyMaker vs SA-deficient **NahG** × exogenous **SA** ×
  spaceflight × time, leaf.

### Key findings
1. **Gene-level leaf responses do NOT replicate** across the two studies (Spearman ρ = 0.05;
   sign concordance 0.51; 9 shared DEGs) — individual genes are not the reproducible unit.
2. **The stress-pattern (Plant PhysioSpace) response IS conserved**, and it matches the
   **SA-deficient (NahG)** state: OSD-767 spaceflight (root) vs APH NahG **Pearson r = 0.78
   (p = 0.001)**, vs wild-type MM r = −0.15.
3. **SA-status gradient** — similarity to the spaceflight signature increases monotonically as
   SA tone falls: SA −0.20 → MM −0.15 → pooled +0.38 → Mock +0.66 → **NahG +0.78**.
4. **Conserved axes:** biotic+hormone (BioMone), nitrogen, and cold stress are co-activated;
   light/UV is co-suppressed.
5. **Outer/epidermal localization** of the defense response in both studies (OSD-767
   exodermis/cortex; APH epidermis/trichome).

**Interpretation:** spaceflight drives tomato into an SA-deficient–like, biotic-defense-primed
state; SA signalling is the conserved causal buffer.

## Reproduce

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Outputs land in `results/tables/` and `results/figures/`.

## Structure

```
code/        physiospace.py + numbered modules (01 concordance, 03 convergence, 04 figures, 05 cell-type)
data/        osd767/, aph/ (published derived matrices), reference/ (shared PhysioSpace assets)
results/     tables/, figures/
docs/        methods.md, PROVENANCE.md
```

## Provenance & data
Only published derived outputs are vendored (see `docs/PROVENANCE.md`); raw reads stay on
NASA GeneLab. This is the **capstone of a three-paper set** (OSD-767 light paper; APH SA
paper; this integration).
