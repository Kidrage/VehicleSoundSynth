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
          "text": "SOUND DESIGN / \u58f0\u97f3\u8bbe\u8ba1 \u2014 profile DSP stays independent; this page only controls it"
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
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            850.0,
            20.0,
            90.0,
            22.0
          ],
          "text": "route profile"
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
            945.0,
            20.0,
            80.0,
            22.0
          ],
          "text": "prepend set"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            780.0,
            50.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            800.0,
            20.0,
            260.0,
            24.0
          ],
          "text": "No active profile / \u672a\u9009\u62e9\u8f66\u578b"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            55.0,
            240.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            20.0,
            240.0,
            20.0
          ],
          "text": "Sound DNA / \u6838\u5fc3\u58f0\u7eb9"
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
            20.0,
            82.0,
            180.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            48.0,
            190.0,
            24.0
          ],
          "text": "Open Sound DNA / \u6253\u5f00 DNA"
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
            20.0,
            112.0,
            70.0,
            22.0
          ],
          "text": "dna_open"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            220.0,
            82.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            225.0,
            48.0,
            24.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            255.0,
            82.0,
            120.0,
            22.0
          ],
          "text": "prepend dna_solo"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            255.0,
            55.0,
            100.0,
            18.0
          ],
          "presentation": 1,
          "presentation_rect": [
            255.0,
            50.0,
            100.0,
            18.0
          ],
          "text": "Solo / \u72ec\u542c"
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
            400.0,
            82.0,
            190.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            380.0,
            48.0,
            200.0,
            24.0
          ],
          "text": "Open Start / \u6253\u5f00\u542f\u52a8\u8bbe\u8ba1\u5668"
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
            400.0,
            112.0,
            80.0,
            22.0
          ],
          "text": "start_open"
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
            600.0,
            82.0,
            175.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            590.0,
            48.0,
            180.0,
            24.0
          ],
          "text": "Audition Start / \u8bd5\u542c\u542f\u52a8"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            600.0,
            112.0,
            95.0,
            22.0
          ],
          "text": "start_audition"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            145.0,
            850.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            92.0,
            850.0,
            20.0
          ],
          "text": "Audition Context / \u8bd5\u542c\u573a\u666f \u2014 Live, Idle, Cruise, Load, Lift, High RPM\uff1b\u4e0d\u5199\u5165 preset"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "items": [
            "Live / \u5b9e\u65f6",
            ",",
            "Idle / \u6020\u901f",
            ",",
            "Cruise / \u5de1\u822a",
            ",",
            "Load / \u9ad8\u8d1f\u8f7d",
            ",",
            "Lift / \u6536\u6cb9",
            ",",
            "High RPM / \u9ad8\u8f6c"
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
            20.0,
            173.0,
            280.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            116.0,
            280.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-19",
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
            310.0,
            173.0,
            105.0,
            22.0
          ],
          "text": "sel 0 1 2 3 4 5"
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
            425.0,
            173.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
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
            510.0,
            145.0,
            145.0,
            22.0
          ],
          "text": "tuning_context live"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            510.0,
            171.0,
            145.0,
            22.0
          ],
          "text": "tuning_context idle"
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
            510.0,
            197.0,
            145.0,
            22.0
          ],
          "text": "tuning_context cruise"
        }
      },
      {
        "box": {
          "id": "obj-24",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            510.0,
            223.0,
            145.0,
            22.0
          ],
          "text": "tuning_context load"
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
            510.0,
            249.0,
            145.0,
            22.0
          ],
          "text": "tuning_context lift"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            510.0,
            275.0,
            145.0,
            22.0
          ],
          "text": "tuning_context high_rpm"
        }
      },
      {
        "box": {
          "args": [
            "main"
          ],
          "id": "obj-27",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/soundscape_control.maxpat",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            245.0,
            1040.0,
            155.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            165.0,
            1040.0,
            160.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            420.0,
            425.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            350.0,
            425.0,
            20.0
          ],
          "text": "Pop / \u77ed\u91c7\u6837\u4e8b\u4ef6"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            490.0,
            420.0,
            540.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            490.0,
            350.0,
            540.0,
            20.0
          ],
          "text": "Noise / \u72ec\u7acb\u673a\u68b0\u00b7\u8def\u566a"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            780.0,
            425.0,
            100.0,
            22.0
          ],
          "text": "sel ioniq6n"
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
            890.0,
            425.0,
            30.0,
            22.0
          ],
          "text": "1"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            930.0,
            425.0,
            30.0,
            22.0
          ],
          "text": "2"
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
            20.0,
            455.0,
            205.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            380.0,
            205.0,
            24.0
          ],
          "text": "Open Pop / \u6253\u5f00\u56de\u706b",
          "varname": "pop_open"
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
            20.0,
            490.0,
            40.0,
            22.0
          ],
          "text": "t b"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            70.0,
            490.0,
            55.0,
            22.0
          ],
          "text": "gate 2"
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
            20.0,
            525.0,
            145.0,
            22.0
          ],
          "text": "backfire_open"
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
            20.0,
            553.0,
            145.0,
            22.0
          ],
          "text": "event_open"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            245.0,
            455.0,
            205.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            245.0,
            380.0,
            205.0,
            24.0
          ],
          "text": "Audition Pop / \u8bd5\u542c\u56de\u706b",
          "varname": "pop_audition"
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
            245.0,
            490.0,
            40.0,
            22.0
          ],
          "text": "t b"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            295.0,
            490.0,
            55.0,
            22.0
          ],
          "text": "gate 2"
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
            245.0,
            525.0,
            145.0,
            22.0
          ],
          "text": "backfire_test 1"
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
            245.0,
            553.0,
            145.0,
            22.0
          ],
          "text": "event_audition"
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
            490.0,
            455.0,
            205.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            490.0,
            380.0,
            205.0,
            24.0
          ],
          "text": "Open Noise / \u6253\u5f00\u566a\u58f0",
          "varname": "noise_open"
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
            490.0,
            490.0,
            100.0,
            22.0
          ],
          "text": "noise_open"
        }
      },
      {
        "box": {
          "id": "obj-45",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            720.0,
            455.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            720.0,
            380.0,
            24.0,
            24.0
          ],
          "varname": "noise_solo"
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
            755.0,
            455.0,
            135.0,
            22.0
          ],
          "text": "prepend noise_solo"
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
            900.0,
            455.0,
            50.0,
            22.0
          ],
          "text": "set 0"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            760.0,
            485.0,
            240.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            755.0,
            382.0,
            240.0,
            20.0
          ],
          "text": "Noise Solo / \u566a\u58f0\u72ec\u542c"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            490.0,
            530.0,
            555.0,
            40.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            420.0,
            1040.0,
            22.0
          ],
          "text": "Noise \u9ed8\u8ba4\u5173\u95ed\uff1a\u5148\u5728 Mix + EQ \u8c03\u9ad8 Noise \u63a8\u5b50\u3002EV Pop \u4ec5\u624b\u52a8\u8bd5\u542c\uff0c\u4e0d\u65b0\u589e\u81ea\u52a8\u71c3\u70e7\u56de\u706b\u3002"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            425.0,
            820.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            460.0,
            1000.0,
            20.0
          ],
          "text": "\u53c2\u6570\u63d0\u793a\uff1a\u63a7\u4ef6\u4ec5\u5728\u5176\u6807\u6ce8\u573a\u666f\u53ef\u542c\uff1bSound DNA \u4e0e Soundscape \u4fdd\u6301\u72ec\u7acb\u8def\u7531\u3002"
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
            "obj-5",
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
            "obj-9",
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
            "obj-15",
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
            "obj-19",
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
            "obj-19",
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
            "obj-22",
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
            "obj-19",
            2
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
            "obj-19",
            3
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
            "obj-19",
            4
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
            "obj-25",
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
            "obj-19",
            5
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
            "obj-26",
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
            "obj-27",
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
            "obj-27",
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
            "obj-4",
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
            "obj-30",
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
            1
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
            "obj-33",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-35",
            1
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
            "obj-31",
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
            "obj-3",
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
            "obj-37",
            0
          ],
          "source": [
            "obj-35",
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
            "obj-38",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-40",
            1
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
            "obj-31",
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
            "obj-32",
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
            "obj-40",
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
            "obj-40",
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
            "obj-3",
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
            "obj-45",
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
      50.0,
      50.0,
      1120,
      610
    ],
    "toolbarvisible": 1
  }
}
