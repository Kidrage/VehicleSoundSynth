# EV-Engine-V7

VehicleSoundSynth 五款独立发动机的V7实现候选。分支：`EV-Engine-V7`。Canonical repository：`https://github.com/Kidrage/VehicleSoundSynth`（private）。

**打开 `EV-Engine-V7.maxproj` → `main.maxpat`，只开一款引擎，Audio默认OFF。**

唯一操作/参数/保存说明：[V7_MANUAL.md](V7_MANUAL.md)。工程交接：[V7_CODEX_HANDOFF.md](V7_CODEX_HANDOFF.md)。

源头主阶次控制、独立低频质量层、IONIQ pitch/收油修复、五车驾驶状态策略、实际dB/ms动态、五页Main与版本隔离保存已经实现。原生Max/BEAP编译、UI实际渲染、实车听评和硬件保护尚需本地验收，当前不是正式声音定稿。

可重复生成：`python tools/build_v7.py --check`。V7测试：`python -m unittest tests.test_v7 -v`。全量严格测试：`python -m unittest discover -s tests -v`。Linux可显式用 `tools/validate_v7.py --portable`，不可将skip称为通过。

V7基于 `fed2b78ecfabc84d673207b3a5f714b89f76720f`，保留旧设计器/Gen/旧入口用于A/B，旧用户说明从当前树移除。`main`未合并或修改。交付包包含实际发布commit记录；本地合成审计Git的commit不能替代该记录。

保留许可：[ASSET_LICENSES.md](ASSET_LICENSES.md)。不可提交`media/local/`、`presets/local/`、私有参考录音或凭据。
