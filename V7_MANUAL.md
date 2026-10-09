# EV-Engine-V7 唯一使用说明书

版本：V7 R2 实现候选，2026-10-09。仓库 `Kidrage/VehicleSoundSynth`，分支 `EV-Engine-V7`。
本轮更新起点：`e979b0cf261004cc60cd70de1cb5dbd747812092`（已有V7，不重建、不覆盖）。V6声音基线：`fed2b78ecfabc84d673207b3a5f714b89f76720f`；包括 Ioniq `739c9d9` 与 Ferrari SF90 V5。
本说明书是此分支唯一操作/调音说明。旧说明书已从当前工作树清理，可从 Git 历史查阅。

**状态边界：代码、JSON图连接、源公式数值、控制模型和模拟文件读写已测试；不是 Max 原生/BEAP 编译、扬声器保护或实车听评合格证。没有把用户文字反馈伪造成车内录音测量。**

## 1. 打开与安全起步

打开 `EV-Engine-V7.maxproj`，再打开 `main.maxpat`。点击五款发动机之一。只开一个引擎；切换引擎会走原有关闭/保存路径。不要同时开旧版与V7实例。

主界面仍不承载DSP。实际入口是 `EV-Engine-V7-{EV,V10,V12,IONIQ6N,Ferrari}.maxpat`；实际声音来自 `patchers/v7_profile_runtime_host_<profile>.maxpat`。目标环境 Max 8.6.5，原有 BEAP 依赖不变。启动 Audio 默认 OFF，先低监听音量，确认 Max Console 没有红色错误、缺失对象、Gen/项目分类错误，再按 Drive 页进行 Ignition / Start / Audio 操作。

没有开启发动机时，新数值框可能尚未得到状态回读，不代表已加载0值。启动后等待状态显示“factory loaded/profile loaded”，再调节与保存。读取的V7快照不含油门、制动、档位、RPM、Audio或solo，不会自动启动播放。

## 2. 六页主界面

`Drive`：驾驶输入、生命周期、实际控制模型输出。`Mix/EQ`：原有七路混音与四段总线EQ。`Sound Design`：进入当前正在发声的DNA、Soundscape、Noise、Start/Pop设计器。`V7 Tone`：源头主阶次与固定低频、连续声频谱定稿。`V7 Response`：毫秒负载包络、Ioniq收油跨度、总线RMS压缩与额外输出余量。`Mix Lab / 核验`：次阶次A/B、高速质量/高频补偿、四路只读数字频段读数、内部驾驶状态/换挡原因、IONIQ实际发声RPM/root与保存核验。

旧界面控件增加 hint/annotation，悬停可看说明；V7新增控件同时显示可见解释、单位和范围。范围来自 `assets/v7/parameter_contracts.json`，与运行时边界和工厂值共用 `tools/v7/schema.py`。IONIQ专用项在其他发动机中禁用，不装作通用参数。

## 3. V7参数：范围不是随便放大

0–1 适合表示形状、比例、混合和宏映射；它并不表示0..1 dB，也不保证到1就更大声。旧brightness的声源、对应混合分支、滤波和高转速交叉淡化都可能限制可闻变化。EV的旧brightness还影响逆变器成分位置；V10/V12高转速时旧分支权重下降，不能靠把参数上限从1改成10修复一个不再主导输出的分支。

因此保留旧brightness的语义与兼容范围，新增实际的 **2kHz高架 `v7_brightness_db`**。它处理连续DNA+Soundscape，范围−12..+6dB，0为不改变该高架；+6dB在高频渐近区约为振幅两倍，而不是声音“真实两倍”。没有该频段内容、相应stem关闭或后级限幅介入时，可闻差异仍会较小。

下列默认列为IONIQ候选值；其他车型见第4节。所有attack/release毫秒表示一阶平滑的时间常数τ；10%到90%约2.2τ，不是固定长方形的0–100%渐变时长。

