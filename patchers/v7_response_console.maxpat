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
          "text": "V7 RESPONSE | 负载包络与总线动态"
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
          "text": "毫秒为时间常数 τ，不是旧OMX rate。负载包络不修改CAN/驾驶遥测；V7=0仅回退源/驾驶策略，安全链仍保留。"
        }
      },
      {
        "box": {
          "id": "readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 13,
          "patching_rect": [
            20.0,
            896.0,
            200.0,
            22.0
          ],
          "text": "route v7_attack_ms v7_release_ms v7_lift_range_db v7_comp_threshold_db v7_comp_ratio v7_comp_attack_ms v7_comp_release_ms v7_output_trim_db v7_status v7_gr_db v7_clip_samples profile"
        }
      },
      {
        "box": {
          "id": "panel-v7_attack_ms",
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
          "id": "label-v7_attack_ms",
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
          "text": "负载渐入 / Attack τ (ms)"
        }
      },
      {
        "box": {
          "id": "v7_attack_ms",
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
          "minimum": 10,
          "maximum": 180,
          "format": 6,
          "varname": "v7_attack_ms",
          "hint": "音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。",
          "annotation": "音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。",
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
          "id": "tag-v7_attack_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            992.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_attack_ms"
        }
      },
      {
        "box": {
          "id": "set-v7_attack_ms",
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
          "id": "help-v7_attack_ms",
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
          "text": "10…180  |  音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。"
        }
      },
      {
        "box": {
          "id": "panel-v7_release_ms",
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
          "id": "label-v7_release_ms",
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
          "text": "收油延续 / Release τ (ms)"
        }
      },
      {
        "box": {
          "id": "v7_release_ms",
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
          "minimum": 80,
          "maximum": 800,
          "format": 6,
          "varname": "v7_release_ms",
          "hint": "音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。",
          "annotation": "音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。",
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
          "id": "tag-v7_release_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1136.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_release_ms"
        }
      },
      {
        "box": {
          "id": "set-v7_release_ms",
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
          "id": "help-v7_release_ms",
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
          "text": "80…800  |  音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。"
        }
      },
      {
        "box": {
          "id": "panel-v7_lift_range_db",
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
          "id": "label-v7_lift_range_db",
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
          "text": "IONIQ 牵引跨度 / Load span (dB)"
        }
      },
      {
        "box": {
          "id": "v7_lift_range_db",
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
          "minimum": 3,
          "maximum": 12,
          "format": 6,
          "varname": "v7_lift_range_db",
          "hint": "仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。",
          "annotation": "仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。",
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
          "id": "tag-v7_lift_range_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1280.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_lift_range_db"
        }
      },
      {
        "box": {
          "id": "set-v7_lift_range_db",
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
          "id": "help-v7_lift_range_db",
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
          "text": "3…12  |  仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。"
        }
      },
      {
        "box": {
          "id": "only-v7_lift_range_db",
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
          "id": "active-v7_lift_range_db-0",
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
          "id": "active-v7_lift_range_db-1",
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
          "id": "panel-v7_comp_threshold_db",
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
          "id": "label-v7_comp_threshold_db",
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
          "text": "总线阈值 / Threshold (dBFS)"
        }
      },
      {
        "box": {
          "id": "v7_comp_threshold_db",
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
          "minimum": -36,
          "maximum": -6,
          "format": 6,
          "varname": "v7_comp_threshold_db",
          "hint": "V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。",
          "annotation": "V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。",
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
          "id": "tag-v7_comp_threshold_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1496.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_comp_threshold_db"
        }
      },
      {
        "box": {
          "id": "set-v7_comp_threshold_db",
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
          "id": "help-v7_comp_threshold_db",
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
          "text": "-36…-6  |  V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。"
        }
      },
      {
        "box": {
          "id": "panel-v7_comp_ratio",
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
          "id": "label-v7_comp_ratio",
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
          "text": "压缩比 / Ratio (:1)"
        }
      },
      {
        "box": {
          "id": "v7_comp_ratio",
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
          "minimum": 1,
          "maximum": 6,
          "format": 6,
          "varname": "v7_comp_ratio",
          "hint": "1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。",
          "annotation": "1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。",
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
          "id": "tag-v7_comp_ratio",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1640.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_comp_ratio"
        }
      },
      {
        "box": {
          "id": "set-v7_comp_ratio",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1664.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_comp_ratio",
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
          "text": "1…6  |  1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。"
        }
      },
      {
        "box": {
          "id": "panel-v7_comp_attack_ms",
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
          "id": "label-v7_comp_attack_ms",
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
          "text": "压缩进入 / Attack τ (ms)"
        }
      },
      {
        "box": {
          "id": "v7_comp_attack_ms",
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
          "minimum": 2,
          "maximum": 100,
          "format": 6,
          "varname": "v7_comp_attack_ms",
          "hint": "V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。",
          "annotation": "V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。",
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
          "id": "tag-v7_comp_attack_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1784.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_comp_attack_ms"
        }
      },
      {
        "box": {
          "id": "set-v7_comp_attack_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1808.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_comp_attack_ms",
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
          "text": "2…100  |  V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。"
        }
      },
      {
        "box": {
          "id": "panel-v7_comp_release_ms",
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
          "id": "label-v7_comp_release_ms",
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
          "text": "压缩释放 / Release τ (ms)"
        }
      },
      {
        "box": {
          "id": "v7_comp_release_ms",
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
          "minimum": 50,
          "maximum": 800,
          "format": 6,
          "varname": "v7_comp_release_ms",
          "hint": "V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。",
          "annotation": "V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。",
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
          "id": "tag-v7_comp_release_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1928.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_comp_release_ms"
        }
      },
      {
        "box": {
          "id": "set-v7_comp_release_ms",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1952.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_comp_release_ms",
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
          "text": "50…800  |  V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。"
        }
      },
      {
        "box": {
          "id": "panel-v7_output_trim_db",
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
          "id": "label-v7_output_trim_db",
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
          "text": "V7 余量 / Output trim (dB)"
        }
      },
      {
        "box": {
          "id": "v7_output_trim_db",
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
          "minimum": -18,
          "maximum": 0,
          "format": 6,
          "varname": "v7_output_trim_db",
          "hint": "在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。",
          "annotation": "在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。",
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
          "id": "tag-v7_output_trim_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2072.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_output_trim_db"
        }
      },
      {
        "box": {
          "id": "set-v7_output_trim_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2096.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_output_trim_db",
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
          "text": "-18…0  |  在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。"
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
            2168.0,
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
            2216.0,
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
            2264.0,
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
            2312.0,
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
            2384.0,
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
            2456.0,
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
            "v7_attack_ms",
            0
          ],
          "destination": [
            "tag-v7_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_attack_ms",
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
            "set-v7_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_attack_ms",
            0
          ],
          "destination": [
            "v7_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_release_ms",
            0
          ],
          "destination": [
            "tag-v7_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_release_ms",
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
            "set-v7_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_release_ms",
            0
          ],
          "destination": [
            "v7_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_lift_range_db",
            0
          ],
          "destination": [
            "tag-v7_lift_range_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_lift_range_db",
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
            "set-v7_lift_range_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_lift_range_db",
            0
          ],
          "destination": [
            "v7_lift_range_db",
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
            "only-v7_lift_range_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_lift_range_db",
            0
          ],
          "destination": [
            "active-v7_lift_range_db-0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_lift_range_db-0",
            0
          ],
          "destination": [
            "v7_lift_range_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "only-v7_lift_range_db",
            1
          ],
          "destination": [
            "active-v7_lift_range_db-1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "active-v7_lift_range_db-1",
            0
          ],
          "destination": [
            "v7_lift_range_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_comp_threshold_db",
            0
          ],
          "destination": [
            "tag-v7_comp_threshold_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_comp_threshold_db",
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
            "set-v7_comp_threshold_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_comp_threshold_db",
            0
          ],
          "destination": [
            "v7_comp_threshold_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_comp_ratio",
            0
          ],
          "destination": [
            "tag-v7_comp_ratio",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_comp_ratio",
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
            "set-v7_comp_ratio",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_comp_ratio",
            0
          ],
          "destination": [
            "v7_comp_ratio",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_comp_attack_ms",
            0
          ],
          "destination": [
            "tag-v7_comp_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_comp_attack_ms",
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
            "set-v7_comp_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_comp_attack_ms",
            0
          ],
          "destination": [
            "v7_comp_attack_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_comp_release_ms",
            0
          ],
          "destination": [
            "tag-v7_comp_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_comp_release_ms",
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
            "set-v7_comp_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_comp_release_ms",
            0
          ],
          "destination": [
            "v7_comp_release_ms",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_output_trim_db",
            0
          ],
          "destination": [
            "tag-v7_output_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_output_trim_db",
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
            "set-v7_output_trim_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_output_trim_db",
            0
          ],
          "destination": [
            "v7_output_trim_db",
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
            8
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
            9
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
            10
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
