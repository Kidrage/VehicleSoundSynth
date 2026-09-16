# IONIQ：主单音平衡与高速中低频保持 — 本地验收交接

性质：基于用户本轮听评实施的修复候选；不是已经通过原生 Max 听评的发布版。

## 仓库 / 基线 / 范围

- Canonical repository：`Kidrage/VehicleSoundSynth`，private。
- URL：`https://github.com/Kidrage/VehicleSoundSynth`。
- 目标分支：`codex/v6-ioniq-dna-accel-detail`。
- 固定父版本：`138a36dc71f119966796702c61b73f2ed1f97219`。
- main 保持 `ac2b37d8639027d79934a2023cf8d1d37d3b2f96`；旧认可 layering 保持 `cff9d0872af7a7b14f07a35b7b8d37de3078b59f`。
- 本轮仅修改 IONIQ 活动 DNA/Soundscape 接入；Ferrari/EV/V10/V12、驾驶/变速、Start/Pop/Noise、总线 EQ/空间效果和用户旧 preset 不变。原有 IONIQ 各版文件留作回退。
- 入口：`VehicleSoundSynth-V6.maxproj` → `main.maxpat` → `VehicleSoundSynth-IONIQ6N.maxpat`。只开一个车型/一套工程。
- 修复 commit、跟踪文件数、校验与实跑测试记录以本次交付 manifest/CI 为准，不能把父版本 SHA 当作修复 SHA。

## 开始前必读

`AGENTS.md`、`.codex/MAINLINE.md`、`.codex/REPO_GUIDE.md`、`.codex/source_index.txt`、`PROJECT_HANDOFF.md`、`SOUND_DESIGN_GUIDE.md`、本文件。先核实 origin、HEAD、分支与工作区。不能对脏工作树运行 reset/clean 或全量重建。

## 用户听评与可证实原因

用户确认总体改善，但 IONIQ 有突出的 200–300 Hz sine-like 音调；启动好，升速后中低频重量丢失，Soundscape 未补足。没有收到这轮本机 WAV、私有 preset 或未提交连线；200–300 Hz 是用户的听评定位，不是假造的录音测量。

代码证据（父版本）：
1. Gen 主阶次 `0.50+0.20*motor_order`，factory=.644；第二阶次初始=.2164，第三=.1252。主正弦振幅大约为第二阶次的三倍，所有分量还经过共享滤波。具体最终响度仍依赖负载、BEAP 与私人参数。
2. 上轮把高转速声学音高压回约 200–320 Hz，但没有重分配主阶次权重。它可能使主单音更久停留在中频，不能据此证明用户听到的唯一峰只来自这一项。
3. DNA Body 仍是 root×.5/.75，Cavity/Mechanical 继续跟随 root；Ready 的 55/110/220 Hz 固定组合在约1900 RPM退出。旧版没有持续独立的低中频质量源。
4. Soundscape 原三模式的 Osc A/B/C、native tone/texture 都由 RPM 派生 pitch 驱动；`bed_v2` 名称只表示之前独立 hiss 分离，不保证固定低频。
5. `make_ioniq6n_soundscape_beap` 原输出：120 Hz 低通为直达返回，120 Hz 以上没有干声返回，只经 Chorus/Reverb 返回。并非理想砖墙分频，也不是高频完全静音，但高频/中低频可闻度受 Motion、Space、速度及湿声比例影响。
6. 外部 EQ 同时影响需保留的层，不能创造缺失的独立声源，也不能针对移动主阶次单独恢复层间比例。本轮没有新增总线 notch。

## 实施结构

### DNA V4

`patchers/ioniq6n_sound_dna_v4~.maxpat`
→ `patchers/ioniq6n_powertrain_v4~.maxpat`
→ `gen/ioniq6n_powertrain_v4.gendsp`。

旧 core L/R 仍走原 Mid/Side 与四个 BEAP filter。唯一主阶次振幅改动为：
```
x = clamp((smoothed_rpm-1600)/1200,0,1)
w = smooth(weight_balance,80ms) * x*x*(3-2*x)
order1_gain = original_order1_gain * (1-.62*w)
```
完全进入时主阶次源振幅乘 .38（约 -8.40 dB，非整层响度）；不改本轮之前的 pitch mapping、order2/3、Ready、旧 Body 公式。1600以下本轮的源改动为零。