| 参数 / 界面 | 范围 | IONIQ默认 | 作用与取值含义 |
|---|---:|---:|---|
| `v7_enable` / V7 处理 / Enable | 0…1 | 1 | 0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。 |
| `v7_core_db` / 主阶次 / Core trim (dB) | -12…3 | -2 | 只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。 |
| `v7_pitch_relief` / IONIQ 拉转 / Pitch relief | 0…1 | 0.7 | 仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。 |
| `v7_attack_ms` / 负载渐入 / Attack τ (ms) | 10…180 | 65 | 音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。 |
| `v7_release_ms` / 收油延续 / Release τ (ms) | 80…800 | 280 | 音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。 |
| `v7_lift_range_db` / IONIQ 牵引跨度 / Load span (dB) | 3…12 | 6 | 仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。 |
| `v7_sub_db` / 深低频 / Sub source (dB) | -60…0 | -18 | 独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。 |
| `v7_foundation_db` / 固定重量 / Foundation (dB) | -60…0 | -22 | 独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。 |
| `v7_weight_trim_db` / IONIQ 旧底床 / Old weight (dB) | -12…0 | -6 | 仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。 |
| `v7_body_db` / 主体平衡 / 90–200 Hz (dB) | -9…6 | 0 | 连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。 |
| `v7_cavity_db` / 腔体平衡 / 200–450 Hz (dB) | -12…3 | -2 | 声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。 |
| `v7_mechanical_db` / 纹理平衡 / 450–2000 Hz (dB) | -9…6 | 0 | 连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。 |
| `v7_brightness_db` / 亮度增益 / >2 kHz (dB) | -12…6 | 0 | 明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。 |
| `v7_comp_threshold_db` / 总线阈值 / Threshold (dBFS) | -36…-6 | -18 | V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。 |
| `v7_comp_ratio` / 压缩比 / Ratio (:1) | 1…6 | 2 | 1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。 |
| `v7_comp_attack_ms` / 压缩进入 / Attack τ (ms) | 2…100 | 20 | V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。 |
| `v7_comp_release_ms` / 压缩释放 / Release τ (ms) | 50…800 | 180 | V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。 |
| `v7_output_trim_db` / V7 余量 / Output trim (dB) | -18…0 | -3 | 在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。 |
| `v7_order2_db` / 次阶次 A / Order A (dB) | -12…3 | 0 | 0=原比例；-6约半幅。EV为2f，V10/V12/Ferrari为h2，IONIQ为1.5×root；不是总线EQ。 |
| `v7_order3_db` / 次阶次 B / Order B (dB) | -12…3 | 0 | 0=原比例；-6约半幅。EV为约3f双侧分量，V10/V12/Ferrari为h3，IONIQ为2.25×root。 |
| `v7_speed_weight_db` / 高速重量保持 / Speed mass (dB) | 0…6 | 0 | 只提升独立Sub+Foundation。60km/h以下0；60–140平滑增长；140以上为设定dB。0=不额外补偿。 |
| `v7_speed_edge_db` / 高速高频约束 / Speed edge (dB) | -6…0 | 0 | 连续DNA+SC的2kHz高架附加量。60–140km/h渐进；0=不补偿，-6=高速最多约半幅。 |

频段名称用于操作理解，不是砖墙分频。Body是135Hz/Q0.7宽峰，Cavity是300Hz/Q0.8宽峰，Mechanical是900Hz/Q0.65宽峰，Brightness是2kHz/S1高架。它们会相互重叠。没有把“Body 90–200Hz”宣称为严格独立stem。

`Core`：EV为主低频coherent分量，IONIQ为order1，V10/V12/Ferrari为新压力源领先partial。并非一键约束所有谐波，更不是所有层的音量。原有不同发动机仍保留自己的谐波关系与音色个性。

`Sub`与`Foundation`是新增的固定/慢变质量层；前者约35–85Hz，后者约90–190Hz。两者和Sound DNA共用DNA推子与solo门控，源头高通28Hz。−60dB为零目标，并通过短平滑淡出，不产生硬截断。它们不是另一个独立LFE物理输出；本版仍是立体声，车内Sub分配必须由已确认的bass management完成。

`weight_trim`只压低IONIQ上版新增的重复中低频底床，DNA与Soundscape均包含；不是把IONIQ全部音色挖空。其它四款已存在的Soundscape Body/Cavity仍在各自Designer里调。

`v7_enable=0`回退本轮源公式/驾驶策略，关闭新增质量层并使新频谱EQ/压缩趋于旁通；额外输出trim、限幅和紧急样本保护仍保留。这不是整条V6链路的bit-exact开关。完整旧版A/B请用保留的 `VehicleSoundSynth-*.maxpat` 单独开启，并匹配响度。

## 4. 五款发动机初始混音取向

这些数值是保守候选起点，不是未经实测就发布的车内目标曲线。五款共享工具，不共享一个音色。

