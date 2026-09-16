# IONIQ V3 / Ferrari V4：可回退音色修复与本地验收

日期：2026-09-16。性质：用户授权的工程修复候选，不是已通过 Max 听评的发布版。

## 1. 仓库绑定与授权

Canonical repository：`Kidrage/VehicleSoundSynth`（private）。
仓库地址：`https://github.com/Kidrage/VehicleSoundSynth`。
目标分支：`codex/v6-ioniq-dna-accel-detail`。
固定修改基线：`467fd7243dc9f419b63e61d28f7d5ea06b309434`。
默认分支 main 保持 `ac2b37d8639027d79934a2023cf8d1d37d3b2f96`；不合并、不推送 main。
此次用户授权修复这条分支的 IONIQ 与 Ferrari，并由用户在本地测试；这取代本分支旧文档的“只改加速两阶次”和“测试前不能上传”范围限制，但不构成量产/听感验收。
修复提交 SHA 由本次交付 manifest、GitHub 分支和 `git rev-parse HEAD` 提供；本文固定的是可复核的父版本，不能将临时 QA 分支视作 canonical。

入口：`VehicleSoundSynth-V6.maxproj` → `main.maxpat` → 仅打开一个车型。
IONIQ：`VehicleSoundSynth-IONIQ6N.maxpat` / `patchers/vehicle_engine_ioniq6n~.maxpat`。
Ferrari：`VehicleSoundSynth-Ferrari.maxpat` / `patchers/vehicle_engine_ferrari~.maxpat`。

Codex 开始前读取：`AGENTS.md`、`.codex/MAINLINE.md`、`.codex/REPO_GUIDE.md`、`.codex/source_index.txt`、`PROJECT_HANDOFF.md`、`SOUND_DESIGN_GUIDE.md`、本文件。

## 2. 证据边界与 Ferrari 历史定位

未获得本机 ignored preset、未提交 Designer 连线和实际 A/B WAV。没有声称听到用户当前实例，也没有把数值模型当成 Max 录音。
检索到了 2026-09-08 的 `VehicleSoundSynth_Design_Review_Codex_Handoff_20260908.md`，并核对完整 Git 历史；未找回标题为“Ferrari 素材提取”的完整原聊天。因此早期参考版本的选择是有代码证据的工程判断，不是伪造用户曾对某 commit 的认可。

历史链：
- `38bcf10edbb4b4c90b4e48a57120654e50cbcafb`：Ferrari 初版 V10 interpretation。
- `adca3885a8b39e5ca72c25121f7be93025b888cb`：realism V2，压力激励、分路声学滤波和更暗的高频边界。
- `cff9d0872af7a7b14f07a35b7b8d37de3078b59f`：layering 发布快照。其 Ferrari V2 Gen 与 V2 Designer 相对 adca388 完全未变；SC/Pop 已演进。
- `012cd378cf54cd81ac9db2bf41f85fa5e494e9d3` 起：Ferrari V3 四组源替代 V2，而非在 V2 上简单加旋钮；候选最后进入 467fd72。

Ferrari 退化的结构性原因候选：V2 参数退出活动链、原来的压力调制材质/不同带通色彩被简化，V3 Character 与 Core 较多共享相同主阶次；Noise 独立后默认 Main -60 dB 静音，不应误认为其原有随机材质仍在 DNA 里。具体各原因对用户听感的比例仍需本地分层 A/B。早期 V2 的 1350 Hz 输出低通是一种偏暗的取舍，不是普适真实标准。

## 3. IONIQ：实际改动

保留新 drivetrain、7600 满油升挡、8000 红线、挡位合法性、模式过渡、全部 Soundscape/activation/Ready 基础代码。
新版本：`patchers/ioniq6n_sound_dna_v3~.maxpat` → `patchers/ioniq6n_powertrain_v3~.maxpat` → `gen/ioniq6n_powertrain_v3.gendsp`。

只在 DNA 内部进行声学转速拟合：
```
d = max(smoothed_rpm - 2600, 0)
compression = 0.5 * (d < 1600 ? d*d/3200 : d - 800)
rpm_for_tone = smoothed_rpm - ReferenceRestore * compression
root = clamp(52 + 0.047 * rpm_for_tone, 52, 522)
```
映射连续且一阶导数连续，斜率由 1 平滑到 0.5；<=2600 保持原映射；7600→5500，8000→5700。不是统一乘比例、不是转速封顶，也不反馈到 CAN/RPM/gear、Soundscape 或 DriveModel。
目的：在新的高转速区间重新接近原 185 Hz Body LP / 315 Hz Cavity BP 的阶次相对位置。固定 BEAP 图和参数不改。

