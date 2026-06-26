# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions use semantic versioning.

## [1.0.0] — 2026-06-26

First public release: cross-mission integration of two ISS tomato spaceflight
RNA-seq studies (OSD-767 × APH/SA).

### Added
- Reproducible Python pipeline (`run_pipeline.py`) with modules:
  - `01_harmonize_concordance.py` — gene-level cross-study concordance (non-replication).
  - `03_pattern_convergence.py` — PhysioSpace stress-pattern convergence (core result).
  - `04_figures.py` — Figures 2–5.
  - `05_celltype_localization.py` — Figure 6 (cell-type localization).
  - `06_schematic.py` — Figure 1 (concept schematic).
  - `physiospace.py` — shared PhysioSpace engine.
- Vendored, provenance-tracked inputs from both source studies (`data/`, see `docs/PROVENANCE.md`).
- Result tables (`results/tables/`) and publication figures (`results/figures/`, PNG + SVG).
- Manuscript draft with embedded figures (`docs/manuscript_draft.md` + Word version).
- Deposit metadata: `.zenodo.json`, `LICENSE` (MIT), `requirements.txt`.

### Key findings (frozen at v1.0.0)
- Leaf Flight-vs-Ground responses do **not** replicate gene-by-gene (Spearman ρ = 0.05; 9 shared DEGs).
- Stress-pattern response **is** conserved; OSD-767 spaceflight (root) matches APH SA-deficient
  NahG state (Pearson r = 0.78, p = 0.001).
- Monotonic SA-status gradient (SA −0.20 → MM −0.15 → Mock +0.66 → NahG +0.78).

### Notes / open items
- Optional joint raw-FASTQ re-quantification deliberately out of scope (meta-integration design).
- To confirm before journal submission: OSD-767 cultivar; APH GeneLab OSD-# accession.