| 车型 | Core dB | Sub dB | Foundation dB | Cavity dB |
|---|---:|---:|---:|---:|
| ev | -2 | -22 | -24 | 0 |
| v10 | -3 | -18 | -20 | -2 |
| v12 | -3 | -20 | -21 | -2 |
| ioniq6n | -2 | -18 | -22 | -2 |
| ferrari | -1.5 | -20 | -23 | -1 |

## 5. 发现听感问题，按什么顺序调

**200–400Hz压住其它内容：** 先做DNA/SC分别solo与相加对比。主单音过强先减Core 1–3dB；IONIQ再试 `weight_trim`，默认−6dB，可在−12..0dB内试；其它车型在SC Designer减少重复Body/Cavity。剩下的宽峰再试Cavity减1–3dB。不要先将总音量或压缩makeup抬高，也不要把整条主阶次直接挖掉。

**单个次阶次冒出来：** 先用Core确定是不是主分量，再用Mix Lab的Order A/B分别减3dB比较。EV的A是2f、B是约3f双侧；IONIQ为1.5×root/2.25×root，不是严格整数谐波；V10/V12/Ferrari为h2/h3。作用于源partial、不是总线EQ。高阶谐波仍由DNA Designer调，不能声称这三个旋钮控制了全部声音。

**三档以上低频空了：** 检查DNA推子与solo、Sub实际路由、后级高通/分频。先把独立Sub或Foundation增加1–3dB作匹配响度A/B，而不是将主pitch拉低八度。新增层频率只随负载/RPM缓慢移动几个Hz；不跟随档位pitchCV到中高频。只有高速时才变薄，可先试Speed mass +1..+3dB；0–60km/h不额外提升，60–140km/h渐进到设定值，约0.8s平滑。仅提升独立Sub+Foundation，不增加旧200–400Hz重复底床。它默认0，+6dB是上限而非推荐常开；会消耗约两倍电压幅值的余量。

**高转速塑料/刺耳：** 先检查紧急clip计数和原有饱和/激励；再比较Brightness −2..−4dB、Mechanical −1..−3dB。不能断言“所有塑料都在2–6kHz”。高频不足先检查对应层是否启用，再试Brightness +1..+3dB。只有高速变硬，试Speed edge −1..−3dB；同样在60–140km/h渐进，是2kHz高架的附加量，会与Brightness相加。它不改RPM，也不自动检测塑料感。

**点油门太硬：** 先试负载attack 65–100ms。不会延迟CAN/仪表输入，平滑只作用于合成源的发声负载。R2补齐Ferrari实际SF90路径的sf_effort，它原来绕过了新增负载包络；SF90自有各层包络仍保留，串联后的整体10–90%时间不等于2.2τ。ICE的负负载不再被当成正牵引负载。**收油断层：** IONIQ试lift_range 4–6dB、release 250–400ms。该范围只约束主源的稳态drive项；整体声压还由SC/事件/其它门控决定，不能把它当作已测整体3–6dB。

**混音/输出：** Mix的DNA/SC/Noise是stem增益；Tone的Core是源partial、Sub/Foundation是子层，不能当成同一个增益重复补偿。原Master trim与V7额外Output trim叠加；后者默认−3dB留余量。先解决源头比例，再调动态。没有自动补偿增益，不以无限压缩救频谱。

## 6. 驾驶与换挡改变了什么

IONIQ保留真实控制RPM与发声RPM分离。高转速原来reference修复压缩pitch增长；新增pitch_relief只释放这个高段压缩，不关闭启动/音色reference修复。0保留旧高段映射，1去掉该压缩，默认0.7；2600RPM以下不改这段映射。

虚拟N e-Shift满油门升挡阈值改为7800RPM附近；仍8档、仍根据车速×当前传动比计算RPM，不随档位不断人为抬高整个音区。升降挡有迟滞是正常设计，不要求同一速度原路反向跳挡。

五款模型区分Drive/Coast/Brake。R2加策略迟滞：油门≥0.16进入Drive，降到≤0.08退出；制动≥0.06进入Brake，降到≤0.02退出。这些是内部模拟策略起点，不延迟原始遥测，也不是实车CAN标准。收油/制动不因油门令升挡阈值下降而触发误升挡；降挡验证目标档位RPM不会立即再升挡/超限。阈值策略负载单独平滑，不修改原油门或外部CAN。切断、pitch sweep与接合分阶段；保留旧策略可对照。EV和关闭eShift的IONIQ仍单速。

