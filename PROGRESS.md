# Project progress — OSD-767 × APH cross-mission integration

Single running status log for the integration (capstone) paper of the three-paper tomato
spaceflight set. Last updated: 2026-06-26.

## Thesis
Spaceflight drives tomato into a salicylic-acid–deficient, biotic-defense-primed
transcriptional state. Gene-level leaf responses do **not** replicate across mission/cultivar/
chamber, but the stress-pattern (PhysioSpace) response is conserved, and the OSD-767 spaceflight
signature matches the APH SA-deficient (*NahG*) state. SA signalling is the conserved causal buffer.

## Headline results (CI-verified each push)
| Result | Value |
|---|---|
| Gene-level leaf concordance (non-replication) | Spearman ρ = 0.05; 9 shared DEGs |
| Pattern-level: OSD-767 root vs APH **NahG** | Pearson r = 0.78; perm p = 0.0004; bootstrap 95% CI [0.39, 0.93] |
| Contrast: OSD-767 root vs APH **MM (WT)** | r = −0.15; perm p = 0.59 (null, as predicted) |
| SA-status gradient (decreasing SA) | SA −0.20 → MM −0.15 → Mock +0.66 → NahG +0.78 (monotonic, ρ = 1.0) |

## Status

### Done ✅
- [x] Assess APH dataset; confirm mergeability (shared genome/IDs/PhysioSpace)
- [x] Lock decisions (meta-integration; leaf-to-leaf; companion paper; Python)
- [x] Stand up repo skeleton + vendor inputs from both studies (`docs/PROVENANCE.md`)
- [x] Harmonize + per-study leaf Flight-vs-Ground (`code/01`)
- [x] Core result: gene-level concordance + joint PhysioSpace convergence (`code/01`, `code/03`)
- [x] SA-axis tuning model + cell-type localization (`code/03`, `code/05`)
- [x] **Build Fig 1 concept schematic** → `results/figures/Fig1_concept_schematic.png` (`code/06`)
- [x] Data figures 2–6 (`code/04`, `code/05`)
- [x] **Write Introduction + Discussion prose** → `docs/manuscript_draft.md` (§1, §3)
- [x] Embed all 6 figures into the manuscript + illustrated `.docx`
- [x] Robustness: permutation + bootstrap (`code/07`)
- [x] Cover letter (`docs/cover_letter.md` / `.docx`)
- [x] Deposit: public GitHub repo, v1.0.0 release, CITATION.cff, Zenodo badge pre-wired
- [x] GitHub Actions CI ("reproduce") — runs pipeline + asserts headline numbers on every push
- [x] Security: token removed from machine; repo/history verified clean of any token

### Open — needs the author ⛏️
- [ ] **Mint the Zenodo DOI** — link the repo at zenodo.org, publish a fresh release; badge then activates
- [ ] Author list (manuscript + `CITATION.cff` + `.zenodo.json`)
- [ ] Confirm OSD-767 cultivar
- [ ] Confirm APH GeneLab OSD-# (data-availability statement)
- [ ] Fill cover-letter `[Email]` / `[ORCID]`

### Optional extras (offered, not yet built)
- [ ] Reviewer-response prep doc (anticipated critiques + answers)
- [ ] Cross-link the 3-paper set (OSD-767 ↔ APH ↔ integration repos/manuscripts)
- [ ] Robustness sensitivity sweep (genes_ratio 0.02–0.10; 15-axis vs 20-axis space)

## Reproduce
```
pip install -r requirements.txt
python run_pipeline.py        # regenerates all tables + figures
python code/verify_ci.py      # asserts the headline results
```

## Source studies
- **OSD-767** (VEG-05; light × spaceflight; leaf + root) — see `docs/PROVENANCE.md`
- **APH** (MoneyMaker vs NahG; ± SA × spaceflight; leaf) — see `docs/PROVENANCE.md`
