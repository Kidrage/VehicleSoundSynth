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
            820.0,
            22.0
          ],
          "text": "MIX + EQ / 混音与均衡 — active profile values; units and safe ranges are explicit"
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
            520.0,
            750.0,
            22.0
          ],
          "text": "route powertrain_level_db start_level_db transient_level_db soundscape_level_db road_level_db rumble_level_db master_trim_db"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            50.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            32.0,
            245.0,
            18.0
          ],
          "text": "Sound DNA / 核心声纹 [dB]",
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
          "id": "obj-6",
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
            20.0,
            73.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            53.0,
            82.0,
            22.0
          ],
          "hint": "DNA总推子：-60..6 dB；V7 -60目标静音，短淡出后归零。包含V7独立质量层，不包含独立Noise。",
          "annotation": "DNA总推子：-60..6 dB；V7 -60目标静音，短淡出后归零。包含V7独立质量层，不包含独立Noise。",
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
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            110.0,
            73.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            205.0,
            73.0,
            155.0,
            22.0
          ],
          "text": "prepend powertrain_level_db"
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
            110.0,
            100.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            280.0,
            50.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            32.0,
            245.0,
            18.0
          ],
          "text": "Start / 启动 [dB]",
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
          "id": "obj-11",
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
            280.0,
            73.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            53.0,
            82.0,
            22.0
          ],
          "hint": "启动声推子：-60..6 dB；只影响启动/就绪声，不修复运行声。",
          "annotation": "启动声推子：-60..6 dB；只影响启动/就绪声，不修复运行声。",
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
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            370.0,
            73.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
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
            465.0,
            73.0,
            155.0,
            22.0
          ],
          "text": "prepend start_level_db"
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
            370.0,
            100.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            540.0,
            50.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            32.0,
            245.0,
            18.0
          ],
          "text": "Pop / Event / 事件 [dB]",
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
          "id": "obj-16",
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
            540.0,
            73.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            53.0,
            82.0,
            22.0
          ],
          "hint": "事件推子：-60..6 dB；换挡/Pop等独立事件，连续DNA不受此推子控制。",
          "annotation": "事件推子：-60..6 dB；换挡/Pop等独立事件，连续DNA不受此推子控制。",
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
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            630.0,
            73.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
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
            725.0,
            73.0,
            155.0,
            22.0
          ],
          "text": "prepend transient_level_db"
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
            630.0,
            100.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            800.0,
            50.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            800.0,
            32.0,
            245.0,
            18.0
          ],
          "text": "Soundscape / 氛围 [dB]",
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
          "id": "obj-21",
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
            800.0,
            73.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            800.0,
            53.0,
            82.0,
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
          "id": "obj-22",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            890.0,
            73.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            985.0,
            73.0,
            155.0,
            22.0
          ],
          "text": "prepend soundscape_level_db"
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
            890.0,
            100.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-25",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            128.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            110.0,
            245.0,
            18.0
          ],
          "text": "Noise / 独立噪声层 [dB]",
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
          "maximum": 6.0,
          "minimum": -60.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            151.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            131.0,
            82.0,
            22.0
          ],
          "hint": "Noise总推子：-60..6 dB；-60静音。它与Soundscape Enable无关。",
          "annotation": "Noise总推子：-60..6 dB；-60静音。它与Soundscape Enable无关。",
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
            110.0,
            151.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
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
            205.0,
            151.0,
            155.0,
            22.0
          ],
          "text": "prepend road_level_db"
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
            110.0,
            178.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            280.0,
            128.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            110.0,
            245.0,
            18.0
          ],
          "text": "Cabin Rumble / 座舱 [dB]",
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
          "id": "obj-31",
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
            280.0,
            151.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            131.0,
            82.0,
            22.0
          ],
          "hint": "原Cabin Rumble推子：-60..6 dB；由DNA激励，可能与低频结构重复。V7新Sub不再额外激励它。",
          "annotation": "原Cabin Rumble推子：-60..6 dB；由DNA激励，可能与低频结构重复。V7新Sub不再额外激励它。",
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
          "id": "obj-32",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            370.0,
            151.0,
            90.0,
            22.0
          ],
          "text": "clip -60 6"
        }
      },
      {
        "box": {
          "id": "obj-33",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            465.0,
            151.0,
            155.0,
            22.0
          ],
          "text": "prepend rumble_level_db"
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
            370.0,
            178.0,
            80.0,
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
            540.0,
            128.0,
            245.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            110.0,
            245.0,
            18.0
          ],
          "text": "Master / 总输出 [dB]",
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
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -24.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            540.0,
            151.0,
            82.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            131.0,
            82.0,
            22.0
          ],
          "hint": "Main Master余量：-24..0 dB；最终总体降低，不增加上限；不能替代物理扬声器保护。",
          "annotation": "Main Master余量：-24..0 dB；最终总体降低，不增加上限；不能替代物理扬声器保护。",
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
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            630.0,
            151.0,
            90.0,
            22.0
          ],
          "text": "clip -24 0"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            725.0,
            151.0,
            155.0,
            22.0
          ],
          "text": "prepend master_trim_db"
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
            630.0,
            178.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            215.0,
            520.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            185.0,
            520.0,
            20.0
          ],
          "text": "Master EQ / 主均衡 — Frequency Hz, Gain dB, Q",
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
          "id": "obj-41",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            245.0,
            240.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            215.0,
            240.0,
            18.0
          ],
          "text": "Low Shelf / 低频架 — Hz / dB",
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
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            269.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            238.0,
            65.0,
            22.0
          ],
          "hint": "低架：30..400Hz、-12..12dB；增益0不改变。频率是架型转折，不是完整频段边界。",
          "annotation": "低架：30..400Hz、-12..12dB；增益0不改变。频率是架型转折，不是完整频段边界。",
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
          "id": "obj-43",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            92.0,
            269.0,
            55.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            92.0,
            238.0,
            55.0,
            22.0
          ],
          "hint": "低架：30..400Hz、-12..12dB；增益0不改变。频率是架型转折，不是完整频段边界。",
          "annotation": "低架：30..400Hz、-12..12dB；增益0不改变。频率是架型转折，不是完整频段边界。",
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
          "id": "obj-44",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            303.0,
            115.0,
            22.0
          ],
          "text": "pak 90 0."
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
            20.0,
            337.0,
            135.0,
            22.0
          ],
          "text": "prepend eq_low"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            371.0,
            105.0,
            22.0
          ],
          "text": "loadmess 90"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            280.0,
            245.0,
            240.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            215.0,
            240.0,
            18.0
          ],
          "text": "Low-Mid / 中低频 — Hz / dB / Q",
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
          "id": "obj-48",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            280.0,
            269.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            280.0,
            238.0,
            65.0,
            22.0
          ],
          "hint": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
          "annotation": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
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
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            352.0,
            269.0,
            55.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            352.0,
            238.0,
            55.0,
            22.0
          ],
          "hint": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
          "annotation": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
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
          "id": "obj-50",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            414.0,
            269.0,
            50.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            414.0,
            238.0,
            50.0,
            22.0
          ],
          "hint": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
          "annotation": "中低峰值EQ：120..1200Hz，-12..12dB，Q0.3..4；Q大更窄。削峰前确认声源/车内传递来源。",
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
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            280.0,
            303.0,
            145.0,
            22.0
          ],
          "text": "pak 250 0. 0.8"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            414.0,
            333.0,
            85.0,
            22.0
          ],
          "text": "loadmess 0.8"
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            280.0,
            337.0,
            135.0,
            22.0
          ],
          "text": "prepend eq_lowmid"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            280.0,
            371.0,
            105.0,
            22.0
          ],
          "text": "loadmess 250"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            540.0,
            245.0,
            240.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            215.0,
            240.0,
            18.0
          ],
          "text": "High-Mid / 中高频 — Hz / dB / Q",
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
          "id": "obj-56",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            540.0,
            269.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            540.0,
            238.0,
            65.0,
            22.0
          ],
          "hint": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
          "annotation": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
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
          "id": "obj-57",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            612.0,
            269.0,
            55.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            612.0,
            238.0,
            55.0,
            22.0
          ],
          "hint": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
          "annotation": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
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
          "id": "obj-58",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            674.0,
            269.0,
            50.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            674.0,
            238.0,
            50.0,
            22.0
          ],
          "hint": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
          "annotation": "中高峰值EQ：1000..8000Hz，-12..12dB，Q0.3..4；Q大更窄，不能补回没有生成的成分。",
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
          "id": "obj-59",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            540.0,
            303.0,
            145.0,
            22.0
          ],
          "text": "pak 3800 0. 1"
        }
      },
      {
        "box": {
          "id": "obj-60",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            674.0,
            333.0,
            85.0,
            22.0
          ],
          "text": "loadmess 1"
        }
      },
      {
        "box": {
          "id": "obj-61",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            540.0,
            337.0,
            135.0,
            22.0
          ],
          "text": "prepend eq_highmid"
        }
      },
      {
        "box": {
          "id": "obj-62",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            540.0,
            371.0,
            105.0,
            22.0
          ],
          "text": "loadmess 3800"
        }
      },
      {
        "box": {
          "id": "obj-63",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            800.0,
            245.0,
            240.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            800.0,
            215.0,
            240.0,
            18.0
          ],
          "text": "High Shelf / 高频架 — Hz / dB",
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
          "id": "obj-64",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            800.0,
            269.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            800.0,
            238.0,
            65.0,
            22.0
          ],
          "hint": "高架：4000..16000Hz，-12..12dB；保留安全余量，过亮先减而非补低音抬总量。",
          "annotation": "高架：4000..16000Hz，-12..12dB；保留安全余量，过亮先减而非补低音抬总量。",
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
          "id": "obj-65",
          "maxclass": "flonum",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            872.0,
            269.0,
            55.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            872.0,
            238.0,
            55.0,
            22.0
          ],
          "hint": "高架：4000..16000Hz，-12..12dB；保留安全余量，过亮先减而非补低音抬总量。",
          "annotation": "高架：4000..16000Hz，-12..12dB；保留安全余量，过亮先减而非补低音抬总量。",
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
          "id": "obj-66",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            800.0,
            303.0,
            115.0,
            22.0
          ],
          "text": "pak 9000 0."
        }
      },
      {
        "box": {
          "id": "obj-67",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            800.0,
            337.0,
            135.0,
            22.0
          ],
          "text": "prepend eq_high"
        }
      },
      {
        "box": {
          "id": "obj-68",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            800.0,
            371.0,
            105.0,
            22.0
          ],
          "text": "loadmess 9000"
        }
      },
      {
        "box": {
          "id": "obj-69",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1010.0,
            268.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1050.0,
            185.0,
            24.0,
            24.0
          ],
          "hint": "0应用EQ，1绕过EQ；不绕过限幅/主推子。",
          "annotation": "0应用EQ，1绕过EQ；不绕过限幅/主推子。"
        }
      },
      {
        "box": {
          "id": "obj-70",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1010.0,
            300.0,
            120.0,
            22.0
          ],
          "text": "prepend eq_bypass"
        }
      },
      {
        "box": {
          "id": "obj-71",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            980.0,
            245.0,
            130.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            900.0,
            188.0,
            145.0,
            18.0
          ],
          "text": "EQ Bypass / 旁路",
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
          "id": "obj-72",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 6,
          "outlettype": [
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            370.0,
            575.0,
            22.0
          ],
          "text": "route eq_low eq_lowmid eq_highmid eq_high eq_bypass"
        }
      },
      {
        "box": {
          "id": "obj-73",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            610.0,
            370.0,
            105.0,
            22.0
          ],
          "text": "unpack 0. 0."
        }
      },
      {
        "box": {
          "id": "obj-74",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            395.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-75",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            610.0,
            419.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-76",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            725.0,
            370.0,
            105.0,
            22.0
          ],
          "text": "unpack 0. 0. 0."
        }
      },
      {
        "box": {
          "id": "obj-77",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            725.0,
            395.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-78",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            725.0,
            419.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-79",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            725.0,
            443.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-80",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            840.0,
            370.0,
            105.0,
            22.0
          ],
          "text": "unpack 0. 0. 0."
        }
      },
      {
        "box": {
          "id": "obj-81",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            840.0,
            395.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-82",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            840.0,
            419.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-83",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            840.0,
            443.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-84",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            955.0,
            370.0,
            105.0,
            22.0
          ],
          "text": "unpack 0. 0."
        }
      },
      {
        "box": {
          "id": "obj-85",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            955.0,
            395.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-86",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            955.0,
            419.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-87",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1010.0,
            335.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-88",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            405.0,
            560.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            390.0,
            560.0,
            20.0
          ],
          "text": "Master Compressor / 总线压缩（Rate 越大响应越快）",
          "hidden": 1,
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
          "id": "obj-89",
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
            20.0,
            550.0,
            760.0,
            22.0
          ],
          "text": "route compressor_threshold_db compressor_ratio compressor_attack_rate compressor_release_rate compressor_makeup_db compressor_bypass"
        }
      },
      {
        "box": {
          "id": "obj-90",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            435.0,
            195.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            420.0,
            195.0,
            18.0
          ],
          "text": "Threshold / 阈值 [dB]",
          "hidden": 1,
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
          "id": "obj-91",
          "maxclass": "flonum",
          "maximum": 0.0,
          "minimum": -36.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            458.0,
            78.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            442.0,
            78.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1,
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
          "id": "obj-92",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            104.0,
            458.0,
            88.0,
            22.0
          ],
          "text": "clip -36 0"
        }
      },
      {
        "box": {
          "id": "obj-93",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_threshold_db"
        }
      },
      {
        "box": {
          "id": "obj-94",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            104.0,
            488.0,
            92.0,
            22.0
          ],
          "text": "loadmess -12"
        }
      },
      {
        "box": {
          "id": "obj-95",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            104.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-96",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            225.0,
            435.0,
            195.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            225.0,
            420.0,
            195.0,
            18.0
          ],
          "text": "Ratio / 压缩比 [:1]",
          "hidden": 1,
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
          "id": "obj-97",
          "maxclass": "flonum",
          "maximum": 50.0,
          "minimum": 1.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            225.0,
            458.0,
            78.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            225.0,
            442.0,
            78.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1,
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
          "id": "obj-98",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            309.0,
            458.0,
            88.0,
            22.0
          ],
          "text": "clip 1 50"
        }
      },
      {
        "box": {
          "id": "obj-99",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            225.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_ratio"
        }
      },
      {
        "box": {
          "id": "obj-100",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            309.0,
            488.0,
            92.0,
            22.0
          ],
          "text": "loadmess 2"
        }
      },
      {
        "box": {
          "id": "obj-101",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            309.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-102",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            430.0,
            435.0,
            195.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            430.0,
            420.0,
            195.0,
            18.0
          ],
          "text": "Attack Rate / 启动速率 [rate]",
          "hidden": 1,
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
          "id": "obj-103",
          "maxclass": "flonum",
          "maximum": 150.0,
          "minimum": 0.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            430.0,
            458.0,
            78.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            430.0,
            442.0,
            78.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1,
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
          "id": "obj-104",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            514.0,
            458.0,
            88.0,
            22.0
          ],
          "text": "clip 0 150"
        }
      },
      {
        "box": {
          "id": "obj-105",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            430.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_attack_rate"
        }
      },
      {
        "box": {
          "id": "obj-106",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            514.0,
            488.0,
            92.0,
            22.0
          ],
          "text": "loadmess 85"
        }
      },
      {
        "box": {
          "id": "obj-107",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            514.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-108",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            435.0,
            195.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635.0,
            420.0,
            195.0,
            18.0
          ],
          "text": "Release Rate / 释放速率 [rate]",
          "hidden": 1,
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
          "id": "obj-109",
          "maxclass": "flonum",
          "maximum": 150.0,
          "minimum": 0.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            635.0,
            458.0,
            78.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635.0,
            442.0,
            78.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1,
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
          "id": "obj-110",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            719.0,
            458.0,
            88.0,
            22.0
          ],
          "text": "clip 0 150"
        }
      },
      {
        "box": {
          "id": "obj-111",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_release_rate"
        }
      },
      {
        "box": {
          "id": "obj-112",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            719.0,
            488.0,
            92.0,
            22.0
          ],
          "text": "loadmess 35"
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
            719.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-114",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            840.0,
            435.0,
            195.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            840.0,
            420.0,
            195.0,
            18.0
          ],
          "text": "Makeup / 补偿 [dB]",
          "hidden": 1,
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
          "id": "obj-115",
          "maxclass": "flonum",
          "maximum": 12.0,
          "minimum": -12.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            840.0,
            458.0,
            78.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            840.0,
            442.0,
            78.0,
            22.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1,
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
          "id": "obj-116",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            924.0,
            458.0,
            88.0,
            22.0
          ],
          "text": "clip -12 12"
        }
      },
      {
        "box": {
          "id": "obj-117",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            840.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_makeup_db"
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
            924.0,
            488.0,
            92.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-119",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            924.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-120",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1040.0,
            458.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1040.0,
            390.0,
            24.0,
            24.0
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "hidden": 1
        }
      },
      {
        "box": {
          "id": "obj-121",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            875.0,
            408.0,
            160.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            875.0,
            393.0,
            160.0,
            18.0
          ],
          "text": "Compressor Bypass / 压缩旁路",
          "hidden": 1,
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
          "id": "obj-122",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            940.0,
            488.0,
            175.0,
            22.0
          ],
          "text": "prepend compressor_bypass"
        }
      },
      {
        "box": {
          "id": "obj-123",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            940.0,
            518.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
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
            20.0,
            570.0,
            150.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            540.0,
            155.0,
            24.0
          ],
          "text": "Save Profile / 保存",
          "hint": "Save Profile / 保存：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Save Profile / 保存：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-125",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            598.0,
            145.0,
            22.0
          ],
          "text": "save_profile_sound"
        }
      },
      {
        "box": {
          "id": "obj-126",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            190.0,
            570.0,
            150.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            190.0,
            540.0,
            155.0,
            24.0
          ],
          "text": "Reload / 重载",
          "hint": "Reload / 重载：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Reload / 重载：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-127",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            190.0,
            598.0,
            145.0,
            22.0
          ],
          "text": "reload_profile_sound"
        }
      },
      {
        "box": {
          "id": "obj-128",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            360.0,
            570.0,
            150.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            360.0,
            540.0,
            155.0,
            24.0
          ],
          "text": "Factory / 恢复出厂",
          "hint": "Reset Mix / 重置混音：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "Reset Mix / 重置混音：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
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
          "id": "obj-129",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            360.0,
            598.0,
            145.0,
            22.0
          ],
          "text": "reset_profile_sound"
        }
      },
      {
        "box": {
          "id": "v7-comp-note",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20,
            368,
            1060,
            46
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            368,
            1060,
            46
          ],
          "fontsize": 14,
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ],
          "linecount": 3,
          "text": "V7 动态已移至 Response 页：阈值 dBFS / 压缩比 / attack-release 毫秒。旧 OMX rate 不再作为 V7 控件。"
        }
      },
      {
        "box": {
          "id": "v7-mix-note",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20,
            425,
            1060,
            48
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            425,
            1060,
            48
          ],
          "fontsize": 13,
          "textcolor": [
            0.84,
            0.9,
            0.97,
            1.0
          ],
          "linecount": 3,
          "text": "混音次序：先减 Core 或 200–450 Hz 过强部分 → 调独立 Sub / Foundation → 最后设 Master 与压缩。-60 dB DNA/Noise = 关闭。"
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
            "obj-4",
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
            "obj-7",
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
            "obj-3",
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
            "obj-9",
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
            "obj-13",
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
            "obj-3",
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
            "obj-4",
            1
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
            "obj-18",
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
            "obj-4",
            2
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
            "obj-19",
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
            "obj-24",
            0
          ],
          "source": [
            "obj-4",
            3
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
            "obj-3",
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
            "obj-29",
            0
          ],
          "source": [
            "obj-4",
            4
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
            "obj-4",
            5
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
            "obj-36",
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
            "obj-37",
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
            "obj-38",
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
            "obj-4",
            6
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
            "obj-39",
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
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-44",
            1
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
            "obj-3",
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
            "obj-42",
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
            "obj-51",
            2
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
            "obj-50",
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
            "obj-51",
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
            "obj-51",
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
            "obj-53",
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
            "obj-3",
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
            "obj-48",
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
            "obj-59",
            2
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
            "obj-58",
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
            "obj-59",
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
            "obj-61",
            0
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
            "obj-3",
            0
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
            "obj-56",
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
            "obj-66",
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
            "obj-66",
            1
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
            "obj-3",
            0
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
            "obj-64",
            0
          ],
          "source": [
            "obj-68",
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
          "destination": [
            "obj-3",
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
            "obj-72",
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
            "obj-73",
            0
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
            "obj-42",
            0
          ],
          "source": [
            "obj-74",
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
            "obj-73",
            1
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
            "obj-75",
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
            "obj-72",
            1
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
            "obj-76",
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
            "obj-77",
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
            1
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
            "obj-78",
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
            "obj-76",
            2
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
            "obj-79",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-80",
            0
          ],
          "source": [
            "obj-72",
            2
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
            "obj-80",
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
            "obj-81",
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
            "obj-80",
            1
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
            "obj-82",
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
            "obj-80",
            2
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
            "obj-83",
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
            "obj-72",
            3
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
            "obj-84",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-64",
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
            "obj-86",
            0
          ],
          "source": [
            "obj-84",
            1
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
            "obj-86",
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
            "obj-72",
            4
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
            "obj-2",
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
            "obj-3",
            0
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
            "obj-91",
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
            "obj-95",
            0
          ],
          "source": [
            "obj-89",
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
            "obj-95",
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
            "obj-98",
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
            "obj-99",
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
            "obj-100",
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
            "obj-89",
            1
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
            "obj-101",
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
            "obj-105",
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
            "obj-106",
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
            "obj-89",
            2
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
            "obj-107",
            0
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
            "obj-111",
            0
          ],
          "source": [
            "obj-110",
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
            "obj-111",
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
            "obj-112",
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
            "obj-89",
            3
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
            "obj-113",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-116",
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
            "obj-117",
            0
          ],
          "source": [
            "obj-116",
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
            "obj-117",
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
            "obj-118",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-119",
            0
          ],
          "source": [
            "obj-89",
            4
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
            "obj-119",
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
            "obj-120",
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
            "obj-89",
            5
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
            "obj-124",
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
            "obj-125",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-127",
            0
          ],
          "source": [
            "obj-126",
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
            "obj-127",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-129",
            0
          ],
          "source": [
            "obj-128",
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
            "obj-129",
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
