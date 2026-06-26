"""Master orchestrator for the OSD-767 x APH tomato spaceflight integration.
Runs the meta-integration modules in order. All inputs are the two studies'
published matrices/scores (see docs/PROVENANCE.md); no raw FASTQ required.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = [
    '01_harmonize_concordance.py',   # gene-level cross-study concordance (non-replication)
    '03_pattern_convergence.py',     # stress-pattern convergence (published scores) — core result
    '04_figures.py',                 # Fig 1-4
    '05_celltype_localization.py',   # Fig 6
    '06_schematic.py',               # Fig 1 (concept schematic)
    # '02_joint_physiospace.py'      # optional: re-projection using the sparse 116-gene reference
]
for m in MODULES:
    print(f'\n=== running {m} ===')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'code', m)], cwd=os.path.join(HERE, 'code'))
    if r.returncode != 0:
        sys.exit(f'FAILED: {m}')
print('\nAll modules complete. See results/tables and results/figures.')
