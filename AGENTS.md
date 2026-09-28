# VehicleSoundSynth V7 Repository Instructions

## Active V7 authorization (2026-09-28)

The user authorized branch **EV-Engine-V7** from **fed2b78ecfabc84d673207b3a5f714b89f76720f**, all-five-profile source balance/independent LF, driving/envelopes, Main UI, per-profile persistence and removal of old manuals. This scope supersedes previous Ferrari-only/protected-control restrictions on this branch, NOT main protection, local preset protection or native/listening acceptance.

Read `.codex/REPO_GUIDE.md`, `PROJECT_HANDOFF.md`, `SOUND_DESIGN_GUIDE.md`, `V7_MANUAL.md` and `V7_CODEX_HANDOFF.md`.

- Open `EV-Engine-V7.maxproj` and `main.maxpat`. One active runtime; audio OFF on load.
- V7 generator: `python tools/build_v7.py --check`; explicit guarded regeneration: `--refresh-generated`. Do not run the old all-tree builder on V7. Keep preserved 113 source seeds byte-identical.
- Recipes: `tools/v7/`; generated live resources have `v7_` names; all local state under `presets/local/v7_*`. Never overwrite/import V6 local state silently.
- Maintain single-source parameter contracts with actual units, endpoint meaning, live routing, readback and save/reopen tests. Do not fake extended ranges on inactive macros.
- Main remains DSP-free. Same DNA fader/solo/lifecycle must govern new LF mass. Do not feed the independent bed into legacy rumble. No permanent whole-bus auto-normalization or makeup masking spectral imbalance.
- Sole user manual: `V7_MANUAL.md`; README/guide/PROJECT_HANDOFF are indices or engineering metadata, not competing manuals.
- Tests: `python -m unittest tests.test_v7 -v`; full strict `python -m unittest discover -s tests -v`; `tools/validate_v7.py --portable` explicitly lists unavailable prerequisites. Never call scalar/VM/JSON tests native Max acceptance.
- Keep ASSET_LICENSES and asset provenance. No tokens, credentials, local audio or private-reference derivatives in commits/artifacts.
- Before publishing, verify branch/HEAD/worktree and preserve old A/B. Never merge main, change the default branch or force push.
- Native gate: actual Max 8.6.5 compile, non-silence, missing objects, transitions, output clipping/GR, save/reopen, all-five no cross-talk. Then level-matched computer/vehicle listening; physical speaker protection is not proven by sample clipping.

## Historical constraints

Historical agent instructions are in the baseline commit; their old allowed-only branch scopes are not the active V7 scope. Start/Pop media provenance and V4 sibling repositories remain protected. V4 was frozen at `v4.0.0`.
