# V7 Repository Guide

Active branch `EV-Engine-V7`, source checkpoint `fed2b78ecfabc84d673207b3a5f714b89f76720f`. Current authority is `AGENTS.md` plus `V7_CODEX_HANDOFF.md`. Only one user manual: `V7_MANUAL.md`.

Entry: `EV-Engine-V7.maxproj` → DSP-free `main.maxpat` → one `EV-Engine-V7-<profile>.maxpat` → `patchers/v7_profile_runtime_host_<profile>.maxpat`.

`tools/build_v7.py` creates versioned copies and five live adaptations from preserved V6 seeds. `tools/v7/` owns schema, drive transformation, source/dynamics/mass Gen recipes, graph/UI and state templates. `assets/v7/resource_map.json` binds sources and protected SHA256; `generated_sha256.json` guards generated outputs.

V7 numeric state: `code/v7_profile_state.js`; native owners use isolated v7_ paths; publish complete tone with `tools/v7_bind_profile.py`. No automatic V6-local import. No unknown worktree overwrite.

Gen belongs in Max project code category with kind `gendsp`; .maxpat belongs in patchers. User BEAP runtime dependencies are still required for native acceptance.

Use `tools/validate_v7.py` and strict old unittest suite; portable dependency skips are explicit. Original V6 launcher tests use frozen `assets/v7/main_v6_template.json`; V7 has separate current UI/graph tests. Native Max and in-car validation remain required, not implied by CI.
