# VehicleSoundSynth V6 使用说明

适用：2026-09-10 用户认可的五车型版本，分支 `codex/v6-layering-dna-pad-pop`。
运行环境：macOS、Max 8.6.5。工程文件夹保持名为 `VehicleSoundSynth-V6`。
本机位置：`/Users/saintpeter/Downloads/VehicleSoundSynth-V6`。

## 1. 启动与退出

1. 先降低耳机／音箱音量。打开 `VehicleSoundSynth-V6.maxproj`，等待 Project 窗口出现。
2. 在同一个 Max 实例打开 `main.maxpat`，选一个车型。不要同时手动打开多个车型 runtime。
3. Main 切到 **Drive / 驾驶** 页，选择 `Internal Manual`，再选 `Keyboard` 或 `Gamepad`。
4. 点击 `Ignition On`，再点击 `Start`，等待启动落入怠速／ready 状态。
5. 开启 Main **Drive 页的 `Audio On / 音频总开关`**，然后缓慢提高监听音量。它不在发动机参数窗口；Ignition 和 Start 不会代替 Audio On。
6. 驾驶试听。切换车型也通过 Main 操作；重新检查所选车型的 Audio、Ignition、输入模式与 Solo 状态。
7. 结束前松开踏板，按各模块 Save 保存有意调整；关 Audio On，再关点火。保存有意修改的 BEAP patcher，关闭 Designer、车型、Main、Project 窗口，最后退出本次 Max。

从 GitHub 下载时应选择上述功能分支，而非默认 `main`。解压后的文件夹重命名为 `VehicleSoundSynth-V6`；保留 `patchers/`、`code/`、`gen/`、`presets/`、`media/` 的相对位置。
不要覆盖正在使用的工程或它的 `presets/local/`。首次干净下载使用工厂状态，不包含本机个人调音。

## 2. 驾驶操作

| 输入 | 油门 | 刹车 | 注意事项 |
|---|---|---|---|
| Keyboard | W：按下 1，松开 0 | S：0.85，优先于 W | 选 Internal Manual；聚焦驾驶／runtime 窗口，别把焦点留在文本编辑框 |
| Gamepad | LT：连续 0–1 | RT：连续 0–1 | 本项目固定 LT 油门、RT 刹车；与常见游戏相反，可同时输入 |
| Internal Manual 控件 | Throttle 0–1 | Brake 0–1 | 用于定点试听；观察实际反馈值，避免键盘／手柄同时覆盖 |
| Internal Auto | 自动驾驶周期 | 自动 | 不接受手动键盘／手柄驾驶 |
| External | 外部 throttle 消息 | 外部 brake 消息 | 使用对应车型的 `vss.<profile>.input`，完整消息契约见 README |

切换输入设备或退出 Manual 会清零踏板，避免卡住油门。急松油门与缓慢松油门的响应不同；高速松油门不代表车速立即归零。EV，以及关闭 N e-Shift 的 IONIQ6N，仍保留速度耦合。

车型模式在各自窗口调整：EV 有 Relax／Expressive／Sport；V10/V12 有启动风格选项；IONIQ6N 有 Ignition／Evolution／Lightspeed，默认 Evolution，N e-Shift 默认开启。这里的 IONIQ “Ignition”是声音模式名，不是 Main 的点火开关。

## 3. 声部和调音顺序

Main 的 **Mix + EQ** 是总体平衡与主 EQ；**Sound Design** 打开正在发声的 Designer。先固定试听条件、关闭无关 Solo，再一次只调整一层。

| 声部 | 负责什么 | 从哪里调整 |
|---|---|---|
| Sound DNA | 主发动机／电驱声纹、阶次、加速质感 | Sound Design → Open Sound DNA；总音量在 Mix + EQ |
| Soundscape | 独立低中频厚度、腔体与行驶铺底，不接收 DNA 音频 | Enable、Open Designer、Solo；总量在 Mix + EQ |
| Noise（原 Road Air） | 机械、进气、轮胎、风噪 | Noise Open／Solo；必须先提高 Mix + EQ 的 Noise 推子 |
| Cabin Rumble | 从发动机激励得到的车体低频共振 | Mix + EQ 的 Rumble；不是 Soundscape |
| Start | 独立启动／激活 | 对应 Start Designer 与混音推子 |
| Pop/Event | 短促回火／事件 | Pop Open／Audition，Pitch／Tone／Level 与混音推子 |
| Master / EQ | 全部声部总量、频响和最终输出 | Mix + EQ；不要靠拉高总量代替声部平衡 |

推荐顺序：DNA Solo 调核心质感 → 退出 Solo，逐步加入 Soundscape → 按需加入 Noise、Rumble → 检查启动与 Pop → 最后调总 EQ 和输出电平。切勿长时间以高响度测试低频或 Pop。

### Sound DNA

V10/V12 当前使用 DNA V2：≤1200 RPM 保留原怠速输出，1200–3000 RPM 渐入强化行驶层。因此在怠速调 Running 参数可能几乎听不出变化，这不是断线。

- Running Body：行驶时的低中频实体感。
- Running Cavity：腔体与排气共鸣。
- HF Softness：高频柔化，减少尖锐／塑料感。
- Release Mass：松油门后的厚度保留与消退。

