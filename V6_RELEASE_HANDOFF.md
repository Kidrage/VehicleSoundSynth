# V6 发布交接 — 用户认可快照（2026-09-10）

## 决策与范围

用户明确表示当前 patcher 已满意，要求推送远端并补齐 V6 handoff 和使用说明。
发布目标：私有仓库 `git@github.com:Kidrage/VehicleSoundSynth.git`，分支
`codex/v6-layering-dna-pad-pop`；不合并、不推送 `main`。
本次只补文档并发布已有实现，不修改 DSP、patcher、参数、工厂状态或现有音色。

本机工程：`/Users/saintpeter/Downloads/VehicleSoundSynth-V6`。
启动：`VehicleSoundSynth-V6.maxproj` → `main.maxpat` → 单一车型。
操作、调音和保存：[V6_USER_GUIDE.md](V6_USER_GUIDE.md)。
代码路线：[.codex/REPO_GUIDE.md](.codex/REPO_GUIDE.md)；消息契约：[README.md](README.md)。
此前完整技术记录：[PROJECT_HANDOFF.md](PROJECT_HANDOFF.md)。

## 当前发声系统

| 车型 | Sound DNA | Soundscape | Pop |
|---|---|---|---|
| EV | 原有 EV DNA | V5 独立行驶 body/cavity bed | V4，仅手动预览 |
| V10 | V2，≤1200 RPM 保留原输出，1200–3000 RPM 混入行驶强化 | V5 | V4，保留 ICE 条件 |
| V12 | V2，同上但独立车型参数与声纹 | V5 | V4，保留 ICE 条件 |
| IONIQ6N | 原有电驱 DNA | Ignition/Evolution/Lightspeed mode bed V2 | V4，保留模式和 e-Shift 门控 |
| Ferrari | 原有 realism-V2 DNA | V7，保留 V6 压力／腔体／Direct Body，断开两条独立机械／空气返回 | V3 |

五车型都新增独立 `vehicle_noise_<profile>~`，取代 Road Air；公共消息
`road_level_db` 不变，−60 dB 精确静音。Noise 与 Soundscape Enable 独立。
所有 Pop 共用已跟踪的 CC0 `media/ferrari_pop_v3.wav`（240 ms、最多两个播放器），
SHA-256 `cf63aab2c16eee3efcf3e94c07baf3a3a1a5c04a5509009174c46559bb49133a`。
发动机连续音频不读取用户提供的 Ferrari／IONIQ 参考录音。

## 维护边界与持久化

- 生成器：`tools/build_project.py`，局部配方在 `tools/ice_dna_v2.py`、
  `tools/soundscape_bed.py`、`tools/noise_layer.py`。先向临时目录生成，不能直接覆盖生产工程。
- 当前 seed-once BEAP 图归用户所有；旧图和旧 factory 保留，不删除、不偷偷迁移。
- Ferrari/IONIQ DNA、启动、驾驶／键盘／手柄、既有空间 FX、EQ 和 dynamics 保持原状。
- 既有 Chorus/Reverb/Cabin 仍存在；这不是零混响版。不要在整理／发布时顺便移除。
- 新 local-state namespace 隔离旧版本，只迁移兼容参数；Noise 和新 Pop 独立保存。
  新存储使用显式 Save，禁止把最后读取的 factory 当成自动保存目标。
- Main 的 Save Profile Sound 仅保存 Mixer／SC／EQ，其他 Designer 单独 Save。
- 本地 `main.maxpat` 原有 Max 序列化／布局改动保持不动，不在本次提交中；
  文本／对象引用与线端点集合核对一致，但不宣称与远端字节相同。
  原有旧手册移入 `docx/` 的改动亦不提交、不回滚。
- 本机 `presets/local/` 与 `media/local/` 不发布。云端是可分发代码和工厂配置，
  不是本机私人 preset 的逐字快照；回退私人调音还需本地备份。

## 验收与已知限制

**用户听感验收：** 2026-09-10 明确认可当前声音并授权发布；据此冻结，不再调音。

**客观验证：** 发布检查结果在下方记录。此前 2026-09-09 记录为 240 项测试通过、
两次新目录生成一致、保护资源 hash 一致；详情与具体限制见
[历史测试记录](.agentlab/V6_LAYERING_2026-09-09.md)。

**不能声称完成的原生 QA：** 之前 Max 自动化测试被保存对话框阻塞，任务实例在备份后
按用户授权强制退出。最终 Gen 原生重新编译、五车型全输出录音矩阵、等响度比较、
原生 Save/Reload/Reset/reopen 全矩阵没有完整有效证据。用户认可与自动化通过是两件事。
本次不启动 Max，不更改任何在用实例，也不虚报“全部窗口本次保存退出”。

Ferrari 低频静态感诊断：RPM cadence 链路正常；保存的 Follow 0.42 下，740→6500 RPM
时两个主 body 模态仅约 142.9→145.4 Hz、212.3→216.2 Hz，持续压力纹理仍激励这些模态。
Cabin Rumble 也有独立固定结构共振。此结论来自磁盘图和公式，不是已完成的听觉隔离。
此处是现有设计记录，**本次不修、不重调**；将来只有用户重新要求才做 Enable/Solo A/B。

## 版本与安全回退

实现基点：`b609e8b729d0986a9c47920bf3c23a325c45b2e5`。历史已认可冻结标签
`v6-accepted-2026-09-04-672ad62` 仍保留。不要移动旧标签或 reset 当前工作区。

本地完整冻结（含当时 dirty/local 状态）位于
`/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/layering-dna-pad-pop-20260909.XxpeKuAh`；
任务 Max 恢复备份位于同一隐藏备份目录的 `max-forcequit-13355.EFLje3`。
二者不发布到 GitHub，也不打包私人录音到 Truenas。

需要回退时，先保存并退出相关 Max，备份现有 local preset／BEAP 图，
在另一个父目录检出所需历史提交，末级目录仍命名 `VehicleSoundSynth-V6`。
只打开一份工程，防止 Max 同名 abstraction／Gen 搜索路径或缓存串用。
不要对脏工作区使用 hard reset，不要把新 namespace preset 直接灌入旧图。

## 发布检查记录

2026-09-10 本机 `python3 -B -m unittest discover -s tests -q`：240 项通过，252.910 秒。
实际 Git 暂存区的干净发布副本（不含本机 Main diff／私人 preset）：同一命令 240 项通过，260.115 秒。
`git diff --check` 和 `git diff --cached --check` 通过；文档本地链接有效，
暂存范围排除私人录音／preset／恢复文件／手册移动，常见密钥格式扫描无命中。
本次未启动 Max，也未改写任何运行时声音资源。
本分支没有跟踪 CI workflow；仓库 API 可见两个历史临时 workflow，但不能视为本提交的测试通过。
推送后的具体 commit/check 状态由交付回执核对；本地测试不等同 GitHub CI。
发布提交可用 `git log -1` 核对，远端应与本地发布 SHA 一致。
远端 `main` 在发布前为 `ac2b37d8639027d79934a2023cf8d1d37d3b2f96`。

## 给下次维护者

没有已授权的下一轮音色调整。先问清新问题、选择最小范围，保护当前已认可声音。
若用户要求排错，可用 `diagnosing-bugs`；仓库导航用 `repo-navigation-token-saver`。
原生 Max 测试必须单一任务实例、临时独立工程、保存有意改动并关闭所有任务窗口，
最后退出任务 Max；不得操作用户自己的实例或输出进程完整环境／凭据。
