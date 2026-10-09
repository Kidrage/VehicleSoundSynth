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
            990.0,
            22.0
          ],
          "text": "V3 acoustic seam: ONE source → DNA groups / pre-mix residuals → independent outputs"
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
            20.0,
            65.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 10,
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
            ""
          ],
          "patching_rect": [
            20.0,
            175.0,
            425.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_v12_dna_source_v3.gendsp"
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "newobj",
          "numinlets": 8,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            300.0,
            240.0,
            22.0
          ],
          "text": "v7_v12_dna_v3_designer~",
          "varname": "v12_dna_v3_designer~"
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-5",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            430.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-6",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            140.0,
            430.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "v7-source-recv",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            944.0,
            200.0,
            22.0
          ],
          "text": "r vss.v7.params.v12"
        }
      },
      {
        "box": {
          "id": "v7-source-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 10,
          "patching_rect": [
            20.0,
            968.0,
            200.0,
            22.0
          ],
          "text": "routepass v7_enable v7_core_db v7_attack_ms v7_release_ms v7_pitch_relief v7_lift_range_db v7_weight_trim_db v7_order2_db v7_order3_db"
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
            "obj-3",
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
            "obj-4",
            1
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
            "obj-4",
            2
          ],
          "source": [
            "obj-3",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            3
          ],
          "source": [
            "obj-3",
            2
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            4
          ],
          "source": [
            "obj-3",
            3
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            5
          ],
          "source": [
            "obj-3",
            4
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            6
          ],
          "source": [
            "obj-3",
            5
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            7
          ],
          "source": [
            "obj-3",
            6
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
            "obj-4",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-source-recv",
            0
          ],
          "destination": [
            "v7-source-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-source-route",
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
            "v7-source-route",
            1
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
            "v7-source-route",
            2
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
            "v7-source-route",
            3
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
            "v7-source-route",
            4
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
            "v7-source-route",
            5
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
            "v7-source-route",
            6
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
            "v7-source-route",
            7
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
            "v7-source-route",
            8
          ],
          "destination": [
            "obj-3",
            0
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 0,
    "rect": [
      50.0,
      50.0,
      1050,
      500
    ],
    "toolbarvisible": 1
  }
}