先在 2000–5000 RPM、相同负载下比较，再检查加速与收油。Ferrari 使用独立 realism-V2 DNA，IONIQ6N 使用独立电驱 DNA；不要照搬 V10/V12 的旋钮含义或工厂值。参数单位与有效试听场景见 Designer 标签及提示。

### Soundscape

EV/V10/V12 使用 V5 行驶铺底：Body、Cavity 调厚度与腔体；Contour 调轮廓；Load Response 调负载反应；Release Mass 调收油后质量感。RPM 驱动节奏／音高逻辑，油门与负载主要改变层量和滤波，不是简单的音量推子。

Ferrari 使用 V7：保留压力激励、低频腔体和 Direct Body，移出独立机械／空气返回。Direct Body 范围 −60…0 dB，工厂 −9 dB，−60 为关闭。IONIQ6N 使用三套 V2 mode bed，保留原有模式特征，只分离独立噪声返回。

**并非所有低频共振中心都应与 RPM 成比例上升。** Ferrari 当前身体模态漂移很小；若要判断某条固定轰鸣来自哪里，在同一 RPM／油门下依次关闭 Soundscape、降低 Rumble，并分别独听 DNA。不要把固定车体共振直接当成 RPM 断链。

Enable 管 Soundscape，不管 Noise。Pitch Follow／Transpose 影响音高／模态映射，但不等于改变物理点火 cadence。Brightness 与滤波改变频谱；Motion／Space 保留现有实现。本发布没有移除既有 Chorus／Reverb／Cabin FX，不应宣传为“零混响版本”。

### Noise

Noise 推子工厂值为 **−60 dB，精确静音**。先启动发动机，再提高这个推子，随后 Solo 和调组件；只调组件而总推子仍静音，不会有声音。

- Mechanical：随 RPM、负载和运行状态变化；稳态 2000–5000 RPM 比较。
- Intake：进气压力；固定 RPM 比较轻／重负载。
- Tire、Air：随车速变化；原地不出路噪／风噪是预期行为。
- Color：打开噪声滤波，不改变发动机音高；可从 0.2–0.5 起试。

Noise 是独立合成层，不从 DNA 或 Soundscape 抽取音频，也不支持未点火的独立试听。内部 BEAP 滤波上限建议 1800–4500 Hz、克制共振，先小幅调整。

### Pop / Event

五车型共享一个合法 CC0、240 ms 单次采样，最多两个按需唤醒的播放器，不是连续发动机采样堆叠。Ferrari 使用 Pop V3，其余使用按车型调音的 V4。

- Pitch：−6…+3 半音，从下一次触发起作用。
- Tone：1200…8000 Hz，越低越暗。
- Level：−24…0 dB，模块内部量；总声部量另看 Mixer。

用 Main 的 Pop Open／Audition 或车型窗口的 Test Pop 试听；不要因为没有自然回火就改变发动机条件。EV 仅手动预览，不产生自动燃烧回火；IONIQ 保留模式／N e-Shift 门控；ICE 保留既有松油门爆发条件。采样丢失会静音并报文件错误，没有自动合成 fallback。

## 4. 保存、重载和恢复

- 调音后按**对应 Designer 的 Save**。Main 的 **Save Profile Sound 只合并保存 Mixer、Soundscape、EQ**，不能代替 DNA、Noise、Pop、Start 的专用 Save。
- Reload 读取该模块已保存状态，不是工厂重置。
- Factory Reset 恢复该模块工厂状态；使用前先备份自己的 preset。Soundscape Reset 有约 0.86 秒延迟，至少等待 1 秒再修改／Save／Reload。
- Max 的 Cmd+S 保存 patcher 结构；它不等于所有模块的 preset Save。改内部 BEAP 图时两个层面都要处理。
- 个人状态在 `presets/local/`，按车型和版本隔离，不进入 Git。旧版本状态保留供回退，新版只迁移兼容参数；Mixer 迁移会把 Noise 设为关闭。
- 备份个人声音时，在保存并退出 Max 后复制整个 `presets/local/` 和有意编辑过的 seed-once BEAP 文件到本地备份位置。不要把个人录音／preset 添加到 GitHub。

常见命名：V10/V12 DNA 由 `code/dna_v2_state_path.js` 解析；EV/V10/V12 Soundscape 为 `<profile>_soundscape_v5.json`，Ferrari 为 `ferrari_soundscape_v7.json`，IONIQ 为 `ioniq6n_soundscape_modes_v2.json`；Noise 为 `<profile>_noise_v1.json`；Ferrari Pop 为 `ferrari_pop_v3.json`，其他为 `<profile>_pop_v4.json`。具体以当前 Designer 存储名为准，不手工改 JSON 前缀。

## 5. 无声／旋钮似乎无效时

依次检查：工程名与路径 → Main 选中车型 → Drive 页 Audio On → Ignition／Start／运行状态 → 输入模式与焦点 → Mixer／Master → Solo／Enable → 参数的有效 RPM、负载或车速条件。

不要用反复重开多个 runtime 排错。若 Max 报 missing object、Gen 编译或 patchcord 错误，先静音，记录错误与打开的工程路径。不要在已打开的同名工程上重新生成文件。

本版本已获用户听感认可；完整自动化原生 Max 五车型矩阵仍有历史未完成项，详见 [发布交接](V6_RELEASE_HANDOFF.md)。本次发布没有启动或退出用户自己的 Max，也没有改动当前音色。
