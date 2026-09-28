{
  "patcher": {
    "appversion": {
      "architecture": "x64",
      "major": 8,
      "minor": 6,
      "modernui": 1,
      "revision": 5
    },
    "bglocked": 0,
    "boxes": [
      {
        "box": {
          "id": "obj-1",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            15.0,
            8.0,
            800.0,
            22.0
          ],
          "text": "SOUNDSCAPE CONTROL — Main > Sound Design; live profile-owned instrument state"
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            735.0,
            8.0,
            190.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            820.0,
            8.0,
            200.0,
            18.0
          ],
          "text": "Running Bed / 独立铺底",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            15.0,
            240.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "messages",
          "id": "obj-4",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1035.0,
            240.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 5,
          "outlettype": [
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            670.0,
            205.0,
            355.0,
            22.0
          ],
          "text": "route soundscape_state soundscape_status soundscape_level_db profile"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 8,
          "outlettype": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            430.0,
            240.0,
            465.0,
            22.0
          ],
          "text": "route enable motion space pitch_follow transpose brightness solo"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            805.0,
            240.0,
            85.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            895.0,
            205.0,
            145.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            820.0,
            70.0,
            200.0,
            22.0
          ],
          "text": "Factory / 独立铺底",
          "hint": "Factory / 独立铺底：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Factory / 独立铺底：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            595.0,
            155.0,
            185.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            585.0,
            70.0,
            180.0,
            18.0
          ],
          "text": "Soundscape Level / 氛围电平",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "flonum",
          "maximum": 6.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            775.0,
            155.0,
            70.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            745.0,
            68.0,
            68.0,
            22.0
          ],
          "hint": "Soundscape推子：-60..6 dB；只调景观层，不调DNA或Noise。SC关闭时此值不发声。",
          "annotation": "Soundscape推子：-60..6 dB；只调景观层，不调DNA或Noise。SC关闭时此值不发声。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            775.0,
            180.0,
            85.0,
            22.0
          ],
          "text": "clip -60. 6."
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            865.0,
            180.0,
            190.0,
            22.0
          ],
          "text": "prepend soundscape_level_db"
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            865.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            945.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            945.0,
            155.0,
            115.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            820.0,
            98.0,
            200.0,
            22.0
          ],
          "text": "No active profile",
          "hint": "No active profile：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "No active profile：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            15.0,
            215.0,
            620.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            102.0,
            620.0,
            18.0
          ],
          "text": "Main > Sound Design：Enable → Level → Open Designer；Ferrari 使用独立 V5 状态。",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            15.0,
            38.0,
            80.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            8.0,
            80.0,
            18.0
          ],
          "text": "Enable / 开启",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            15.0,
            60.0,
            22.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            30.0,
            22.0,
            22.0
          ],
          "hint": "0关闭Soundscape；1启用。不会关闭DNA/Noise或替代Audio开关。",
          "annotation": "0关闭Soundscape；1启用。不会关闭DNA/Noise或替代Audio开关。"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            15.0,
            92.0,
            170.0,
            22.0
          ],
          "text": "prepend soundscape_enable"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            45.0,
            60.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-21",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            105.0,
            38.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            105.0,
            8.0,
            130.0,
            18.0
          ],
          "text": "Motion / 动态",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            105.0,
            60.0,
            72.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            105.0,
            30.0,
            72.0,
            22.0
          ],
          "hint": "0..1：景观层动态/运动深度；需动态工况验证。",
          "annotation": "0..1：景观层动态/运动深度；需动态工况验证。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            105.0,
            92.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-24",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            105.0,
            122.0,
            175.0,
            22.0
          ],
          "text": "prepend soundscape_motion"
        }
      },
      {
        "box": {
          "id": "obj-25",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            235.0,
            38.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            235.0,
            8.0,
            130.0,
            18.0
          ],
          "text": "Space / 空间",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            235.0,
            60.0,
            72.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            235.0,
            30.0,
            72.0,
            22.0
          ],
          "hint": "0..1：空间/湿声深度；0最干、1最湿，受各车型设计约束。",
          "annotation": "0..1：空间/湿声深度；0最干、1最湿，受各车型设计约束。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-27",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            235.0,
            92.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            235.0,
            122.0,
            175.0,
            22.0
          ],
          "text": "prepend soundscape_space"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            365.0,
            38.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            365.0,
            8.0,
            130.0,
            18.0
          ],
          "text": "Pitch Follow / 转速跟随",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            365.0,
            60.0,
            72.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            365.0,
            30.0,
            72.0,
            22.0
          ],
          "hint": "0..1：Soundscape跟随RPM的深度，0最固定、1最跟随；不改变车辆RPM/档位。",
          "annotation": "0..1：Soundscape跟随RPM的深度，0最固定、1最跟随；不改变车辆RPM/档位。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            365.0,
            92.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            365.0,
            122.0,
            175.0,
            22.0
          ],
          "text": "prepend soundscape_pitch_follow"
        }
      },
      {
        "box": {
          "id": "obj-33",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            505.0,
            38.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            505.0,
            8.0,
            130.0,
            18.0
          ],
          "text": "Transpose / 移调",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-34",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            505.0,
            60.0,
            72.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            505.0,
            30.0,
            72.0,
            22.0
          ],
          "hint": "Soundscape音高偏移：-12..12半音；0不移调。大幅上移会损失低频底座，V7质量层不跟随。",
          "annotation": "Soundscape音高偏移：-12..12半音；0不移调。大幅上移会损失低频底座，V7质量层不跟随。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            505.0,
            92.0,
            90.0,
            22.0
          ],
          "text": "clip -12 12"
        }
      },
      {
        "box": {
          "id": "obj-36",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            505.0,
            122.0,
            175.0,
            22.0
          ],
          "text": "prepend soundscape_transpose"
        }
      },
      {
        "box": {
          "id": "obj-37",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            645.0,
            38.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            645.0,
            8.0,
            130.0,
            18.0
          ],
          "text": "Brightness / 明亮度",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            645.0,
            60.0,
            72.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            645.0,
            30.0,
            72.0,
            22.0
          ],
          "hint": "0..1：景观层滤波/音色宏，0暗、1亮；只对启用的SC层有效，不是总线高架dB。",
          "annotation": "0..1：景观层滤波/音色宏，0暗、1亮；只对启用的SC层有效，不是总线高架dB。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-39",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            645.0,
            92.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            645.0,
            122.0,
            175.0,
            22.0
          ],
          "text": "prepend soundscape_brightness"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            560.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            650.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            740.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-45",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            920.0,
            205.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            15.0,
            155.0,
            115.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            68.0,
            115.0,
            22.0
          ],
          "text": "Open Designer",
          "hint": "Open Designer：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open Designer：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            15.0,
            185.0,
            120.0,
            22.0
          ],
          "text": "soundscape_open"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            145.0,
            155.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            145.0,
            68.0,
            65.0,
            22.0
          ],
          "text": "Save",
          "hint": "Save：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Save：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            145.0,
            185.0,
            120.0,
            22.0
          ],
          "text": "soundscape_save"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            225.0,
            155.0,
            115.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            225.0,
            68.0,
            115.0,
            22.0
          ],
          "text": "Reload",
          "hint": "Reload：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Reload：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-51",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            225.0,
            185.0,
            120.0,
            22.0
          ],
          "text": "soundscape_reload"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            355.0,
            155.0,
            115.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            355.0,
            68.0,
            115.0,
            22.0
          ],
          "text": "Factory Reset",
          "hint": "Factory Reset：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Factory Reset：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.15,
            0.2,
            0.28,
            1.0
          ],
          "textcolor": [
            0.93,
            0.97,
            1.0,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            355.0,
            185.0,
            120.0,
            22.0
          ],
          "text": "soundscape_reset"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            460.0,
            155.0,
            90.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            513.0,
            70.0,
            80.0,
            18.0
          ],
          "text": "Solo / 独听",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            500.0,
            155.0,
            22.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            485.0,
            68.0,
            22.0,
            22.0
          ],
          "hint": "0普通混合，1独听此声层；不写入定稿预设，避免下次开机误静音其他层。",
          "annotation": "0普通混合，1独听此声层；不写入定稿预设，避免下次开机误静音其他层。"
        }
      },
      {
        "box": {
          "id": "obj-56",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            530.0,
            155.0,
            160.0,
            22.0
          ],
          "text": "prepend soundscape_solo"
        }
      },
      {
        "box": {
          "id": "obj-57",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            530.0,
            185.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-58",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            620.0,
            185.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-59",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            735.0,
            155.0,
            45.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            600.0,
            70.0,
            45.0,
            18.0
          ],
          "text": "State",
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ]
        }
      }
    ],
    "classnamespace": "box",
    "default_fontface": 0,
    "default_fontname": "Arial",
    "default_fontsize": 12.0,
    "enablehscroll": 1,
    "enablevscroll": 1,
    "fileversion": 1,
    "gridonopen": 1,
    "gridsize": [
      15.0,
      15.0
    ],
    "gridsnaponopen": 1,
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-3",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "source": [
            "obj-5",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "source": [
            "obj-5",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-8",
            0
          ],
          "source": [
            "obj-7",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-11",
            0
          ],
          "source": [
            "obj-10",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-12",
            0
          ],
          "source": [
            "obj-11",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-12",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-13",
            0
          ],
          "source": [
            "obj-5",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-10",
            0
          ],
          "source": [
            "obj-13",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-14",
            0
          ],
          "source": [
            "obj-5",
            3
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-15",
            0
          ],
          "source": [
            "obj-14",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-19",
            0
          ],
          "source": [
            "obj-18",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-19",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-20",
            0
          ],
          "source": [
            "obj-6",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-18",
            0
          ],
          "source": [
            "obj-20",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-23",
            0
          ],
          "source": [
            "obj-22",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-24",
            0
          ],
          "source": [
            "obj-23",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-24",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-27",
            0
          ],
          "source": [
            "obj-26",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-28",
            0
          ],
          "source": [
            "obj-27",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-28",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-31",
            0
          ],
          "source": [
            "obj-30",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-32",
            0
          ],
          "source": [
            "obj-31",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-32",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-35",
            0
          ],
          "source": [
            "obj-34",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-36",
            0
          ],
          "source": [
            "obj-35",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-36",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-39",
            0
          ],
          "source": [
            "obj-38",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-40",
            0
          ],
          "source": [
            "obj-39",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-40",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-41",
            0
          ],
          "source": [
            "obj-6",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-22",
            0
          ],
          "source": [
            "obj-41",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-42",
            0
          ],
          "source": [
            "obj-6",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-26",
            0
          ],
          "source": [
            "obj-42",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-43",
            0
          ],
          "source": [
            "obj-6",
            3
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-30",
            0
          ],
          "source": [
            "obj-43",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-44",
            0
          ],
          "source": [
            "obj-6",
            4
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-34",
            0
          ],
          "source": [
            "obj-44",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-45",
            0
          ],
          "source": [
            "obj-6",
            5
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-38",
            0
          ],
          "source": [
            "obj-45",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-47",
            0
          ],
          "source": [
            "obj-46",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-47",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-49",
            0
          ],
          "source": [
            "obj-48",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-49",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-51",
            0
          ],
          "source": [
            "obj-50",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-51",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-53",
            0
          ],
          "source": [
            "obj-52",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-53",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-56",
            0
          ],
          "source": [
            "obj-55",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-56",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-55",
            0
          ],
          "source": [
            "obj-57",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-58",
            0
          ],
          "source": [
            "obj-6",
            6
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-55",
            0
          ],
          "source": [
            "obj-58",
            0
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "rect": [
      50.0,
      50.0,
      1080,
      275
    ],
    "toolbarvisible": 1,
    "bgcolor": [
      0.065,
      0.085,
      0.12,
      1.0
    ]
  }
}