起步存在感：复用 1.5×、2.25× 两条阶次，1900–2600 平滑进入、3000–4500 退出；使用正加速 × sqrt(throttle × positive load)，65 ms attack / 220 ms release。最高额外振幅为 1.28 / 1.40；不是整体推大主音量。1900 以下修复贡献精确为零。原 Accel Orders 保持独立，0/.30/1 语义不变。
没有新增 IONIQ 振荡器、噪声、失真、混响；没有更改原 Body、Ready 或收油分量公式。

## 4. Ferrari：实际改动

新版本：`patchers/ferrari_acoustic_v4~.maxpat` → 一份 `gen/ferrari_dna_source_v4.gendsp`，分为 DNA 四组与原有 Noise 三个原始残余输出。
DNA Designer：`patchers/ferrari_dna_v4_designer~.maxpat`。

保留原 V3 八宏、四组混音/滤波、独立 Body carrier、输出保护与单声源时钟。修复不是整个 V2 回滚，也不承诺复制未知的本机 V2 preset。
- 复用相同 phase 的有限压力谐波，向 V2 的五次幂压力形态恢复部分二、三阶比例。
- Character 减少复制主阶次的权重，引入参考中 1.37/1.43、2.61/2.73 比率的连续相位材料振荡器；围绕 355/405、820/930 Hz 的宽声学窗口塑形，不把所有材质都随 RPM 一起平移。
- Body 减少独立低频持续音的比例，加强已有半阶与压力相关成分，不靠更响的低频掩盖主体单薄。
- 接通原 V3 没有转发的 accel 到新 V4 声源：快边沿 35/160 ms、慢质量 120/420 ms；收油先退 Upper，Body 受 bounded release_mass 控制稍晚退。
- 4 个新增材料振荡器是确定性声音设计，不是“真实进气/排气干声”。没有新随机噪声进入 DNA。

原 V3 `v3_pressure/v3_peak` 和 residual out8–10 计算不改；Noise 仍为独立 Main 推子，仍可 -60 精确关闭。禁止为使新音色显得丰富而自动开 Noise。

## 5. A/B 操作与状态保护

两款 DNA Designer 底部有 **Reference Restore**：1 默认修复；0 上一候选的声源行为；0.5 中间值。80 ms 平滑，不重置振荡器相位。
注意：0 是 467fd72 候选源的回退，不是让旧驾驶模型和全部旧软件状态一起回来。音高改变后相位需要稳定或重启相同测试条件；切到 0 的瞬间不应期待逐样本 null。

新状态：
- IONIQ：`presets/local/ioniq6n_sound_dna_v3.json`，首次加载按 V2→V1 的顺序导入兼容宏与 BEAP 值。
- Ferrari：`presets/local/ferrari_sound_dna_v4.json`，首次加载导入 V3 兼容宏与 BEAP；不把 V2 不同语义的旋钮伪装成 V3 值。
- 新状态优先；缺项回 factory。坏字符串、NaN、数组长度错误回默认。只写新文件。
- 明确点击 **Save DNA**；Save Profile Sound 不代替它。Factory Reset 会保存新版本 factory，不影响旧 namespace，但会覆盖本次新版本已保存的调整。
- 旧 Designer、factory、Gen 和 ignored preset 均不覆盖。新 Designer 为 seed-once，局部 installer 重跑也保留已存在的新 seed。

## 6. 本地启动顺序

先保存工作、关闭 Max。检查 origin、当前分支、`git status --short --branch`、HEAD；脏工作区不要 reset/clean。
工作区干净且当前就是目标分支时：
```sh
git fetch origin
git pull --ff-only origin codex/v6-ioniq-dna-accel-detail
```
更安全的 A/B 方式是保留原目录，另外建 worktree：
```sh
git fetch origin
git worktree add --detach ../VehicleSoundSynth-TimbreRepair origin/codex/v6-ioniq-dna-accel-detail
```
若比较用户现有音色，先将原目录的 `presets/local/*.json` 备份并复制到新的测试目录（不得反向覆盖原目录）。只复制 JSON，不同步到 GitHub。新版本首次读取时自动迁移两款 DNA，其他 namespace 保持原值。没有这些私有状态的新 clone 比较的是 factory，而不是用户现场调音。
本机未提交的 Designer 连线改变不会自动迁移；此时保留原目录作为最终参考，先由本地 Codex 对比旧 Designer diff，不能用 Factory Reset 代替调音找回。