额外两路是独立的 Body / Cavity 压力底床，不是把总线低频抬高：两组连续慢变声源用有限的 1–5 阶 Chebyshev 分量形成分散频谱，主基频权重较低，避免再增加一根大正弦。三路恒定峰值带通 biquad，Q=1.15/1.30/1.25，频率慢变范围约144–152、252–265、404–421 Hz。它们不是物理测得的 IR。

新 out3/out4 分别与原 Mid 在 **Body/Cavity 滤波器之前**相加；四个输出复用同一 Main DNA 增益。仍受实际 BEAP 滤波、内部 Mixer 通道电平/Mute、Output VCA、总线保护控制，没有不可关闭的秘密总线。新源默认 Foundation=.70；保留 `body_pressure`、`cavity_structure` 对对应底床的控制。

### Soundscape Mode Beds V3

`patchers/ioniq6n_cinematic_soundscape_host_v3~.maxpat`
→ 三个 `patchers/ioniq6n_soundscape_<mode>_bed_v3_beap~.maxpat`
→ 共享定义、独立实例的 `gen/ioniq6n_weight_bed.gendsp`。

保留三种模式原有振荡器、native texture、BEAP、滤波、模式交叉淡化、Chorus/Reverb参数和湿声线路。新底床是额外的 **单声道中低频干声返回**，加在各声道原28 Hz高通与模式trim之前，不经过空间湿声的衰减。Main SC推子、Solo、Enable、ignition/running和模式权重仍然有效。

底床不读取 DNA 音频，不由 pitch-follow/transpose/速度直接移调；raw RPM仅负责1600–2800的进入以及极小慢变，不成为声源时钟。Pitch Follow仍控制原有运动音调，不能再把重量层带出目标频区。

结构中心大致范围：
| Mode | Body Hz | Cavity Hz | Upper body Hz |
|---|---:|---:|---:|
| Ignition |148–156|272–285|430–447|
| Evolution |132–140|238–251|382–399|
| Lightspeed |158–166|286–299|454–471|

新质量包络：快速负载55 ms；质量层120 ms attack / 550 ms release；频率参数650 ms慢变；生命周期额外返回40 ms attack / 90 ms release。关闭SC仍允许平滑短尾，不新增关机后持续自振。

## 控制 / 状态 / A-B

DNA Open 与每一种 Soundscape Open 的面板下方都有：
- **Weight Balance**：1本轮修复；0取消本轮贡献，回到138a36d对应声源/链路（同输入/旧参数）。
- **Foundation**：0–1，只管本轮的结构底床，默认 .70。DNA Foundation=0不撤销主阶次衰减；完全A/B请使用Weight Balance。

原 **Reference Restore** 是上一轮的控制，保持你之前的值，本轮A/B不要同时改它。DNA与当前SC模式的Weight Balance各自独立：只想比较DNA先SC关/做DNA Solo；完整回退本轮要将DNA和当前模式的Weight Balance都设0。

新 state：`presets/local/ioniq6n_sound_dna_v4.json` 与 `presets/local/ioniq6n_soundscape_modes_v3.json`。
DNA首次按V3→V2→V1读取；SC按bed V2→原始三模式读取，并重命名对应前缀。已有有效新state优先，缺项补factory。新SC factory覆盖253个已知客户项，包括新增底床控制与BEAP完整默认值；非法数字/数组/模式名回退。只写新state，旧JSON只读。

明确点击Save DNA / Save Soundscape。Save Profile Sound不代替Save DNA。不要先按Factory Reset“试试”；它会保存新factory并覆盖当前新版本的调整。未提交的旧Designer连线不自动迁移，遇到这种情况先由本地Codex核对工作树diff，不能假装JSON等于完整音色快照。

## 本地安装与第一优先测试

