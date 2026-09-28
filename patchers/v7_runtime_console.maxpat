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
            10.0,
            760.0,
            22.0
          ],
          "text": "EV-ENGINE V7 | DRIVE · MIX · DESIGN · TONE · RESPONSE"
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
            1120.0,
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
            1120.0,
            680.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "tab",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            42.0,
            1080,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            10.0,
            1080,
            36.0
          ],
          "tabs": [
            "Drive / 驾驶",
            "Mix + EQ / 混音与均衡",
            "Sound Design / 声音设计",
            "V7 Tone / 频段定稿",
            "V7 Response / 动态"
          ],
          "hint": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。",
          "annotation": "操作/显示：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            680.0,
            42.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 6,
          "outlettype": [
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            770.0,
            42.0,
            70.0,
            22.0
          ],
          "text": "sel 0 1 2 3 4"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_drive_console.maxpat",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            95.0,
            1120.0,
            590.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            55.0,
            1120.0,
            590.0
          ],
          "varname": "drive_page"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_mix_eq_console.maxpat",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            95.0,
            1120.0,
            590.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            55.0,
            1120.0,
            590.0
          ],
          "varname": "mix_page"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_sound_design_console.maxpat",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            95.0,
            1120.0,
            590.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            55.0,
            1120.0,
            590.0
          ],
          "varname": "design_page"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1040.0,
            42.0,
            85.0,
            22.0
          ],
          "text": "thispatcher"
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
            850.0,
            85.0,
            280.0,
            22.0
          ],
          "text": "script sendbox drive_page hidden 0, script sendbox mix_page hidden 1, script sendbox design_page hidden 1, script sendbox v7_tone_page hidden 1, script sendbox v7_response_page hidden 1"
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
            850.0,
            127.0,
            280.0,
            22.0
          ],
          "text": "script sendbox drive_page hidden 1, script sendbox mix_page hidden 0, script sendbox design_page hidden 1, script sendbox v7_tone_page hidden 1, script sendbox v7_response_page hidden 1"
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
            850.0,
            169.0,
            280.0,
            22.0
          ],
          "text": "script sendbox drive_page hidden 1, script sendbox mix_page hidden 1, script sendbox design_page hidden 0, script sendbox v7_tone_page hidden 1, script sendbox v7_response_page hidden 1"
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            690.0,
            900.0,
            22.0
          ],
          "text": "audio_enable | ignition | drive_source | powertrain_level_db | eq_low | compressor_threshold_db"
        }
      },
      {
        "box": {
          "id": "v7-page0",
          "maxclass": "bpatcher",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20,
            95,
            1120,
            590
          ],
          "name": "Patcher:/patchers/v7_tone_console.maxpat",
          "varname": "v7_tone_page",
          "presentation": 1,
          "presentation_rect": [
            20,
            55,
            1120,
            590
          ],
          "hidden": 1
        }
      },
      {
        "box": {
          "id": "v7-page1",
          "maxclass": "bpatcher",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20,
            95,
            1120,
            590
          ],
          "name": "Patcher:/patchers/v7_response_console.maxpat",
          "varname": "v7_response_page",
          "presentation": 1,
          "presentation_rect": [
            20,
            55,
            1120,
            590
          ],
          "hidden": 1
        }
      },
      {
        "box": {
          "id": "v7-tab3",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1184.0,
            200.0,
            22.0
          ],
          "text": "script sendbox drive_page hidden 1, script sendbox mix_page hidden 1, script sendbox design_page hidden 1, script sendbox v7_tone_page hidden 0, script sendbox v7_response_page hidden 1"
        }
      },
      {
        "box": {
          "id": "v7-tab4",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1208.0,
            200.0,
            22.0
          ],
          "text": "script sendbox drive_page hidden 1, script sendbox mix_page hidden 1, script sendbox design_page hidden 1, script sendbox v7_tone_page hidden 1, script sendbox v7_response_page hidden 0"
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
            "obj-5",
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
            "obj-4",
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
            "obj-2",
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
            "obj-7",
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
            "obj-2",
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
            "obj-2",
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
      },
      {
        "patchline": {
          "destination": [
            "obj-11",
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
            "obj-10",
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
            "obj-12",
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
            "obj-10",
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
            "obj-6",
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
          "source": [
            "obj-2",
            0
          ],
          "destination": [
            "v7-page0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-page0",
            0
          ],
          "destination": [
            "obj-3",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-2",
            0
          ],
          "destination": [
            "v7-page1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-page1",
            0
          ],
          "destination": [
            "obj-3",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-6",
            3
          ],
          "destination": [
            "v7-tab3",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-tab3",
            0
          ],
          "destination": [
            "obj-10",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-6",
            4
          ],
          "destination": [
            "v7-tab4",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-tab4",
            0
          ],
          "destination": [
            "obj-10",
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
      1160,
      720
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