外部遥测模式保持独立入口，不能把内置模型轨迹当实车CAN或证明外部CAN已跑通。新增state/shift_reason用于判断内部状态。封闭台架/记录数据回放足够验证全档位，不需要道路超速测试。

## 7. 保存当前发动机、重载与跨电脑定稿

主界面 `Save/保存当前发动机` 同时请求：V7数值、DNA、Soundscape、Noise、Start、Pop/Event、EQ与Mix的各自状态所有者保存。八套文件分别保存，不互相抢gain authority。IONIQ的Event使用同一个Pop V4状态，不虚构第二份事件文件。

V7新增数值保存在 `presets/local/v7_<profile>_profile.json`，schema_version=7、schema_revision=2，包含车型和22个参数白名单。旧V7合法18参数快照可迁移，新增4项自动取0；缺失老参数、错误车型、未知字段、越界/非有限数值不会被悄悄当作有效本地定稿。写入后进行物理文件重读校验，上一份有效数值快照保留`.bak`。

主数值读取顺序是：有效本地 → 有效本地备份 → 有效发布绑定 → 本版factory。备份优先于发布绑定；写入及校验绝不偷读绑定文件来掩盖失败。其它原生模块沿用V7隔离的pattrstorage读写；它们不是都具有数值模块的`.bak`机制。

**R2新增“核验保存 / Verify”：** Save发出之前先建立回执收集，再扇出到七个原生模块。Mix Lab核对8个白名单文件、正确pattrstorage名称、有效slot 1、V7参数完整性，并观察原生write通知。缺文件、错误owner、明确失败回执或未收到通知，均显示未完成；不会把“数值文件已保存”升级成“整套音色已保存”。文件契约在 `assets/v7/state_contracts.json`。

这仍不是八文件原子事务，也不保证所有Max版本的write通知形状相同。`8/8`表示本次请求后观察到相应通知且文件有效，不代替关闭重开和音色听评。不要连续快速连点Save；约1.2秒会做一次检查，磁盘慢或通知延迟时手动Verify。Max不发可识别通知时保持“未确认”，由本地Codex按真实事件修适配，禁止伪造成功。重要调整先主动Save、Verify、再关闭，不依赖关闭回调中尚未完成的异步任务。

所有本地文件带`v7_`前缀，不导入/覆盖旧V6状态。Factory按钮仅恢复当前实例候选值，Save后才覆盖本地；不会改仓库定稿绑定。原生模块只有在本地文件不存在时才回退发布绑定，损坏本地原生文件必须单独处理。

**同一电脑：** 调好 → Save → 关闭当前引擎 → 重新打开 →核对数值并回放同一驾驶轨迹。**换电脑/交付：** 保存并关闭Max后，在仓库根目录执行：

```sh
python tools/v7_bind_profile.py ioniq6n
python tools/v7_bind_profile.py ioniq6n --write
```

第一条只检查完整性；第二条才把白名单的八个有效JSON快照写入 `presets/v7_bindings/`，并生成SHA-256清单。任一文件缺失/非有限/错误车型或pattrstorage名称/异常绝对素材路径则拒绝，不发布半套音色。把该目录中对应车型的文件提交到本V7分支，就成为下一次干净下载的声音绑定。其它车型替换为ev/v10/v12/ferrari。它不修改任何旧V6或本地源文件，也不证明已通过人工听评。

仓库目前提供可加载的候选factory，不包含凭空生成的“用户已实车验收定稿”。状态文件清单在 `assets/v7/state_owners.json`，每个文件的owner名称约束在 `assets/v7/state_contracts.json`。发布工具验证文件完整性，不验证本次保存回执或实际声音，因此必须先完成Max重开验证。复制工程时不要把V7 overlay安装在未知的已改工作区上；新下载目录更安全。

### Mix Lab读数的边界

四个读数是DNA+SC连续总线经过V7频谱平衡后的数字信号，未包含全部Start/Pop/Noise、总线动态或车内扬声器响应。中心为60Hz/Q0.7、170Hz/Q0.8、300Hz/Q1.4、3.5kHz/Q0.9，250ms立体声平均能量。它们重叠且带宽不等，不能直接相加，也不能调成同一dBFS当作平衡目标。0.1峰值的中心正弦应显示约−23.01dBFS RMS；静音显示−120下限。精确20–120、120–250等频带以实际WAV离线审计为准。

