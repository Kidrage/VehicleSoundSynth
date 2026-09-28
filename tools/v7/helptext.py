"""Legacy control explanations; no normalized macro is presented as a dB guarantee."""
SHAPES={
'aggression':'攻击形状：0最柔和，1此源最强攻击。可能同时改变脉冲/高阶/调制，不是总增益。',
'brightness':'归一化音色形状，不是高架dB。EV会改逆变器阶次位置；ICE旧源在高转区淡出时该钮可能很弱。实际高频增益用 V7 Brightness dB。',
'body':'源内部重量/谐波比例；0最少、1此算法最大。频率可能仍随RPM移动，不能代替固定低频层。',
'body_pressure':'IONIQ随根频移动的Body分量；0减少、1最大。高速不保证超低频，补底床用V7 Sub/Foundation。',
'cavity_structure':'IONIQ腔体相关阶次比例；0最少、1最大。它不是从真实录音分离的排气声。',
'motor_order':'IONIQ主阶次及低阶比例；0仍保留基准项，1增加量最大。尖突主根频优先调V7 Core dB。',
'mechanical_texture':'机械高阶纹理量；0最少、1内部最大。受源电平、负载和下游滤波影响。',
'hf_edge':'高频边缘阶次量；0最少、1内部最大，不保证总线+固定dB。过亮先减此项或V7亮度。',
'load_depth':'IONIQ负载对源驱动增益的深度；0较平、1变化最大。V7运行区牵引/滑行跨度另由Load span控制。',
'release_mass':'收油时的延续/质量感深度；0最少、1最多。需用收油工况听，不是稳态音量钮。',
'ready_bed':'就绪/低RPM底床量；0少、1多。高RPM会退出，不能当作全速域低频。',
'accel_orders':'正加速度细节增量；0关增量、1最大。须同时有油门/负载/加速度，稳态改变可能听不出。',
'weight_balance':'IONIQ旧修复的运行权重；0原修复前比例，1削根频并引入固定中低频结构。V7 Sub是另一路。',
'foundation':'IONIQ旧120–600Hz结构填充量；0关、1最大。不是超低频旋钮，V7 Old Weight可削重复叠加。',
'reference_restore':'旧参考修复混合：0早期源，1修复源。IONIQ高转速压缩另由V7 Pitch relief解除；非整车EQ旁通。',
'sf90_material':'Ferrari SF90材料声形状的版本混合；0前版本、1V5压力/固定结构，非真实性百分比。',
'v3_aggression':'V3运行源的压力开放/攻击形状；0柔和、1更强高阶。不同于旧aggression，非总增益。',
'v3_body':'V3 Body载波谐波分配；0偏基音、1更丰富上方结构。增加不一定单调变响。',
'v3_character':'V3腔体/个性层的频谱与量；0少、1多。下游BEAP滤波会改变最终听感。',
'v3_softness':'V3高阶柔化量；0较硬、1抑制高阶，增加此值通常更暗而不是更亮。',
'v3_release_mass':'V3释放时长/重量深度；0短、1长。V7外层负载包络可叠加，需测收油响应。',
'v3_width':'V3分支侧向量；0该分支单声道，1最大。旧怠速分支与空间总线仍独立。',
'v3_load_response':'V3负载响应深度；0保守、1更随负载变化；不是油门开度或真实CAN。',
'v3_pressure_blend':'把主压力谐波混入Body的比例；0不加、1最多。可能导致阶次重复，应看200–450Hz能量。',
'stereo_width':'源内部宽度；0最窄、1算法最大，并非整个工程完全mono/100%宽度保证。低频主干应居中。',
'saturation':'源局部非线性强度；0最轻、1最大。0不保证完全线性旁通；过大可能加重塑料边缘。',
'cycle_irregularity':'确定性周期/拍频调制深度；0最规整、1更多变化。不是修复低频与动态的替代品。',
'texture':'原源纹理比例；0少、1多。常与RPM和其他层相乘，单独调最大未必主观变化明显。',
'air_detail':'源内部空气高阶量；0少、1多。不是独立Noise stem的开关。',
'combustion_pulse':'燃烧脉冲形状/比例；0基准、1最大增量。仅燃油解释源有效，EV不伪造真实燃烧。',
'intake_detail':'源内部进气感阶次量；0少、1多，不是真实进气干声stem。',
'exhaust_detail':'源内部排气感阶次量；0少、1多，不是真实排气录音。',
'residual_detail':'程序性残余纹理比例；0少、1多，增大前先确认Noise/主源不重复。',
'gear_mesh_level':'EV齿轮相关阶次量；0少、1多，随RPM变化。',
'electrical_detail':'EV逆变器/电气阶次量；0少、1多，与Brightness位置控制不同。',
 'torque_ripple_level':'EV低阶扭矩纹理量；0少、1多，频率仍随主根频变化。',
}
DB_HELP={
 'powertrain_level_db':'DNA总推子：-60..6 dB；V7 -60目标静音，短淡出后归零。包含V7独立质量层，不包含独立Noise。',
 'start_level_db':'启动声推子：-60..6 dB；只影响启动/就绪声，不修复运行声。',
 'transient_level_db':'事件推子：-60..6 dB；换挡/Pop等独立事件，连续DNA不受此推子控制。',
 'soundscape_level_db':'Soundscape推子：-60..6 dB；只调景观层，不调DNA或Noise。SC关闭时此值不发声。',
 'road_level_db':'Noise总推子：-60..6 dB；-60静音。它与Soundscape Enable无关。',
 'rumble_level_db':'原Cabin Rumble推子：-60..6 dB；由DNA激励，可能与低频结构重复。V7新Sub不再额外激励它。',
 'master_trim_db':'Main Master余量：-24..0 dB；最终总体降低，不增加上限；不能替代物理扬声器保护。',
 'throttle_loudness_depth':'0..8 dB，是旧源油门增益的最大增量，不是0..1比例。稳态满油门约按此深度增强，其他负载项仍可叠加。',
 'noise_mechanical_db':'Noise机械分支：-60..0 dB，-60关闭；需Noise总推子打开和发动机运行。',
 'noise_intake_db':'Noise进气分支：-60..0 dB，-60关闭；需Noise总推子打开。',
 'noise_tire_db':'轮胎噪声：-60..0 dB，依车速而动；静止时无声是预期行为。',
 'noise_air_db':'风噪：-60..0 dB，依车速而动；不是DNA高频增益。',
 'noise_combustion_db':'Ferrari独立压力残余Noise：-60..0 dB；-60关闭。不是主DNA音量。',
 'soundscape_transpose':'Soundscape音高偏移：-12..12半音；0不移调。大幅上移会损失低频底座，V7质量层不跟随。',
 'soundscape_pitch_follow':'0..1：Soundscape跟随RPM的深度，0最固定、1最跟随；不改变车辆RPM/档位。',
 'soundscape_brightness':'0..1：景观层滤波/音色宏，0暗、1亮；只对启用的SC层有效，不是总线高架dB。',
 'soundscape_space':'0..1：空间/湿声深度；0最干、1最湿，受各车型设计约束。',
 'soundscape_motion':'0..1：景观层动态/运动深度；需动态工况验证。',
 'soundscape_enable':'0关闭Soundscape；1启用。不会关闭DNA/Noise或替代Audio开关。',
 'eq_low':'低架：30..400Hz、-12..12dB；增益0不改变。频率是架型转折，不是完整频段边界。',
 'eq_lowmid':'中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。',
 'eq_highmid':'中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。',
 'eq_high':'高架：4000..16000Hz，-12..12dB；保留安全余量，过亮先减而非补低音抬总量。',
 'eq_bypass':'0应用EQ，1绕过EQ；不绕过限幅/主推子。',
}

def explain(name,box=None):
 original=name
 name=name.removeprefix('dna_').removeprefix('legacy_').removeprefix('mix_')
 if name in DB_HELP:return DB_HELP[name]
 if name in SHAPES:
  prefix='仅旧源分支；高转区V3淡入后效果可能很弱。' if original.startswith('legacy_') else ''
  return prefix+'0..1归一化形状。'+SHAPES[name]
 if name.startswith('idle_'):return '0..1：该怠速子层的比例；0最少、1最大。退出怠速后权重降低，不能用于补高速低频。'
 if name.endswith('_solo'):return '0普通混合，1独听此声层；不写入定稿预设，避免下次开机误静音其他层。'
 if name.endswith(('_open','_save','_reload','_reset','_audition','_test')):return '当前发动机模块动作：打开/保存/载入/恢复或预听；预听仍需要音频开启。'
 return None
