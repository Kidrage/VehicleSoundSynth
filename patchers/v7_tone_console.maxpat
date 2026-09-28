{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 8,
      "minor": 6,
      "revision": 5,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      50.0,
      50.0,
      1120,
      610
    ],
    "openinpresentation": 1,
    "default_fontname": "Arial",
    "default_fontsize": 12.0,
    "boxes": [
      {
        "box": {
          "id": "in",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            0,
            700,
            25,
            25
          ]
        }
      },
      {
        "box": {
          "id": "out",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1090,
            700,
            25,
            25
          ]
        }
      },
      {
        "box": {
          "id": "title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            10,
            1080,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            10,
            1080,
            26
          ],
          "fontsize": 18,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "V7 TONE | 音色身份与频段平衡"
        }
      },
      {
        "box": {
          "id": "description",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            38,
            1080,
            30
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            38,
            1080,
            30
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "先减过强主阶次与重复腔体，再补低频。新参数按发动机保存；这些是宽频段工程起点，不是实车自动校准。"
        }
      },
      {
        "box": {
          "id": "readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 15,
          "patching_rect": [
            20.0,
            896.0,
            200.0,
            22.0
          ],
          "text": "route v7_enable v7_core_db v7_pitch_relief v7_weight_trim_db v7_sub_db v7_foundation_db v7_body_db v7_cavity_db v7_mechanical_db v7_brightness_db v7_status v7_gr_db v7_clip_samples profile"
        }
      },
      {
        "box": {
          "id": "panel-v7_enable",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            76,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            76,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_enable",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            80,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            80,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "V7 处理 / Enable"
        }
      },
      {
        "box": {
          "id": "v7_enable",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            440,
            82,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            440,
            82,
            100,
            23
          ],
          "minimum": 0,
          "maximum": 1,
          "format": 6,
          "varname": "v7_enable",
          "hint": "0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。",
          "annotation": "0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_enable",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            992.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_enable"
        }
      },
      {
        "box": {
          "id": "set-v7_enable",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1016.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_enable",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            107,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            107,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "0…1  |  0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。"
        }
      },
      {
        "box": {
          "id": "panel-v7_core_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            566,
            76,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            566,
            76,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_core_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            80,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            80,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "主阶次 / Core trim (dB)"
        }
      },
      {
        "box": {
          "id": "v7_core_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            990,
            82,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            82,
            100,
            23
          ],
          "minimum": -12,
          "maximum": 3,
          "format": 6,
          "varname": "v7_core_db",
          "hint": "只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。",
          "annotation": "只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_core_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1136.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_core_db"
        }
      },
      {
        "box": {
          "id": "set-v7_core_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1160.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_core_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            107,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            107,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-12…3  |  只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。"
        }
      },
      {
        "box": {
          "id": "panel-v7_pitch_relief",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            163,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            163,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_pitch_relief",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            167,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            167,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "IONIQ 拉转 / Pitch relief"
        }
      },
      {
        "box": {
          "id": "v7_pitch_relief",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            440,
            169,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            440,
            169,
            100,
            23
          ],
          "minimum": 0,
          "maximum": 1,
          "format": 6,
          "varname": "v7_pitch_relief",
          "hint": "仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。",
          "annotation": "仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_pitch_relief",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1280.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_pitch_relief"
        }
      },
      {
        "box": {
          "id": "set-v7_pitch_relief",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1304.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_pitch_relief",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            194,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            194,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "0…1  |  仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。"
        }
      },
      {
        "box": {
          "id": "only-v7_pitch_relief",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            20.0,
            1352.0,
            200.0,
            22.0
          ],
          "text": "sel ioniq6n"
        }
      },
      {
        "box": {
          "id": "active-v7_pitch_relief-0",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1376.0,
            200.0,
            22.0
          ],
          "text": "ignoreclick 0"
        }
      },
      {
        "box": {
          "id": "active-v7_pitch_relief-1",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1400.0,
            200.0,
            22.0
          ],
          "text": "ignoreclick 1"
        }
      },
      {
        "box": {
          "id": "panel-v7_weight_trim_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            566,
            163,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            566,
            163,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_weight_trim_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            167,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            167,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "IONIQ 旧底床 / Old weight (dB)"
        }
      },
      {
        "box": {
          "id": "v7_weight_trim_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            990,
            169,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            169,
            100,
            23
          ],
          "minimum": -12,
          "maximum": 0,
          "format": 6,
          "varname": "v7_weight_trim_db",
          "hint": "仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。",
          "annotation": "仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_weight_trim_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1496.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_weight_trim_db"
        }
      },
      {
        "box": {
          "id": "set-v7_weight_trim_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1520.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_weight_trim_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            194,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            194,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-12…0  |  仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。"
        }
      },
      {
        "box": {
          "id": "only-v7_weight_trim_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            20.0,
            1568.0,
            200.0,
            22.0
          ],
          "text": "sel ioniq6n"
        }
      },
      {
        "box": {
          "id": "active-v7_weight_trim_db-0",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1592.0,
            200.0,
            22.0
          ],
          "text": "ignoreclick 0"
        }
      },
      {
        "box": {
          "id": "active-v7_weight_trim_db-1",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1616.0,
            200.0,
            22.0
          ],
          "text": "ignoreclick 1"
        }
      },
      {
        "box": {
          "id": "panel-v7_sub_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            250,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            250,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_sub_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            254,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            254,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "深低频 / Sub source (dB)"
        }
      },
      {
        "box": {
          "id": "v7_sub_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            440,
            256,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            440,
            256,
            100,
            23
          ],
          "minimum": -60,
          "maximum": 0,
          "format": 6,
          "varname": "v7_sub_db",
          "hint": "独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。",
          "annotation": "独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_sub_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1712.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_sub_db"
        }
      },
      {
        "box": {
          "id": "set-v7_sub_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1736.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_sub_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            281,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            281,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-60…0  |  独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。"
        }
      },
      {
        "box": {
          "id": "panel-v7_foundation_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            566,
            250,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            566,
            250,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_foundation_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            254,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            254,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "固定重量 / Foundation (dB)"
        }
      },
      {
        "box": {
          "id": "v7_foundation_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            990,
            256,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            256,
            100,
            23
          ],
          "minimum": -60,
          "maximum": 0,
          "format": 6,
          "varname": "v7_foundation_db",
          "hint": "独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。",
          "annotation": "独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_foundation_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1856.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_foundation_db"
        }
      },
      {
        "box": {
          "id": "set-v7_foundation_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1880.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_foundation_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            281,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            281,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-60…0  |  独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。"
        }
      },
      {
        "box": {
          "id": "panel-v7_body_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            337,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            337,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_body_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            341,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            341,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "主体平衡 / 90–200 Hz (dB)"
        }
      },
      {
        "box": {
          "id": "v7_body_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            440,
            343,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            440,
            343,
            100,
            23
          ],
          "minimum": -9,
          "maximum": 6,
          "format": 6,
          "varname": "v7_body_db",
          "hint": "连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。",
          "annotation": "连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_body_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2000.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_body_db"
        }
      },
      {
        "box": {
          "id": "set-v7_body_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2024.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_body_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            368,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            368,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-9…6  |  连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。"
        }
      },
      {
        "box": {
          "id": "panel-v7_cavity_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            566,
            337,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            566,
            337,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_cavity_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            341,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            341,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "腔体平衡 / 200–450 Hz (dB)"
        }
      },
      {
        "box": {
          "id": "v7_cavity_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            990,
            343,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            343,
            100,
            23
          ],
          "minimum": -12,
          "maximum": 3,
          "format": 6,
          "varname": "v7_cavity_db",
          "hint": "声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。",
          "annotation": "声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_cavity_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2144.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_cavity_db"
        }
      },
      {
        "box": {
          "id": "set-v7_cavity_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2168.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_cavity_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            368,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            368,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-12…3  |  声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。"
        }
      },
      {
        "box": {
          "id": "panel-v7_mechanical_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            424,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            424,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_mechanical_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            428,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            428,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "纹理平衡 / 450–2000 Hz (dB)"
        }
      },
      {
        "box": {
          "id": "v7_mechanical_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            440,
            430,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            440,
            430,
            100,
            23
          ],
          "minimum": -9,
          "maximum": 6,
          "format": 6,
          "varname": "v7_mechanical_db",
          "hint": "连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。",
          "annotation": "连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_mechanical_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2288.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_mechanical_db"
        }
      },
      {
        "box": {
          "id": "set-v7_mechanical_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2312.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_mechanical_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            26,
            455,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            26,
            455,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-9…6  |  连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。"
        }
      },
      {
        "box": {
          "id": "panel-v7_brightness_db",
          "maxclass": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            566,
            424,
            536,
            81
          ],
          "presentation": 1,
          "presentation_rect": [
            566,
            424,
            536,
            81
          ],
          "bgcolor": [
            0.11,
            0.14,
            0.19,
            1.0
          ],
          "rounded": 8
        }
      },
      {
        "box": {
          "id": "label-v7_brightness_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            428,
            403,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            428,
            403,
            23
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "亮度增益 / >2 kHz (dB)"
        }
      },
      {
        "box": {
          "id": "v7_brightness_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            990,
            430,
            100,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            430,
            100,
            23
          ],
          "minimum": -12,
          "maximum": 6,
          "format": 6,
          "varname": "v7_brightness_db",
          "hint": "明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。",
          "annotation": "明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。",
          "bgcolor": [
            0.18,
            0.23,
            0.31,
            1.0
          ],
          "textcolor": [
            0.9,
            0.96,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "tag-v7_brightness_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2432.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_brightness_db"
        }
      },
      {
        "box": {
          "id": "set-v7_brightness_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2456.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_brightness_db",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            576,
            455,
            514,
            44
          ],
          "presentation": 1,
          "presentation_rect": [
            576,
            455,
            514,
            44
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "-12…6  |  明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。"
        }
      },
      {
        "box": {
          "id": "button0",
          "maxclass": "textbutton",
          "numinlets": 1,
          "numoutlets": 3,
          "patching_rect": [
            16,
            523,
            222,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            523,
            222,
            28
          ],
          "hint": "作用于当前发动机的V7参数与DNA/SC/Noise/Start/Pop/EQ/Mix；不会存储音频开关/油门/solo。",
          "text": "保存当前发动机 / Save"
        }
      },
      {
        "box": {
          "id": "action0",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2528.0,
            200.0,
            22.0
          ],
          "text": "save_profile_sound"
        }
      },
      {
        "box": {
          "id": "button1",
          "maxclass": "textbutton",
          "numinlets": 1,
          "numoutlets": 3,
          "patching_rect": [
            251,
            523,
            222,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            251,
            523,
            222,
            28
          ],
          "hint": "作用于当前发动机的V7参数与DNA/SC/Noise/Start/Pop/EQ/Mix；不会存储音频开关/油门/solo。",
          "text": "重载 / Reload"
        }
      },
      {
        "box": {
          "id": "action1",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2576.0,
            200.0,
            22.0
          ],
          "text": "reload_profile_sound"
        }
      },
      {
        "box": {
          "id": "button2",
          "maxclass": "textbutton",
          "numinlets": 1,
          "numoutlets": 3,
          "patching_rect": [
            486,
            523,
            222,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            486,
            523,
            222,
            28
          ],
          "hint": "作用于当前发动机的V7参数与DNA/SC/Noise/Start/Pop/EQ/Mix；不会存储音频开关/油门/solo。",
          "text": "恢复出厂 / Factory"
        }
      },
      {
        "box": {
          "id": "action2",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2624.0,
            200.0,
            22.0
          ],
          "text": "reset_profile_sound"
        }
      },
      {
        "box": {
          "id": "status",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            560,
            1080,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            560,
            1080,
            28
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "等待发动机状态 / Select one engine; audio starts OFF"
        }
      },
      {
        "box": {
          "id": "status-set",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2672.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "v7_gr_db-label",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            733,
            514,
            232,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            733,
            514,
            232,
            23
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "RMS GR (dB)"
        }
      },
      {
        "box": {
          "id": "v7_gr_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            970,
            514,
            110,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            970,
            514,
            110,
            23
          ],
          "ignoreclick": 1,
          "format": 6
        }
      },
      {
        "box": {
          "id": "v7_gr_db-set",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2744.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "v7_clip_samples-label",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            733,
            541,
            232,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            733,
            541,
            232,
            23
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "Emergency clip samples"
        }
      },
      {
        "box": {
          "id": "v7_clip_samples",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            970,
            541,
            110,
            23
          ],
          "presentation": 1,
          "presentation_rect": [
            970,
            541,
            110,
            23
          ],
          "ignoreclick": 1,
          "format": 6
        }
      },
      {
        "box": {
          "id": "v7_clip_samples-set",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2816.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "in",
            0
          ],
          "destination": [
            "readback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_enable",
            0
          ],
          "destination": [
            "tag-v7_enable",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_enable",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            0
          ],
          "destination": [
            "set-v7_enable",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_enable",
            0
          ],
          "destination": [
            "v7_enable",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_core_db",
            0
          ],
          "destination": [
            "tag-v7_core_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_core_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            1
          ],
          "destination": [
            "set-v7_core_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_core_db",
            0
          ],
          "destination": [
            "v7_core_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_pitch_relief",
            0
          ],
          "destination": [
            "tag-v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_pitch_relief",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            2
          ],
          "destination": [
            "set-v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_pitch_relief",
            0
          ],
          "destination": [
            "v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            13
          ],
          "destination": [
            "only-v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_pitch_relief",
            0
          ],
          "destination": [
            "active-v7_pitch_relief-0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_pitch_relief-0",
            0
          ],
          "destination": [
            "v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_pitch_relief",
            1
          ],
          "destination": [
            "active-v7_pitch_relief-1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_pitch_relief-1",
            0
          ],
          "destination": [
            "v7_pitch_relief",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_weight_trim_db",
            0
          ],
          "destination": [
            "tag-v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_weight_trim_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            3
          ],
          "destination": [
            "set-v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_weight_trim_db",
            0
          ],
          "destination": [
            "v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            13
          ],
          "destination": [
            "only-v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_weight_trim_db",
            0
          ],
          "destination": [
            "active-v7_weight_trim_db-0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_weight_trim_db-0",
            0
          ],
          "destination": [
            "v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_weight_trim_db",
            1
          ],
          "destination": [
            "active-v7_weight_trim_db-1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_weight_trim_db-1",
            0
          ],
          "destination": [
            "v7_weight_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_sub_db",
            0
          ],
          "destination": [
            "tag-v7_sub_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_sub_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            4
          ],
          "destination": [
            "set-v7_sub_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_sub_db",
            0
          ],
          "destination": [
            "v7_sub_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_foundation_db",
            0
          ],
          "destination": [
            "tag-v7_foundation_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_foundation_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            5
          ],
          "destination": [
            "set-v7_foundation_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_foundation_db",
            0
          ],
          "destination": [
            "v7_foundation_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_body_db",
            0
          ],
          "destination": [
            "tag-v7_body_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_body_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            6
          ],
          "destination": [
            "set-v7_body_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_body_db",
            0
          ],
          "destination": [
            "v7_body_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_cavity_db",
            0
          ],
          "destination": [
            "tag-v7_cavity_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_cavity_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            7
          ],
          "destination": [
            "set-v7_cavity_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_cavity_db",
            0
          ],
          "destination": [
            "v7_cavity_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_mechanical_db",
            0
          ],
          "destination": [
            "tag-v7_mechanical_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_mechanical_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            8
          ],
          "destination": [
            "set-v7_mechanical_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_mechanical_db",
            0
          ],
          "destination": [
            "v7_mechanical_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_brightness_db",
            0
          ],
          "destination": [
            "tag-v7_brightness_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_brightness_db",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            9
          ],
          "destination": [
            "set-v7_brightness_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_brightness_db",
            0
          ],
          "destination": [
            "v7_brightness_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "button0",
            0
          ],
          "destination": [
            "action0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "action0",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "button1",
            0
          ],
          "destination": [
            "action1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "action1",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "button2",
            0
          ],
          "destination": [
            "action2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "action2",
            0
          ],
          "destination": [
            "out",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            10
          ],
          "destination": [
            "status-set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "status-set",
            0
          ],
          "destination": [
            "status",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            11
          ],
          "destination": [
            "v7_gr_db-set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_gr_db-set",
            0
          ],
          "destination": [
            "v7_gr_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "readback",
            12
          ],
          "destination": [
            "v7_clip_samples-set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_clip_samples-set",
            0
          ],
          "destination": [
            "v7_clip_samples",
            0
          ]
        }
      }
    ],
    "bgcolor": [
      0.065,
      0.085,
      0.12,
      1.0
    ]
  }
}
