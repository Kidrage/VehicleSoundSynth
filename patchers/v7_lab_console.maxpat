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
          "text": "V7 MIX LAB | 阶次比例 · 高速保持 · 核验"
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
          "text": "先减突出的单音，再补固定低频。高速补偿默认0；只在确认有余量后增加，随当前发动机保存。"
        }
      },
      {
        "box": {
          "id": "readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 9,
          "patching_rect": [
            20.0,
            896.0,
            200.0,
            22.0
          ],
          "text": "route v7_order2_db v7_order3_db v7_speed_weight_db v7_speed_edge_db v7_status v7_gr_db v7_clip_samples profile"
        }
      },
      {
        "box": {
          "id": "panel-v7_order2_db",
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
          "id": "label-v7_order2_db",
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
          "text": "次阶次 A / Order A (dB)"
        }
      },
      {
        "box": {
          "id": "v7_order2_db",
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
          "minimum": -12,
          "maximum": 3,
          "format": 6,
          "varname": "v7_order2_db",
          "hint": "0=原比例；-6约半幅。EV为2f，V10/V12/Ferrari为h2，IONIQ为1.5×root；不是总线EQ。",
          "annotation": "0=原比例；-6约半幅。EV为2f，V10/V12/Ferrari为h2，IONIQ为1.5×root；不是总线EQ。",
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
          "id": "tag-v7_order2_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            992.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_order2_db"
        }
      },
      {
        "box": {
          "id": "set-v7_order2_db",
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
          "id": "help-v7_order2_db",
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
          "text": "-12…3  |  0=原比例；-6约半幅。EV为2f，V10/V12/Ferrari为h2，IONIQ为1.5×root；不是总线EQ。"
        }
      },
      {
        "box": {
          "id": "panel-v7_order3_db",
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
          "id": "label-v7_order3_db",
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
          "text": "次阶次 B / Order B (dB)"
        }
      },
      {
        "box": {
          "id": "v7_order3_db",
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
          "varname": "v7_order3_db",
          "hint": "0=原比例；-6约半幅。EV为约3f双侧分量，V10/V12/Ferrari为h3，IONIQ为2.25×root。",
          "annotation": "0=原比例；-6约半幅。EV为约3f双侧分量，V10/V12/Ferrari为h3，IONIQ为2.25×root。",
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
          "id": "tag-v7_order3_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1136.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_order3_db"
        }
      },
      {
        "box": {
          "id": "set-v7_order3_db",
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
          "id": "help-v7_order3_db",
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
          "text": "-12…3  |  0=原比例；-6约半幅。EV为约3f双侧分量，V10/V12/Ferrari为h3，IONIQ为2.25×root。"
        }
      },
      {
        "box": {
          "id": "panel-v7_speed_weight_db",
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
          "id": "label-v7_speed_weight_db",
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
          "text": "高速重量保持 / Speed mass (dB)"
        }
      },
      {
        "box": {
          "id": "v7_speed_weight_db",
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
          "maximum": 6,
          "format": 6,
          "varname": "v7_speed_weight_db",
          "hint": "只提升独立Sub+Foundation。60km/h以下0；60–140平滑增长；140以上为设定dB。0=不额外补偿。",
          "annotation": "只提升独立Sub+Foundation。60km/h以下0；60–140平滑增长；140以上为设定dB。0=不额外补偿。",
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
          "id": "tag-v7_speed_weight_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1280.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_speed_weight_db"
        }
      },
      {
        "box": {
          "id": "set-v7_speed_weight_db",
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
          "id": "help-v7_speed_weight_db",
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
          "text": "0…6  |  只提升独立Sub+Foundation。60km/h以下0；60–140平滑增长；140以上为设定dB。0=不额外补偿。"
        }
      },
      {
        "box": {
          "id": "panel-v7_speed_edge_db",
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
          "id": "label-v7_speed_edge_db",
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
          "text": "高速高频约束 / Speed edge (dB)"
        }
      },
      {
        "box": {
          "id": "v7_speed_edge_db",
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
          "minimum": -6,
          "maximum": 0,
          "format": 6,
          "varname": "v7_speed_edge_db",
          "hint": "连续DNA+SC的2kHz高架附加量。60–140km/h渐进；0=不补偿，-6=高速最多约半幅。",
          "annotation": "连续DNA+SC的2kHz高架附加量。60–140km/h渐进；0=不补偿，-6=高速最多约半幅。",
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
          "id": "tag-v7_speed_edge_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1424.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_speed_edge_db"
        }
      },
      {
        "box": {
          "id": "set-v7_speed_edge_db",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1448.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "help-v7_speed_edge_db",
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
          "text": "-6…0  |  连续DNA+SC的2kHz高架附加量。60–140km/h渐进；0=不补偿，-6=高速最多约半幅。"
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
            1520.0,
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
            1568.0,
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
            1616.0,
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
            1664.0,
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
            1736.0,
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
            1808.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "meter-note",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            257,
            1080,
            34
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            257,
            1080,
            34
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "连续 DNA + SC 的数字输出观察（EQ后／事件与车内处理前），250ms RMS，重叠宽带估计；不是座舱声压。"
        }
      },
      {
        "box": {
          "id": "lab-meter-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 10,
          "patching_rect": [
            20.0,
            1856.0,
            200.0,
            22.0
          ],
          "text": "route v7_meter_sub_db v7_meter_body_db v7_meter_cavity_db v7_meter_edge_db drive_state shift_reason v7_render_rpm v7_root_hz v7_save_status"
        }
      },
      {
        "box": {
          "id": "v7_meter_sub_db-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            302,
            260,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            302,
            260,
            26
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "60 Hz / LF / dBFS"
        }
      },
      {
        "box": {
          "id": "v7_meter_sub_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            16,
            333,
            253,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            333,
            253,
            28
          ],
          "ignoreclick": 1,
          "format": 6,
          "hint": "Bandpass 60 Hz, Q=0.7; overlap with adjacent meters; digital RMS, not acoustic SPL."
        }
      },
      {
        "box": {
          "id": "v7_meter_sub_db-readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1928.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "v7_meter_body_db-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            290,
            302,
            260,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            290,
            302,
            260,
            26
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "170 Hz / Body / dBFS"
        }
      },
      {
        "box": {
          "id": "v7_meter_body_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            290,
            333,
            253,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            290,
            333,
            253,
            28
          ],
          "ignoreclick": 1,
          "format": 6,
          "hint": "Bandpass 170 Hz, Q=0.8; overlap with adjacent meters; digital RMS, not acoustic SPL."
        }
      },
      {
        "box": {
          "id": "v7_meter_body_db-readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2000.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "v7_meter_cavity_db-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            564,
            302,
            260,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            564,
            302,
            260,
            26
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "300 Hz / Cavity / dBFS"
        }
      },
      {
        "box": {
          "id": "v7_meter_cavity_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            564,
            333,
            253,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            564,
            333,
            253,
            28
          ],
          "ignoreclick": 1,
          "format": 6,
          "hint": "Bandpass 300 Hz, Q=1.4; overlap with adjacent meters; digital RMS, not acoustic SPL."
        }
      },
      {
        "box": {
          "id": "v7_meter_cavity_db-readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2072.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "v7_meter_edge_db-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            838,
            302,
            260,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            838,
            302,
            260,
            26
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "3.5 kHz / Edge / dBFS"
        }
      },
      {
        "box": {
          "id": "v7_meter_edge_db",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            838,
            333,
            253,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            838,
            333,
            253,
            28
          ],
          "ignoreclick": 1,
          "format": 6,
          "hint": "Bandpass 3500 Hz, Q=0.9; overlap with adjacent meters; digital RMS, not acoustic SPL."
        }
      },
      {
        "box": {
          "id": "v7_meter_edge_db-readback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2144.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "meter-meaning",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            372,
            1080,
            35
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            372,
            1080,
            35
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "不要把四个读数调成一样：它们的带宽不同。比较同一驾驶轨迹的 A/B；谐波能量占比用导出的 WAV 审核。"
        }
      },
      {
        "box": {
          "id": "drive_state-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            415,
            252,
            24
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            415,
            252,
            24
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "内部驾驶状态"
        }
      },
      {
        "box": {
          "id": "drive_state",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            440,
            252,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            440,
            252,
            28
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "—"
        }
      },
      {
        "box": {
          "id": "drive_state-setter",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2240.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "shift_reason-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            290,
            415,
            252,
            24
          ],
          "presentation": 1,
          "presentation_rect": [
            290,
            415,
            252,
            24
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "最近一次换挡原因"
        }
      },
      {
        "box": {
          "id": "shift_reason",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            290,
            440,
            252,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            290,
            440,
            252,
            28
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "—"
        }
      },
      {
        "box": {
          "id": "shift_reason-setter",
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
          "id": "v7_render_rpm-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            565,
            415,
            252,
            24
          ],
          "presentation": 1,
          "presentation_rect": [
            565,
            415,
            252,
            24
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "IONIQ 发声RPM"
        }
      },
      {
        "box": {
          "id": "v7_render_rpm",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            565,
            440,
            252,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            565,
            440,
            252,
            28
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "—"
        }
      },
      {
        "box": {
          "id": "v7_render_rpm-setter",
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
          "id": "v7_root_hz-title",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            840,
            415,
            252,
            24
          ],
          "presentation": 1,
          "presentation_rect": [
            840,
            415,
            252,
            24
          ],
          "fontsize": 12,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "IONIQ root / Hz"
        }
      },
      {
        "box": {
          "id": "v7_root_hz",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            840,
            440,
            252,
            28
          ],
          "presentation": 1,
          "presentation_rect": [
            840,
            440,
            252,
            28
          ],
          "fontsize": 13,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 1,
          "text": "—"
        }
      },
      {
        "box": {
          "id": "v7_root_hz-setter",
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
          "id": "save-status",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            16,
            480,
            780,
            32
          ],
          "presentation": 1,
          "presentation_rect": [
            16,
            480,
            780,
            32
          ],
          "fontsize": 11,
          "textcolor": [
            0.86,
            0.9,
            0.96,
            1.0
          ],
          "linecount": 2,
          "text": "保存回执：尚未请求；关闭窗口前请完成核验。"
        }
      },
      {
        "box": {
          "id": "save-status-set",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2504.0,
            200.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "verify-save",
          "maxclass": "textbutton",
          "numinlets": 1,
          "numoutlets": 3,
          "patching_rect": [
            832,
            480,
            260,
            30
          ],
          "presentation": 1,
          "presentation_rect": [
            832,
            480,
            260,
            30
          ],
          "text": "核验保存 / Verify"
        }
      },
      {
        "box": {
          "id": "verify-command",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2552.0,
            200.0,
            22.0
          ],
          "text": "verify_profile_sound"
        }
      },
      {
        "box": {
          "id": "lab-profile",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            20.0,
            2576.0,
            200.0,
            22.0
          ],
          "text": "route profile"
        }
      },
      {
        "box": {
          "id": "lab-clear",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2600.0,
            200.0,
            22.0
          ],
          "text": "set —"
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
            "v7_order2_db",
            0
          ],
          "destination": [
            "tag-v7_order2_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_order2_db",
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
            "set-v7_order2_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_order2_db",
            0
          ],
          "destination": [
            "v7_order2_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_order3_db",
            0
          ],
          "destination": [
            "tag-v7_order3_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_order3_db",
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
            "set-v7_order3_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_order3_db",
            0
          ],
          "destination": [
            "v7_order3_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_speed_weight_db",
            0
          ],
          "destination": [
            "tag-v7_speed_weight_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_speed_weight_db",
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
            "set-v7_speed_weight_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_speed_weight_db",
            0
          ],
          "destination": [
            "v7_speed_weight_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_speed_edge_db",
            0
          ],
          "destination": [
            "tag-v7_speed_edge_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "tag-v7_speed_edge_db",
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
            "set-v7_speed_edge_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "set-v7_speed_edge_db",
            0
          ],
          "destination": [
            "v7_speed_edge_db",
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
            4
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
            5
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
            6
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
      },
      {
        "patchline": {
          "source": [
            "in",
            0
          ],
          "destination": [
            "lab-meter-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            0
          ],
          "destination": [
            "v7_meter_sub_db-readback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_meter_sub_db-readback",
            0
          ],
          "destination": [
            "v7_meter_sub_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            1
          ],
          "destination": [
            "v7_meter_body_db-readback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_meter_body_db-readback",
            0
          ],
          "destination": [
            "v7_meter_body_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            2
          ],
          "destination": [
            "v7_meter_cavity_db-readback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_meter_cavity_db-readback",
            0
          ],
          "destination": [
            "v7_meter_cavity_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            3
          ],
          "destination": [
            "v7_meter_edge_db-readback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_meter_edge_db-readback",
            0
          ],
          "destination": [
            "v7_meter_edge_db",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            4
          ],
          "destination": [
            "drive_state-setter",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "drive_state-setter",
            0
          ],
          "destination": [
            "drive_state",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            5
          ],
          "destination": [
            "shift_reason-setter",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "shift_reason-setter",
            0
          ],
          "destination": [
            "shift_reason",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            6
          ],
          "destination": [
            "v7_render_rpm-setter",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_render_rpm-setter",
            0
          ],
          "destination": [
            "v7_render_rpm",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            7
          ],
          "destination": [
            "v7_root_hz-setter",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7_root_hz-setter",
            0
          ],
          "destination": [
            "v7_root_hz",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-meter-route",
            8
          ],
          "destination": [
            "save-status-set",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "save-status-set",
            0
          ],
          "destination": [
            "save-status",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "verify-save",
            0
          ],
          "destination": [
            "verify-command",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "verify-command",
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
            "in",
            0
          ],
          "destination": [
            "lab-profile",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-profile",
            0
          ],
          "destination": [
            "lab-clear",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-clear",
            0
          ],
          "destination": [
            "drive_state",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-clear",
            0
          ],
          "destination": [
            "shift_reason",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-clear",
            0
          ],
          "destination": [
            "v7_render_rpm",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lab-clear",
            0
          ],
          "destination": [
            "v7_root_hz",
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