直接打开 maxproj 即可；下载/提交里已经包含生成的 patcher，不需要先重建全工程。仅需要重生成局部资源时运行 `python3 tools/install_timbre_repair.py`。
一次只运行一个车型实例。先 IONIQ，再 Ferrari；不要同时开两套同名全局 receive 的工程。

## 7. 建议 A/B 工况与素材

本轮没有 Max 录制 WAV；以下是待本地录制清单，不是已生成素材：
- I0：IONIQ 650 怠速、1450 activation，确认与原候选不变。
- I1：IONIQ 固定 2600、4000、6500、8000 RPM，各 0.2/0.5/1 load，DNA Solo，Restore 0/1。
- I2：同一踏板脚本起步→加速→换挡→高速→快收油；记录真实驱动 RTPC，不推断 CAN。
- I3：Soundscape 三模式 Solo 与完整混合，确认铺底、模式和空间状态没变。
- F0：Ferrari 固定 740/2600/4000/6500 RPM，Core/Body/Character/Upper Solo，Restore 0/1。
- F1：Ferrari 全层加速→快/缓收油→换挡，Noise 保持原推子；另做 Noise Solo 证明不变。
- F2：adca388/cff9d08 的旧 V2（独立工作树）作历史参考，保持同轨迹与监听链。

所有素材保留未归一化原件；听评副本仅作固定增益响度匹配，目标 ±0.5 dB，不做逐帧 AGC。先监听，再实车；分别评价起步动作、中低频重量、音调单一程度、材质自然度、疲劳和空间铺底。主观接受前不改已认可 SC 补偿 DNA。

## 8. 测试与验收边界

运行：`python3 -m unittest discover -s tests -v`。
数值检查：`python3 tools/check_timbre_repair_math.py <repo外QA目录>`。
数值检查是自写标量 C++ 的 GenExpr 子集代理，不是 Cycling '74 导出的源代码；84 工况覆盖 44.1/48 kHz、不同 RPM/负载，检查有限输出、A/B0、IONIQ低转速保护、Ferrari Noise 不变。它不能证明 BEAP/完整 Max 无削波，更不能证明好听。

Linux 首轮全测试曾有：新增 Gen 清单和实际活动 Designer 版本断言未更新，以及系统没有 macOS `afconvert`。前两项已更新并做针对性回归；afconvert 不能用 mock 假装通过，应在 macOS 跑原完整测试。最终实跑结果以交付 QA report/Actions 日志为准，不把旧文档测试计数拿来当本次结果。

必须本地 Max 验证：项目类型/缺失对象、Gen 编译与 outlet/patchcord、实际非静音、峰值/削波、启动停止门控、保存→重开持久化、三 Soundscape 模式、极限 RPM、连续换挡、快速收油与踏板变化。CPU 必须完整工程实测；新增 4 个 Ferrari 材料振荡器不等于任何已测 CPU 百分比。
通过前只称 repair candidate。验收要求：IONIQ SC/activation 不退化，起步与高速优于 Restore0；Ferrari 单一主音调减轻且有中低频支撑，Noise关闭仍能独立成立；同响度确认改善，无主观尖锐/轰鸣、无门控泄露。

## 9. 后续阶段与禁止事项

P0 已实施：源码可回退修复、独立 namespace、局部生成、结构和数值测试。先完成本地验证。
P1 仅允许依据 A/B 录音调整 `tools/timbre_repair.py` 内有界系数或新 Designer 参数；一次一款，不同时调 Main EQ/SC。
P2 若确认“需要的是 V2 随机压力材质”，再单独讨论 Noise 中受控窄带压力纹理；不越权塞回 DNA、不自动取消 Noise mute。
禁止整车重构、回滚 eShift、改动 EV/V10/V12、复制未授权参考音频进入 runtime、虚构源部件/物理 IR、强推或污染 main、覆盖用户 seed/local state。

## 10. 回滚

即时听评：Reference Restore=0，并等待平滑稳定；需要保存则 Save DNA。
完整软件回滚：关闭任务 Max，重新打开保留的 467fd72 工作树及其备份状态。或在干净 feature 分支 revert 本次修复 commit，保留记录；不要 `reset --hard` 或 force-push。
本次新的 V3/V4 local JSON 可保留，旧版本不会读取它们。
