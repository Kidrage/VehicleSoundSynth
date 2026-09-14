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
            1400.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            15,
            1400,
            22
          ],
          "text": "V12 DNA V3 \u2014 Core / Body / Character / Upper"
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
            45.0,
            1450.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            45,
            1450,
            22
          ],
          "text": "1 Solo group \u2192 2 BEAP group dB \u2192 3 macros \u2192 4 filters. Main DNA fader owns the whole stem. No SC / Noise input."
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
            75.0,
            1500.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            75,
            1500,
            22
          ],
          "text": "\u22641200 RPM = original idle; 1200\u20133000 = smooth blend. V3 group audition excludes legacy idle; turn audition OFF for normal playback."
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
            115.0,
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
            360.0,
            115.0,
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
            505.0,
            115.0,
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
            650.0,
            115.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            795.0,
            115.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            940.0,
            115.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            1085.0,
            115.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "inlet",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            1230.0,
            115.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-12",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            1580.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-13",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            170.0,
            1580.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "messages",
          "id": "obj-14",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1700.0,
            1580.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 39,
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
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            155.0,
            1770.0,
            22.0
          ],
          "text": "route v3_aggression v3_body v3_character v3_softness v3_release_mass v3_width v3_load_response aggression brightness body texture air_detail cycle_irregularity stereo_width throttle_loudness_depth saturation idle_level idle_body idle_metal idle_irregularity idle_air idle_width combustion_pulse intake_detail exhaust_detail residual_detail rpm throttle load accel engine_running combustion_gain shift_cut powertrain_level_db dna_group dna_save dna_reload dna_reset"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            200.0,
            80.0,
            22.0
          ],
          "text": "loadbang"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            1200.0,
            390.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/dna_v3_output.gendsp"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            115,
            240,
            22
          ],
          "text": "Aggression / odd-even + local drive"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            145,
            90,
            22
          ],
          "varname": "v3_aggression"
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
            20.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            20.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_aggression"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            270.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            270,
            115,
            240,
            22
          ],
          "text": "Body / independent low-mid mass"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            270.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            270,
            145,
            90,
            22
          ],
          "varname": "v3_body"
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
            270.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            270.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_body"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            520.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            520,
            115,
            240,
            22
          ],
          "text": "Character / dual cavity depth"
        }
      },
      {
        "box": {
          "id": "obj-27",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            520.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            520,
            145,
            90,
            22
          ],
          "varname": "v3_character"
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
            520.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            520.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_character"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            770.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            770,
            115,
            240,
            22
          ],
          "text": "Softness / upper spectral rolloff"
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            770.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            770,
            145,
            90,
            22
          ],
          "varname": "v3_softness"
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
            770.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            770.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_softness"
        }
      },
      {
        "box": {
          "id": "obj-34",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1020.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1020,
            115,
            240,
            22
          ],
          "text": "Release Mass / body release time"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1020.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1020,
            145,
            90,
            22
          ],
          "varname": "v3_release_mass"
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
            1020.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            1020.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_release_mass"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1270.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1270,
            115,
            240,
            22
          ],
          "text": "Width / Side above 120 Hz"
        }
      },
      {
        "box": {
          "id": "obj-39",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1270.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1270,
            145,
            90,
            22
          ],
          "varname": "v3_width"
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
            1270.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            1270.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_width"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1520.0,
            240.0,
            240.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1520,
            115,
            240,
            22
          ],
          "text": "Load Response / gain + spectral opening"
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1520.0,
            270.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1520,
            145,
            90,
            22
          ],
          "varname": "v3_load_response"
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
            1520.0,
            305.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.5"
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
            1520.0,
            340.0,
            200.0,
            22.0
          ],
          "text": "prepend v3_load_response"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 aggression"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            855,
            85,
            22
          ],
          "varname": "legacy_aggression"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            115.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.62"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            210.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend aggression"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            295.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 brightness"
        }
      },
      {
        "box": {
          "id": "obj-51",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            295.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            855,
            85,
            22
          ],
          "varname": "legacy_brightness"
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
            390.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.78"
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
            485.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend brightness"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            570.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 body"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            570.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            855,
            85,
            22
          ],
          "varname": "legacy_body"
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
            665.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.72"
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
            760.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend body"
        }
      },
      {
        "box": {
          "id": "obj-58",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            845.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 texture"
        }
      },
      {
        "box": {
          "id": "obj-59",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            845.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            855,
            85,
            22
          ],
          "varname": "legacy_texture"
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
            940.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.52"
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
            1035.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend texture"
        }
      },
      {
        "box": {
          "id": "obj-62",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1120.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 air_detail"
        }
      },
      {
        "box": {
          "id": "obj-63",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1120.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            855,
            85,
            22
          ],
          "varname": "legacy_air_detail"
        }
      },
      {
        "box": {
          "id": "obj-64",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1215.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.68"
        }
      },
      {
        "box": {
          "id": "obj-65",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1310.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend air_detail"
        }
      },
      {
        "box": {
          "id": "obj-66",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1395.0,
            830.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            830,
            265,
            22
          ],
          "text": "Idle only \u00b7 cycle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-67",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1395.0,
            855.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            855,
            85,
            22
          ],
          "varname": "legacy_cycle_irregularity"
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
            1490.0,
            855.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.34"
        }
      },
      {
        "box": {
          "id": "obj-69",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1585.0,
            855.0,
            170.0,
            22.0
          ],
          "text": "prepend cycle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-70",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 stereo_width"
        }
      },
      {
        "box": {
          "id": "obj-71",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            927,
            85,
            22
          ],
          "varname": "legacy_stereo_width"
        }
      },
      {
        "box": {
          "id": "obj-72",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            115.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.64"
        }
      },
      {
        "box": {
          "id": "obj-73",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            210.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend stereo_width"
        }
      },
      {
        "box": {
          "id": "obj-74",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            295.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 throttle_loudness_depth"
        }
      },
      {
        "box": {
          "id": "obj-75",
          "maxclass": "flonum",
          "maximum": 8,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            295.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            927,
            85,
            22
          ],
          "varname": "legacy_throttle_loudness_depth"
        }
      },
      {
        "box": {
          "id": "obj-76",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            390.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 4.5"
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
            485.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend throttle_loudness_depth"
        }
      },
      {
        "box": {
          "id": "obj-78",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            570.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 saturation"
        }
      },
      {
        "box": {
          "id": "obj-79",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            570.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            927,
            85,
            22
          ],
          "varname": "legacy_saturation"
        }
      },
      {
        "box": {
          "id": "obj-80",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            665.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.28"
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
            760.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend saturation"
        }
      },
      {
        "box": {
          "id": "obj-82",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            845.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_level"
        }
      },
      {
        "box": {
          "id": "obj-83",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            845.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            927,
            85,
            22
          ],
          "varname": "legacy_idle_level"
        }
      },
      {
        "box": {
          "id": "obj-84",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            940.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.78"
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
            1035.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_level"
        }
      },
      {
        "box": {
          "id": "obj-86",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1120.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_body"
        }
      },
      {
        "box": {
          "id": "obj-87",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1120.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            927,
            85,
            22
          ],
          "varname": "legacy_idle_body"
        }
      },
      {
        "box": {
          "id": "obj-88",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1215.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.86"
        }
      },
      {
        "box": {
          "id": "obj-89",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1310.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_body"
        }
      },
      {
        "box": {
          "id": "obj-90",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1395.0,
            902.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            902,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_metal"
        }
      },
      {
        "box": {
          "id": "obj-91",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1395.0,
            927.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            927,
            85,
            22
          ],
          "varname": "legacy_idle_metal"
        }
      },
      {
        "box": {
          "id": "obj-92",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1490.0,
            927.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.58"
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
            1585.0,
            927.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_metal"
        }
      },
      {
        "box": {
          "id": "obj-94",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-95",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            999,
            85,
            22
          ],
          "varname": "legacy_idle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-96",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            115.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.18"
        }
      },
      {
        "box": {
          "id": "obj-97",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            210.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-98",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            295.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_air"
        }
      },
      {
        "box": {
          "id": "obj-99",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            295.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            295,
            999,
            85,
            22
          ],
          "varname": "legacy_idle_air"
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
            390.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.34"
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
            485.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_air"
        }
      },
      {
        "box": {
          "id": "obj-102",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            570.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 idle_width"
        }
      },
      {
        "box": {
          "id": "obj-103",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            570.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            570,
            999,
            85,
            22
          ],
          "varname": "legacy_idle_width"
        }
      },
      {
        "box": {
          "id": "obj-104",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            665.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.52"
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
            760.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend idle_width"
        }
      },
      {
        "box": {
          "id": "obj-106",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            845.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 combustion_pulse"
        }
      },
      {
        "box": {
          "id": "obj-107",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            845.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            845,
            999,
            85,
            22
          ],
          "varname": "legacy_combustion_pulse"
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
            940.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.8"
        }
      },
      {
        "box": {
          "id": "obj-109",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend combustion_pulse"
        }
      },
      {
        "box": {
          "id": "obj-110",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1120.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 intake_detail"
        }
      },
      {
        "box": {
          "id": "obj-111",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1120.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1120,
            999,
            85,
            22
          ],
          "varname": "legacy_intake_detail"
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
            1215.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.68"
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
            1310.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend intake_detail"
        }
      },
      {
        "box": {
          "id": "obj-114",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1395.0,
            974.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            974,
            265,
            22
          ],
          "text": "Idle only \u00b7 exhaust_detail"
        }
      },
      {
        "box": {
          "id": "obj-115",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1395.0,
            999.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1395,
            999,
            85,
            22
          ],
          "varname": "legacy_exhaust_detail"
        }
      },
      {
        "box": {
          "id": "obj-116",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1490.0,
            999.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.62"
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
            1585.0,
            999.0,
            170.0,
            22.0
          ],
          "text": "prepend exhaust_detail"
        }
      },
      {
        "box": {
          "id": "obj-118",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            1046.0,
            265.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            1046,
            265,
            22
          ],
          "text": "Idle only \u00b7 residual_detail"
        }
      },
      {
        "box": {
          "id": "obj-119",
          "maxclass": "flonum",
          "maximum": 1,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            1071.0,
            85.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            1071,
            85,
            22
          ],
          "varname": "legacy_residual_detail"
        }
      },
      {
        "box": {
          "id": "obj-120",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            115.0,
            1071.0,
            95.0,
            22.0
          ],
          "text": "loadmess 0.64"
        }
      },
      {
        "box": {
          "id": "obj-121",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            210.0,
            1071.0,
            170.0,
            22.0
          ],
          "text": "prepend residual_detail"
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
            20.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip 0 10000"
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
            20.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend rpm"
        }
      },
      {
        "box": {
          "id": "obj-124",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            250.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-125",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            250.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend throttle"
        }
      },
      {
        "box": {
          "id": "obj-126",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            480.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip -1 1"
        }
      },
      {
        "box": {
          "id": "obj-127",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            480.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend load"
        }
      },
      {
        "box": {
          "id": "obj-128",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            710.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip -1 1"
        }
      },
      {
        "box": {
          "id": "obj-129",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            710.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend accel"
        }
      },
      {
        "box": {
          "id": "obj-130",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            940.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-131",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            940.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend engine_running"
        }
      },
      {
        "box": {
          "id": "obj-132",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1170.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-133",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1170.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend combustion_gain"
        }
      },
      {
        "box": {
          "id": "obj-134",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1400.0,
            390.0,
            100.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-135",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1400.0,
            425.0,
            170.0,
            22.0
          ],
          "text": "prepend shift_cut"
        }
      },
      {
        "box": {
          "id": "obj-136",
          "maxclass": "number",
          "maximum": 4,
          "minimum": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            470.0,
            65.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            195,
            65,
            22
          ]
        }
      },
      {
        "box": {
          "id": "obj-137",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            95.0,
            470.0,
            1000.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            95,
            195,
            1000,
            22
          ],
          "text": "Audition: 0 All \u00b7 1 Core \u00b7 2 Body \u00b7 3 Character \u00b7 4 Upper (not saved)"
        }
      },
      {
        "box": {
          "id": "obj-138",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            500.0,
            90.0,
            22.0
          ],
          "text": "loadmess 0"
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
          "id": "obj-139",
          "lockeddragscroll": 0,
          "maxclass": "bpatcher",
          "numinlets": 4,
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
                  "id": "obj-9",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    24.0,
                    73.0,
                    169.0,
                    18.0
                  ],
                  "text": "## Four input audio mixer ## "
                }
              },
              {
                "box": {
                  "coldcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "hotcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ],
                  "id": "obj-8",
                  "maxclass": "live.meter~",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "float",
                    "int"
                  ],
                  "patching_rect": [
                    439.0,
                    879.5,
                    5.0,
                    100.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    187.9129638671875,
                    41.71455001831055,
                    5.0,
                    47.0
                  ],
                  "warmcolor": [
                    0.278431,
                    0.839216,
                    1.0,
                    1.0
                  ]
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
                  "fontsize": 8.0,
                  "id": "obj-70",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    937.912964,
                    36.470001,
                    15.0,
                    15.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    158.0,
                    41.71455001831055,
                    15.0,
                    14.764644622802734
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        0.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "MuteCh4",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "MuteCh4",
                      "parameter_type": 2
                    }
                  },
                  "text": "m",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "m",
                  "varname": "MuteCh4"
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
                  "fontsize": 8.0,
                  "id": "obj-64",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    699.912964,
                    36.470001,
                    15.0,
                    15.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    116.9771728515625,
                    41.71455001831055,
                    15.0,
                    14.764644622802734
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        0.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "MuteCh3",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "MuteCh3",
                      "parameter_type": 2
                    }
                  },
                  "text": "m",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "m",
                  "varname": "MuteCh1[2]"
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
                  "fontsize": 8.0,
                  "id": "obj-58",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    458.912964,
                    36.470001,
                    15.0,
                    15.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    72.5,
                    41.71455001831055,
                    15.0,
                    14.764644622802734
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        0.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "MuteCh2",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "MuteCh2",
                      "parameter_type": 2
                    }
                  },
                  "text": "m",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "m",
                  "varname": "MuteCh2"
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
                  "fontsize": 8.0,
                  "id": "obj-49",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    234.75,
                    36.470001,
                    15.0,
                    15.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    29.0,
                    41.71455001831055,
                    15.0,
                    14.764644622802734
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        0.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "MuteCh1",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "MuteCh1",
                      "parameter_type": 2
                    }
                  },
                  "text": "m",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "m",
                  "varname": "MuteCh1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-68",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    1055.873535,
                    90.0,
                    35.0,
                    20.0
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-69",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    1055.873535,
                    121.470001,
                    59.0,
                    20.0
                  ],
                  "text": "active $1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-71",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 3,
                  "outlettype": [
                    "bang",
                    "bang",
                    ""
                  ],
                  "patching_rect": [
                    933.912964,
                    177.0,
                    109.0,
                    20.0
                  ],
                  "text": "sel 1 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-72",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    933.912964,
                    277.5,
                    29.5,
                    20.0
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-73",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    978.912964,
                    277.5,
                    61.0,
                    20.0
                  ],
                  "text": "0.000251"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-62",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    821.162964,
                    90.0,
                    35.0,
                    20.0
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-63",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    821.162964,
                    121.470001,
                    59.0,
                    20.0
                  ],
                  "text": "active $1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-65",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 3,
                  "outlettype": [
                    "bang",
                    "bang",
                    ""
                  ],
                  "patching_rect": [
                    695.912964,
                    177.0,
                    109.0,
                    20.0
                  ],
                  "text": "sel 1 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-66",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    695.912964,
                    277.5,
                    29.5,
                    20.0
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-67",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    740.912964,
                    277.5,
                    61.0,
                    20.0
                  ],
                  "text": "0.000251"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-56",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    580.162964,
                    90.0,
                    35.0,
                    20.0
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-57",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    580.162964,
                    121.470001,
                    59.0,
                    20.0
                  ],
                  "text": "active $1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-59",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 3,
                  "outlettype": [
                    "bang",
                    "bang",
                    ""
                  ],
                  "patching_rect": [
                    454.912964,
                    177.0,
                    109.0,
                    20.0
                  ],
                  "text": "sel 1 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-60",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    454.912964,
                    277.5,
                    29.5,
                    20.0
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-61",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    499.912964,
                    277.5,
                    61.0,
                    20.0
                  ],
                  "text": "0.000251"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-53",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    356.0,
                    90.0,
                    35.0,
                    20.0
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-52",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    356.0,
                    121.470001,
                    59.0,
                    20.0
                  ],
                  "text": "active $1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-43",
                  "maxclass": "newobj",
                  "numinlets": 3,
                  "numoutlets": 3,
                  "outlettype": [
                    "bang",
                    "bang",
                    ""
                  ],
                  "patching_rect": [
                    230.75,
                    177.0,
                    109.0,
                    20.0
                  ],
                  "text": "sel 1 0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-42",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    230.75,
                    277.5,
                    29.5,
                    20.0
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-13",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    275.75,
                    277.5,
                    61.0,
                    20.0
                  ],
                  "text": "1."
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-35",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    432.0,
                    837.5,
                    42.0,
                    20.0
                  ],
                  "text": "*~ 0.2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-27",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    356.0,
                    226.5,
                    41.0,
                    20.0
                  ],
                  "text": "dbtoa"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-23",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    585.5,
                    226.5,
                    41.0,
                    20.0
                  ],
                  "text": "dbtoa"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-22",
                  "maxclass": "newobj",
                  "numinlets": 1,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    820.686768,
                    226.5,
                    41.0,
                    20.0
                  ],
                  "text": "dbtoa"
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
                    1055.873535,
                    226.5,
                    41.0,
                    20.0
                  ],
                  "text": "dbtoa"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-3",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    690.477173,
                    497.838623,
                    26.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    174.0,
                    0.5,
                    26.0,
                    17.0
                  ],
                  "text": "In 4",
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
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-2",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    579.205811,
                    497.838623,
                    26.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    118.16666412353516,
                    0.5,
                    26.0,
                    17.0
                  ],
                  "text": "In 3",
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
                  "id": "obj-4",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    467.934326,
                    497.838623,
                    26.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    57.33333206176758,
                    0.5,
                    26.0,
                    17.0
                  ],
                  "text": "In 2",
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
                  "id": "obj-5",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    307.912964,
                    497.838623,
                    26.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    3.5,
                    0.5,
                    26.0,
                    17.0
                  ],
                  "text": "In 1",
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
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-6",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "int"
                  ],
                  "patching_rect": [
                    299.75,
                    684.5,
                    32.5,
                    20.0
                  ],
                  "text": "!= 1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-50",
                  "maxclass": "newobj",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    "signal"
                  ],
                  "patching_rect": [
                    299.75,
                    755.5,
                    75.25,
                    20.0
                  ],
                  "text": "gate~ 1 1"
                }
              },
              {
                "box": {
                  "comment": "signal output",
                  "id": "obj-7",
                  "index": 1,
                  "maxclass": "outlet",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    299.75,
                    809.5,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-47",
                  "index": 4,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    681.5,
                    528.0,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-48",
                  "index": 3,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    573.0,
                    528.0,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-46",
                  "index": 2,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    464.5,
                    528.0,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "comment": "",
                  "id": "obj-45",
                  "index": 1,
                  "maxclass": "inlet",
                  "numinlets": 0,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    307.25,
                    528.0,
                    25.0,
                    25.0
                  ]
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-10",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    245.912964,
                    809.5,
                    40.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    1.5,
                    96.33863830566406,
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
                  "id": "obj-37",
                  "maxclass": "live.text",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    ""
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    299.75,
                    639.4375,
                    40.0,
                    20.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    144.9771728515625,
                    18.65743637084961,
                    52.0,
                    14.764644622802734
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_defer": 1,
                      "parameter_enum": [
                        "val1",
                        "val2"
                      ],
                      "parameter_initial": [
                        0.0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "Mute",
                      "parameter_mmax": 1.0,
                      "parameter_shortname": "Mute",
                      "parameter_type": 2
                    }
                  },
                  "text": "mute",
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                  ],
                  "texton": "mute",
                  "varname": "Mute"
                }
              },
              {
                "box": {
                  "fontname": "Ableton Sans Bold Regular",
                  "fontsize": 9.0,
                  "id": "obj-38",
                  "maxclass": "comment",
                  "numinlets": 1,
                  "numoutlets": 0,
                  "patching_rect": [
                    24.0,
                    48.0,
                    71.0,
                    17.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    1.5,
                    18.65743637084961,
                    71.0,
                    17.0
                  ],
                  "text": "AUDIO MIXER",
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
                    0.7
                  ],
                  "id": "obj-33",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    1055.873535,
                    163.5,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    129.0,
                    41.71455001831055,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_initial": [
                        -21
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "4",
                      "parameter_mmax": 0.0,
                      "parameter_mmin": -72.0,
                      "parameter_shortname": "4",
                      "parameter_type": 0,
                      "parameter_unitstyle": 4
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.7
                  ],
                  "varname": "in4"
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
                    1055.873535,
                    432.5,
                    47.0,
                    21.0
                  ],
                  "text": "3 0 $1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-25",
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
                    24.0,
                    98.5,
                    59.5,
                    20.0
                  ],
                  "restore": {
                    "Mute": [
                      0.0
                    ],
                    "MuteCh1": [
                      0.0
                    ],
                    "MuteCh1[2]": [
                      0.0
                    ],
                    "MuteCh2": [
                      0.0
                    ],
                    "MuteCh4": [
                      0.0
                    ],
                    "in1": [
                      0
                    ],
                    "in2": [
                      -5
                    ],
                    "in3": [
                      -9
                    ],
                    "in4": [
                      -21
                    ]
                  },
                  "text": "autopattr",
                  "varname": "u441003309"
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
                    0.7
                  ],
                  "id": "obj-29",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    820.686768,
                    163.5,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    85.0,
                    41.71455001831055,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_initial": [
                        -9
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "3",
                      "parameter_mmax": 0.0,
                      "parameter_mmin": -72.0,
                      "parameter_shortname": "3",
                      "parameter_type": 0,
                      "parameter_unitstyle": 4
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.7
                  ],
                  "varname": "in3"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-31",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    820.686768,
                    432.5,
                    47.0,
                    21.0
                  ],
                  "text": "2 0 $1"
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
                    0.7
                  ],
                  "id": "obj-32",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    585.5,
                    163.5,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    41.0,
                    41.71455001831055,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_initial": [
                        -5
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "2",
                      "parameter_mmax": 0.0,
                      "parameter_mmin": -72.0,
                      "parameter_shortname": "2",
                      "parameter_type": 0,
                      "parameter_unitstyle": 4
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.7
                  ],
                  "varname": "in2"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-36",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    585.5,
                    432.5,
                    47.0,
                    21.0
                  ],
                  "text": "1 0 $1"
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
                    0.7
                  ],
                  "id": "obj-39",
                  "maxclass": "live.dial",
                  "numinlets": 1,
                  "numoutlets": 2,
                  "outlettype": [
                    "",
                    "float"
                  ],
                  "parameter_enable": 1,
                  "patching_rect": [
                    356.0,
                    163.5,
                    44.0,
                    48.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    -3.0,
                    41.71455001831055,
                    44.0,
                    48.0
                  ],
                  "saved_attribute_attributes": {
                    "valueof": {
                      "parameter_initial": [
                        0
                      ],
                      "parameter_initial_enable": 1,
                      "parameter_longname": "1",
                      "parameter_mmax": 0.0,
                      "parameter_mmin": -72.0,
                      "parameter_shortname": "1",
                      "parameter_type": 0,
                      "parameter_unitstyle": 4
                    }
                  },
                  "textcolor": [
                    1.0,
                    1.0,
                    1.0,
                    0.7
                  ],
                  "varname": "in1"
                }
              },
              {
                "box": {
                  "fontname": "Arial",
                  "fontsize": 13.0,
                  "id": "obj-40",
                  "maxclass": "message",
                  "numinlets": 2,
                  "numoutlets": 1,
                  "outlettype": [
                    ""
                  ],
                  "patching_rect": [
                    356.0,
                    432.5,
                    68.0,
                    21.0
                  ],
                  "text": "0 0 $1"
                }
              },
              {
                "box": {
                  "fontface": 0,
                  "fontname": "Arial",
                  "fontsize": 12.0,
                  "id": "obj-41",
                  "maxclass": "newobj",
                  "numinlets": 4,
                  "numoutlets": 2,
                  "outlettype": [
                    "signal",
                    "list"
                  ],
                  "patching_rect": [
                    356.0,
                    607.0,
                    344.5,
                    20.0
                  ],
                  "text": "matrix~ 4 1 1. @ramp 20."
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
                    24.0,
                    28.711639,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    37.0,
                    425.0,
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
                    68.337189,
                    28.711639,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    17.0,
                    425.0,
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
                    111.079285,
                    28.711639,
                    37.0,
                    5.0
                  ],
                  "presentation": 1,
                  "presentation_rect": [
                    0.0,
                    0.0,
                    425.0,
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
                    "obj-34",
                    0
                  ],
                  "order": 0,
                  "source": [
                    "obj-1",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-73",
                    1
                  ],
                  "order": 1,
                  "source": [
                    "obj-1",
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
                    "obj-13",
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
                  "order": 0,
                  "source": [
                    "obj-22",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-67",
                    1
                  ],
                  "order": 1,
                  "source": [
                    "obj-22",
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
                  "order": 0,
                  "source": [
                    "obj-23",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-61",
                    1
                  ],
                  "order": 1,
                  "source": [
                    "obj-23",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-13",
                    1
                  ],
                  "order": 1,
                  "source": [
                    "obj-27",
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
                  "order": 0,
                  "source": [
                    "obj-27",
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
                    "obj-29",
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
                    "obj-31",
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
                    "obj-32",
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
                    "obj-33",
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
                    "obj-34",
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
                    "obj-35",
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
                    "obj-36",
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
                    "obj-37",
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
                    "obj-39",
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
                    "obj-50",
                    1
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
                    "obj-40",
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
                    "obj-13",
                    0
                  ],
                  "source": [
                    "obj-43",
                    1
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
                    "obj-43",
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
                    "obj-45",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "destination": [
                    "obj-41",
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
                    "obj-41",
                    3
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
                    "obj-41",
                    2
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
                    "obj-43",
                    0
                  ],
                  "order": 1,
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
                  "order": 0,
                  "source": [
                    "obj-49",
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
                  "order": 0,
                  "source": [
                    "obj-50",
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
                  "order": 1,
                  "source": [
                    "obj-50",
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
                    "obj-52",
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
                    "obj-53",
                    0
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
                    "obj-32",
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
                    "obj-56",
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
                    "obj-59",
                    0
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
                    "obj-60",
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
                    "obj-61",
                    0
                  ],
                  "source": [
                    "obj-59",
                    1
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
                    "obj-6",
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
                    "obj-60",
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
                    "obj-61",
                    0
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
                    "obj-29",
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
                    "obj-62",
                    0
                  ],
                  "order": 0,
                  "source": [
                    "obj-64",
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
                  "order": 1,
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
                    "obj-65",
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
                    "obj-66",
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
                    "obj-68",
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
                    "obj-69",
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
                  "order": 0,
                  "source": [
                    "obj-70",
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
                  "order": 1,
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
                    "obj-71",
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
                    "obj-71",
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
                    "obj-72",
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
                    "obj-73",
                    0
                  ]
                }
              }
            ],
            "objectsnaponopen": 1,
            "openinpresentation": 1,
            "rect": [
              435.0,
              109.0,
              583.0,
              652.0
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
            1010.0,
            201.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            590,
            201.0,
            116.0
          ],
          "varname": "V3_Group_Mixer",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-140",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            460.0,
            1010.0,
            1160.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            460,
            590,
            1160,
            22
          ],
          "text": "BEAP inputs 1 / 2 / 3 / 4 = Core / Body / Character / Upper. Start with factory ratios; recommended \u221230..0 dB."
        }
      },
      {
        "box": {
          "id": "obj-141",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            540.0,
            210.0,
            22.0
          ],
          "text": "expr ($i1==0)||($i1==1)"
        }
      },
      {
        "box": {
          "id": "obj-142",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            575.0,
            105.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-143",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            610.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-144",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            645.0,
            45.0,
            22.0
          ],
          "text": "*~"
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
          "id": "obj-145",
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
                  ]
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
                  "varname": "ResCV"
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
                  "annotation": "",
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
                        2700
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
                  "varname": "Freq"
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
                  "annotation": "Time mode: when Sync is selected, the LFO runs in sync with Live's transport. When in Freq mode, the LFO runs using its own internal clock. Synced rates are expressed in note values, and Frequency rates are expressed in Herz.",
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
                  "hint": "",
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
                  "annotation": "",
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
                  "varname": "Offset[2]"
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
                  ]
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
                  "varname": "CV3"
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
                  "varname": "CV1"
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
                  "varname": "CV2"
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
                  "varname": "FilterType"
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
                  "varname": "Res"
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
                  "varname": "power[1]"
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
                      2700
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
            690.0,
            427.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            270,
            427.0,
            116.0
          ],
          "varname": "V3_Core",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-146",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            665.0,
            425.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            20,
            235,
            425,
            22
          ],
          "text": "Core \u00b7 LP; low resonance 0.3\u20130.8"
        }
      },
      {
        "box": {
          "id": "obj-147",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            470.0,
            540.0,
            210.0,
            22.0
          ],
          "text": "expr ($i1==0)||($i1==2)"
        }
      },
      {
        "box": {
          "id": "obj-148",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            470.0,
            575.0,
            105.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-149",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            470.0,
            610.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-150",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            470.0,
            645.0,
            45.0,
            22.0
          ],
          "text": "*~"
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
          "id": "obj-151",
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
                  ]
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
                  "varname": "ResCV"
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
                  "annotation": "",
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
                        850
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
                  "varname": "Freq"
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
                  "annotation": "Time mode: when Sync is selected, the LFO runs in sync with Live's transport. When in Freq mode, the LFO runs using its own internal clock. Synced rates are expressed in note values, and Frequency rates are expressed in Herz.",
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
                  "hint": "",
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
                  "annotation": "",
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
                  "varname": "Offset[2]"
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
                  ]
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
                  "varname": "CV3"
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
                  "varname": "CV1"
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
                  "varname": "CV2"
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
                  "varname": "FilterType"
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
                  "varname": "Res"
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
                  "varname": "power[1]"
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
                      850
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
            470.0,
            690.0,
            427.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            470,
            270,
            427.0,
            116.0
          ],
          "varname": "V3_Body",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-152",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            470.0,
            665.0,
            425.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            470,
            235,
            425,
            22
          ],
          "text": "Body \u00b7 LP; low resonance 0.3\u20130.8"
        }
      },
      {
        "box": {
          "id": "obj-153",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            920.0,
            540.0,
            210.0,
            22.0
          ],
          "text": "expr ($i1==0)||($i1==3)"
        }
      },
      {
        "box": {
          "id": "obj-154",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            920.0,
            575.0,
            105.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-155",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            920.0,
            610.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-156",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            920.0,
            645.0,
            45.0,
            22.0
          ],
          "text": "*~"
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
          "id": "obj-157",
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
                  ]
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
                  "varname": "ResCV"
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
                  "annotation": "",
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
                        2400
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
                  "varname": "Freq"
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
                  "annotation": "Time mode: when Sync is selected, the LFO runs in sync with Live's transport. When in Freq mode, the LFO runs using its own internal clock. Synced rates are expressed in note values, and Frequency rates are expressed in Herz.",
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
                  "hint": "",
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
                  "annotation": "",
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
                  "varname": "Offset[2]"
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
                  ]
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
                  "varname": "CV3"
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
                  "varname": "CV1"
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
                  "varname": "CV2"
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
                  "varname": "FilterType"
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
                  "varname": "Res"
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
                  "varname": "power[1]"
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
                      2400
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
            920.0,
            690.0,
            427.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            920,
            270,
            427.0,
            116.0
          ],
          "varname": "V3_Character",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-158",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            920.0,
            665.0,
            425.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            920,
            235,
            425,
            22
          ],
          "text": "Character \u00b7 LP; low resonance 0.3\u20130.8"
        }
      },
      {
        "box": {
          "id": "obj-159",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1370.0,
            540.0,
            210.0,
            22.0
          ],
          "text": "expr ($i1==0)||($i1==4)"
        }
      },
      {
        "box": {
          "id": "obj-160",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1370.0,
            575.0,
            105.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-161",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1370.0,
            610.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-162",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1370.0,
            645.0,
            45.0,
            22.0
          ],
          "text": "*~"
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
          "id": "obj-163",
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
                  ]
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
                  "varname": "ResCV"
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
                  "annotation": "",
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
                        3500
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
                  "varname": "Freq"
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
                  "annotation": "Time mode: when Sync is selected, the LFO runs in sync with Live's transport. When in Freq mode, the LFO runs using its own internal clock. Synced rates are expressed in note values, and Frequency rates are expressed in Herz.",
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
                  "hint": "",
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
                  "annotation": "",
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
                  "varname": "Offset[2]"
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
                  ]
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
                  "varname": "CV3"
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
                  "varname": "CV1"
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
                  "varname": "CV2"
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
                  "varname": "FilterType"
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
                  "varname": "Res"
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
                  "varname": "power[1]"
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
                      3500
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
            1370.0,
            690.0,
            427.0,
            116.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1370,
            270,
            427.0,
            116.0
          ],
          "varname": "V3_Upper",
          "viewvisibility": 1
        }
      },
      {
        "box": {
          "id": "obj-164",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1370.0,
            665.0,
            425.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1370,
            235,
            425,
            22
          ],
          "text": "Upper \u00b7 LP; low resonance 0.3\u20130.8"
        }
      },
      {
        "box": {
          "id": "obj-165",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1450.0,
            1200.0,
            60.0,
            22.0
          ],
          "text": "== 0"
        }
      },
      {
        "box": {
          "id": "obj-166",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1530.0,
            1200.0,
            100.0,
            22.0
          ],
          "text": "pack 1. 35"
        }
      },
      {
        "box": {
          "id": "obj-167",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1650.0,
            1200.0,
            60.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-168",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            500.0,
            1200.0,
            45.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-169",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            650.0,
            1200.0,
            45.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-170",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            1300.0,
            85.0,
            22.0
          ],
          "text": "clip -60. 6."
        }
      },
      {
        "box": {
          "id": "obj-171",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            1336.0,
            150.0,
            22.0
          ],
          "text": "expr pow(10., $f1/20.)"
        }
      },
      {
        "box": {
          "id": "obj-172",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            1372.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 50"
        }
      },
      {
        "box": {
          "id": "obj-173",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            20.0,
            1408.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-174",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            120.0,
            1300.0,
            95.0,
            22.0
          ],
          "text": "loadmess -3"
        }
      },
      {
        "box": {
          "id": "obj-175",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            20.0,
            1480.0,
            45.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-176",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            170.0,
            1480.0,
            45.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-177",
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
            900.0,
            1300.0,
            190.0,
            22.0
          ],
          "text": "autopattr @autorestore 0"
        }
      },
      {
        "box": {
          "id": "obj-178",
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
            900.0,
            1340.0,
            550.0,
            22.0
          ],
          "text": "pattrstorage v12_sound_dna_v3 @autorestore 0 @savemode 0"
        }
      },
      {
        "box": {
          "id": "obj-179",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            900.0,
            1380.0,
            370.0,
            22.0
          ],
          "text": "js Patcher:/code/dna_v3_state.js v12"
        }
      },
      {
        "box": {
          "id": "obj-180",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            900.0,
            1440.0,
            180.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            470,
            680,
            180,
            22
          ],
          "text": "Save DNA"
        }
      },
      {
        "box": {
          "id": "obj-181",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            900.0,
            1480.0,
            90.0,
            22.0
          ],
          "text": "save"
        }
      },
      {
        "box": {
          "id": "obj-182",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1130.0,
            1440.0,
            180.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            700,
            680,
            180,
            22
          ],
          "text": "Reload DNA"
        }
      },
      {
        "box": {
          "id": "obj-183",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1130.0,
            1480.0,
            90.0,
            22.0
          ],
          "text": "restore"
        }
      },
      {
        "box": {
          "id": "obj-184",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            900.0,
            1520.0,
            85.0,
            22.0
          ],
          "text": "delay 250"
        }
      },
      {
        "box": {
          "id": "obj-185",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1360.0,
            1440.0,
            180.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            930,
            680,
            180,
            22
          ],
          "text": "Factory Reset"
        }
      },
      {
        "box": {
          "id": "obj-186",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1360.0,
            1480.0,
            90.0,
            22.0
          ],
          "text": "reset"
        }
      },
      {
        "box": {
          "id": "obj-187",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1250.0,
            1340.0,
            260.0,
            22.0
          ],
          "text": "r open.v12.sound_dna"
        }
      },
      {
        "box": {
          "id": "obj-188",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1530.0,
            1340.0,
            60.0,
            22.0
          ],
          "text": "front"
        }
      },
      {
        "box": {
          "id": "obj-189",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1620.0,
            1340.0,
            100.0,
            22.0
          ],
          "text": "thispatcher"
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
            "obj-15",
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
            "obj-19",
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
            "obj-19",
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
            "obj-14",
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
            "obj-15",
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
            "obj-23",
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
            "obj-15",
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
            "obj-29",
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
            "obj-14",
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
            "obj-31",
            0
          ],
          "source": [
            "obj-15",
            3
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
            "obj-32",
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
            "obj-31",
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
            "obj-15",
            4
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
            "obj-15",
            5
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
            "obj-41",
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
            "obj-14",
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
            "obj-17",
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
            "obj-15",
            6
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
            "obj-43",
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
            "obj-15",
            7
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
            "obj-48",
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
            "obj-47",
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
            "obj-15",
            8
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
            "obj-52",
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
            "obj-14",
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
            "obj-55",
            0
          ],
          "source": [
            "obj-15",
            9
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
            "obj-56",
            0
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
            "obj-55",
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
            "obj-57",
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
            "obj-15",
            10
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
            "obj-60",
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
            "obj-14",
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
            "obj-63",
            0
          ],
          "source": [
            "obj-15",
            11
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
            "obj-64",
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
            "obj-63",
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
            "obj-15",
            12
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
            "obj-68",
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
            "obj-67",
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
            "obj-69",
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
            "obj-15",
            13
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
            "obj-72",
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
            "obj-71",
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
            "obj-15",
            14
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
            "obj-76",
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
            "obj-75",
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
            "obj-77",
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
            "obj-15",
            15
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
            "obj-80",
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
            "obj-79",
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
            "obj-81",
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
            "obj-15",
            16
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
            "obj-83",
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
            "obj-85",
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
            "obj-15",
            17
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
            "obj-88",
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
            "obj-87",
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
            "obj-15",
            18
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
            "obj-92",
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
            "obj-91",
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
            "obj-93",
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
            "obj-15",
            19
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
            "obj-96",
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
            "obj-95",
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
            "obj-15",
            20
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
            "obj-99",
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
            "obj-101",
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
            "obj-15",
            21
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
            "obj-104",
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
            "obj-103",
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
            "obj-15",
            22
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
            "obj-107",
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
            "obj-15",
            23
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
            "obj-111",
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
            "obj-113",
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
            "obj-15",
            24
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
            "obj-116",
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
            "obj-115",
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
            "obj-117",
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
            "obj-15",
            25
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
            "obj-120",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-121",
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
            "obj-14",
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
            "obj-122",
            0
          ],
          "source": [
            "obj-15",
            26
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
            "obj-122",
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
            "obj-123",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-124",
            0
          ],
          "source": [
            "obj-15",
            27
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
            "obj-14",
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
            "obj-126",
            0
          ],
          "source": [
            "obj-15",
            28
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
            "obj-14",
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
            "obj-128",
            0
          ],
          "source": [
            "obj-15",
            29
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
            "obj-14",
            0
          ],
          "source": [
            "obj-129",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-130",
            0
          ],
          "source": [
            "obj-15",
            30
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-131",
            0
          ],
          "source": [
            "obj-130",
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
            "obj-131",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-132",
            0
          ],
          "source": [
            "obj-15",
            31
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-133",
            0
          ],
          "source": [
            "obj-132",
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
            "obj-133",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-134",
            0
          ],
          "source": [
            "obj-15",
            32
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-135",
            0
          ],
          "source": [
            "obj-134",
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
            "obj-135",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-136",
            0
          ],
          "source": [
            "obj-15",
            34
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-136",
            0
          ],
          "source": [
            "obj-138",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-141",
            0
          ],
          "source": [
            "obj-136",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-142",
            0
          ],
          "source": [
            "obj-141",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-143",
            0
          ],
          "source": [
            "obj-142",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-144",
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
            "obj-144",
            1
          ],
          "source": [
            "obj-143",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-145",
            0
          ],
          "source": [
            "obj-144",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-139",
            0
          ],
          "source": [
            "obj-145",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-147",
            0
          ],
          "source": [
            "obj-136",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-148",
            0
          ],
          "source": [
            "obj-147",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-149",
            0
          ],
          "source": [
            "obj-148",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-150",
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
            "obj-150",
            1
          ],
          "source": [
            "obj-149",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-151",
            0
          ],
          "source": [
            "obj-150",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-139",
            1
          ],
          "source": [
            "obj-151",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-153",
            0
          ],
          "source": [
            "obj-136",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-154",
            0
          ],
          "source": [
            "obj-153",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-155",
            0
          ],
          "source": [
            "obj-154",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-156",
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
            "obj-156",
            1
          ],
          "source": [
            "obj-155",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-157",
            0
          ],
          "source": [
            "obj-156",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-139",
            2
          ],
          "source": [
            "obj-157",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-159",
            0
          ],
          "source": [
            "obj-136",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-160",
            0
          ],
          "source": [
            "obj-159",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-161",
            0
          ],
          "source": [
            "obj-160",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-162",
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
            "obj-162",
            1
          ],
          "source": [
            "obj-161",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-163",
            0
          ],
          "source": [
            "obj-162",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-139",
            3
          ],
          "source": [
            "obj-163",
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
            "obj-139",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-165",
            0
          ],
          "source": [
            "obj-136",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-166",
            0
          ],
          "source": [
            "obj-165",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-167",
            0
          ],
          "source": [
            "obj-166",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-168",
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
            "obj-168",
            1
          ],
          "source": [
            "obj-167",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-17",
            1
          ],
          "source": [
            "obj-168",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-169",
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
            "obj-169",
            1
          ],
          "source": [
            "obj-167",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-17",
            2
          ],
          "source": [
            "obj-169",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-17",
            3
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
            "obj-170",
            0
          ],
          "source": [
            "obj-15",
            33
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-170",
            0
          ],
          "source": [
            "obj-174",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-171",
            0
          ],
          "source": [
            "obj-170",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-172",
            0
          ],
          "source": [
            "obj-171",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-173",
            0
          ],
          "source": [
            "obj-172",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-175",
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
            "obj-175",
            1
          ],
          "source": [
            "obj-173",
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
            "obj-175",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-176",
            0
          ],
          "source": [
            "obj-17",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-176",
            1
          ],
          "source": [
            "obj-173",
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
            "obj-176",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-178",
            0
          ],
          "source": [
            "obj-179",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-181",
            0
          ],
          "source": [
            "obj-180",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-181",
            0
          ],
          "source": [
            "obj-15",
            35
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-179",
            0
          ],
          "source": [
            "obj-181",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-183",
            0
          ],
          "source": [
            "obj-182",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-183",
            0
          ],
          "source": [
            "obj-15",
            36
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-179",
            0
          ],
          "source": [
            "obj-183",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-184",
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
            "obj-183",
            0
          ],
          "source": [
            "obj-184",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-186",
            0
          ],
          "source": [
            "obj-185",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-186",
            0
          ],
          "source": [
            "obj-15",
            37
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-179",
            0
          ],
          "source": [
            "obj-186",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-188",
            0
          ],
          "source": [
            "obj-187",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-189",
            0
          ],
          "source": [
            "obj-188",
            0
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "parameters": {
      "obj-139::obj-29": [
        "V3_Group_Mixer.3",
        "V3_Group_Mixer.3",
        0
      ],
      "obj-139::obj-32": [
        "V3_Group_Mixer.2",
        "V3_Group_Mixer.2",
        0
      ],
      "obj-139::obj-33": [
        "V3_Group_Mixer.4",
        "V3_Group_Mixer.4",
        0
      ],
      "obj-139::obj-37": [
        "V3_Group_Mixer.Mute",
        "V3_Group_Mixer.Mute",
        0
      ],
      "obj-139::obj-39": [
        "V3_Group_Mixer.1",
        "V3_Group_Mixer.1",
        0
      ],
      "obj-139::obj-49": [
        "V3_Group_Mixer.MuteCh1",
        "V3_Group_Mixer.MuteCh1",
        0
      ],
      "obj-139::obj-58": [
        "V3_Group_Mixer.MuteCh2",
        "V3_Group_Mixer.MuteCh2",
        0
      ],
      "obj-139::obj-64": [
        "V3_Group_Mixer.MuteCh3",
        "V3_Group_Mixer.MuteCh3",
        0
      ],
      "obj-139::obj-70": [
        "V3_Group_Mixer.MuteCh4",
        "V3_Group_Mixer.MuteCh4",
        0
      ],
      "obj-145::obj-11": [
        "V3_Core.Res",
        "V3_Core.Res",
        0
      ],
      "obj-145::obj-20": [
        "V3_Core.Freq",
        "V3_Core.Freq",
        0
      ],
      "obj-145::obj-22": [
        "V3_Core.TimeMode",
        "V3_Core.TimeMode",
        1
      ],
      "obj-145::obj-23": [
        "V3_Core.Offset",
        "V3_Core.Offset",
        0
      ],
      "obj-145::obj-38": [
        "V3_Core.FilterType",
        "V3_Core.FilterType",
        0
      ],
      "obj-145::obj-51": [
        "V3_Core.CV2",
        "V3_Core.CV2",
        0
      ],
      "obj-145::obj-54": [
        "V3_Core.CV1",
        "V3_Core.CV1",
        0
      ],
      "obj-145::obj-55": [
        "V3_Core.power",
        "V3_Core.power",
        0
      ],
      "obj-145::obj-63": [
        "V3_Core.CV3",
        "V3_Core.CV3",
        0
      ],
      "obj-145::obj-95": [
        "V3_Core.ResCV",
        "V3_Core.CV",
        0
      ],
      "obj-151::obj-11": [
        "V3_Body.Res",
        "V3_Body.Res",
        0
      ],
      "obj-151::obj-20": [
        "V3_Body.Freq",
        "V3_Body.Freq",
        0
      ],
      "obj-151::obj-22": [
        "V3_Body.TimeMode",
        "V3_Body.TimeMode",
        1
      ],
      "obj-151::obj-23": [
        "V3_Body.Offset",
        "V3_Body.Offset",
        0
      ],
      "obj-151::obj-38": [
        "V3_Body.FilterType",
        "V3_Body.FilterType",
        0
      ],
      "obj-151::obj-51": [
        "V3_Body.CV2",
        "V3_Body.CV2",
        0
      ],
      "obj-151::obj-54": [
        "V3_Body.CV1",
        "V3_Body.CV1",
        0
      ],
      "obj-151::obj-55": [
        "V3_Body.power",
        "V3_Body.power",
        0
      ],
      "obj-151::obj-63": [
        "V3_Body.CV3",
        "V3_Body.CV3",
        0
      ],
      "obj-151::obj-95": [
        "V3_Body.ResCV",
        "V3_Body.CV",
        0
      ],
      "obj-157::obj-11": [
        "V3_Character.Res",
        "V3_Character.Res",
        0
      ],
      "obj-157::obj-20": [
        "V3_Character.Freq",
        "V3_Character.Freq",
        0
      ],
      "obj-157::obj-22": [
        "V3_Character.TimeMode",
        "V3_Character.TimeMode",
        1
      ],
      "obj-157::obj-23": [
        "V3_Character.Offset",
        "V3_Character.Offset",
        0
      ],
      "obj-157::obj-38": [
        "V3_Character.FilterType",
        "V3_Character.FilterType",
        0
      ],
      "obj-157::obj-51": [
        "V3_Character.CV2",
        "V3_Character.CV2",
        0
      ],
      "obj-157::obj-54": [
        "V3_Character.CV1",
        "V3_Character.CV1",
        0
      ],
      "obj-157::obj-55": [
        "V3_Character.power",
        "V3_Character.power",
        0
      ],
      "obj-157::obj-63": [
        "V3_Character.CV3",
        "V3_Character.CV3",
        0
      ],
      "obj-157::obj-95": [
        "V3_Character.ResCV",
        "V3_Character.CV",
        0
      ],
      "obj-163::obj-11": [
        "V3_Upper.Res",
        "V3_Upper.Res",
        0
      ],
      "obj-163::obj-20": [
        "V3_Upper.Freq",
        "V3_Upper.Freq",
        0
      ],
      "obj-163::obj-22": [
        "V3_Upper.TimeMode",
        "V3_Upper.TimeMode",
        1
      ],
      "obj-163::obj-23": [
        "V3_Upper.Offset",
        "V3_Upper.Offset",
        0
      ],
      "obj-163::obj-38": [
        "V3_Upper.FilterType",
        "V3_Upper.FilterType",
        0
      ],
      "obj-163::obj-51": [
        "V3_Upper.CV2",
        "V3_Upper.CV2",
        0
      ],
      "obj-163::obj-54": [
        "V3_Upper.CV1",
        "V3_Upper.CV1",
        0
      ],
      "obj-163::obj-55": [
        "V3_Upper.power",
        "V3_Upper.power",
        0
      ],
      "obj-163::obj-63": [
        "V3_Upper.CV3",
        "V3_Upper.CV3",
        0
      ],
      "obj-163::obj-95": [
        "V3_Upper.ResCV",
        "V3_Upper.CV",
        0
      ],
      "parameterbanks": {}
    },
    "rect": [
      50.0,
      50.0,
      1860,
      1650
    ],
    "toolbarvisible": 1
  }
}
