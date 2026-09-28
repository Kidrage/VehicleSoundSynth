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
      1000,
      720
    ],
    "openinpresentation": 0,
    "default_fontname": "Arial",
    "default_fontsize": 12.0,
    "boxes": [
      {
        "box": {
          "id": "in0",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            40,
            40,
            30,
            22
          ]
        }
      },
      {
        "box": {
          "id": "in1",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            160,
            40,
            30,
            22
          ]
        }
      },
      {
        "box": {
          "id": "in2",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            280,
            40,
            30,
            22
          ]
        }
      },
      {
        "box": {
          "id": "comp",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 3,
          "patching_rect": [
            20.0,
            872.0,
            200.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_dynamics.gendsp"
        }
      },
      {
        "box": {
          "id": "v7-comp-recv",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            896.0,
            200.0,
            22.0
          ],
          "text": "r vss.v7.params.#1"
        }
      },
      {
        "box": {
          "id": "v7-comp-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 7,
          "patching_rect": [
            20.0,
            920.0,
            200.0,
            22.0
          ],
          "text": "routepass v7_enable v7_comp_threshold_db v7_comp_ratio v7_comp_attack_ms v7_comp_release_ms v7_output_trim_db"
        }
      },
      {
        "box": {
          "id": "lim",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 4,
          "patching_rect": [
            20.0,
            944.0,
            200.0,
            22.0
          ],
          "text": "omx.peaklim~"
        }
      },
      {
        "box": {
          "id": "guard",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 4,
          "patching_rect": [
            20.0,
            968.0,
            200.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_clip_counter.gendsp"
        }
      },
      {
        "box": {
          "id": "out0",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            100,
            600,
            30,
            22
          ]
        }
      },
      {
        "box": {
          "id": "out1",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            400,
            600,
            30,
            22
          ]
        }
      },
      {
        "box": {
          "id": "feedback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            1040.0,
            200.0,
            22.0
          ],
          "text": "s vss.runtime.feedback.#1"
        }
      },
      {
        "box": {
          "id": "grsnap",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1064.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "grtag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1088.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_gr_db"
        }
      },
      {
        "box": {
          "id": "clipssnap",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1112.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "clipstag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            1136.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_clip_samples"
        }
      },
      {
        "box": {
          "id": "note",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            30,
            15,
            930,
            35
          ],
          "presentation": 1,
          "presentation_rect": [
            30,
            15,
            930,
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
          "text": "V7 RMS dB/ms compressor → preserved peak limiter → emergency clip counter. NOT true-peak or physical speaker protection."
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "in1",
            0
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "in2",
            0
          ],
          "destination": [
            "comp",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-recv",
            0
          ],
          "destination": [
            "v7-comp-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            0
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            1
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            2
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            3
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            4
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-comp-route",
            5
          ],
          "destination": [
            "comp",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "comp",
            0
          ],
          "destination": [
            "lim",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "comp",
            1
          ],
          "destination": [
            "lim",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lim",
            0
          ],
          "destination": [
            "guard",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lim",
            1
          ],
          "destination": [
            "guard",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "guard",
            0
          ],
          "destination": [
            "out0",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "guard",
            1
          ],
          "destination": [
            "out1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "comp",
            2
          ],
          "destination": [
            "grsnap",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "grsnap",
            0
          ],
          "destination": [
            "grtag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "grtag",
            0
          ],
          "destination": [
            "feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "guard",
            2
          ],
          "destination": [
            "clipssnap",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "clipssnap",
            0
          ],
          "destination": [
            "clipstag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "clipstag",
            0
          ],
          "destination": [
            "feedback",
            0
          ]
        }
      }
    ]
  }
}
