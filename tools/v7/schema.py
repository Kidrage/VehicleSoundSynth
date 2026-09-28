"""V7 controls: single authority for runtime, UI, factory and manual (units explicit)."""
PROFILES = ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari')
# name, min, max, default, label, explanation, owner
ROWS = [
 ('v7_enable',0,1,1,'V7 处理 / Enable','0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。','all'),
 ('v7_core_db',-12,3,-3,'主阶次 / Core trim (dB)','只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。','source'),
 ('v7_pitch_relief',0,1,.7,'IONIQ 拉转 / Pitch relief','仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。','ioniq-source'),
 ('v7_attack_ms',10,180,65,'负载渐入 / Attack τ (ms)','音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。','source'),
 ('v7_release_ms',80,800,280,'收油延续 / Release τ (ms)','音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。','source'),
 ('v7_lift_range_db',3,12,6,'IONIQ 牵引跨度 / Load span (dB)','仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。','ioniq-source'),
 ('v7_sub_db',-60,0,-18,'深低频 / Sub source (dB)','独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。','bed'),
 ('v7_foundation_db',-60,0,-20,'固定重量 / Foundation (dB)','独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。','bed'),
 ('v7_weight_trim_db',-12,0,-6,'IONIQ 旧底床 / Old weight (dB)','仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。','ioniq-weight'),
 ('v7_body_db',-9,6,0,'主体平衡 / 90–200 Hz (dB)','连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。','balance'),
 ('v7_cavity_db',-12,3,-2,'腔体平衡 / 200–450 Hz (dB)','声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。','balance'),
 ('v7_mechanical_db',-9,6,0,'纹理平衡 / 450–2000 Hz (dB)','连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。','balance'),
 ('v7_brightness_db',-12,6,0,'亮度增益 / >2 kHz (dB)','明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。','balance'),
 ('v7_comp_threshold_db',-36,-6,-18,'总线阈值 / Threshold (dBFS)','V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。','dynamics'),
 ('v7_comp_ratio',1,6,2,'压缩比 / Ratio (:1)','1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。','dynamics'),
 ('v7_comp_attack_ms',2,100,20,'压缩进入 / Attack τ (ms)','V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。','dynamics'),
 ('v7_comp_release_ms',50,800,180,'压缩释放 / Release τ (ms)','V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。','dynamics'),
 ('v7_output_trim_db',-18,0,-3,'V7 余量 / Output trim (dB)','在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。','dynamics'),
]
PARAMS = {r[0]:dict(zip(('min','max','default','label','help','owner'),r[1:])) for r in ROWS}
OVERRIDES = {
 'ev':{'v7_core_db':-2,'v7_sub_db':-22,'v7_foundation_db':-24,'v7_cavity_db':0},
 'v10':{'v7_core_db':-3,'v7_sub_db':-18,'v7_foundation_db':-20},
 'v12':{'v7_core_db':-3,'v7_sub_db':-20,'v7_foundation_db':-21},
 'ioniq6n':{'v7_core_db':-2,'v7_sub_db':-18,'v7_foundation_db':-22,'v7_cavity_db':-2},
 'ferrari':{'v7_core_db':-1.5,'v7_sub_db':-20,'v7_foundation_db':-23,'v7_cavity_db':-1},
}
def defaults(profile):
    assert profile in PROFILES
    return {**{k:v['default'] for k,v in PARAMS.items()}, **OVERRIDES[profile]}