IONIQ的发声RPM/root直接来自正在发声的Gen运算输出，不在JS重算第二套。它们是只读诊断端口，不路由到音频输出或CAN。其它车型这些读数为空；驾驶状态/原因仅代表内置模拟器，外部遥测模式不要套用。

## 8. 谐波均衡是明确的验收要求，不是全部谐波等响

保留发动机的主阶次身份，但任何单根主频、某个窄带或重复的Body叠加都不应在未说明的情况下占据绝大部分可用输出余量。独立低频层不能只是另一个越来越响的正弦；本版采用多个有限低频分量/轻AM与独立包络，运行压力和中低频结构各自调节。

在Max导出每车的低/中/高RPM×低/中/高负载网格以及点油门、收油、换挡轨迹。分别导出DNA、SC、二者合成及完整输出；固定参数和输出电平，不对每段单独normalize。记录band RMS、峰值、紧急clip、RMS GR以及主线能量比例。可运行：

```sh
python tools/v7_audio_audit.py path/to/max_capture.wav --out qa/ioniq_capture
```

该工具真正读取WAV并验证非空/非静音，输出采样信息、七频带RMS、立体声相关性、峰线三bin占比。占20–6000Hz功率45%以上仅作为**人工复核警告**，不作为一刀切真实性判定；瞬态、身份基频、FFT分辨率都影响这个数。它没有伪造声部来源、RPM、LUFS或true-peak。

建议审核：中高RPM时20–120Hz新质量层不能被pitch移走；200–400Hz不得挤占到其它层消失；只调Core不应摧毁整套声音；开关新层需匹配响度评价而不是更响更好。音色最終必须在耳机/电脑/实际车内三端听评。不能用源公式数值通过代替完整BEAP/车内曲线通过。

## 9. 动态、保护与播放链路边界

V7使用可读单位的双声道联动RMS压缩：10ms能量检测、6dB软拐点、实际ratio/dB/ms，不沿用旧OMX的attack/release对数rate作为毫秒。保留原峰值限幅后，最后样本clip±0.891并计数；正常调音不应长期触发末级clip。RMS GR显示用于诊断持续压缩，不追求恒定高GR。

这不是true-peak limiter，也不提供功放功率、扬声器位移/温度或低音单元硬件保护。尚未验证的OMX峰值限幅器默认行为也不应被当成最终硬件安全条件。车上有Sub不等于程序有独立LFE声道；立体声bass management、后级EQ/DRC/空间处理和音乐通路是否一致必须单独核验。

## 10. 测试、开发与回滚

```sh
python tools/build_v7.py --check
python -m unittest tests.test_v7 tests.test_v7_r2 -v
python tools/validate_v7.py --portable --report qa/portable.json
# 装有原始完整Git历史与Max/BEAP的机器再运行严格全量测试：
python -m unittest discover -s tests -v
```

`--portable`只把明确缺失Max/BEAP、macOS afconvert或不存在历史commit的依赖项列为skip；真实断言和未知错误仍失败。V7源码数值测试使用自写C++标量解释框架，不是Cycling '74原生导出，不测BEAP、音频设备、CPU或实际声学结果。

V7生成器 `tools/build_v7.py` 仅读保留的旧种子，生成新命名资源；重复生成可校验。修改配方后用 `--refresh-generated`，仍会检查之前生成文件的SHA，拒绝覆盖本地用户编辑。不要直接运行旧版build_project对整个V7目录重建，否则会把main还原。

只回退R2：关闭Max，在独立工作树检出 `e979b0cf261004cc60cd70de1cb5dbd747812092`，保留现有本地设置副本。完整回滚V6：关闭Max，在独立工作树检出基线 `fed2b78ecfabc84d673207b3a5f714b89f76720f`，不对有未提交调整的工作区执行reset --hard。用户本地V7预设独立保留；main及其它分支未被合并修改。

工程交接和下一阶段验收见 `V7_CODEX_HANDOFF.md`，不是第二份使用说明。

## 官方实现语义参考

Max Gen slide（样本尺度）：https://docs.cycling74.com/reference/gen_dsp_slide/

Max OMX compressor（对数rate参数）：https://docs.cycling74.com/reference/omx.comp~/

Max JavaScript File API：https://docs.cycling74.com/apiref/js/file/
