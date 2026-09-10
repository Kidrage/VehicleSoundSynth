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
            25.0,
            15.0,
            1050.0,
            22.0
          ],
          "text": "V12 USER-TUNABLE SOUND DNA \u2014 synthesis controls only; state/RPM remain drivetrain-owned"
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
            35.0,
            60.0,
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
          "numoutlets": 24,
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
            ""
          ],
          "patching_rect": [
            35.0,
            100.0,
            1160.0,
            22.0
          ],
          "text": "route aggression brightness body texture air_detail cycle_irregularity stereo_width throttle_loudness_depth saturation idle_level idle_body idle_metal idle_irregularity idle_air idle_width combustion_pulse intake_detail exhaust_detail residual_detail running_body running_cavity hf_softness release_mass"
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
            475.0,
            850.0,
            175.0,
            22.0
          ],
          "text": "v12_powertrain_v2~"
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
            475.0,
            1030.0,
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
            675.0,
            1030.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-7",
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
            930.0,
            15.0,
            155.0,
            22.0
          ],
          "text": "autopattr @autorestore 0"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            760.0,
            15.0,
            160.0,
            22.0
          ],
          "text": "r open.v12.sound_dna"
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
            760.0,
            45.0,
            45.0,
            22.0
          ],
          "text": "front"
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
            815.0,
            45.0,
            75.0,
            22.0
          ],
          "text": "thispatcher"
        }
      },
      {
        "box": {
          "id": "obj-11",
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
            930.0,
            50.0,
            300.0,
            22.0
          ],
          "text": "pattrstorage v12_sound_dna_v2 @savemode 0 @changemode 1 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            930.0,
            85.0,
            260.0,
            22.0
          ],
          "text": "js Patcher:/code/dna_v2_state_path.js v12"
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
            930.0,
            120.0,
            60.0,
            22.0
          ],
          "text": "loadbang"
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1000.0,
            120.0,
            70.0,
            22.0
          ],
          "text": "delay 140"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1080.0,
            120.0,
            50.0,
            22.0
          ],
          "text": "t b b"
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
            1140.0,
            120.0,
            55.0,
            22.0
          ],
          "text": "restore"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1080.0,
            155.0,
            65.0,
            22.0
          ],
          "text": "delay 35"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1155.0,
            155.0,
            30.0,
            22.0
          ],
          "text": "1"
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
            930.0,
            190.0,
            45.0,
            22.0
          ],
          "text": "save"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            985.0,
            190.0,
            65.0,
            22.0
          ],
          "text": "closebang"
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
            1080.0,
            210.0,
            75.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1090.0,
            990.0,
            80.0,
            22.0
          ],
          "text": "Reset DNA"
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
            930.0,
            210.0,
            70.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            910.0,
            990.0,
            75.0,
            22.0
          ],
          "text": "Save DNA"
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
            1005.0,
            210.0,
            80.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            995.0,
            990.0,
            85.0,
            22.0
          ],
          "text": "Reload DNA"
        }
      },
      {
        "box": {
          "id": "obj-24",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1090.0,
            945.0,
            65.0,
            22.0
          ],
          "text": "delay 50"
        }
      },
      {
        "box": {
          "id": "obj-25",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            925.0,
            1100.0,
            40.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35.0,
            925.0,
            1100.0,
            40.0
          ],
          "text": "V2 \u8c03\u53c2\u987a\u5e8f\uff1aRunning Body \u2192 Running Cavity \u2192 HF Softness \u2192 Release Mass\u3002\u22641200 RPM \u4fdd\u7559\u539f\u58f0\uff1b1200\u20133000 RPM \u5e73\u6ed1\u8fdb\u5165\u65b0\u7ed3\u6784\u3002"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            135.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            135,
            285.0,
            20.0
          ],
          "text": "Response / \u54cd\u5e94 \u00b7 Aggression / \u6fc0\u8fdb\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-27",
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
            35.0,
            159.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            159,
            90.0,
            22.0
          ],
          "varname": "dna_aggression"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            159.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            157,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load / \u52a0\u901f \u2014 \u589e\u52a0\u8d1f\u8f7d\u54cd\u5e94\u4e0e\u52a8\u6001\u5b58\u5728\u611f"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            135.0,
            203.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            230.0,
            203.0,
            100.0,
            22.0
          ],
          "text": "prepend aggression"
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
            35.0,
            203.0,
            65.0,
            22.0
          ],
          "text": "0.62"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            135.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            135,
            285.0,
            20.0
          ],
          "text": "Tone / \u97f3\u8272 \u00b7 Brightness / \u660e\u4eae\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-33",
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
            335.0,
            159.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            159,
            90.0,
            22.0
          ],
          "varname": "dna_brightness"
        }
      },
      {
        "box": {
          "id": "obj-34",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            159.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            157,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: High RPM / \u9ad8\u8f6c \u2014 \u63d0\u5347\u9ad8\u9636\u8c10\u6ce2\uff0c\u4e0d\u76f4\u63a5\u6539\u53d8\u4e3b\u97f3\u9ad8"
        }
      },
      {
        "box": {
          "id": "obj-35",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            435.0,
            203.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            530.0,
            203.0,
            100.0,
            22.0
          ],
          "text": "prepend brightness"
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
            335.0,
            203.0,
            65.0,
            22.0
          ],
          "text": "0.78"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            135.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            135,
            285.0,
            20.0
          ],
          "text": "Body / \u4e3b\u4f53 \u00b7 Body / \u539a\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-39",
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
            635.0,
            159.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            159,
            90.0,
            22.0
          ],
          "varname": "dna_body"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            159.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            157,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle + Cruise / \u6020\u901f\u5de1\u822a \u2014 \u586b\u5145\u4f4e\u9891\u4e0e\u4e2d\u4f4e\u9891\u4e3b\u4f53"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            203.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            203.0,
            100.0,
            22.0
          ],
          "text": "prepend body"
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
            635.0,
            203.0,
            65.0,
            22.0
          ],
          "text": "0.72"
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            935.0,
            135.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            135,
            285.0,
            20.0
          ],
          "text": "Structure / \u7ed3\u6784 \u00b7 Texture / \u7ed3\u6784\u7eb9\u7406 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-45",
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
            935.0,
            159.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            159,
            90.0,
            22.0
          ],
          "varname": "dna_texture"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1031.0,
            159.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1031,
            157,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load / \u8d1f\u8f7d \u2014 \u589e\u52a0\u673a\u68b0\u4e0e\u8868\u9762\u7ec6\u8282"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            203.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            1130.0,
            203.0,
            100.0,
            22.0
          ],
          "text": "prepend texture"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            935.0,
            203.0,
            65.0,
            22.0
          ],
          "text": "0.52"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            245.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            245,
            285.0,
            20.0
          ],
          "text": "Air / \u7a7a\u6c14 \u00b7 Air Detail / \u7a7a\u6c14\u7ec6\u8282 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-51",
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
            35.0,
            269.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            269,
            90.0,
            22.0
          ],
          "varname": "dna_air_detail"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            269.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            267,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: High RPM / \u9ad8\u8f6c \u2014 \u63a7\u5236\u9ad8\u9891\u7a7a\u6c14\u5c42"
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            135.0,
            313.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            230.0,
            313.0,
            100.0,
            22.0
          ],
          "text": "prepend air_detail"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            35.0,
            313.0,
            65.0,
            22.0
          ],
          "text": "0.68"
        }
      },
      {
        "box": {
          "id": "obj-56",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            245.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            245,
            285.0,
            20.0
          ],
          "text": "Motion / \u5f8b\u52a8 \u00b7 Cycle Irregularity / \u5468\u671f\u4e0d\u89c4\u5219\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-57",
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
            335.0,
            269.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            269,
            90.0,
            22.0
          ],
          "varname": "dna_cycle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-58",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            269.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            267,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u6539\u53d8\u5fae\u5c0f\u5468\u671f\u8d77\u4f0f\uff0c\u4e0d\u6539\u53d8\u5e73\u5747\u8f6c\u901f"
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
            435.0,
            313.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            530.0,
            313.0,
            100.0,
            22.0
          ],
          "text": "prepend cycle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-61",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            335.0,
            313.0,
            65.0,
            22.0
          ],
          "text": "0.34"
        }
      },
      {
        "box": {
          "id": "obj-62",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            245.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            245,
            285.0,
            20.0
          ],
          "text": "Space / \u7a7a\u95f4 \u00b7 Stereo / Bank Separation / \u7acb\u4f53\u58f0\u5bbd\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-63",
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
            635.0,
            269.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            269,
            90.0,
            22.0
          ],
          "varname": "dna_stereo_width"
        }
      },
      {
        "box": {
          "id": "obj-64",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            269.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            267,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: All / \u5168\u573a\u666f \u2014 \u63a7\u5236\u4e2d\u9ad8\u9891\u58f0\u50cf\u4e0e\u7f38\u7ec4\u5206\u79bb"
        }
      },
      {
        "box": {
          "id": "obj-65",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            313.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-66",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            313.0,
            100.0,
            22.0
          ],
          "text": "prepend stereo_width"
        }
      },
      {
        "box": {
          "id": "obj-67",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            313.0,
            65.0,
            22.0
          ],
          "text": "0.64"
        }
      },
      {
        "box": {
          "id": "obj-68",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            935.0,
            245.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            245,
            285.0,
            20.0
          ],
          "text": "Response / \u54cd\u5e94 \u00b7 Throttle Loudness Depth dB / \u6cb9\u95e8\u54cd\u5ea6\u6df1\u5ea6 [dB]"
        }
      },
      {
        "box": {
          "id": "obj-69",
          "maxclass": "flonum",
          "maximum": 8.0,
          "minimum": 0.0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            935.0,
            269.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            269,
            90.0,
            22.0
          ],
          "varname": "dna_throttle_loudness_depth"
        }
      },
      {
        "box": {
          "id": "obj-70",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1031.0,
            269.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1031,
            267,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load / \u52a0\u901f \u2014 \u6cb9\u95e8\u4ece 0 \u5230 1 \u7684\u54cd\u5ea6\u589e\u91cf"
        }
      },
      {
        "box": {
          "id": "obj-71",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            313.0,
            90.0,
            22.0
          ],
          "text": "clip 0 8"
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
            1130.0,
            313.0,
            100.0,
            22.0
          ],
          "text": "prepend throttle_loudness_depth"
        }
      },
      {
        "box": {
          "id": "obj-73",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            935.0,
            313.0,
            65.0,
            22.0
          ],
          "text": "4.5"
        }
      },
      {
        "box": {
          "id": "obj-74",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            355.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            355,
            285.0,
            20.0
          ],
          "text": "Dynamics / \u52a8\u6001 \u00b7 Saturation / \u9971\u548c\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-75",
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
            35.0,
            379.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            379,
            90.0,
            22.0
          ],
          "varname": "dna_saturation"
        }
      },
      {
        "box": {
          "id": "obj-76",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            379.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            377,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load / \u9ad8\u8d1f\u8f7d \u2014 \u589e\u52a0\u5bc6\u5ea6\u4e0e\u8f6f\u524a\u6ce2\u5f3a\u5ea6"
        }
      },
      {
        "box": {
          "id": "obj-77",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            135.0,
            423.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            230.0,
            423.0,
            100.0,
            22.0
          ],
          "text": "prepend saturation"
        }
      },
      {
        "box": {
          "id": "obj-79",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            35.0,
            423.0,
            65.0,
            22.0
          ],
          "text": "0.28"
        }
      },
      {
        "box": {
          "id": "obj-80",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            355.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            355,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Level / \u6020\u901f\u5c42\u7535\u5e73 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-81",
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
            335.0,
            379.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            379,
            90.0,
            22.0
          ],
          "varname": "dna_idle_level"
        }
      },
      {
        "box": {
          "id": "obj-82",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            379.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            377,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u4e13\u7528\u6020\u901f\u5c42\u603b\u4f53\u5b58\u5728\u611f"
        }
      },
      {
        "box": {
          "id": "obj-83",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            435.0,
            423.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            530.0,
            423.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_level"
        }
      },
      {
        "box": {
          "id": "obj-85",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            335.0,
            423.0,
            65.0,
            22.0
          ],
          "text": "0.78"
        }
      },
      {
        "box": {
          "id": "obj-86",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            355.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            355,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Body / \u6020\u901f\u4e3b\u4f53 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-87",
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
            635.0,
            379.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            379,
            90.0,
            22.0
          ],
          "varname": "dna_idle_body"
        }
      },
      {
        "box": {
          "id": "obj-88",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            379.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            377,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u6020\u901f\u4f4e\u9891\u4e0e\u4e2d\u4f4e\u9891\u6a21\u6001"
        }
      },
      {
        "box": {
          "id": "obj-89",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            423.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-90",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            423.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_body"
        }
      },
      {
        "box": {
          "id": "obj-91",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            423.0,
            65.0,
            22.0
          ],
          "text": "0.86"
        }
      },
      {
        "box": {
          "id": "obj-92",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            935.0,
            355.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            355,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Metal / \u6020\u901f\u91d1\u5c5e [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-93",
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
            935.0,
            379.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            379,
            90.0,
            22.0
          ],
          "varname": "dna_idle_metal"
        }
      },
      {
        "box": {
          "id": "obj-94",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1031.0,
            379.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1031,
            377,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u6020\u901f\u7ed3\u6784\u4e0e\u91d1\u5c5e\u4fa7\u5e26"
        }
      },
      {
        "box": {
          "id": "obj-95",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            423.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            1130.0,
            423.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_metal"
        }
      },
      {
        "box": {
          "id": "obj-97",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            935.0,
            423.0,
            65.0,
            22.0
          ],
          "text": "0.58"
        }
      },
      {
        "box": {
          "id": "obj-98",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            465.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            465,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Irregularity / \u6020\u901f\u4e0d\u89c4\u5219\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-99",
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
            35.0,
            489.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            489,
            90.0,
            22.0
          ],
          "varname": "dna_idle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-100",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            489.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            487,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u71c3\u70e7/\u7535\u78c1\u80fd\u91cf\u7684\u7ec6\u5fae\u6ce2\u52a8"
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
            135.0,
            533.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-102",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            230.0,
            533.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_irregularity"
        }
      },
      {
        "box": {
          "id": "obj-103",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            35.0,
            533.0,
            65.0,
            22.0
          ],
          "text": "0.18"
        }
      },
      {
        "box": {
          "id": "obj-104",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            465.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            465,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Air / \u6020\u901f\u7a7a\u6c14 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-105",
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
            335.0,
            489.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            489,
            90.0,
            22.0
          ],
          "varname": "dna_idle_air"
        }
      },
      {
        "box": {
          "id": "obj-106",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            489.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            487,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u6020\u901f\u9ad8\u9891\u7a7a\u6c14\u7ec6\u8282"
        }
      },
      {
        "box": {
          "id": "obj-107",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            435.0,
            533.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            530.0,
            533.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_air"
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
            335.0,
            533.0,
            65.0,
            22.0
          ],
          "text": "0.34"
        }
      },
      {
        "box": {
          "id": "obj-110",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            465.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            465,
            285.0,
            20.0
          ],
          "text": "Idle / \u6020\u901f \u00b7 Idle Width / \u6020\u901f\u5bbd\u5ea6 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-111",
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
            635.0,
            489.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            489,
            90.0,
            22.0
          ],
          "varname": "dna_idle_width"
        }
      },
      {
        "box": {
          "id": "obj-112",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            489.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            487,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle / \u6020\u901f \u2014 \u63a7\u5236\u6020\u901f\u4e2d\u9ad8\u9891\u7a7a\u95f4\u5bbd\u5ea6"
        }
      },
      {
        "box": {
          "id": "obj-113",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            533.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-114",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            533.0,
            100.0,
            22.0
          ],
          "text": "prepend idle_width"
        }
      },
      {
        "box": {
          "id": "obj-115",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            533.0,
            65.0,
            22.0
          ],
          "text": "0.52"
        }
      },
      {
        "box": {
          "id": "obj-116",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            935.0,
            465.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            465,
            285.0,
            20.0
          ],
          "text": "Combustion / \u71c3\u70e7 \u00b7 Combustion Pulse / \u71c3\u70e7\u8109\u51b2 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-117",
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
            935.0,
            489.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            489,
            90.0,
            22.0
          ],
          "varname": "dna_combustion_pulse"
        }
      },
      {
        "box": {
          "id": "obj-118",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1031.0,
            489.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1031,
            487,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Idle + Load / \u6020\u901f\u8d1f\u8f7d \u2014 \u63a7\u5236\u70b9\u706b\u8109\u51b2\u7684\u51b2\u51fb\u4e0e\u8f6e\u5ed3"
        }
      },
      {
        "box": {
          "id": "obj-119",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            533.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            1130.0,
            533.0,
            100.0,
            22.0
          ],
          "text": "prepend combustion_pulse"
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
            935.0,
            533.0,
            65.0,
            22.0
          ],
          "text": "0.8"
        }
      },
      {
        "box": {
          "id": "obj-122",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            575.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            575,
            285.0,
            20.0
          ],
          "text": "Intake / \u8fdb\u6c14 \u00b7 Intake Detail / \u8fdb\u6c14\u7ec6\u8282 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-123",
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
            35.0,
            599.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            599,
            90.0,
            22.0
          ],
          "varname": "dna_intake_detail"
        }
      },
      {
        "box": {
          "id": "obj-124",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            599.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            597,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load / \u52a0\u901f \u2014 \u63a7\u5236\u8fdb\u6c14\u9636\u6b21\u4e0e\u8d1f\u8f7d\u547c\u5438"
        }
      },
      {
        "box": {
          "id": "obj-125",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            135.0,
            643.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            230.0,
            643.0,
            100.0,
            22.0
          ],
          "text": "prepend intake_detail"
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
            35.0,
            643.0,
            65.0,
            22.0
          ],
          "text": "0.68"
        }
      },
      {
        "box": {
          "id": "obj-128",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            575.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            575,
            285.0,
            20.0
          ],
          "text": "Exhaust / \u6392\u6c14 \u00b7 Exhaust Detail / \u6392\u6c14\u7ec6\u8282 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-129",
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
            335.0,
            599.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            599,
            90.0,
            22.0
          ],
          "varname": "dna_exhaust_detail"
        }
      },
      {
        "box": {
          "id": "obj-130",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            599.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            597,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: Load + Lift / \u8d1f\u8f7d\u6536\u6cb9 \u2014 \u63a7\u5236\u6392\u6c14\u9636\u6b21\u4e0e\u6536\u6cb9\u80fd\u91cf"
        }
      },
      {
        "box": {
          "id": "obj-131",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            435.0,
            643.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            530.0,
            643.0,
            100.0,
            22.0
          ],
          "text": "prepend exhaust_detail"
        }
      },
      {
        "box": {
          "id": "obj-133",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            335.0,
            643.0,
            65.0,
            22.0
          ],
          "text": "0.62"
        }
      },
      {
        "box": {
          "id": "obj-134",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            575.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            575,
            285.0,
            20.0
          ],
          "text": "Combustion / \u71c3\u70e7 \u00b7 Residual Detail / \u6b8b\u4f59\u7ed3\u6784 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-135",
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
            635.0,
            599.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            599,
            90.0,
            22.0
          ],
          "varname": "dna_residual_detail"
        }
      },
      {
        "box": {
          "id": "obj-136",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            599.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            597,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: All running / \u8fd0\u8f6c \u2014 \u63a7\u5236\u8109\u51b2\u540e\u7684\u673a\u68b0\u4f59\u632f"
        }
      },
      {
        "box": {
          "id": "obj-137",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            643.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
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
            830.0,
            643.0,
            100.0,
            22.0
          ],
          "text": "prepend residual_detail"
        }
      },
      {
        "box": {
          "id": "obj-139",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            643.0,
            65.0,
            22.0
          ],
          "text": "0.64"
        }
      },
      {
        "box": {
          "id": "obj-140",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            935.0,
            575.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            575,
            285.0,
            20.0
          ],
          "text": "Running / \u8fd0\u8f6c \u00b7 Running Body / 120\u2013350 Hz \u4e3b\u4f53 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-141",
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
            935.0,
            599.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            935,
            599,
            90.0,
            22.0
          ],
          "varname": "dna_running_body"
        }
      },
      {
        "box": {
          "id": "obj-142",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1031.0,
            599.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            1031,
            597,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: >1200 RPM / \u52a0\u901f \u2014 \u5efa\u8bae 0.5\u20130.9\uff1b\u71c3\u70e7\u6fc0\u53d1\u4e3b\u4f53\uff0c\u4e0d\u6539\u53d8\u539f\u6020\u901f"
        }
      },
      {
        "box": {
          "id": "obj-143",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1035.0,
            643.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-144",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1130.0,
            643.0,
            100.0,
            22.0
          ],
          "text": "prepend running_body"
        }
      },
      {
        "box": {
          "id": "obj-145",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            935.0,
            643.0,
            65.0,
            22.0
          ],
          "text": "0.88"
        }
      },
      {
        "box": {
          "id": "obj-146",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            35.0,
            685.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            685,
            285.0,
            20.0
          ],
          "text": "Running / \u8fd0\u8f6c \u00b7 Running Cavity / 250\u2013650 Hz \u8154\u4f53 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-147",
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
            35.0,
            709.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            35,
            709,
            90.0,
            22.0
          ],
          "varname": "dna_running_cavity"
        }
      },
      {
        "box": {
          "id": "obj-148",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            131.0,
            709.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            131,
            707,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: >1200 RPM / \u8d1f\u8f7d \u2014 \u5efa\u8bae 0.4\u20130.8\uff1b\u8fdb\u6392\u6c14\u8154\u4f53\uff0c\u4e0d\u6539\u53d8\u4e3b\u97f3\u9ad8"
        }
      },
      {
        "box": {
          "id": "obj-149",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            135.0,
            753.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-150",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            230.0,
            753.0,
            100.0,
            22.0
          ],
          "text": "prepend running_cavity"
        }
      },
      {
        "box": {
          "id": "obj-151",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            35.0,
            753.0,
            65.0,
            22.0
          ],
          "text": "0.66"
        }
      },
      {
        "box": {
          "id": "obj-152",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            335.0,
            685.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            685,
            285.0,
            20.0
          ],
          "text": "Running / \u8fd0\u8f6c \u00b7 HF Softness / \u9ad8\u9891\u67d4\u5316 [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-153",
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
            335.0,
            709.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            335,
            709,
            90.0,
            22.0
          ],
          "varname": "dna_hf_softness"
        }
      },
      {
        "box": {
          "id": "obj-154",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            431.0,
            709.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            431,
            707,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: >1200 RPM / \u9ad8\u8f6c \u2014 \u5efa\u8bae 0.7\u20131\uff1b\u8d8a\u5927\u8d8a\u67d4\u548c\uff0c\u4e0d\u662f\u603b\u97f3\u91cf"
        }
      },
      {
        "box": {
          "id": "obj-155",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            435.0,
            753.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-156",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            530.0,
            753.0,
            100.0,
            22.0
          ],
          "text": "prepend hf_softness"
        }
      },
      {
        "box": {
          "id": "obj-157",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            335.0,
            753.0,
            65.0,
            22.0
          ],
          "text": "0.88"
        }
      },
      {
        "box": {
          "id": "obj-158",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            635.0,
            685.0,
            285.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            685,
            285.0,
            20.0
          ],
          "text": "Running / \u8fd0\u8f6c \u00b7 Release Mass / \u6536\u6cb9\u8d28\u91cf\u611f [0..1]"
        }
      },
      {
        "box": {
          "id": "obj-159",
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
            635.0,
            709.0,
            90.0,
            22.0
          ],
          "presentation": 1,
          "presentation_rect": [
            635,
            709,
            90.0,
            22.0
          ],
          "varname": "dna_release_mass"
        }
      },
      {
        "box": {
          "id": "obj-160",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            731.0,
            709.0,
            194.0,
            38.0
          ],
          "presentation": 1,
          "presentation_rect": [
            731,
            707,
            194.0,
            40.0
          ],
          "text": "Audible / \u53ef\u542c: >1200 RPM / \u6536\u6cb9 \u2014 \u5efa\u8bae 0.4\u20130.8\uff1b\u4f4e\u4e2d\u9891\u7f13\u91ca\uff0c\u9ad8\u9891\u5148\u9000"
        }
      },
      {
        "box": {
          "id": "obj-161",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            735.0,
            753.0,
            90.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-162",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            830.0,
            753.0,
            100.0,
            22.0
          ],
          "text": "prepend release_mass"
        }
      },
      {
        "box": {
          "id": "obj-163",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            635.0,
            753.0,
            65.0,
            22.0
          ],
          "text": "0.76"
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
            "obj-3",
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
            "obj-4",
            0
          ],
          "source": [
            "obj-3",
            23
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
            1
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
            "obj-16",
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
            "obj-12",
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
          "source": [
            "obj-17",
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
            "obj-20",
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
            "obj-19",
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
            "obj-22",
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
            "obj-21",
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
            "obj-3",
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
            "obj-30",
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
            "obj-4",
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
          "source": [
            "obj-21",
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
            "obj-3",
            1
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
            "obj-33",
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
            "obj-4",
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
            "obj-13",
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
            "obj-3",
            2
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            3
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
            "obj-48",
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            4
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
            "obj-54",
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
            "obj-4",
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
            "obj-55",
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
            "obj-55",
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
            "obj-51",
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
            "obj-57",
            0
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            6
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
            "obj-4",
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
            "obj-67",
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
            "obj-67",
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
            "obj-63",
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
            "obj-3",
            7
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            8
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-79",
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
            "obj-3",
            9
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            10
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
            "obj-90",
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
            "obj-4",
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
            "obj-91",
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
            "obj-87",
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
            "obj-3",
            11
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
            "obj-93",
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
            "obj-95",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            12
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
            "obj-4",
            0
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
            "obj-103",
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
            "obj-103",
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
            "obj-99",
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
            "obj-3",
            13
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
            "obj-108",
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
            "obj-4",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            14
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
            "obj-4",
            0
          ],
          "source": [
            "obj-114",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            15
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
            "obj-117",
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
            "obj-119",
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
            "obj-13",
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
            "obj-21",
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
            "obj-121",
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
            "obj-3",
            16
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
            "obj-123",
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
            "obj-125",
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
            "obj-126",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            17
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
            "obj-129",
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
            "obj-131",
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
            "obj-132",
            0
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
            "obj-13",
            0
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
            "obj-21",
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
            "obj-133",
            0
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
            "obj-3",
            18
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-137",
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
            "obj-138",
            0
          ],
          "source": [
            "obj-137",
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
            "obj-138",
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
            "obj-13",
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
            "obj-21",
            0
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
            "obj-139",
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
            "obj-3",
            19
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
            "obj-141",
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
            "obj-143",
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
            "obj-144",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            20
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
            "obj-147",
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
            "obj-149",
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
            "obj-150",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            21
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
            "obj-153",
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
            "obj-155",
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
            "obj-156",
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
            "obj-13",
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
            "obj-21",
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
            "obj-3",
            22
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
            "obj-159",
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
            "obj-161",
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
            "obj-162",
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
            "obj-13",
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
            "obj-21",
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
            "obj-163",
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
            "obj-4",
            1
          ]
        }
      }
    ],
    "objectsnaponopen": 1,
    "openinpresentation": 1,
    "rect": [
      50.0,
      50.0,
      1280,
      1060
    ],
    "toolbarvisible": 1
  }
}
