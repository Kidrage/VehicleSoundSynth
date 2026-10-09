# Active branch index — EV-Engine-V7

Canonical private repository: https://github.com/Kidrage/VehicleSoundSynth
Default branch remains `main` at `ac2b37d8639027d79934a2023cf8d1d37d3b2f96`; no merge or default-branch change authorized.
Active development: `EV-Engine-V7`. R2 starts from exact V7 `e979b0cf261004cc60cd70de1cb5dbd747812092`.
V6 source checkpoint: `fed2b78ecfabc84d673207b3a5f714b89f76720f`.

Current authority: `AGENTS.md`, `.codex/REPO_GUIDE.md`, `V7_CODEX_HANDOFF.md`.
Only user manual: `V7_MANUAL.md`. This file is an engineering index, not a second manual.
The previous V6-only restrictions and historical module map remain in Git history at the R2 base; do not treat them as the active V7 allowed branch.

Before editing, compare branch/HEAD/worktree to the exact delivery manifest. Preserve 113 source seeds and all uncommitted local tuning. Run `tools/build_v7.py --check`; do not run the old all-tree builder.
R2 recipe: `tools/v7/review.py`; numerical contracts: `tools/v7/schema.py`; native save-owner contracts: `assets/v7/state_contracts.json`.
Native Max, save/reopen and in-car acceptance are still separate gates, not inferred from portable CI.

Historical frozen source lineage: V4 tag `v4.0.0` (`6aa49d0`); keep its source/asset restrictions intact.
