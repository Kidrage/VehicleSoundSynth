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
            620.0,
            22.0
          ],
          "text": "vehicle_engine_ferrari~ — fixed-profile public seam"
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
            45.0,
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
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            45.0,
            105.0,
            165.0,
            22.0
          ],
          "text": "v7_engine_controller_ferrari",
          "varname": "engine_controller_ferrari"
        }
      },
      {
        "box": {
          "id": "obj-4",
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
            45.0,
            150.0,
            135.0,
            22.0
          ],
          "text": "t l l l l l l l"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 76,
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
            190.0,
            150.0,
            990.0,
            22.0
          ],
          "text": "route ignition start speed_kph rpm throttle brake load accel gear shift shift_dir overrun pop intake_backfire exhaust_pop click aggression brightness body texture air_detail cycle_irregularity stereo_width throttle_loudness_depth saturation idle_level idle_body idle_metal idle_irregularity idle_air idle_width torque_ripple_level gear_mesh_level electrical_detail combustion_pulse intake_detail exhaust_detail residual_detail cabin_width cabin_rumble exhaust_boom structure_vibration cabin_ir_mix powertrain_level_db start_level_db transient_level_db road_level_db rumble_level_db pad_level_db pad_mute pad_solo soundscape_enable soundscape_level_db soundscape_motion soundscape_space soundscape_solo dna_solo backfire_enable backfire_intensity backfire_solo reference_texture_level_db reference_texture_mute eq_low eq_lowmid eq_highmid eq_high eq_bypass master_trim_db compressor_threshold_db compressor_ratio compressor_attack_rate compressor_release_rate compressor_makeup_db compressor_bypass start_style"
        }
      },
      {
        "box": {
          "id": "obj-6",
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
            95.0,
            260.0,
            175.0,
            22.0
          ],
          "text": "v7_ferrari_acoustic_v5~",
          "varname": "ferrari_acoustic_v5~"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            ""
          ],
          "patching_rect": [
            95.0,
            305.0,
            220.0,
            22.0
          ],
          "text": "v7_ferrari_cinematic_soundscape_host~",
          "varname": "ferrari_cinematic_soundscape_host~"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            285.0,
            260.0,
            120.0,
            22.0
          ],
          "text": "v7_transient_ferrari~",
          "varname": "transient_ferrari~"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            625.0,
            260.0,
            110.0,
            22.0
          ],
          "text": "v7_cabin_rumble~",
          "varname": "cabin_rumble~"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            800.0,
            450.0,
            110.0,
            22.0
          ],
          "text": "v7_cabin_master~",
          "varname": "cabin_master~"
        }
      },
      {
        "box": {
          "args": [
            "ferrari"
          ],
          "id": "obj-11",
          "maxclass": "bpatcher",
          "name": "Patcher:/patchers/v7_vehicle_bus_eq~.maxpat",
          "numinlets": 3,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            460.0,
            495.0,
            970.0,
            340.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            15.0,
            970.0,
            340.0
          ],
          "varname": "vehicle_bus_eq~"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1030.0,
            500.0,
            110.0,
            22.0
          ],
          "text": "v7_mix_master~ ferrari",
          "varname": "mix_master~"
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            130.0,
            350.0,
            35.0,
            22.0
          ],
          "text": "+~"
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
            235.0,
            390.0,
            35.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            340.0,
            430.0,
            35.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            390.0,
            350.0,
            35.0,
            22.0
          ],
          "text": "+~"
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
            495.0,
            390.0,
            35.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            600.0,
            430.0,
            35.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-19",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1030.0,
            815.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "signal",
          "id": "obj-20",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1120.0,
            815.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "comment": "messages",
          "id": "obj-21",
          "maxclass": "outlet",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            1210.0,
            815.0,
            30.0,
            22.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-22",
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
            25.0,
            45.0,
            1180.0,
            22.0
          ],
          "text": "routepass eq_low eq_lowmid eq_highmid eq_high eq_bypass compressor_threshold_db compressor_ratio compressor_attack_rate compressor_release_rate compressor_makeup_db compressor_bypass"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            25.0,
            195.0,
            330.0,
            22.0
          ],
          "text": "js Patcher:/code/v7_design_control.js ferrari"
        }
      },
      {
        "box": {
          "id": "obj-24",
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
            980.0,
            175.0,
            365.0,
            22.0
          ],
          "text": "route save_profile_sound reload_profile_sound reset_profile_sound"
        }
      },
      {
        "box": {
          "id": "obj-25",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            980.0,
            205.0,
            50.0,
            22.0
          ],
          "text": "t b b"
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
            980.0,
            235.0,
            110.0,
            22.0
          ],
          "text": "soundscape_save"
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
            980.0,
            265.0,
            75.0,
            22.0
          ],
          "text": "eq_save"
        }
      },
      {
        "box": {
          "id": "obj-28",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1095.0,
            205.0,
            50.0,
            22.0
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1095.0,
            235.0,
            110.0,
            22.0
          ],
          "text": "soundscape_reload"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1095.0,
            265.0,
            75.0,
            22.0
          ],
          "text": "eq_reload"
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1210.0,
            205.0,
            50.0,
            22.0
          ],
          "text": "t b b"
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
            1210.0,
            235.0,
            110.0,
            22.0
          ],
          "text": "soundscape_reset"
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
            1210.0,
            265.0,
            75.0,
            22.0
          ],
          "text": "eq_reset"
        }
      },
      {
        "box": {
          "id": "obj-34",
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
            980.0,
            210.0,
            410.0,
            22.0
          ],
          "text": "route soundscape_solo pad_solo backfire_solo dna_solo noise_solo"
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
            1010.0,
            250.0,
            65.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-36",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1085.0,
            250.0,
            65.0,
            22.0
          ],
          "text": "clip 0 1"
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
            1160.0,
            250.0,
            65.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-38",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1160.0,
            285.0,
            65.0,
            22.0
          ],
          "text": "clip 0 1"
        }
      },
      {
        "box": {
          "id": "obj-39",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1235.0,
            250.0,
            105.0,
            22.0
          ],
          "text": "pak 0 0 0 0"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1180.0,
            220.0,
            300.0,
            22.0
          ],
          "text": "expr (1-$i4)*($i3+(1-$i3)*(1-max($i1,$i2)))"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1180.0,
            280.0,
            280.0,
            22.0
          ],
          "text": "expr (1-$i4)*(1-$i3)*(1-max($i1,$i2))"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1180.0,
            310.0,
            280.0,
            22.0
          ],
          "text": "expr (1-$i4)*(1-$i3)*(1-$i1*(1-$i2))"
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1180.0,
            340.0,
            240.0,
            22.0
          ],
          "text": "expr (1-$i4)*(1-$i3)*(1-$i2)"
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "newobj",
          "numinlets": 4,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            980.0,
            435.0,
            400.0,
            22.0
          ],
          "text": "expr $i4+(1-$i4)*(1-$i3)*(1-max($i1,$i2))"
        }
      },
      {
        "box": {
          "id": "obj-45",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            970.0,
            370.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1065.0,
            370.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1115.0,
            370.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1210.0,
            370.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-49",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1260.0,
            370.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-50",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1355.0,
            370.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-51",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1260.0,
            400.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-52",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1355.0,
            400.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-53",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            970.0,
            465.0,
            85.0,
            22.0
          ],
          "text": "pack 0. 35"
        }
      },
      {
        "box": {
          "id": "obj-54",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "patching_rect": [
            1065.0,
            465.0,
            50.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-55",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            1090.0,
            285.0,
            80.0,
            22.0
          ],
          "text": "loadmess 0"
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
            95.0,
            300.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-57",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            390.0,
            300.0,
            40.0,
            22.0
          ],
          "text": "*~"
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
            285.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-59",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            335.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
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
            465.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-61",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            515.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
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
            625.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-63",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            675.0,
            305.0,
            40.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-64",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            95.0,
            335.0,
            40.0,
            22.0
          ],
          "text": "*~"
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
            390.0,
            335.0,
            40.0,
            22.0
          ],
          "text": "*~"
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
            1010.0,
            320.0,
            205.0,
            22.0
          ],
          "text": "prepend soundscape_state solo"
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
            95.0,
            340.0,
            35.0,
            22.0
          ],
          "text": "+~"
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
            390.0,
            340.0,
            35.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "v7-all-owner-actions",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 4,
          "patching_rect": [
            20.0,
            2432.0,
            200.0,
            22.0
          ],
          "text": "route save_profile_sound reload_profile_sound reset_profile_sound"
        }
      },
      {
        "box": {
          "id": "v7-owner-fanout-save",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2456.0,
            200.0,
            22.0
          ],
          "text": "dna_save, noise_save, start_save, backfire_save, event_save"
        }
      },
      {
        "box": {
          "id": "v7-owner-fanout-reload",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2480.0,
            200.0,
            22.0
          ],
          "text": "dna_reload, noise_reload, start_reload, backfire_reload, event_reload"
        }
      },
      {
        "box": {
          "id": "v7-owner-fanout-reset",
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2504.0,
            200.0,
            22.0
          ],
          "text": "dna_reset, noise_reset, start_reset, backfire_reset, event_reset"
        }
      },
      {
        "box": {
          "id": "v7-mass",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2528.0,
            200.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_mass_ferrari.gendsp"
        }
      },
      {
        "box": {
          "id": "v7-mass-controls-recv",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2552.0,
            200.0,
            22.0
          ],
          "text": "r vss.v7.params.ferrari"
        }
      },
      {
        "box": {
          "id": "v7-mass-controls-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 7,
          "patching_rect": [
            20.0,
            2576.0,
            200.0,
            22.0
          ],
          "text": "routepass v7_enable v7_sub_db v7_foundation_db v7_attack_ms v7_release_ms v7_speed_weight_db"
        }
      },
      {
        "box": {
          "id": "v7-mass-state",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 7,
          "patching_rect": [
            20.0,
            2600.0,
            200.0,
            22.0
          ],
          "text": "routepass rpm throttle load engine_running shift_cut powertrain_level_db"
        }
      },
      {
        "box": {
          "id": "v7-mass-solo",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2624.0,
            200.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "v7-mass-sum0",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2648.0,
            200.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "v7-mass-sum1",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2672.0,
            200.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "v7-balance",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "patching_rect": [
            20.0,
            2696.0,
            200.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_balance.gendsp"
        }
      },
      {
        "box": {
          "id": "v7-balance-controls-recv",
          "maxclass": "newobj",
          "numinlets": 0,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2720.0,
            200.0,
            22.0
          ],
          "text": "r vss.v7.params.ferrari"
        }
      },
      {
        "box": {
          "id": "v7-balance-controls-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 7,
          "patching_rect": [
            20.0,
            2744.0,
            200.0,
            22.0
          ],
          "text": "routepass v7_enable v7_body_db v7_cavity_db v7_mechanical_db v7_brightness_db v7_speed_edge_db"
        }
      },
      {
        "box": {
          "id": "v7-speed-route",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 2,
          "patching_rect": [
            20.0,
            2768.0,
            200.0,
            22.0
          ],
          "text": "routepass speed_kph"
        }
      },
      {
        "box": {
          "id": "v7-meter",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 4,
          "patching_rect": [
            20.0,
            2792.0,
            200.0,
            22.0
          ],
          "text": "gen~ @gen Patcher:/gen/v7_meter.gendsp"
        }
      },
      {
        "box": {
          "id": "v7-meter-feedback",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            20.0,
            2816.0,
            200.0,
            22.0
          ],
          "text": "s vss.runtime.feedback.ferrari"
        }
      },
      {
        "box": {
          "id": "v7-meter-0-snapshot",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2840.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "v7-meter-0-tag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2864.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_meter_sub_db"
        }
      },
      {
        "box": {
          "id": "v7-meter-1-snapshot",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2888.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "v7-meter-1-tag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2912.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_meter_body_db"
        }
      },
      {
        "box": {
          "id": "v7-meter-2-snapshot",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2936.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "v7-meter-2-tag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2960.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_meter_cavity_db"
        }
      },
      {
        "box": {
          "id": "v7-meter-3-snapshot",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            2984.0,
            200.0,
            22.0
          ],
          "text": "snapshot~ 100"
        }
      },
      {
        "box": {
          "id": "v7-meter-3-tag",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "patching_rect": [
            20.0,
            3008.0,
            200.0,
            22.0
          ],
          "text": "prepend v7_meter_edge_db"
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
            "obj-22",
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
            "obj-23",
            0
          ],
          "source": [
            "obj-22",
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
            "obj-22",
            2
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
            3
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
            4
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
            5
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
            6
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
            7
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
            8
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
            9
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
            10
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
            11
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
            "obj-21",
            0
          ],
          "source": [
            "obj-23",
            1
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
            6
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
            5
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
            "obj-4",
            5
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
            "obj-4",
            4
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
            "obj-4",
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
            "obj-4",
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
            "obj-4",
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
            "obj-7",
            2
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
            "obj-2",
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
            "obj-25",
            1
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
            "obj-25",
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
            "obj-26",
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
            "obj-27",
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
            "obj-24",
            1
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
            "obj-28",
            1
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
            "obj-28",
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
            "obj-29",
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
            "obj-24",
            2
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
            1
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
            "obj-7",
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
            "obj-11",
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
            "obj-45",
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
            "obj-47",
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
            "obj-49",
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
            "obj-50",
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
            "obj-43",
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
            "obj-51",
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
            "obj-44",
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
            "obj-34",
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
            "obj-35",
            0
          ],
          "source": [
            "obj-34",
            1
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
            "obj-34",
            2
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
            "obj-34",
            3
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
            "obj-34",
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
            "obj-55",
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
            "obj-55",
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
            "obj-55",
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
            "obj-55",
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
            "obj-35",
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
            "obj-35",
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
            "obj-66",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-39",
            1
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
            "obj-39",
            2
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
            3
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
            "obj-44",
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
            "obj-39",
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
            "obj-39",
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
            "obj-6",
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
            "obj-6",
            1
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
            "obj-8",
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
            "obj-8",
            1
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
            "obj-6",
            2
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
            "obj-6",
            3
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
            "obj-9",
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
            "obj-9",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-56",
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
            "obj-57",
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
            "obj-62",
            1
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
            "obj-63",
            1
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
            "obj-60",
            1
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
            "obj-61",
            1
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
            "obj-58",
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
            "obj-59",
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
            "obj-64",
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
            "obj-65",
            0
          ],
          "source": [
            "obj-7",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-64",
            1
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
            "obj-65",
            1
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
            "v7-mass-sum0",
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
            "obj-67",
            1
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
            "v7-mass-sum1",
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
            "obj-68",
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
            "obj-13",
            0
          ],
          "source": [
            "v7-balance",
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
          "source": [
            "obj-58",
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
            "obj-14",
            1
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
            "obj-15",
            1
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
            "obj-16",
            0
          ],
          "source": [
            "v7-balance",
            1
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
            "obj-59",
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
            "obj-17",
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
            "obj-18",
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
            "obj-9",
            1
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
            "obj-9",
            2
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
            "obj-10",
            1
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
            "obj-10",
            2
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
            "obj-11",
            1
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
            "obj-11",
            2
          ],
          "source": [
            "obj-10",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-12",
            1
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
            2
          ],
          "source": [
            "obj-11",
            1
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
            "obj-12",
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
            "obj-12",
            1
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
            "v7-all-owner-actions",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-all-owner-actions",
            0
          ],
          "destination": [
            "v7-owner-fanout-save",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-owner-fanout-save",
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
            "v7-all-owner-actions",
            1
          ],
          "destination": [
            "v7-owner-fanout-reload",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-owner-fanout-reload",
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
            "v7-all-owner-actions",
            2
          ],
          "destination": [
            "v7-owner-fanout-reset",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-owner-fanout-reset",
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
            "v7-mass-controls-recv",
            0
          ],
          "destination": [
            "v7-mass-controls-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            0
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            1
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            2
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            3
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            4
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-controls-route",
            5
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-3",
            0
          ],
          "destination": [
            "v7-mass-state",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            0
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            1
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            2
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            3
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            4
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-state",
            5
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass",
            0
          ],
          "destination": [
            "v7-mass-solo",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-46",
            0
          ],
          "destination": [
            "v7-mass-solo",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-solo",
            0
          ],
          "destination": [
            "v7-mass-sum0",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-sum0",
            0
          ],
          "destination": [
            "obj-67",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-solo",
            0
          ],
          "destination": [
            "v7-mass-sum1",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-mass-sum1",
            0
          ],
          "destination": [
            "obj-68",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-recv",
            0
          ],
          "destination": [
            "v7-balance-controls-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            0
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            1
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            2
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            3
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            4
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance-controls-route",
            5
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-67",
            0
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-68",
            0
          ],
          "destination": [
            "v7-balance",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-3",
            0
          ],
          "destination": [
            "v7-speed-route",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-speed-route",
            0
          ],
          "destination": [
            "v7-mass",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-speed-route",
            0
          ],
          "destination": [
            "v7-balance",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance",
            0
          ],
          "destination": [
            "v7-meter",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-balance",
            1
          ],
          "destination": [
            "v7-meter",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter",
            0
          ],
          "destination": [
            "v7-meter-0-snapshot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-0-snapshot",
            0
          ],
          "destination": [
            "v7-meter-0-tag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-0-tag",
            0
          ],
          "destination": [
            "v7-meter-feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter",
            1
          ],
          "destination": [
            "v7-meter-1-snapshot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-1-snapshot",
            0
          ],
          "destination": [
            "v7-meter-1-tag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-1-tag",
            0
          ],
          "destination": [
            "v7-meter-feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter",
            2
          ],
          "destination": [
            "v7-meter-2-snapshot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-2-snapshot",
            0
          ],
          "destination": [
            "v7-meter-2-tag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-2-tag",
            0
          ],
          "destination": [
            "v7-meter-feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter",
            3
          ],
          "destination": [
            "v7-meter-3-snapshot",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-3-snapshot",
            0
          ],
          "destination": [
            "v7-meter-3-tag",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "v7-meter-3-tag",
            0
          ],
          "destination": [
            "v7-meter-feedback",
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
      1450,
      860
    ],
    "toolbarvisible": 1
  }
}
