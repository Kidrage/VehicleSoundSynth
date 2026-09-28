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
            30.0,
            20.0,
            650.0,
            22.0
          ],
          "text": "EV-ENGINE-V7  |  声音设计 · 驾驶响应 · 混音定稿",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ],
          "fontsize": 23,
          "presentation": 1,
          "presentation_rect": [
            30,
            12,
            1180,
            33
          ]
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            30.0,
            48.0,
            830.0,
            40.0
          ],
          "text": "五款独立发动机 · 当前音色保存绑定本车 · V7 Tone / Response 可直接调音 · 音频启动默认 OFF",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            48,
            1180,
            31
          ]
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1030.0,
            100.0,
            70.0,
            22.0
          ],
          "text": "pcontrol"
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            860.0,
            100.0,
            145.0,
            22.0
          ],
          "text": "s vss.runtime.select"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 7,
          "outlettype": [
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            835.0,
            165.0,
            250.0,
            22.0
          ],
          "text": "sel ev v10 v12 ioniq6n ferrari none"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            30.0,
            92.0,
            280.0,
            22.0
          ],
          "text": "Future EV",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            30.0,
            118.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            90,
            380,
            30
          ],
          "text": "Open Future EV",
          "hint": "Open Future EV：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open Future EV：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            30.0,
            146.0,
            50.0,
            22.0
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            90.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "ev"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            160.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "delay 40"
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            30.0,
            174.0,
            260.0,
            22.0
          ],
          "text": "loadunique EV-Engine-V7-EV.maxpat"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            330.0,
            92.0,
            280.0,
            22.0
          ],
          "text": "Ferrari-referenced V10",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            330.0,
            118.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            425,
            90,
            380,
            30
          ],
          "text": "Open Ferrari-referenced V10",
          "hint": "Open Ferrari-referenced V10：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open Ferrari-referenced V10：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            330.0,
            146.0,
            50.0,
            22.0
          ],
          "text": "t b b"
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
            390.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "v10"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            460.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "delay 40"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            330.0,
            174.0,
            260.0,
            22.0
          ],
          "text": "loadunique EV-Engine-V7-V10.maxpat"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            630.0,
            92.0,
            280.0,
            22.0
          ],
          "text": "Independent V12",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            630.0,
            118.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            820,
            90,
            380,
            30
          ],
          "text": "Open Independent V12",
          "hint": "Open Independent V12：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open Independent V12：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            630.0,
            146.0,
            50.0,
            22.0
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-21",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            690.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "v12"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            760.0,
            146.0,
            65.0,
            22.0
          ],
          "text": "delay 40"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            630.0,
            174.0,
            260.0,
            22.0
          ],
          "text": "loadunique EV-Engine-V7-V12.maxpat"
        }
      },
      {
        "box": {
          "id": "obj-24",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            30.0,
            150.0,
            280.0,
            22.0
          ],
          "text": "IONIQ 6 N",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-25",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            30.0,
            176.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            129,
            380,
            30
          ],
          "text": "Open IONIQ 6 N",
          "hint": "Open IONIQ 6 N：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open IONIQ 6 N：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            30.0,
            204.0,
            50.0,
            22.0
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-27",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            90.0,
            204.0,
            65.0,
            22.0
          ],
          "text": "ioniq6n"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            160.0,
            204.0,
            65.0,
            22.0
          ],
          "text": "delay 40"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            30.0,
            232.0,
            260.0,
            22.0
          ],
          "text": "loadunique EV-Engine-V7-IONIQ6N.maxpat"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            330.0,
            150.0,
            280.0,
            22.0
          ],
          "text": "Ferrari SF90 — V10 Acoustic Interpretation",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            330.0,
            176.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            425,
            129,
            380,
            30
          ],
          "text": "Open Ferrari SF90 / 声学演绎",
          "hint": "Open Ferrari SF90 — V10 Acoustic Interpretation：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Open Ferrari SF90 — V10 Acoustic Interpretation：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            330.0,
            204.0,
            50.0,
            22.0
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-33",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            390.0,
            204.0,
            65.0,
            22.0
          ],
          "text": "ferrari"
        }
      },
      {
        "box": {
          "id": "obj-34",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            460.0,
            204.0,
            65.0,
            22.0
          ],
          "text": "delay 40"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            330.0,
            232.0,
            260.0,
            22.0
          ],
          "text": "loadunique EV-Engine-V7-Ferrari.maxpat"
        }
      },
      {
        "box": {
          "id": "obj-36",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            930.0,
            176.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            820,
            129,
            380,
            30
          ],
          "text": "Close Active / 关闭当前车型",
          "hint": "Close Active / 关闭当前车型：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Close Active / 关闭当前车型：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "bgcolor": [
            0.16,
            0.22,
            0.3,
            1.0
          ],
          "textcolor": [
            0.92,
            0.97,
            1.0,
            1.0
          ],
          "fontsize": 14
        }
      },
      {
        "box": {
          "id": "obj-37",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1090.0,
            205.0,
            55.0,
            22.0
          ],
          "text": "none"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_runtime_console.maxpat",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            30.0,
            270.0,
            1180.0,
            600.0
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            178,
            1180,
            660
          ],
          "varname": "runtime_console"
        }
      },
      {
        "box": {
          "id": "obj-39",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            873.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "1"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            911.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "2"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            949.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "3"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            987.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "4"
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1025.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "5"
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            835.0,
            235.0,
            30.0,
            22.0
          ],
          "text": "0"
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
            835.0,
            265.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 5,
          "outlettype": [
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            1030.0,
            750.0,
            65.0,
            22.0
          ],
          "text": "gate 5"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "newobj",
          "numinlets": 6,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1030.0,
            800.0,
            75.0,
            22.0
          ],
          "text": "switch 5"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            530.0,
            190.0,
            22.0
          ],
          "text": "s vss.runtime.control.ev"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            530.0,
            220.0,
            22.0
          ],
          "text": "r vss.runtime.feedback.ev"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            555.0,
            190.0,
            22.0
          ],
          "text": "s vss.runtime.control.v10"
        }
      },
      {
        "box": {
          "id": "obj-51",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            555.0,
            220.0,
            22.0
          ],
          "text": "r vss.runtime.feedback.v10"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            580.0,
            190.0,
            22.0
          ],
          "text": "s vss.runtime.control.v12"
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            580.0,
            220.0,
            22.0
          ],
          "text": "r vss.runtime.feedback.v12"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            605.0,
            190.0,
            22.0
          ],
          "text": "s vss.runtime.control.ioniq6n"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            605.0,
            220.0,
            22.0
          ],
          "text": "r vss.runtime.feedback.ioniq6n"
        }
      },
      {
        "box": {
          "id": "obj-56",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            630.0,
            190.0,
            22.0
          ],
          "text": "s vss.runtime.control.ferrari"
        }
      },
      {
        "box": {
          "id": "obj-57",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            630.0,
            220.0,
            22.0
          ],
          "text": "r vss.runtime.feedback.ferrari"
        }
      },
      {
        "box": {
          "id": "obj-58",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            30.0,
            875.0,
            900.0,
            22.0
          ],
          "text": "候选版本：本机 Max 与实车听评尚待验收。仅开启一个发动机；请先低音量试听。唯一操作说明：V7_MANUAL.md",
          "textcolor": [
            0.82,
            0.88,
            0.95,
            1.0
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            850,
            1180,
            44
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
            "obj-9",
            0
          ],
          "source": [
            "obj-8",
            1
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
            "obj-9",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-9",
            0
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
            "obj-8",
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
            "obj-3",
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
            "obj-14",
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
            "obj-15",
            0
          ],
          "source": [
            "obj-14",
            1
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
            "obj-15",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-15",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-16",
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
            "obj-17",
            0
          ],
          "source": [
            "obj-16",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-3",
            0
          ],
          "source": [
            "obj-17",
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
            "obj-19",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-21",
            0
          ],
          "source": [
            "obj-20",
            1
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
            "obj-21",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-21",
            0
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
            "obj-3",
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
            "obj-26",
            0
          ],
          "source": [
            "obj-25",
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
            1
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
            "obj-27",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
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
            "obj-28",
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
            "obj-29",
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
            "obj-3",
            0
          ],
          "source": [
            "obj-29",
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
            "obj-33",
            0
          ],
          "source": [
            "obj-32",
            1
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
            "obj-33",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-33",
            0
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
            "obj-3",
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
            "obj-37",
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
            "obj-4",
            0
          ],
          "source": [
            "obj-37",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-37",
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
            "obj-5",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
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
            "obj-47",
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
            "obj-40",
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
            "obj-46",
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
            "obj-47",
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
            "obj-5",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
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
            "obj-47",
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
            "obj-5",
            3
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
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
            "obj-47",
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
            "obj-5",
            4
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
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
            "obj-47",
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
            "obj-5",
            5
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
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
            "obj-47",
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
            "obj-46",
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
            "obj-45",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-46",
            1
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
            "obj-48",
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
            "obj-47",
            1
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
            "obj-50",
            0
          ],
          "source": [
            "obj-46",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-47",
            2
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
            "obj-52",
            0
          ],
          "source": [
            "obj-46",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-47",
            3
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
            "obj-54",
            0
          ],
          "source": [
            "obj-46",
            3
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-47",
            4
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
            "obj-56",
            0
          ],
          "source": [
            "obj-46",
            4
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-47",
            5
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
            "obj-38",
            0
          ],
          "source": [
            "obj-47",
            0
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "rect": [
      50,
      50,
      1240,
      910
    ],
    "toolbarvisible": 1,
    "bgcolor": [
      0.04,
      0.055,
      0.085,
      1.0
    ]
  }
}
