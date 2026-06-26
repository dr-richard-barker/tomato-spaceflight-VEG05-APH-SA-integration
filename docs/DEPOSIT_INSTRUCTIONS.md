# Deposit instructions — GitHub + Zenodo

The repository is committed locally and tagged `v1.0.0`. Follow these steps to publish.
(The GitHub CLI `gh` is not installed on this machine, so the remote is created manually.)

## 1. Create the GitHub repository
Option A — web: go to https://github.com/new, name it
`tomato-spaceflight-VEG05-APH-SA-integration`, **Public**, do **not** add a README/license
(they already exist), then create.

Option B — if you later install the GitHub CLI:
```bash
gh repo create tomato-spaceflight-VEG05-APH-SA-integration --public --source . --push
```

## 2. Push the local repo
```bash
cd "C:/Users/drric/Downloads/tomato-spaceflight-VEG05-APH-SA-integration"
git remote add origin https://github.com/<your-user>/tomato-spaceflight-VEG05-APH-SA-integration.git
git branch -M main
git push -u origin main
git push origin v1.0.0          # push the release tag
```

## 3. Link to Zenodo (DOI on release)
1. Sign in at https://zenodo.org with your GitHub account.
2. Go to **Account → GitHub**, find the repo, and toggle it **ON** (this enables archiving).
3. Back on GitHub, create a **Release** from tag `v1.0.0`
   (Releases → Draft a new release → choose tag `v1.0.0` → Publish).
4. Zenodo automatically archives that release and mints a DOI.
5. Copy the DOI badge Zenodo provides and paste it into `README.md` (replace the License
   badge row or add beside it), and into `.zenodo.json` history if desired.

`.zenodo.json` is already filled (title, description, creators, keywords, MIT licence,
`isDerivedFrom` links to OSD-767 and the APH study). It is set to `upload_type: "software"`
(standard for a GitHub-release archive); change to `"dataset"` if you would rather cite it as data.

## 4. Before journal submission (manuscript-side)
- Add the minted Zenodo DOI to the manuscript Data-and-code-availability section.
- Confirm the OSD-767 cultivar and the APH GeneLab OSD-# (currently marked "to confirm").
- Fill the author list in `docs/manuscript_draft.md` (`[+ OSD-767 and APH co-authors]`).

## Provenance
Every vendored input is mapped to its source study in `docs/PROVENANCE.md`. Raw FASTQ are
**not** redistributed here — they remain on NASA GeneLab/OSDR; only published/derived matrices
and the shared PhysioSpace reference are included, under the source studies' terms.
