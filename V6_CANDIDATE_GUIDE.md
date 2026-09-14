# V6 Control / DNA V3 候选版使用与交接

这是独立候选版，不是已验收 V6 的覆盖更新。

- 候选目录：`Downloads/VehicleSoundSynth-V6-Candidate/VehicleSoundSynth-V6`。
- 分支：`codex/v6-control-dna-v3`，基点 `cff9d08`；未合并 main。
- 现用版本仍在 `Downloads/VehicleSoundSynth-V6`，保持原音色和私人状态。
- 验证进度与未完成门禁：[候选记录](.agentlab/V6_CONTROL_DNA_V3.md)。
- 本轮没有改 Soundscape、Start、Pop、空间 FX、EQ 或压缩算法，没有增加连续音频采样。

## 启动与试音

1. 保存并退出正在使用的 Max 工程；不要同时打开现用版和候选版，避免同名资源缓存。
2. 打开本目录的 `VehicleSoundSynth-V6.maxproj`，再打开 `main.maxpat`。
3. 在 Main 选择一款车型并打开。只保留一个车型 runtime。
4. 在 Drive 页打开 Audio，打开 Ignition，再启动；先保持较低监听音量。
5. 到 Sound Design 页选 Load 或 High RPM 试听场景；这些场景只冻结驾驶输入，不冻结调音控制。
6. 打开 Sound DNA，先单独听 DNA，再逐一加入 Soundscape、Noise。Noise 默认 −60 dB 是精确关闭；Solo 不会自动抬高它。
7. 退出前分别保存有意修改的 Designer/preset 和 patcher，关闭所有测试窗口并退出 Max。

其余 Main 操作仍见 [V6 原使用说明](V6_USER_GUIDE.md)。该说明里的 V2 DNA 版本描述对本候选的 Ferrari/V10/V12 已由下文替代。

## 这次实际改变了什么

| 车型 | 候选 DNA | 保持不变的部分 |
|---|---|---|
| Ferrari | 一个共享燃烧时钟，分出确定性 Core/Body/Character/Upper 与独立随机 Noise V2 | 原 Soundscape V7、Start、Pop V3、驾驶模型 |
| V10 | 奇偶阶混合与缸组特征，独立随 RPM 移动的低中频实体 | ≤1200 RPM 原输出，旧文件、SC、事件、驾驶 |
| V12 | 更平顺的十二阶叠加、宽共振区与较长收油实体尾部 | 同上；不是复制 V10 参数 |
| EV | 音源不变 | DNA、SC、事件、驾驶模型 |
| IONIQ6N | 同 RTPC 下音源不变 | 只修 eShift 模型及纯声音模式的控制路径 |

IONIQ eShift On 的虚拟红线为 8000，满油门升挡目标约 7600；Off 保持原 9950 映射。
重复 On/Off 不重置挡位或触发额外事件。真实切换选择合法近似挡位并用 300 ms 平滑过渡。
其他四款驾驶轨迹回归保持一致。

Ferrari 的 Noise 接在 DNA 输出增益之前：调 Main DNA 不会顺带改变 Noise。Soundscape 仍是原独立铺底，没有被移入 DNA。
V10/V12 的 V3 声纹在 1200–3000 RPM 渐入；不要在怠速下判断行驶宏是否有效。

## DNA V3 调参顺序

先用 Audition 单听一个组，再调 BEAP 四路 Mixer 比例，然后调宏，最后微调该组滤波器。
Audition 0 恢复正常组合；1/2/3/4 分别为 Core/Body/Character/Upper，不保存独听状态。
V10/V12 的组独听会排除旧怠速，检查原怠速时必须回到 0。

| 控件（0…1） | 实际含义 / 推荐听法 |
|---|---|
| Aggression | 改变谐波配比和局部驱动；固定 RPM、高负载比较，不是总音量旋钮 |
| Body Weight | 由更深的基频重心向低中频二、三阶配比移动；整体 Body Level 另由 BEAP Mixer 控制 |
| Body Pressure | 独立调燃烧压力对 Body 的激励份额，不改变 Body 自身频率公式 |
| Character | 改变腔体/缸组特征深度；Ferrari 另含浅双路相位调制 |
| Softness | 控制 Upper 高频衰减；不影响 Main EQ |
| Release Mass | 主体与边缘采用不同释放时间；比较高负载突然收油，不用稳态 RMS 判定 |
| Width | 只扩展 V3 的 120 Hz 以上 Side；0 接近单声道，旧 ICE 怠速立体声保持原状 |
| Load Response | 油门/负载对密度和频谱开启的深度；不会直接改主点火阶次 |

Body 自身基频分别为 Ferrari `48 + 0.018 × RPM`、V10 `60 + 0.020 × RPM`、V12 `42 + 0.014 × RPM` Hz，另有受控压力激励和阶次成分，不是固定低音。

BEAP Mixer 1…4 对应上述四组，实际范围 −72…0 dB，建议从 −30…0 内调。
工厂 Core/Body/Character/Upper 分别为 Ferrari `0/−5/−9/−18`、V10 `0/−6/−10/−19`、V12 `0/−5/−9/−21` dB。
每组有独立 BEAP MMF；Freq、FreqMode、Offset、CV、Res、Mute 等都参与完整工厂状态恢复。
不要将 BEAP 的百分比 Resonance 控件误读为 Q 值，也不要一开始就拉高共振。

Legacy 控件保留旧语义，仅影响 3000 RPM 以下旧输出的部分。
唯一例外是标为 **Shared clock (all RPM)** 的 `cycle_irregularity`：它控制继承的主时钟，在全转速都有效，迁移旧设置也会保留这一行为。

## 保存与回退

| 操作 / 模块 | 保存范围 |
|---|---|
| Main Save Profile Sound | Mixer + Soundscape + EQ；不包含以下独立 Designer，也不包含压缩器 |
| Ferrari/V10/V12 DNA Save | `presets/local/<profile>_sound_dna_v3.json` |
| Ferrari Noise Save | `presets/local/ferrari_noise_v2.json`，不保存或开启 Main Noise 总推子 |
| 其他 Noise / SC / Start / Pop | 保持已有版本空间与各自 Save 操作 |
| Compressor / 试听场景 / Solo | 不新增持久化；重开采用既有默认/临时状态 |

V3 只迁移旧 V2 中意义未变的 ICE 旧路参数，不把旧 running 宏硬灌入新宏；Ferrari 不迁移旧混合噪声语义。
新 Noise V2 只迁移兼容的组件/滤波值，不改变 Main 的精确静音状态。Factory Reset 读取跟踪的完整工厂状态并显式保存到新 local 空间。
旧 V1/V2、旧 factory 和旧私人文件不删除、不改写。简单回退就是退出 Max 后重新打开原 Downloads V6 目录。

## 验证解释与发布条件

源码/结构、Max 导出 Gen、完整 Max 分轨、用户听评是四类不同证据。
不能以结构通过替代全部旋钮可听，不能以响度增加替代音色改善。

`code/design_control.js` 是 91 个共享控制契约的权威；`tools/audit_v3_controls.py <工程外目录>`
导出契约及 1520 条可见控件记录（含按车型重复的 Main 控件）。记录实际范围、局部链路与保存空间；没有逐控件原生证据的仍标 `native_unverified`。
登记表不是“1520 个控件已全部听测通过”的声明。

发布前仍须完成完整原生矩阵、真实 CPU before/after、参数 Save/Reload/Reset/重开验证，以及至少两轮同 RTPC、等响度的用户听评。
未通过前不替换现用工程，不推送该候选分支；原已认可版本的云端分支不受影响。
