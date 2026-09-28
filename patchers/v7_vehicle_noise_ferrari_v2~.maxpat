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
            15.0,
            1150.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            15,
            1150,
            22
          ],
          "text": "FERRARI NOISE — mechanical / intake / road / air"
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            42.0,
            1160.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            45,
            1160,
            22
          ],
          "text": "1 Main Noise fader (−60 = OFF) → 2 Solo → 3 component dB → 4 Color / BEAP ceiling. No reverb."
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            67.0,
            1160.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            73,
            1160,
            22
          ],
          "text": "Run engine first. V2 residuals come from the shared pre-mix source, NEVER DNA output gain; SC is independent."
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            110.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            65.0,
            70.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            115.0,
            70.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            165.0,
            70.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 12,
          "outlettype": [
            "",
            "",
            "",
            "",
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
            65.0,
            110.0,
            1110.0,
            22.0
          ],
          "text": "route noise_mechanical_db noise_intake_db noise_tire_db noise_air_db noise_color noise_combustion_db noise_open noise_save noise_reload noise_reset noise_solo"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            335.0,
            340.0,
            22.0
          ],
          "text": "js Patcher:/code/v7_noise_control.js ferrari 2"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1070.0,
            335.0,
            70.0,
            22.0
          ],
          "text": "loadbang"
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            115,
            235,
            22
          ],
          "text": "Mechanical / 机械 dB"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            145,
            94,
            22
          ],
          "varname": "noise_mechanical_db",
          "hint": "Noise机械分支：-60..0 dB，-60关闭；需Noise总推子打开和发动机运行。",
          "annotation": "Noise机械分支：-60..0 dB，-60关闭；需Noise总推子打开和发动机运行。"
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            180,
            231,
            62
          ],
          "text": "RPM cadence + moving 290–1360 Hz band; try at a steady 2000–5000 RPM."
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
            20.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess -10"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_mechanical_db"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            262.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            262,
            115,
            235,
            22
          ],
          "text": "Intake / 进气 dB"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            262.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            262,
            145,
            94,
            22
          ],
          "varname": "noise_intake_db",
          "hint": "Noise进气分支：-60..0 dB，-60关闭；需Noise总推子打开。",
          "annotation": "Noise进气分支：-60..0 dB，-60关闭；需Noise总推子打开。"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            262.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            262,
            180,
            231,
            62
          ],
          "text": "Load + throttle pressure; compare light/full load at the same RPM."
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
            262.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess -15"
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
            262.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_intake_db"
        }
      },
      {
        "box": {
          "id": "obj-21",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            504.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            504,
            115,
            235,
            22
          ],
          "text": "Tire / 路面 dB"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            504.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            504,
            145,
            94,
            22
          ],
          "varname": "noise_tire_db",
          "hint": "轮胎噪声：-60..0 dB，依车速而动；静止时无声是预期行为。",
          "annotation": "轮胎噪声：-60..0 dB，依车速而动；静止时无声是预期行为。"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            504.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            504,
            180,
            231,
            62
          ],
          "text": "70–900 Hz common-center road texture; speed only, silent while parked."
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
            504.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess -14"
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
            504.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_tire_db"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            746.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            746,
            115,
            235,
            22
          ],
          "text": "Air / 风噪 dB"
        }
      },
      {
        "box": {
          "id": "obj-27",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            746.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            746,
            145,
            94,
            22
          ],
          "varname": "noise_air_db",
          "hint": "风噪：-60..0 dB，依车速而动；不是DNA高频增益。",
          "annotation": "风噪：-60..0 dB，依车速而动；不是DNA高频增益。"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            746.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            746,
            180,
            231,
            62
          ],
          "text": "Stereo air above 400 Hz; speed curve, not an always-on hiss."
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            746.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess -22"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            746.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_air_db"
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            988.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            988,
            115,
            235,
            22
          ],
          "text": "Color / 色彩 0–1"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "flonum",
          "maximum": 1.0,
          "minimum": 0.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            988.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            988,
            145,
            94,
            22
          ],
          "varname": "noise_color",
          "hint": "noise_color | 范围 0.0…1.0。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
          "annotation": "noise_color | 范围 0.0…1.0。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
        }
      },
      {
        "box": {
          "id": "obj-33",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            988.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            988,
            180,
            231,
            62
          ],
          "text": "Opens intake/wind filters, not engine pitch. Start at 0.2–0.5."
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
            988.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess 0.35"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            988.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_color"
        }
      },
      {
        "box": {
          "id": "obj-36",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1230.0,
            155.0,
            235.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1230,
            115,
            235,
            22
          ],
          "text": "Combustion / 燃烧残差 dB"
        }
      },
      {
        "box": {
          "id": "obj-37",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1230.0,
            187.0,
            94.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1230,
            145,
            94,
            22
          ],
          "varname": "noise_combustion_db",
          "hint": "Ferrari独立压力残余Noise：-60..0 dB；-60关闭。不是主DNA音量。",
          "annotation": "Ferrari独立压力残余Noise：-60..0 dB；-60关闭。不是主DNA音量。"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1230.0,
            222.0,
            231.0,
            62.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1230,
            180,
            231,
            62
          ],
          "text": "Shared DNA cadence, PRE-DNA-gain random pressure. Main Noise fader still owns the stem."
        }
      },
      {
        "box": {
          "id": "obj-39",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1230.0,
            291.0,
            100.0,
            22.0
          ],
          "text": "loadmess -10"
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
            1230.0,
            315.0,
            220.0,
            22.0
          ],
          "text": "prepend noise_combustion_db"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 12,
          "outlettype": [
            "",
            "",
            "",
            "",
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
            375.0,
            1150.0,
            22.0
          ],
          "text": "route active stem cadence mechanical_hz intake_hz air_hz mechanical intake tire air combustion"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            142.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-45",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            142.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            264.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            264.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            386.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            386.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            508.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-51",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            508.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            630.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            630.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            752.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            752.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-56",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            874.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-57",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            874.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-58",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            996.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-59",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            996.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-60",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1118.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-61",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1118.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-62",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1240.0,
            412.0,
            100.0,
            22.0
          ],
          "text": "pack 0. 40"
        }
      },
      {
        "box": {
          "id": "obj-63",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1240.0,
            445.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-64",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            495.0,
            60.0,
            22.0
          ],
          "text": "noise~"
        }
      },
      {
        "box": {
          "id": "obj-65",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            95.0,
            495.0,
            65.0,
            22.0
          ],
          "text": "cycle~"
        }
      },
      {
        "box": {
          "id": "obj-66",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            170.0,
            495.0,
            75.0,
            22.0
          ],
          "text": "*~ 0.35"
        }
      },
      {
        "box": {
          "id": "obj-67",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            255.0,
            495.0,
            75.0,
            22.0
          ],
          "text": "+~ 0.65"
        }
      },
      {
        "box": {
          "id": "obj-68",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            340.0,
            495.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-69",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            550.0,
            115.0,
            22.0
          ],
          "text": "svf~ 650 0.58"
        }
      },
      {
        "box": {
          "id": "obj-70",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            215.0,
            550.0,
            125.0,
            22.0
          ],
          "text": "svf~ 1000 0.45"
        }
      },
      {
        "box": {
          "id": "obj-71",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            590.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-72",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            215.0,
            590.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-73",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            405.0,
            495.0,
            55.0,
            22.0
          ],
          "text": "pink~"
        }
      },
      {
        "box": {
          "id": "obj-74",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            405.0,
            535.0,
            110.0,
            22.0
          ],
          "text": "svf~ 70 0.65"
        }
      },
      {
        "box": {
          "id": "obj-75",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            405.0,
            575.0,
            130.0,
            22.0
          ],
          "text": "lores~ 900 0.25"
        }
      },
      {
        "box": {
          "id": "obj-76",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            405.0,
            615.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-77",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            635.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-78",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            85.0,
            635.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "bgmode": 0,
          "border": 0,
          "clickthrough": 0,
          "embed": 1,
          "enablehscroll": 0,
          "enablevscroll": 0,
          "id": "obj-79",
          "lockeddragscroll": 0,
          "maxclass": "bpatcher",
          "numinlets": 5,
          "numoutlets": 1,
          "offset": [
            0.0,
            0.0
          ],
          "outlettype": [
            "signal"
          ],
          "patcher": {
            "appversion": {
              "architecture": "x64",
              "major": 8,
              "minor": 0,
              "modernui": 1,
              "revision": 0
            },
            "bgcolor": [
              1.0,
              1.0,
              1.0,
              0.0
            ],
            "bglocked": 0,
            "bottomtoolbarpinned": 0,
            "boxanimatetime": 200,
            "boxes": [
              {
                "box": {
                  "id": "obj-3",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    48.0,
                    89.0,
                    295.0,
                    18.0
                  ],
                  "text": "## Two pole multi-mode filter with graphic display ## "
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-102",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    1699.439941,
                    588.822571,
                    55.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    371.67645263671875,
                    0.0,
                    55.0,
                    17.0
                  ],
                  "text": "Res (0-5v)",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "textjustification": 2
                }
              },
              {
                "box": {
                  "id": "obj-101",
                  "linecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.32
                  ],
                  "maxclass": "live.line",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    23.72583,
                    42.529999,
                    5.0,
                    100.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    238.00209045410156,
                    65.71651458740234,
                    12.437604904174805,
                    7.793193817138672
                  ],
                  "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
                  "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-100",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    878.439941,
                    1221.076904,
                    83.0,
                    20.0
                  ],
                  "text": "snapshot~ 10"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-99",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    627.033691,
                    1022.23761,
                    56.0,
                    20.0
                  ],
                  "text": "clip~ 0 1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-98",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    627.033691,
                    968.23761,
                    118.40625,
                    20.0
                  ],
                  "text": "+~"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-97",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1699.439941,
                    726.314514,
                    56.0,
                    20.0
                  ],
                  "text": "clip~ 0 5"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-96",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1699.439941,
                    819.344482,
                    42.0,
                    20.0
                  ],
                  "text": "*~ 0.2"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-79",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1699.439941,
                    778.476807,
                    140.406006,
                    20.0
                  ],
                  "text": "*~"
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-80",
                  "index": 5,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    1699.439941,
                    629.053833,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-85",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1820.845947,
                    695.87915,
                    45.0,
                    21.0
                  ],
                  "text": "sig~ 2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-93",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1820.845947,
                    738.820435,
                    81.0,
                    21.0
                  ],
                  "text": "pow~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-94",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    1882.845947,
                    704.637573,
                    37.0,
                    20.0
                  ],
                  "text": "* 0.01"
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "appearance": 1,
                  "id": "obj-95",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    1882.845947,
                    638.053833,
                    47.0,
                    36.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    247.64053344726562,
                    41.83863830566406,
                    47.0,
                    36.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_longname": "ResCV",
                      "parameter_mmax": 100.0,
                      "parameter_shortname": "CV",
                      "parameter_type": 0,
                      "parameter_unitstyle": 5
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "ResCV",
                  "hint": "ResCV | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "ResCV | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-1",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    490.981201,
                    231.822601,
                    47.0,
                    20.0
                  ],
                  "text": "ftom 0."
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-5",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    433.439941,
                    231.822601,
                    34.0,
                    20.0
                  ],
                  "text": "+ 60"
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.4
                  ],
                  "annotation": "Freq | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "bordercolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.2
                  ],
                  "focusbordercolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.2
                  ],
                  "hidden": 1,
                  "id": "obj-20",
                  "maxclass": "live.dial",
                  "needlecolor": [
                    0.752941,
                    0.784314,
                    0.839216,
                    1.0
                  ],
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    490.981201,
                    165.822601,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    2.0,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "prototypename": "freq",
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_exponent": 4.0,
                      "parameter_initial": [
                        3400.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "Freq",
                      "parameter_mmax": 20000.0,
                      "parameter_shortname": "Freq",
                      "parameter_speedlim": 0.0,
                      "parameter_type": 0,
                      "parameter_unitstyle": 3
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "Freq",
                  "hint": "Freq | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-86",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "patcher": {
                    "appversion": {
                      "architecture": "x64",
                      "major": 8,
                      "minor": 0,
                      "modernui": 1,
                      "revision": 0
                    },
                    "bgfillcolor_color": [
                      0.290196,
                      0.309804,
                      0.301961,
                      1.0
                    ],
                    "bgfillcolor_color1": [
                      0.435294,
                      0.462745,
                      0.498039,
                      1.0
                    ],
                    "bgfillcolor_color2": [
                      0.290196,
                      0.309804,
                      0.301961,
                      1.0
                    ],
                    "bgfillcolor_type": "gradient",
                    "bglocked": 0,
                    "bottomtoolbarpinned": 0,
                    "boxanimatetime": 200,
                    "boxes": [
                      {
                        "box": {
                          "id": "obj-5",
                          "maxclass": "toggle",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            256.0,
                            128.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-6",
                          "maxclass": "message",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            ""
                          ],
                          "patching_rect": [
                            256.0,
                            160.0,
                            57.0,
                            16.0
                          ],
                          "text": "hidden $1"
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-4",
                          "maxclass": "newobj",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "patching_rect": [
                            96.0,
                            88.0,
                            32.5,
                            18.0
                          ],
                          "text": "== 0"
                        }
                      },
                      {
                        "box": {
                          "id": "obj-9",
                          "maxclass": "toggle",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            96.0,
                            112.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-3",
                          "maxclass": "message",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            ""
                          ],
                          "patching_rect": [
                            96.0,
                            160.0,
                            57.0,
                            16.0
                          ],
                          "text": "hidden $1"
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-2",
                          "maxclass": "comment",
                          "numinlets": 1,
                          "numoutlets": 0,
                          "patching_rect": [
                            40.0,
                            15.0,
                            63.0,
                            18.0
                          ],
                          "text": "Time mode"
                        }
                      },
                      {
                        "box": {
                          "fontname": "Arial",
                          "fontsize": 10.0,
                          "id": "obj-7",
                          "maxclass": "comment",
                          "numinlets": 1,
                          "numoutlets": 0,
                          "patching_rect": [
                            56.0,
                            40.0,
                            24.0,
                            18.0
                          ],
                          "text": "1/0"
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-14",
                          "maxclass": "newobj",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "patching_rect": [
                            176.0,
                            64.0,
                            32.5,
                            18.0
                          ],
                          "text": "== 0"
                        }
                      },
                      {
                        "box": {
                          "comment": "",
                          "id": "obj-26",
                          "index": 2,
                          "maxclass": "outlet",
                          "numinlets": 1,
                          "numoutlets": 0,
                          "patching_rect": [
                            176.0,
                            232.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-29",
                          "maxclass": "message",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            ""
                          ],
                          "patching_rect": [
                            200.0,
                            160.0,
                            53.0,
                            16.0
                          ],
                          "text": "active $1"
                        }
                      },
                      {
                        "box": {
                          "id": "obj-30",
                          "maxclass": "button",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "bang"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            176.0,
                            160.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-33",
                          "maxclass": "newobj",
                          "numinlets": 2,
                          "numoutlets": 2,
                          "outlettype": [
                            "bang",
                            ""
                          ],
                          "patching_rect": [
                            176.0,
                            120.0,
                            47.0,
                            18.0
                          ],
                          "text": "select 1"
                        }
                      },
                      {
                        "box": {
                          "id": "obj-36",
                          "maxclass": "toggle",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            176.0,
                            88.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "comment": "",
                          "id": "obj-25",
                          "index": 1,
                          "maxclass": "outlet",
                          "numinlets": 1,
                          "numoutlets": 0,
                          "patching_rect": [
                            16.0,
                            232.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-24",
                          "maxclass": "message",
                          "numinlets": 2,
                          "numoutlets": 1,
                          "outlettype": [
                            ""
                          ],
                          "patching_rect": [
                            40.0,
                            160.0,
                            53.0,
                            16.0
                          ],
                          "text": "active $1"
                        }
                      },
                      {
                        "box": {
                          "id": "obj-21",
                          "maxclass": "button",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "bang"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            16.0,
                            160.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-19",
                          "maxclass": "newobj",
                          "numinlets": 2,
                          "numoutlets": 2,
                          "outlettype": [
                            "bang",
                            ""
                          ],
                          "patching_rect": [
                            16.0,
                            120.0,
                            47.0,
                            18.0
                          ],
                          "text": "select 1"
                        }
                      },
                      {
                        "box": {
                          "id": "obj-18",
                          "maxclass": "toggle",
                          "numinlets": 1,
                          "numoutlets": 1,
                          "outlettype": [
                            "int"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            16.0,
                            80.0,
                            18.0,
                            18.0
                          ]
                        }
                      },
                      {
                        "box": {
                          "fontname": "Ableton Sans Bold Regular",
                          "fontsize": 10.0,
                          "id": "obj-15",
                          "maxclass": "number",
                          "maximum": 1,
                          "minimum": 0,
                          "numinlets": 1,
                          "numoutlets": 2,
                          "outlettype": [
                            "",
                            "bang"
                          ],
                          "parameter_enable": 0,
                          "patching_rect": [
                            16.0,
                            39.0,
                            40.0,
                            18.0
                          ],
                          "prototypename": "Live",
                          "triscale": 0.75
                        }
                      },
                      {
                        "box": {
                          "comment": "",
                          "id": "obj-17",
                          "index": 1,
                          "maxclass": "inlet",
                          "numinlets": 0,
                          "numoutlets": 1,
                          "outlettype": [
                            ""
                          ],
                          "patching_rect": [
                            16.0,
                            8.0,
                            18.0,
                            18.0
                          ]
                        }
                      }
                    ],
                    "classnamespace": "box",
                    "default_fontface": 0,
                    "default_fontname": "Ableton Sans Bold Regular",
                    "default_fontsize": 10.0,
                    "description": "",
                    "devicewidth": 0.0,
                    "digest": "",
                    "enablehscroll": 1,
                    "enablevscroll": 1,
                    "fileversion": 1,
                    "gridonopen": 2,
                    "gridsize": [
                      8.0,
                      8.0
                    ],
                    "gridsnaponopen": 1,
                    "lefttoolbarpinned": 0,
                    "lines": [
                      {
                        "patchline": {
                          "destination": [
                            "obj-36",
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
                            "obj-14",
                            0
                          ],
                          "order": 1,
                          "source": [
                            "obj-15",
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
                          "order": 3,
                          "source": [
                            "obj-15",
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
                          "order": 2,
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
                          "midpoints": [
                            25.5,
                            58.0,
                            265.5,
                            58.0
                          ],
                          "order": 0,
                          "source": [
                            "obj-15",
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
                            "obj-17",
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
                          "order": 1,
                          "source": [
                            "obj-18",
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
                          "order": 0,
                          "source": [
                            "obj-18",
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
                            "obj-19",
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
                            "obj-24",
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
                            "obj-29",
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
                            "obj-3",
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
                            "obj-30",
                            0
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
                            "obj-33",
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
                          "order": 0,
                          "source": [
                            "obj-36",
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
                          "order": 1,
                          "source": [
                            "obj-36",
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
                            "obj-4",
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
                            "obj-26",
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
                            "obj-3",
                            0
                          ],
                          "source": [
                            "obj-9",
                            0
                          ]
                        }
                      }
                    ],
                    "objectsnaponopen": 1,
                    "openinpresentation": 0,
                    "rect": [
                      1560.0,
                      203.0,
                      440.0,
                      307.0
                    ],
                    "righttoolbarpinned": 0,
                    "statusbarvisible": 1,
                    "style": "",
                    "subpatcher_template": "",
                    "tags": "",
                    "tallnewobj": 0,
                    "toolbars_unpinned_last_save": 0,
                    "toolbarvisible": 1,
                    "toptoolbarpinned": 0
                  },
                  "patching_rect": [
                    433.439941,
                    122.822601,
                    76.541275,
                    20.0
                  ],
                  "saved_object_attributes": {
                    "description": "",
                    "digest": "",
                    "fontname": "Ableton Sans Bold Regular",
                    "fontsize": 10.0,
                    "globalpatchername": "",
                    "tags": ""
                  },
                  "text": "p TimeMode"
                }
              },
              {
                "box": {
                  "activebgcolor": [
                    0.917647,
                    0.94902,
                    0.054902,
                    0.0
                  ],
                  "activebgoncolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activetextcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activetextoncolor": [
                    0.137255,
                    0.145098,
                    0.160784,
                    1.0
                  ],
                  "annotation": "FreqMode | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "automation": "Freq",
                  "automationon": "Semitone",
                  "bgcolor": [
                    0.6,
                    0.6,
                    0.6,
                    0.0
                  ],
                  "bordercolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "focusbordercolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "hint": "FreqMode | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "id": "obj-22",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    433.439941,
                    76.822601,
                    35.0,
                    19.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    43.0,
                    41.83863830566406,
                    33.0,
                    15.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_enum": [
                        "Freq",
                        "Semitone"
                      ],
                      "parameter_initial": [
                        1
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "TimeMode",
                      "parameter_mmax": 1.0,
                      "parameter_order": 1,
                      "parameter_shortname": "TimeMode",
                      "parameter_speedlim": 0.0,
                      "parameter_type": 2
                    }
                  },
                  "text": "Freq",
                  "textcolor": [
                    0.556863,
                    0.556863,
                    0.556863,
                    1.0
                  ],
                  "texton": "Semi",
                  "varname": "FreqMode"
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.4
                  ],
                  "annotation": "Offset[2] | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "bordercolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.2
                  ],
                  "focusbordercolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.2
                  ],
                  "id": "obj-23",
                  "maxclass": "live.dial",
                  "needlecolor": [
                    0.752941,
                    0.784314,
                    0.839216,
                    1.0
                  ],
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    433.439941,
                    165.822601,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    2.0,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "prototypename": "freq",
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_initial": [
                        0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "Offset",
                      "parameter_mmax": 64.0,
                      "parameter_mmin": -64.0,
                      "parameter_shortname": "Offset",
                      "parameter_speedlim": 0.0,
                      "parameter_type": 0,
                      "parameter_unitstyle": 1
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "Offset[2]",
                  "hint": "Offset[2] | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "bubble": 1,
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-62",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    704.439941,
                    398.961334,
                    69.0,
                    22.0
                  ],
                  "text": "0v = C3"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-53",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    654.033691,
                    253.039948,
                    140.406006,
                    20.0
                  ],
                  "text": "*~"
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-56",
                  "index": 2,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    654.033691,
                    204.0383,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-57",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    775.439758,
                    170.44223,
                    45.0,
                    21.0
                  ],
                  "text": "sig~ 2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-59",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    775.439758,
                    213.383514,
                    81.0,
                    21.0
                  ],
                  "text": "pow~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-61",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    837.439758,
                    179.200653,
                    37.0,
                    20.0
                  ],
                  "text": "* 0.01"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-52",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    866.439941,
                    333.461334,
                    140.406006,
                    20.0
                  ],
                  "text": "*~"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-27",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1251.439941,
                    446.970123,
                    42.0,
                    20.0
                  ],
                  "text": "*~ 0.2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-33",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1189.439941,
                    457.112579,
                    45.0,
                    21.0
                  ],
                  "text": "sig~ 2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-47",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1189.439941,
                    500.053864,
                    81.0,
                    21.0
                  ],
                  "text": "pow~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-48",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1251.439941,
                    415.970123,
                    140.406006,
                    20.0
                  ],
                  "text": "*~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-50",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    1372.845947,
                    374.845947,
                    37.0,
                    20.0
                  ],
                  "text": "* 0.01"
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-4",
                  "index": 3,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    866.439941,
                    284.459686,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-7",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    987.846008,
                    250.863617,
                    45.0,
                    21.0
                  ],
                  "text": "sig~ 2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-16",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    987.846008,
                    293.804901,
                    81.0,
                    21.0
                  ],
                  "text": "pow~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 10.0,
                  "id": "obj-24",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    1049.845947,
                    259.62204,
                    37.0,
                    20.0
                  ],
                  "text": "* 0.01"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-49",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    878.439941,
                    1258.0,
                    35.0,
                    20.0
                  ],
                  "text": "* 25."
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-45",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    781.011353,
                    1258.0,
                    83.0,
                    20.0
                  ],
                  "text": "snapshot~ 10"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-44",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    618.533691,
                    1251.076904,
                    60.0,
                    20.0
                  ],
                  "text": "bandstop"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-31",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    574.008423,
                    1223.076904,
                    63.0,
                    20.0
                  ],
                  "text": "bandpass"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-30",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    531.008423,
                    1243.076904,
                    59.0,
                    20.0
                  ],
                  "text": "highpass"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-29",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    488.0,
                    1223.076904,
                    54.0,
                    20.0
                  ],
                  "text": "lowpass"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-26",
                  "maxclass": "newobj",
                  "numinlets": 5,
                  "numoutlets": 5,
                  "outlettype": [
                    "bang",
                    "bang",
                    "bang",
                    "bang",
                    ""
                  ],
                  "patching_rect": [
                    488.0,
                    1188.0,
                    191.033691,
                    20.0
                  ],
                  "text": "sel 1 2 3 4"
                }
              },
              {
                "box": {
                  "autoout": 1,
                  "bgcolor": [
                    0.0,
                    0.0,
                    0.0,
                    1.0
                  ],
                  "curvecolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "domain": [
                    0.0,
                    22050.0
                  ],
                  "fontface": 1,
                  "fontname": "Arial",
                  "hcurvecolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "id": "obj-36",
                  "ignoreclick": 1,
                  "linmarkers": [
                    0.0,
                    11025.0,
                    16537.5
                  ],
                  "logmarkers": [
                    0.0,
                    100.0,
                    1000.0,
                    10000.0
                  ],
                  "markercolor": [
                    0.509804,
                    0.509804,
                    0.509804,
                    0.0
                  ],
                  "maxclass": "filtergraph~",
                  "nfilters": 1,
                  "numinlets": 8,
                  "numoutlets": 7,
                  "outlettype": [
                    "list",
                    "float",
                    "float",
                    "float",
                    "float",
                    "list",
                    "int"
                  ],
                  "parameter_enable": 0,
                  "patching_rect": [
                    537.439941,
                    1307.237549,
                    360.0,
                    155.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    348.9093017578125,
                    41.83863830566406,
                    73.76712036132812,
                    51.16136169433594
                  ],
                  "setfilter": [
                    0,
                    1,
                    0,
                    0,
                    0,
                    261.6255798339844,
                    1.0,
                    0.5,
                    9.9999997474e-05,
                    22050.0,
                    9.9999997474e-05,
                    16.0,
                    0.5,
                    25.0
                  ],
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.0
                  ],
                  "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
                  "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-74",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    866.439941,
                    259.62204,
                    63.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    184.45094299316406,
                    0.0,
                    63.0,
                    17.0
                  ],
                  "text": "CV2 (1v/oct)",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "textjustification": 1
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-2",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    866.439941,
                    451.461334,
                    38.0,
                    20.0
                  ],
                  "text": "-~ 60"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-46",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    654.033691,
                    398.961334,
                    38.0,
                    20.0
                  ],
                  "text": "-~ 60"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-92",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    433.439941,
                    551.893127,
                    775.0,
                    20.0
                  ],
                  "text": "+~"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-91",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    433.439941,
                    500.053864,
                    452.0,
                    20.0
                  ],
                  "text": "+~"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-90",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    433.439941,
                    449.053833,
                    239.59375,
                    20.0
                  ],
                  "text": "+~"
                }
              },
              {
                "box": {
                  "bubble": 1,
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-89",
                  "linecount": 2,
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    704.439941,
                    360.461334,
                    109.0,
                    34.0
                  ],
                  "text": "12 semitones in an oct"
                }
              },
              {
                "box": {
                  "bubble": 1,
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-88",
                  "linecount": 2,
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    704.439941,
                    314.461334,
                    109.0,
                    34.0
                  ],
                  "text": "add 5v to bring to 0-10v range"
                }
              },
              {
                "box": {
                  "bubble": 1,
                  "bubbleside": 3,
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-87",
                  "linecount": 4,
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    1132.439941,
                    320.768982,
                    102.0,
                    58.0
                  ],
                  "text": "convert 0-5v to 0-120 range of semitones"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-84",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1251.439941,
                    342.768982,
                    39.0,
                    20.0
                  ],
                  "text": "*~ 24"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-83",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    1251.439941,
                    284.459686,
                    56.0,
                    20.0
                  ],
                  "text": "clip~ 0 5"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-81",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    866.439941,
                    422.12204,
                    39.0,
                    20.0
                  ],
                  "text": "*~ 12"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-82",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    866.439941,
                    384.12204,
                    35.0,
                    20.0
                  ],
                  "text": "+~ 5"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-78",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    654.033691,
                    360.961334,
                    39.0,
                    20.0
                  ],
                  "text": "*~ 12"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-76",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    654.033691,
                    322.961334,
                    35.0,
                    20.0
                  ],
                  "text": "+~ 5"
                }
              },
              {
                "box": {
                  "annotation": "1v/oct",
                  "comment": "",
                  "id": "obj-60",
                  "index": 4,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    1251.439941,
                    240.959686,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "id": "obj-63",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    1372.845947,
                    293.804901,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    159.64053344726562,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_longname": "CV3",
                      "parameter_mmax": 100.0,
                      "parameter_shortname": "CV3",
                      "parameter_type": 0,
                      "parameter_unitstyle": 5
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "CV3",
                  "hint": "CV3 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "CV3 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-58",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    433.439941,
                    661.053833,
                    82.0,
                    20.0
                  ],
                  "text": "clip~ 0 22000"
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "id": "obj-54",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    837.439758,
                    106.018127,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    71.64053344726562,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_longname": "CV1",
                      "parameter_mmax": 100.0,
                      "parameter_shortname": "CV1",
                      "parameter_type": 0,
                      "parameter_unitstyle": 5
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "CV1",
                  "hint": "CV1 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "CV1 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "id": "obj-51",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    1049.845947,
                    193.0383,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    115.64053344726562,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_longname": "CV2",
                      "parameter_mmax": 100.0,
                      "parameter_shortname": "CV2",
                      "parameter_type": 0,
                      "parameter_unitstyle": 5
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "CV2",
                  "hint": "CV2 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "CV2 | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-69",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    433.439941,
                    354.961334,
                    43.0,
                    21.0
                  ],
                  "text": "$1 20"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-70",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 2,
                  "outlettype": [
                    "signal",
                    "bang"
                  ],
                  "patching_rect": [
                    433.439941,
                    390.961334,
                    53.0,
                    21.0
                  ],
                  "text": "line~ 0."
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-71",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    433.439941,
                    614.893127,
                    41.0,
                    20.0
                  ],
                  "text": "mtof~"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-43",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    109.875977,
                    1072.076904,
                    32.5,
                    20.0
                  ],
                  "text": "+ 1"
                }
              },
              {
                "box": {
                  "activebgoncolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "id": "obj-38",
                  "maxclass": "live.tab",
                  "num_lines_patching": 4,
                  "num_lines_presentation": 4,
                  "numinlets": 1,
                  "numoutlets": 3,
                  "outlettype": [
                    "",
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    109.875977,
                    941.23761,
                    55.25,
                    101.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    297.6405334472656,
                    37.83863830566406,
                    49.08415985107422,
                    55.16136169433594
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_enum": [
                        "LPF",
                        "HPF",
                        "BPF",
                        "Notch"
                      ],
                      "parameter_initial": [
                        0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "FilterType",
                      "parameter_shortname": "FilterType",
                      "parameter_type": 2,
                      "parameter_unitstyle": 0
                    }
                  },
                  "varname": "FilterType",
                  "hint": "FilterType | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "FilterType | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-28",
                  "maxclass": "newobj",
                  "numinlets": 5,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    109.875977,
                    1118.076904,
                    536.157715,
                    20.0
                  ],
                  "text": "selector~ 4 1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-12",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 4,
                  "outlettype": [
                    "signal",
                    "signal",
                    "signal",
                    "signal"
                  ],
                  "patching_rect": [
                    239.846191,
                    1079.076904,
                    406.1875,
                    20.0
                  ],
                  "text": "svf~"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-42",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    1251.439941,
                    213.383514,
                    55.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    287.6764221191406,
                    0.0,
                    55.0,
                    17.0
                  ],
                  "text": "CV3 (0-5v)",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "textjustification": 1
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-41",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    654.033691,
                    179.200653,
                    63.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    81.22547149658203,
                    0.0,
                    63.0,
                    17.0
                  ],
                  "text": "CV1 (1v/oct)",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "textjustification": 1
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-10",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    54.875977,
                    1196.076904,
                    32.5,
                    20.0
                  ],
                  "text": "+ 1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-9",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    54.875977,
                    1241.076904,
                    129.0,
                    20.0
                  ],
                  "text": "selector~ 2 1"
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-6",
                  "index": 1,
                  "maxclass": "outlet",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    54.875977,
                    1289.076904,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-37",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "float"
                  ],
                  "patching_rect": [
                    627.033691,
                    850.005188,
                    42.0,
                    20.0
                  ],
                  "text": "* 0.01"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-34",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    627.033691,
                    888.505188,
                    43.0,
                    21.0
                  ],
                  "text": "$1 20"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-35",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "bang"
                  ],
                  "patching_rect": [
                    627.033691,
                    923.344482,
                    46.0,
                    21.0
                  ],
                  "text": "line 0."
                }
              },
              {
                "box": {
                  "activedialcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activefgdialcolor": [
                    0.65098,
                    0.666667,
                    0.662745,
                    1.0
                  ],
                  "activeneedlecolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "id": "obj-11",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    627.033691,
                    785.005188,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    203.64053344726562,
                    41.83863830566406,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_exponent": 2.0,
                      "parameter_initial": [
                        0.45
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "Res",
                      "parameter_mmax": 100.0,
                      "parameter_shortname": "Res",
                      "parameter_type": 0,
                      "parameter_unitstyle": 5
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.6
                  ],
                  "varname": "Res",
                  "hint": "Res | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "Res | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-17",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    109.875977,
                    1196.076904,
                    36.0,
                    20.0
                  ],
                  "text": "*~ 5."
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-32",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    239.846191,
                    1022.23761,
                    42.0,
                    20.0
                  ],
                  "text": "*~ 0.2"
                }
              },
              {
                "box": {
                  "activebgcolor": [
                    0.572549,
                    0.615686,
                    0.658824,
                    0.0
                  ],
                  "activebgoncolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "activetextcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.57
                  ],
                  "activetextoncolor": [
                    0.0,
                    0.019608,
                    0.078431,
                    1.0
                  ],
                  "bgcolor": [
                    0.101961,
                    0.101961,
                    0.101961,
                    0.78
                  ],
                  "bordercolor": [
                    0.0,
                    0.019608,
                    0.078431,
                    0.37
                  ],
                  "id": "obj-55",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    54.875977,
                    1154.576904,
                    43.0,
                    19.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    347.9093017578125,
                    19.0,
                    73.76713562011719,
                    17.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        1
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "power",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "power",
                      "parameter_type": 2
                    }
                  },
                  "text": "bypass",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "bypass",
                  "varname": "power[1]",
                  "hint": "power[1] | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。",
                  "annotation": "power[1] | 范围 见标注…见标注。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。"
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-39",
                  "index": 1,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    164.875977,
                    863.73761,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-40",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 4,
                  "outlettype": [
                    "",
                    "",
                    "",
                    ""
                  ],
                  "patching_rect": [
                    48.0,
                    122.822601,
                    59.5,
                    20.0
                  ],
                  "restore": {
                    "CV1": [
                      0.0
                    ],
                    "CV2": [
                      0.0
                    ],
                    "CV3": [
                      0.0
                    ],
                    "FilterType": [
                      0
                    ],
                    "Freq": [
                      3400.0
                    ],
                    "FreqMode": [
                      1.0
                    ],
                    "Offset[2]": [
                      0.0
                    ],
                    "Res": [
                      0.45
                    ],
                    "ResCV": [
                      0.0
                    ],
                    "power[1]": [
                      1
                    ]
                  },
                  "text": "autopattr",
                  "varname": "u396008153"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-8",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    94.205505,
                    1293.076904,
                    40.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    2.0,
                    97.0,
                    40.0,
                    17.0
                  ],
                  "text": "Output",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-19",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    118.500977,
                    867.73761,
                    38.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    2.0,
                    0.0,
                    38.0,
                    17.0
                  ],
                  "text": "Signal",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-13",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    48.0,
                    65.0,
                    77.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    2.0,
                    19.0,
                    77.0,
                    17.0
                  ],
                  "text": "MMF (12dB/oct)",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ]
                }
              },
              {
                "box": {
                  "angle": 0.0,
                  "background": 1,
                  "bgcolor": [
                    0.137255,
                    0.145098,
                    0.160784,
                    0.65
                  ],
                  "id": "obj-130",
                  "maxclass": "panel",
                  "mode": 0,
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    48.0,
                    42.529999,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    37.0,
                    472.0,
                    60.338157653808594
                  ],
                  "proportion": 0.39,
                  "rounded": 0
                }
              },
              {
                "box": {
                  "angle": 0.0,
                  "background": 1,
                  "bgcolor": [
                    0.367404,
                    0.389405,
                    0.430238,
                    1.0
                  ],
                  "id": "obj-131",
                  "maxclass": "panel",
                  "mode": 0,
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    96.983887,
                    42.529999,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    17.0,
                    472.0,
                    80.3381576538086
                  ],
                  "proportion": 0.39,
                  "rounded": 0
                }
              },
              {
                "box": {
                  "angle": 0.0,
                  "background": 1,
                  "bgcolor": [
                    0.0,
                    0.0,
                    0.0,
                    1.0
                  ],
                  "id": "obj-135",
                  "maxclass": "panel",
                  "mode": 0,
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    144.205505,
                    42.529999,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    0.0,
                    472.0,
                    133.0
                  ],
                  "proportion": 0.39,
                  "rounded": 0
                }
              }
            ],
            "classnamespace": "box",
            "default_fontface": 0,
            "default_fontname": "Arial",
            "default_fontsize": 12.0,
            "description": "",
            "devicewidth": 0.0,
            "digest": "",
            "enablehscroll": 1,
            "enablevscroll": 1,
            "fileversion": 1,
            "gridonopen": 1,
            "gridsize": [
              15.0,
              15.0
            ],
            "gridsnaponopen": 1,
            "lefttoolbarpinned": 0,
            "lines": [
              {
                "patchline": {
                  "destination": [
                    "obj-69",
                    0
                  ],
                  "source": [
                    "obj-1",
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
                    "obj-10",
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
                    "obj-100",
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
                    "obj-11",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-28",
                    4
                  ],
                  "source": [
                    "obj-12",
                    3
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-28",
                    3
                  ],
                  "source": [
                    "obj-12",
                    2
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-28",
                    2
                  ],
                  "source": [
                    "obj-12",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-28",
                    1
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
                    "obj-52",
                    1
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
                    "obj-9",
                    1
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
                    "obj-91",
                    1
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
                    "obj-1",
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
                    "obj-86",
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
                    "obj-5",
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
                    "obj-16",
                    1
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
                    "obj-29",
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
                    "obj-30",
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
                    "obj-31",
                    0
                  ],
                  "source": [
                    "obj-26",
                    2
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
                    "obj-26",
                    3
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
                    "obj-27",
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
                    "obj-28",
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
                    "obj-29",
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
                    "obj-30",
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
                    "obj-31",
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
                    "obj-32",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "color": [
                    0.501961,
                    0.501961,
                    0.501961,
                    0.901961
                  ],
                  "destination": [
                    "obj-47",
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
                    "obj-98",
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
                    "obj-34",
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
                    "obj-43",
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
                    "obj-32",
                    0
                  ],
                  "order": 0,
                  "source": [
                    "obj-39",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-9",
                    2
                  ],
                  "order": 1,
                  "source": [
                    "obj-39",
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
                    "obj-4",
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
                  "order": 0,
                  "source": [
                    "obj-43",
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
                  "order": 1,
                  "source": [
                    "obj-43",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-36",
                    1
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
                    "obj-36",
                    5
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
                    "obj-90",
                    1
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
                    "obj-92",
                    1
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
                    "obj-27",
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
                    "obj-36",
                    7
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
                    "obj-69",
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
                    "obj-48",
                    1
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
                    "obj-24",
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
                    "obj-82",
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
                    "obj-76",
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
                    "obj-61",
                    0
                  ],
                  "source": [
                    "obj-54",
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
                    "obj-55",
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
                    "obj-56",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "color": [
                    0.501961,
                    0.501961,
                    0.501961,
                    0.901961
                  ],
                  "destination": [
                    "obj-59",
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
                    "obj-12",
                    1
                  ],
                  "order": 1,
                  "source": [
                    "obj-58",
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
                  "order": 0,
                  "source": [
                    "obj-58",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-53",
                    1
                  ],
                  "source": [
                    "obj-59",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-83",
                    0
                  ],
                  "source": [
                    "obj-60",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-59",
                    1
                  ],
                  "source": [
                    "obj-61",
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
                    "obj-63",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-70",
                    0
                  ],
                  "source": [
                    "obj-69",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "color": [
                    0.501961,
                    0.501961,
                    0.501961,
                    0.901961
                  ],
                  "destination": [
                    "obj-16",
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
                    "obj-90",
                    0
                  ],
                  "source": [
                    "obj-70",
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
                    "obj-71",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-78",
                    0
                  ],
                  "source": [
                    "obj-76",
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
                    "obj-78",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-96",
                    0
                  ],
                  "source": [
                    "obj-79",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-97",
                    0
                  ],
                  "source": [
                    "obj-80",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-2",
                    0
                  ],
                  "source": [
                    "obj-81",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-81",
                    0
                  ],
                  "source": [
                    "obj-82",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-84",
                    0
                  ],
                  "source": [
                    "obj-83",
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
                    "obj-84",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "color": [
                    0.501961,
                    0.501961,
                    0.501961,
                    0.901961
                  ],
                  "destination": [
                    "obj-93",
                    0
                  ],
                  "source": [
                    "obj-85",
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
                    "obj-86",
                    1
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
                    "obj-86",
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
                    "obj-9",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-91",
                    0
                  ],
                  "source": [
                    "obj-90",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-92",
                    0
                  ],
                  "source": [
                    "obj-91",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-71",
                    0
                  ],
                  "source": [
                    "obj-92",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-79",
                    1
                  ],
                  "source": [
                    "obj-93",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-93",
                    1
                  ],
                  "source": [
                    "obj-94",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-94",
                    0
                  ],
                  "source": [
                    "obj-95",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-98",
                    1
                  ],
                  "midpoints": [
                    1708.939941,
                    903.291016,
                    735.939941,
                    903.291016
                  ],
                  "source": [
                    "obj-96",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-79",
                    0
                  ],
                  "source": [
                    "obj-97",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-99",
                    0
                  ],
                  "source": [
                    "obj-98",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-100",
                    0
                  ],
                  "order": 0,
                  "source": [
                    "obj-99",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-12",
                    2
                  ],
                  "order": 1,
                  "source": [
                    "obj-99",
                    0
                  ]
                }
              }
            ],
            "objectsnaponopen": 1,
            "openinpresentation": 1,
            "rect": [
              98.0,
              297.0,
              886.0,
              699.0
            ],
            "righttoolbarpinned": 0,
            "statusbarvisible": 1,
            "style": "",
            "subpatcher_template": "",
            "tags": "",
            "tallnewobj": 0,
            "toolbars_unpinned_last_save": 0,
            "toolbarvisible": 1,
            "toptoolbarpinned": 0
          },
          "patching_rect": [
            20.0,
            685.0,
            427.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            295,
            427.0,
            116.0
          ],
          "varname": "Noise_Ceiling",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-80",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            370.0,
            685.0,
            800.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            365,
            302,
            815,
            22
          ],
          "text": "BEAP ceiling: LP / 1800–4500 Hz / restrained resonance (0.3–0.8)."
        }
      },
      {
        "box": {
          "id": "obj-81",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            1400.0,
            540.0,
            125.0,
            22.0
          ],
          "text": "svf~ 250 0.65"
        }
      },
      {
        "box": {
          "id": "obj-82",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1400.0,
            500.0,
            80.0,
            22.0
          ],
          "text": "*~ 0.55"
        }
      },
      {
        "box": {
          "id": "obj-83",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1400.0,
            590.0,
            45.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-84",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1400.0,
            635.0,
            45.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-85",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            540.0,
            705.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-86",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            495.0,
            60.0,
            22.0
          ],
          "text": "noise~"
        }
      },
      {
        "box": {
          "id": "obj-87",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            685.0,
            495.0,
            75.0,
            22.0
          ],
          "text": "*~ 0.25"
        }
      },
      {
        "box": {
          "id": "obj-88",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            770.0,
            495.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-89",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            610.0,
            535.0,
            120.0,
            22.0
          ],
          "text": "svf~ 400 0.65"
        }
      },
      {
        "box": {
          "id": "obj-90",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            575.0,
            130.0,
            22.0
          ],
          "text": "lores~ 2300 0.2"
        }
      },
      {
        "box": {
          "id": "obj-91",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            615.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-92",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            660.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-93",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            610.0,
            715.0,
            110.0,
            22.0
          ],
          "text": "svf~ 28 0.7"
        }
      },
      {
        "box": {
          "id": "obj-94",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            755.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-95",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            610.0,
            810.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-96",
          "maxclass": "meter~",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            670.0,
            785.0,
            150.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            370,
            365,
            250,
            20
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-97",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            915.0,
            495.0,
            60.0,
            22.0
          ],
          "text": "noise~"
        }
      },
      {
        "box": {
          "id": "obj-98",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            990.0,
            495.0,
            75.0,
            22.0
          ],
          "text": "*~ 0.25"
        }
      },
      {
        "box": {
          "id": "obj-99",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1075.0,
            495.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-100",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            915.0,
            535.0,
            120.0,
            22.0
          ],
          "text": "svf~ 400 0.65"
        }
      },
      {
        "box": {
          "id": "obj-101",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            915.0,
            575.0,
            130.0,
            22.0
          ],
          "text": "lores~ 2300 0.2"
        }
      },
      {
        "box": {
          "id": "obj-102",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            915.0,
            615.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-103",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            915.0,
            660.0,
            40.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-104",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            915.0,
            715.0,
            110.0,
            22.0
          ],
          "text": "svf~ 28 0.7"
        }
      },
      {
        "box": {
          "id": "obj-105",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            915.0,
            755.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-106",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            915.0,
            810.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-107",
          "maxclass": "meter~",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            975.0,
            785.0,
            150.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            660,
            365,
            250,
            20
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-108",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            855.0,
            180.0,
            22.0
          ],
          "text": "r open.ferrari.noise"
        }
      },
      {
        "box": {
          "id": "obj-109",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            210.0,
            855.0,
            55.0,
            22.0
          ],
          "text": "front"
        }
      },
      {
        "box": {
          "id": "obj-110",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            275.0,
            855.0,
            90.0,
            22.0
          ],
          "text": "thispatcher"
        }
      },
      {
        "box": {
          "id": "obj-111",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            385.0,
            855.0,
            24.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            960,
            355,
            24,
            24
          ],
          "hint": "0普通混合，1独听此声层；不写入定稿预设，避免下次开机误静音其他层。",
          "annotation": "0普通混合，1独听此声层；不写入定稿预设，避免下次开机误静音其他层。"
        }
      },
      {
        "box": {
          "id": "obj-112",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            420.0,
            855.0,
            105.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            990,
            356,
            130,
            22
          ],
          "text": "Noise Solo"
        }
      },
      {
        "box": {
          "id": "obj-113",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            385.0,
            895.0,
            145.0,
            22.0
          ],
          "text": "prepend noise_solo"
        }
      },
      {
        "box": {
          "id": "obj-114",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            535.0,
            895.0,
            220.0,
            22.0
          ],
          "text": "s vss.runtime.control.ferrari"
        }
      },
      {
        "box": {
          "id": "obj-115",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            720.0,
            895.0,
            100.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-116",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            895.0,
            180.0,
            22.0
          ],
          "text": "autopattr @autorestore 0"
        }
      },
      {
        "box": {
          "id": "obj-117",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 4,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            935.0,
            420.0,
            22.0
          ],
          "text": "pattrstorage noise_ferrari_v2 @autorestore 0 @savemode 0"
        }
      },
      {
        "box": {
          "id": "obj-118",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            455.0,
            935.0,
            335.0,
            22.0
          ],
          "text": "js Patcher:/code/v7_noise_state.js ferrari 2"
        }
      },
      {
        "box": {
          "id": "obj-119",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            365.0,
            975.0,
            155.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            365,
            420,
            155,
            22
          ],
          "text": "Save Noise",
          "hint": "Save Noise：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Save Noise：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-120",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            365.0,
            1010.0,
            65.0,
            22.0
          ],
          "text": "save"
        }
      },
      {
        "box": {
          "id": "obj-121",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            555.0,
            975.0,
            155.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            555,
            420,
            155,
            22
          ],
          "text": "Reload Noise",
          "hint": "Reload Noise：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Reload Noise：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-122",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            555.0,
            1010.0,
            65.0,
            22.0
          ],
          "text": "restore"
        }
      },
      {
        "box": {
          "id": "obj-123",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1070.0,
            895.0,
            80.0,
            22.0
          ],
          "text": "delay 250"
        }
      },
      {
        "box": {
          "id": "obj-124",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            745.0,
            975.0,
            155.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            745,
            420,
            155,
            22
          ],
          "text": "Factory Reset",
          "hint": "Factory Reset：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Factory Reset：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-125",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            745.0,
            1010.0,
            65.0,
            22.0
          ],
          "text": "reset"
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
            "obj-4",
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
            11
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
            "obj-8",
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
            "obj-14",
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
            "obj-12",
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
            "obj-15",
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
            "obj-8",
            1
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
            "obj-17",
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
            "obj-20",
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
            "obj-8",
            2
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
            "obj-24",
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
            "obj-22",
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
            "obj-8",
            3
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
            "obj-29",
            0
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
            "obj-27",
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
            "obj-8",
            4
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
            "obj-34",
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
            "obj-32",
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
            "obj-8",
            5
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
            "obj-37",
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
            "obj-9",
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
            "obj-41",
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
            "obj-41",
            1
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
            "obj-41",
            2
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
            "obj-48",
            0
          ],
          "source": [
            "obj-41",
            3
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
            "obj-50",
            0
          ],
          "source": [
            "obj-41",
            4
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
            "obj-52",
            0
          ],
          "source": [
            "obj-41",
            5
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
            "obj-54",
            0
          ],
          "source": [
            "obj-41",
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
            "obj-54",
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
            "obj-41",
            7
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-57",
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
            "obj-58",
            0
          ],
          "source": [
            "obj-41",
            8
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-59",
            0
          ],
          "source": [
            "obj-58",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-60",
            0
          ],
          "source": [
            "obj-41",
            9
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-61",
            0
          ],
          "source": [
            "obj-60",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-62",
            0
          ],
          "source": [
            "obj-41",
            10
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-63",
            0
          ],
          "source": [
            "obj-62",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-65",
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
            "obj-66",
            0
          ],
          "source": [
            "obj-65",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-67",
            0
          ],
          "source": [
            "obj-66",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-68",
            0
          ],
          "source": [
            "obj-64",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-68",
            1
          ],
          "source": [
            "obj-67",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-69",
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
            "obj-69",
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
            "obj-70",
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
            "obj-70",
            1
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
            "obj-71",
            0
          ],
          "source": [
            "obj-69",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-71",
            1
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
            "obj-72",
            0
          ],
          "source": [
            "obj-70",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-72",
            1
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
            "obj-74",
            0
          ],
          "source": [
            "obj-73",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-75",
            0
          ],
          "source": [
            "obj-74",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-76",
            0
          ],
          "source": [
            "obj-75",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-76",
            1
          ],
          "source": [
            "obj-59",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-77",
            0
          ],
          "source": [
            "obj-71",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-77",
            1
          ],
          "source": [
            "obj-72",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-78",
            0
          ],
          "source": [
            "obj-77",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-78",
            1
          ],
          "source": [
            "obj-76",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-82",
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
            "obj-81",
            1
          ],
          "source": [
            "obj-82",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-81",
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
            "obj-83",
            0
          ],
          "source": [
            "obj-81",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-83",
            1
          ],
          "source": [
            "obj-63",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-84",
            0
          ],
          "source": [
            "obj-78",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-84",
            1
          ],
          "source": [
            "obj-83",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-79",
            0
          ],
          "source": [
            "obj-84",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-85",
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
            "obj-85",
            1
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
            "obj-87",
            0
          ],
          "source": [
            "obj-86",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-88",
            0
          ],
          "source": [
            "obj-64",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-88",
            1
          ],
          "source": [
            "obj-87",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-89",
            0
          ],
          "source": [
            "obj-88",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-90",
            0
          ],
          "source": [
            "obj-89",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-90",
            1
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
            "obj-91",
            0
          ],
          "source": [
            "obj-90",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-91",
            1
          ],
          "source": [
            "obj-61",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-92",
            0
          ],
          "source": [
            "obj-79",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-92",
            1
          ],
          "source": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-93",
            0
          ],
          "source": [
            "obj-92",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-94",
            0
          ],
          "source": [
            "obj-93",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-94",
            1
          ],
          "source": [
            "obj-85",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-95",
            0
          ],
          "source": [
            "obj-94",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-96",
            0
          ],
          "source": [
            "obj-94",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-98",
            0
          ],
          "source": [
            "obj-97",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-99",
            0
          ],
          "source": [
            "obj-64",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-99",
            1
          ],
          "source": [
            "obj-98",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-100",
            0
          ],
          "source": [
            "obj-99",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-101",
            0
          ],
          "source": [
            "obj-100",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-101",
            1
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
            "obj-102",
            0
          ],
          "source": [
            "obj-101",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-102",
            1
          ],
          "source": [
            "obj-61",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-103",
            0
          ],
          "source": [
            "obj-79",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-103",
            1
          ],
          "source": [
            "obj-102",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-104",
            0
          ],
          "source": [
            "obj-103",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-105",
            0
          ],
          "source": [
            "obj-104",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-105",
            1
          ],
          "source": [
            "obj-85",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-106",
            0
          ],
          "source": [
            "obj-105",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-107",
            0
          ],
          "source": [
            "obj-105",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-109",
            0
          ],
          "source": [
            "obj-108",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-109",
            0
          ],
          "source": [
            "obj-8",
            6
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-110",
            0
          ],
          "source": [
            "obj-109",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-115",
            0
          ],
          "source": [
            "obj-8",
            10
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-111",
            0
          ],
          "source": [
            "obj-115",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-113",
            0
          ],
          "source": [
            "obj-111",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-114",
            0
          ],
          "source": [
            "obj-113",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-117",
            0
          ],
          "source": [
            "obj-118",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-120",
            0
          ],
          "source": [
            "obj-8",
            7
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-120",
            0
          ],
          "source": [
            "obj-119",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-118",
            0
          ],
          "source": [
            "obj-120",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-122",
            0
          ],
          "source": [
            "obj-8",
            8
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-122",
            0
          ],
          "source": [
            "obj-121",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-118",
            0
          ],
          "source": [
            "obj-122",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-123",
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
            "obj-122",
            0
          ],
          "source": [
            "obj-123",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-125",
            0
          ],
          "source": [
            "obj-8",
            9
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-125",
            0
          ],
          "source": [
            "obj-124",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-118",
            0
          ],
          "source": [
            "obj-125",
            0
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "parameters": {
      "obj-79::obj-11": [
        "Noise_Ceiling.Res",
        "Noise_Ceiling.Res",
        0
      ],
      "obj-79::obj-20": [
        "Noise_Ceiling.Freq",
        "Noise_Ceiling.Freq",
        0
      ],
      "obj-79::obj-22": [
        "Noise_Ceiling.TimeMode",
        "Noise_Ceiling.TimeMode",
        1
      ],
      "obj-79::obj-23": [
        "Noise_Ceiling.Offset",
        "Noise_Ceiling.Offset",
        0
      ],
      "obj-79::obj-38": [
        "Noise_Ceiling.FilterType",
        "Noise_Ceiling.FilterType",
        0
      ],
      "obj-79::obj-51": [
        "Noise_Ceiling.CV2",
        "Noise_Ceiling.CV2",
        0
      ],
      "obj-79::obj-54": [
        "Noise_Ceiling.CV1",
        "Noise_Ceiling.CV1",
        0
      ],
      "obj-79::obj-55": [
        "Noise_Ceiling.power",
        "Noise_Ceiling.power",
        0
      ],
      "obj-79::obj-63": [
        "Noise_Ceiling.CV3",
        "Noise_Ceiling.CV3",
        0
      ],
      "obj-79::obj-95": [
        "Noise_Ceiling.ResCV",
        "Noise_Ceiling.CV",
        0
      ],
      "parameterbanks": {}
    },
    "rect": [
      50.0,
      50.0,
      1580,
      1010
    ],
    "toolbarvisible": 1
  }
}
