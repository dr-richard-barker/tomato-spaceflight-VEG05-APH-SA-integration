# Methods — cross-study integration

## Rationale
Two independent ISS tomato RNA-seq studies are integrated: **OSD-767** (VEG-05 chamber;
light quality × spaceflight; leaf + root; RSEM quantification) and the **APH** study
(Advanced Plant Habitat; MoneyMaker vs SA-deficient NahG × exogenous SA × spaceflight ×
time; leaf; STAR quantification). Study identity is perfectly confounded with cultivar,
chamber, and quantifier, so integration is performed on **relative quantities**
(fold-changes and PhysioSpace patterns), and conserved signal is defined as what
replicates across both studies despite those differences.

## Gene-level concordance (Module 1)
Leaf Flight-vs-Ground log2 fold-changes from each study's deposited DE table were matched
on version-stripped `Solyc` IDs over the shared gene universe (16,516 genes). Concordance
was quantified by Spearman and Pearson correlation, genome-wide sign concordance, and the
overlap of significant DEGs (each study's own significance calls).

## Stress-pattern convergence (Module 3, primary)
Each study's **published full-reference PhysioScores** (Plant PhysioSpace,
AT_Stress_Meta, 15 axes) were used directly — OSD-767 group-mean flight effects (root and
leaf, per light condition) and APH per-axis flight effects stratified by genotype (MM,
NahG) and treatment (SA, Mock). Cross-study similarity was the Pearson/Spearman correlation
of the 15-axis flight-effect vectors. An **SA-status gradient** was constructed by
correlating the OSD-767 (root) spaceflight signature against APH groups ordered by SA tone
(SA → MM → pooled → Mock → NahG).

> Note: the APH repository's `at_stress_space.csv` is a compact 116-gene curated reference;
> it is too sparse to re-project OSD-767 (only 78 genes map). A direct re-projection module
> (`02_joint_physiospace.py`) is included for completeness but the primary analysis uses each
> study's published full-reference scores.

## Cell-type localization (Module 5)
Cell-type defense-axis scores were compared: OSD-767 `Biotic.Hormone` (AT_Stress_Space,
cell-type projection) vs APH `BioMone` (cell-type flight delta).

## Software
Python 3.10+, numpy, pandas, scipy, matplotlib. PhysioSpace scoring reuses the APH study's
`calculate_physio_map` (a port of `PhysioSpaceMethods::calculatePhysioMap`), GenesRatio = 0.05.
Run `python run_pipeline.py`.
