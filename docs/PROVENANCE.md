# Data provenance

This integration vendors only **published, derived outputs** from two independent ISS
tomato RNA-seq studies. No raw sequencing data is redistributed here — raw reads remain
on NASA GeneLab under each study's accession.

| File (in `data/`) | Source study | Original artifact |
|---|---|---|
| `osd767/osd767_leaf_Flight_vs_Ground.csv` | OSD-767 (VEG-05, light × spaceflight) | `light_interaction/leaf_condition_Flight_vs_Ground.csv` |
| `osd767/osd767_leaf_VST_counts.csv` | OSD-767 | `leaf_deseq2/leaf_VST_counts.csv` |
| `osd767/osd767_physio_group_means.csv` | OSD-767 | `Supplementary_Data_12_group_means_interactions.csv` |
| `osd767/osd767_celltype_physioscores.csv` | OSD-767 | `Supplementary_Data_13_celltype_physioscores.csv` |
| `aph/aph_log2cpm_filtered.csv` | APH (MM/NahG, SA × spaceflight) | `data/processed/log2cpm_filtered.csv` |
| `aph/aph_conditions.csv` | APH | `data/raw/conditions_pivert_V2.csv` |
| `aph/aph_leaf_Flight_vs_Ground_MM.csv` | APH | `05_Source_Data_Tables/DEG_Flight_vs_Ground_MM.csv` |
| `aph/aph_physio_scores.csv`, `aph/aph_physio_interaction.csv` | APH | `05_Source_Data_Tables/physio_*.csv` |
| `aph/aph_cell_stress_delta.csv` | APH | `05_Source_Data_Tables/cell_stress_delta.csv` |
| `reference/at_stress_space.csv`, `solyc_to_at_entrez.json`, `cell_type_markers.json`, `tomato_kegg.gmt` | APH repo (shared Plant PhysioSpace assets) | `data/reference/*` |

**Reference genome:** both studies use *S. lycopersicum* SL4.0 / ITAG4.0 with versioned `Solyc` IDs.

## To confirm before submission
- **OSD-767 cultivar** (VEG-05 line — not stated in the OSD-767 manuscript).
- **GeneLab accessions**: OSD-767 (known) and the **APH study OSD-#** (not found in the APH package).
- Source **Zenodo DOIs** for both studies to cite as dependencies.
