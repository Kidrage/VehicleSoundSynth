# EV-Engine-V7

VehicleSoundSynth 五款独立发动机的V7 R2实现候选（2026-10-09）。分支：`EV-Engine-V7`。Canonical repository：`https://github.com/Kidrage/VehicleSoundSynth`（private）。

**打开 `EV-Engine-V7.maxproj` → `main.maxpat`，只开一款引擎，Audio默认OFF。**

唯一操作/参数/保存说明：[V7_MANUAL.md](V7_MANUAL.md)。工程交接：[V7_CODEX_HANDOFF.md](V7_CODEX_HANDOFF.md)。

源头主阶次控制、独立低频质量层、IONIQ pitch/收油修复、五车驾驶状态策略、实际dB/ms动态、六页Main与版本隔离保存已经实现。原生Max/BEAP编译、UI实际渲染、实车听评和硬件保护尚需本地验收，当前不是正式声音定稿。

可重复生成：`python tools/build_v7.py --check`。V7测试：`python -m unittest tests.test_v7 tests.test_v7_r2 -v`。全量严格测试：`python -m unittest discover -s tests -v`。Linux可显式用 `tools/validate_v7.py --portable`，不可将skip称为通过。

V7基于 `fed2b78ecfabc84d673207b3a5f714b89f76720f`，保留旧设计器/Gen/旧入口用于A/B，旧用户说明从当前树移除。`main`未合并或修改。交付包包含实际发布commit记录；本地合成审计Git的commit不能替代该记录。

保留许可：[ASSET_LICENSES.md](ASSET_LICENSES.md)。不可提交`media/local/`、`presets/local/`、私有参考录音或凭据。

本轮延续已存在的V7提交 `e979b0cf261004cc60cd70de1cb5dbd747812092`，不覆盖分支。新增次阶次A/B源增益、高速固定质量/高频补偿（四项默认0），补齐Ferrari实际SF90负载包络，加入驾驶策略迟滞、实际IONIQ发声参数与只读频段监视、8项保存核验和严格版本迁移。新增模块不是已通过实车标定的产品预设。最终发布SHA与测试结果见交付manifest，不把临时传输提交当成正式交付。
