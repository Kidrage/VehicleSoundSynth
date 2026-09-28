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
            20.0,
            12.0,
            760.0,
            22.0
          ],
          "text": "DRIVE / 驾驶 — common lifecycle and exclusive Keyboard/Gamepad input"
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1060.0,
            20.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "messages",
          "id": "obj-3",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1060.0,
            565.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            50.0,
            150.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            50.0,
            47.0,
            150.0,
            18.0
          ],
          "text": "Audio On / 音频总开关",
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
          "id": "obj-5",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            75.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            44.0,
            24.0,
            24.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            55.0,
            75.0,
            145.0,
            22.0
          ],
          "text": "prepend audio_enable"
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
            205.0,
            75.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            310.0,
            50.0,
            170.0,
            22.0
          ],
          "text": "Lifecycle / 点火与启动"
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
            310.0,
            75.0,
            125.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            210.0,
            44.0,
            125.0,
            24.0
          ],
          "text": "Ignition On / 点火",
          "hint": "Ignition On / 点火：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Ignition On / 点火：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-10",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            310.0,
            110.0,
            75.0,
            22.0
          ],
          "text": "ignition 1"
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
            445.0,
            75.0,
            95.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            345.0,
            44.0,
            95.0,
            24.0
          ],
          "text": "Start / 启动",
          "hint": "Start / 启动：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Start / 启动：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-12",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            445.0,
            110.0,
            60.0,
            22.0
          ],
          "text": "start 1"
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
            550.0,
            75.0,
            130.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            450.0,
            44.0,
            130.0,
            24.0
          ],
          "text": "Ignition Off / 熄火",
          "hint": "Ignition Off / 熄火：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Ignition Off / 熄火：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-14",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            550.0,
            110.0,
            75.0,
            22.0
          ],
          "text": "ignition 0"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            710.0,
            50.0,
            170.0,
            22.0
          ],
          "text": "Drive Source / 控制模式"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "items": [
            "Internal Manual / 手动",
            ",",
            "Internal Auto / 自动",
            ",",
            "External / 外部"
          ],
          "maxclass": "umenu",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            710.0,
            75.0,
            210.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            600.0,
            44.0,
            210.0,
            24.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            930.0,
            75.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            710.0,
            110.0,
            150.0,
            22.0
          ],
          "text": "prepend drive_source"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            870.0,
            110.0,
            45.0,
            22.0
          ],
          "text": "== 0"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            150.0,
            250.0,
            22.0
          ],
          "text": "Live State / 实时状态（只读）"
        }
      },
      {
        "box": {
          "id": "obj-21",
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
            20.0,
            178.0,
            560.0,
            22.0
          ],
          "text": "route audio_enable speed_kph rpm throttle brake load gear"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            590.0,
            178.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "Speed / 速度 [km/h]",
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
          "id": "obj-24",
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-25",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            118.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            192.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            192.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "RPM / 转速 [rpm]",
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
          "id": "obj-27",
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            192.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            192.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-28",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            290.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            364.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            364.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "Throttle / 油门 [0..1]",
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
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            364.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            364.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            462.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            536.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            536.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "Brake / 刹车 [0..1]",
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
          "id": "obj-33",
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            536.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            536.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-34",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            634.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            708.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            708.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "Load / 负载 [-1..1]",
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
          "id": "obj-36",
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            708.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            708.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-37",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            806.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            880.0,
            215.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            880.0,
            95.0,
            160.0,
            18.0
          ],
          "text": "Gear / 档位 [gear]",
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
          "id": "obj-39",
          "ignoreclick": 1,
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            880.0,
            238.0,
            92.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            880.0,
            116.0,
            92.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-40",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            978.0,
            238.0,
            75.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            285.0,
            720.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            155.0,
            720.0,
            20.0
          ],
          "text": "Input Device / 输入设备 — 仅 Manual 激活；切换模式或设备会立即清零踏板",
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
          "id": "obj-42",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_manual_input.maxpat",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            315.0,
            1000.0,
            250.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            180.0,
            1000.0,
            390.0
          ],
          "varname": "manual_input"
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
            820.0,
            575.0,
            115.0,
            22.0
          ],
          "text": "prepend throttle"
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
            940.0,
            575.0,
            105.0,
            22.0
          ],
          "text": "prepend brake"
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
            "obj-3",
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
            "obj-5",
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
            "obj-10",
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
            "obj-3",
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
            "obj-3",
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
            "obj-3",
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
            "obj-16",
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
            "obj-18",
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
            "obj-18",
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
            "obj-16",
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
            "obj-2",
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
            "obj-22",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-25",
            0
          ],
          "source": [
            "obj-21",
            1
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
            "obj-25",
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
            "obj-21",
            2
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
            "obj-21",
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
            "obj-31",
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
            "obj-21",
            4
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
            "obj-34",
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
            "obj-21",
            5
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
            "obj-37",
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
            "obj-21",
            6
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
            "obj-40",
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
            "obj-19",
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
            "obj-42",
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
            "obj-42",
            1
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
            "obj-43",
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
            "obj-44",
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
      1120,
      610
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
