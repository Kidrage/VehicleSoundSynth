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
            18.0,
            620.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            15.0,
            620.0,
            24.0
          ],
          "text": "VehicleSoundSynth V6 \u2014 Ferrari SF90 \u2014 V10 Acoustic Interpretation"
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
            48.0,
            860.0,
            36.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            48.0,
            860.0,
            36.0
          ],
          "text": "Common Audio / Ignition / Drive / Mix / EQ controls live in main.maxpat.  \u6b64\u7a97\u53e3\u4ec5\u4fdd\u7559\u8f66\u578b\u6a21\u5f0f\u3002"
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
            82.0,
            860.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            82.0,
            860.0,
            24.0
          ],
          "text": "Ferrari Soundscape V5: Main \u2192 Sound Design\uff1b\u7535\u5e73\u4e5f\u5728\u8be5\u9875\u76f4\u63a5\u663e\u793a\u548c\u8c03\u6574\u3002"
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/profile_runtime_host_ferrari.maxpat",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            330.0,
            220.0,
            55.0
          ],
          "varname": "ferrari_runtime_host"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            700.0,
            330.0,
            145.0,
            22.0
          ],
          "text": "r vss.runtime.select"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            850.0,
            330.0,
            75.0,
            22.0
          ],
          "text": "sel ferrari"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            850.0,
            365.0,
            75.0,
            22.0
          ],
          "text": "delay 120"
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
            850.0,
            395.0,
            55.0,
            22.0
          ],
          "text": "wclose"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            915.0,
            395.0,
            85.0,
            22.0
          ],
          "text": "thispatcher"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            105.0,
            330.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            105.0,
            330.0,
            20.0
          ],
          "text": "Start / \u542f\u52a8\u97f3\u8272\uff08procedural only\uff09"
        }
      },
      {
        "box": {
          "id": "obj-11",
          "items": [
            "Ferrari V10 Procedural BEAP / \u7a0b\u5e8f\u5408\u6210"
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
            133.0,
            330.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20.0,
            133.0,
            330.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            167.0,
            70.0,
            22.0
          ],
          "text": "sel 0"
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
            360.0,
            133.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
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
            20.0,
            197.0,
            165.0,
            22.0
          ],
          "text": "start_style cinematic"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            380.0,
            105.0,
            440.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            380.0,
            105.0,
            440.0,
            20.0
          ],
          "text": "Backfire / \u56de\u706b\uff1aEnable + Intensity [0..1] + Solo"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            380.0,
            133.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            380.0,
            133.0,
            24.0,
            24.0
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
            415.0,
            133.0,
            155.0,
            22.0
          ],
          "text": "prepend backfire_enable"
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
            575.0,
            133.0,
            80.0,
            22.0
          ],
          "text": "loadmess 1"
        }
      },
      {
        "box": {
          "id": "obj-19",
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
            665.0,
            133.0,
            75.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            665.0,
            133.0,
            75.0,
            24.0
          ]
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
            750.0,
            133.0,
            175.0,
            22.0
          ],
          "text": "prepend backfire_intensity"
        }
      },
      {
        "box": {
          "id": "obj-21",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            665.0,
            165.0,
            100.0,
            22.0
          ],
          "text": "loadmess 0.65"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "toggle",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            380.0,
            190.0,
            24.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            380.0,
            190.0,
            24.0,
            24.0
          ]
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
            415.0,
            190.0,
            150.0,
            22.0
          ],
          "text": "prepend backfire_solo"
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
            575.0,
            190.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
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
            665.0,
            190.0,
            150.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            665.0,
            190.0,
            150.0,
            24.0
          ],
          "text": "Test Pop / \u6d4b\u8bd5\u56de\u706b"
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
            665.0,
            220.0,
            110.0,
            22.0
          ],
          "text": "backfire_test 1"
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
            380.0,
            250.0,
            260.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            380.0,
            250.0,
            260.0,
            24.0
          ],
          "text": "Open Pop Designer / \u6253\u5f00\u56de\u706b\u8bbe\u8ba1\u5668"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            380.0,
            285.0,
            180.0,
            22.0
          ],
          "text": "s open.ferrari.backfire"
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
            "obj-7",
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
            "obj-13",
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
            "obj-14",
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
            "obj-4",
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
            "obj-24",
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
            "obj-4",
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
            "obj-4",
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
            "obj-4",
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
            "obj-4",
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
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "rect": [
      50.0,
      50.0,
      980,
      420
    ],
    "toolbarvisible": 1
  }
}