优先保留旧目录，关闭Max后建独立worktree；新完整ZIP无须重建。复制原`presets/local/*.json`到测试目录前先备份，不能反向覆盖生产目录。否则听到的是factory，而不是现有认可调音。禁止同时运行两个同名控制总线的工程。

在干净、正确目标分支上可以 `git fetch origin` 后 `git pull --ff-only origin codex/v6-ioniq-dna-accel-detail`。独立A/B可使用 `git worktree add --detach ../VehicleSoundSynth-IoniqWeight <本轮修复SHA>`。

第一优先场景（待本地录制，不是本轮已交付WAV）：
1. 650怠速、1450启动落稳：同preset下应保持前版本；不将高油门起步混为activation。
2. DNA Solo，固定4000/6000/8000 RPM，油门/负载=.2/.7/1：先Balance0/1，确认单线不再统治、重量在SC关闭时也存在。
3. Evolution Soundscape Solo，8000 RPM且engine_running/ignition有效：把Motion与Space设0，再开关Foundation/Weight Balance。新增中低频仍应存在；不会只剩高频湿声。
4. 三模式各跑一次同样的起步→换挡→高速→快/慢收油；完整混合比对，录制未归一化原件和固定增益响度匹配副本（±0.5 dB），不得逐帧自动增益匹配。
5. SC Enable=0、Main SC静音、DNA/SC Solo互切、停止/重启、保存→关闭Max→重开。确认声音与UI同一实例。

先不要调整总线EQ、加更多Noise或动其他车型。若已用EQ大幅挖掉200–300Hz，要记录并在测试副本上取消那个人工补偿，否则可能把新重量也切走。不是要求抹掉全部已认可车内EQ。

旧 `tools/build_runtime_probe.py` 的独立Soundscape测试入口仍指向旧host，不能把旧probe的成功当作本轮验证；本轮验收以真实maxproj的上述新活动路径为准。需要自动录音时由本地Codex显式实例化新host/新DNA，不在未核对路径时复用旧probe。

## 自动验证和边界

`python3 -m unittest discover -s tests -v`；新增 `tests/test_ioniq_weight.py` 检查14项：原资源hash、仅两处活动引用变更、BEAP不变、增益/滤波真实线路、SC干声返回、完整factory/迁移、坏值处理、端口与生成确定性。

`python3 tools/check_ioniq_weight_math.py <仓库外目录>`：NumPy + C++。这是自行定义slide/cycle/history的标量源代理，**不是Cycling '74导出C++，不是Max/BEAP/最终混音录音**。28个稳态案例覆盖44.1/48k、650–10000RPM、.2/1 effort；另做旁路、模式、满Foundation、关闭/关机状态及扫转。检验主线下降、120–600能量、跨转速保持、非有限值与原源等价。

设计依据：源音量相对分配、频域独立性与真实线路；滤波采用公开RBJ恒定峰值bandpass公式（W3C Audio EQ Cookbook），不是用户外置EQ修补。对Gen历史/采样率的运行假设参照Cycling '74文档，最后仍需原生编译验证。

本轮未获得Max可执行运行环境/用户实际preset/新录音，所以不能声称“已经听到200–300峰”“整链无削波”“CPU通过”或“主观问题彻底解决”。交付QA应准确区分Linux运行记录、macOS全测试、数值代理和待完成的听评。

## 后续边界与回滚

下一阶段只允许基于同条件A/B调整本模块有界增益、低中频频率分布和包络；一次只改一个维度。若仍有窄带峰，先分别录Gen/BEAP后/DNA/SC/总线，确认是否为私有filter resonance、局部参数或实车响应，不盲目继续挖总线。

禁止修改其他四款、回滚eShift、强推main、覆盖已有seed/local、用新随机噪声掩盖主阶次问题、把底床叫作真实排气/座舱IR。保留旧版A/B与当前Weight Balance控制。

即时回滚：当前模式SC与DNA的Weight Balance均设0；保存需要分别执行。完整回滚：关闭测试Max，打开保留的138a36d工程和其原state；或者在干净feature分支revert本次commit。不要reset --hard/force-push。
