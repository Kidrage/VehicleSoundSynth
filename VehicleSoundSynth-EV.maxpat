{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 8,
			"minor" : 6,
			"revision" : 5,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"classnamespace" : "box",
		"rect" : [ 134.0, 87.0, 1180.0, 779.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "",
		"assistshowspatchername" : 0,
		"boxes" : [ 			{
				"box" : 				{
					"id" : "obj-1",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 18.0, 720.0, 20.0 ],
					"text" : "VehicleSoundSynth V4 — Future EV independent runtime"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-2",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 48.0, 620.0, 20.0 ],
					"text" : "Audio starts OFF. This patch contains only this profile's DSP graph."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-3",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 850.0, 25.0, 145.0, 22.0 ],
					"text" : "r vss.runtime.select"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-4",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "" ],
					"patching_rect" : [ 850.0, 60.0, 65.0, 22.0 ],
					"text" : "sel ev"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-5",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "bang", "bang" ],
					"patching_rect" : [ 930.0, 95.0, 50.0, 22.0 ],
					"text" : "t b b"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-6",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 990.0, 70.0, 45.0, 22.0 ],
					"text" : "write"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-7",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "bang" ],
					"patching_rect" : [ 990.0, 105.0, 65.0, 22.0 ],
					"text" : "delay 20"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-8",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 1070.0, 105.0, 55.0, 22.0 ],
					"text" : "wclose"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-9",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 1070.0, 140.0, 85.0, 22.0 ],
					"save" : [ "#N", "thispatcher", ";", "#Q", "end", ";" ],
					"text" : "thispatcher"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-10",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 35.0, 390.0, 155.0, 22.0 ],
					"text" : "drive_simulator_ev"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-11",
					"maxclass" : "newobj",
					"numinlets" : 0,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 215.0, 390.0, 130.0, 22.0 ],
					"text" : "r vss.ev.input"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-12",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 35.0, 435.0, 75.0, 22.0 ],
					"text" : "switch 2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-13",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 125.0, 435.0, 80.0, 22.0 ],
					"text" : "loadmess 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-14",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "signal" ],
					"patching_rect" : [ 400.0, 390.0, 165.0, 22.0 ],
					"text" : "vehicle_engine_ev~",
					"varname" : "vehicle_engine_ev~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-15",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 105.0, 120.0, 20.0 ],
					"text" : "Lifecycle"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-16",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 25.0, 135.0, 75.0, 22.0 ],
					"text" : "ignition 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-17",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 115.0, 135.0, 60.0, 22.0 ],
					"text" : "start 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-18",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 190.0, 135.0, 75.0, 22.0 ],
					"text" : "ignition 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-19",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 300.0, 105.0, 120.0, 20.0 ],
					"text" : "Drive source"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-20",
					"items" : [ "Internal Manual", ",", "Internal Auto", ",", "External vss.ev.input" ],
					"maxclass" : "umenu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "int", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 300.0, 135.0, 155.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-21",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 470.0, 135.0, 120.0, 22.0 ],
					"text" : "expr 1+($i1==2)"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-22",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 470.0, 170.0, 45.0, 22.0 ],
					"text" : "== 1"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-23",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 525.0, 170.0, 95.0, 22.0 ],
					"text" : "prepend auto"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-24",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 600.0, 135.0, 80.0, 22.0 ],
					"text" : "loadmess 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-25",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"patching_rect" : [ 630.0, 170.0, 45.0, 22.0 ],
					"text" : "== 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-26",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 205.0, 100.0, 20.0 ],
					"text" : "Throttle"
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-27",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 25.0, 232.0, 75.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-28",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 25.0, 266.0, 75.0, 22.0 ],
					"text" : "clip 0. 1."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-29",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 25.0, 300.0, 110.0, 22.0 ],
					"text" : "prepend throttle"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-30",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 105.0, 232.0, 80.0, 22.0 ],
					"text" : "loadmess 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-31",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 175.0, 205.0, 100.0, 20.0 ],
					"text" : "Brake"
				}

			}
, 			{
				"box" : 				{
					"format" : 6,
					"id" : "obj-32",
					"maxclass" : "flonum",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "bang" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 175.0, 232.0, 75.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-33",
					"maxclass" : "newobj",
					"numinlets" : 3,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 175.0, 266.0, 75.0, 22.0 ],
					"text" : "clip 0. 1."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-34",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 175.0, 300.0, 110.0, 22.0 ],
					"text" : "prepend brake"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-35",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 255.0, 232.0, 80.0, 22.0 ],
					"text" : "loadmess 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-36",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 2,
					"outlettype" : [ "", "" ],
					"patching_rect" : [ 25.0, 345.0, 135.0, 22.0 ],
					"text" : "keyboard_drive_ws"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-37",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 175.0, 347.0, 470.0, 20.0 ],
					"text" : "Focus this window: hold W = throttle, hold S = brake (Internal Manual only)"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-38",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 330.0, 205.0, 150.0, 20.0 ],
					"text" : "BEAP soundscape"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-39",
					"items" : [ "Relax", ",", "Expressive", ",", "Sport" ],
					"maxclass" : "umenu",
					"numinlets" : 1,
					"numoutlets" : 3,
					"outlettype" : [ "int", "", "" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 330.0, 232.0, 145.0, 22.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-40",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 330.0, 270.0, 105.0, 22.0 ],
					"text" : "ev_mode relax"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-41",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 445.0, 270.0, 135.0, 22.0 ],
					"text" : "ev_mode expressive"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-42",
					"maxclass" : "message",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 590.0, 270.0, 105.0, 22.0 ],
					"text" : "ev_mode sport"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-43",
					"maxclass" : "newobj",
					"numinlets" : 4,
					"numoutlets" : 4,
					"outlettype" : [ "bang", "bang", "bang", "" ],
					"patching_rect" : [ 490.0, 232.0, 70.0, 22.0 ],
					"text" : "sel 0 1 2"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-44",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 575.0, 232.0, 80.0, 22.0 ],
					"text" : "loadmess 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-45",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 760.0, 105.0, 120.0, 20.0 ],
					"text" : "Audio + Output"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-46",
					"maxclass" : "toggle",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "int" ],
					"parameter_enable" : 0,
					"patching_rect" : [ 760.0, 135.0, 24.0, 24.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-47",
					"maxclass" : "newobj",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 795.0, 135.0, 80.0, 22.0 ],
					"text" : "loadmess 0"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-48",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 760.0, 175.0, 85.0, 22.0 ],
					"text" : "pack 0. 60"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-49",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 2,
					"outlettype" : [ "signal", "bang" ],
					"patching_rect" : [ 760.0, 210.0, 50.0, 22.0 ],
					"text" : "line~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-50",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 690.0, 505.0, 40.0, 22.0 ],
					"text" : "*~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-51",
					"maxclass" : "newobj",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "signal" ],
					"patching_rect" : [ 815.0, 505.0, 40.0, 22.0 ],
					"text" : "*~"
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-52",
					"maxclass" : "ezdac~",
					"numinlets" : 2,
					"numoutlets" : 0,
					"patching_rect" : [ 740.0, 620.0, 45.0, 45.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-53",
					"maxclass" : "meter~",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "float" ],
					"patching_rect" : [ 660.0, 565.0, 18.0, 80.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-54",
					"maxclass" : "meter~",
					"numinlets" : 1,
					"numoutlets" : 1,
					"outlettype" : [ "float" ],
					"patching_rect" : [ 850.0, 565.0, 18.0, 80.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-55",
					"maxclass" : "spectroscope~",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 885.0, 390.0, 300.0, 100.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-56",
					"maxclass" : "spectroscope~",
					"numinlets" : 2,
					"numoutlets" : 1,
					"outlettype" : [ "" ],
					"patching_rect" : [ 885.0, 560.0, 300.0, 100.0 ]
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-57",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 720.0, 550.0, 20.0 ],
					"text" : "Shared shaping controls can also be sent to the profile receive seam."
				}

			}
, 			{
				"box" : 				{
					"id" : "obj-58",
					"maxclass" : "comment",
					"numinlets" : 1,
					"numoutlets" : 0,
					"patching_rect" : [ 25.0, 750.0, 520.0, 20.0 ],
					"text" : "External control: send named messages to vss.ev.input"
				}

			}
 ],
		"lines" : [ 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 1 ],
					"source" : [ "obj-10", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 2 ],
					"source" : [ "obj-11", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"source" : [ "obj-12", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"source" : [ "obj-13", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-50", 0 ],
					"source" : [ "obj-14", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-51", 0 ],
					"source" : [ "obj-14", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-16", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-17", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-18", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-21", 0 ],
					"order" : 2,
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-22", 0 ],
					"order" : 1,
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-25", 0 ],
					"order" : 0,
					"source" : [ "obj-20", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-12", 0 ],
					"source" : [ "obj-21", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-23", 0 ],
					"source" : [ "obj-22", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-23", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-20", 0 ],
					"source" : [ "obj-24", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-36", 0 ],
					"source" : [ "obj-25", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-28", 0 ],
					"source" : [ "obj-27", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-29", 0 ],
					"source" : [ "obj-28", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-29", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-4", 0 ],
					"source" : [ "obj-3", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-27", 0 ],
					"source" : [ "obj-30", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-33", 0 ],
					"source" : [ "obj-32", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-34", 0 ],
					"source" : [ "obj-33", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-10", 0 ],
					"source" : [ "obj-34", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-32", 0 ],
					"source" : [ "obj-35", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-27", 0 ],
					"source" : [ "obj-36", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-32", 0 ],
					"source" : [ "obj-36", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-43", 0 ],
					"source" : [ "obj-39", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-5", 0 ],
					"source" : [ "obj-4", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"source" : [ "obj-40", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"source" : [ "obj-41", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-14", 0 ],
					"source" : [ "obj-42", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-40", 0 ],
					"source" : [ "obj-43", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-41", 0 ],
					"source" : [ "obj-43", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-42", 0 ],
					"source" : [ "obj-43", 2 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-39", 0 ],
					"source" : [ "obj-44", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-48", 0 ],
					"order" : 0,
					"source" : [ "obj-46", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-52", 0 ],
					"order" : 1,
					"source" : [ "obj-46", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-46", 0 ],
					"source" : [ "obj-47", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-49", 0 ],
					"source" : [ "obj-48", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-50", 1 ],
					"order" : 1,
					"source" : [ "obj-49", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-51", 1 ],
					"order" : 0,
					"source" : [ "obj-49", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-6", 0 ],
					"source" : [ "obj-5", 1 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-7", 0 ],
					"source" : [ "obj-5", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-52", 0 ],
					"order" : 1,
					"source" : [ "obj-50", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-53", 0 ],
					"order" : 2,
					"source" : [ "obj-50", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-55", 0 ],
					"order" : 0,
					"source" : [ "obj-50", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-52", 1 ],
					"order" : 2,
					"source" : [ "obj-51", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-54", 0 ],
					"order" : 1,
					"source" : [ "obj-51", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-56", 0 ],
					"order" : 0,
					"source" : [ "obj-51", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-9", 0 ],
					"source" : [ "obj-6", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-8", 0 ],
					"source" : [ "obj-7", 0 ]
				}

			}
, 			{
				"patchline" : 				{
					"destination" : [ "obj-9", 0 ],
					"source" : [ "obj-8", 0 ]
				}

			}
 ],
		"parameters" : 		{
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-106" : [ "CV3[23]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-107" : [ "Linear[15]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-11" : [ "PWM[15]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-129" : [ "CV2[23]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-36" : [ "PW[15]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-4" : [ "Waveform[15]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-45" : [ "FreqMode[15]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-46" : [ "Offset[23]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-51" : [ "Freq[23]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-53" : [ "Mute[31]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-106" : [ "CV3[22]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-107" : [ "Linear[14]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-11" : [ "PWM[14]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-129" : [ "CV2[22]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-36" : [ "PW[14]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-4" : [ "Waveform[14]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-45" : [ "FreqMode[14]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-46" : [ "Offset[22]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-51" : [ "Freq[22]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-53" : [ "Mute[30]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-29" : [ "3[7]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-32" : [ "2[7]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-33" : [ "4[7]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-37" : [ "Mute[29]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-39" : [ "1[7]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-49" : [ "MuteCh1[7]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-58" : [ "MuteCh2[7]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-64" : [ "MuteCh3[7]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-70" : [ "MuteCh4[7]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-20" : [ "Freq[21]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-22" : [ "TimeMode[7]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-23" : [ "CV2[21]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-28" : [ "Res[7]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-4" : [ "Offset[21]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-54" : [ "CV1[7]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-55" : [ "power[7]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-63" : [ "CV3[21]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-95" : [ "ResCV[7]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-1" : [ "Attack[7]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-15" : [ "Legato[7]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-20" : [ "Mute[28]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-29" : [ "Decay[7]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-31" : [ "Release[7]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-32" : [ "Sustain[7]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-33" : [ "Quadrants[7]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-55" : [ "Bypass[7]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-80" : [ "Response[7]", "Response", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-106" : [ "CV3[20]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-107" : [ "Linear[13]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-11" : [ "PWM[13]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-129" : [ "CV2[20]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-36" : [ "PW[13]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-4" : [ "Waveform[13]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-45" : [ "FreqMode[13]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-46" : [ "Offset[20]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-51" : [ "Freq[20]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-53" : [ "Mute[27]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-106" : [ "CV3[19]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-107" : [ "Linear[12]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-11" : [ "PWM[12]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-129" : [ "CV2[19]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-36" : [ "PW[12]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-4" : [ "Waveform[12]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-45" : [ "FreqMode[12]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-46" : [ "Offset[19]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-51" : [ "Freq[19]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-53" : [ "Mute[26]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-29" : [ "3[6]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-32" : [ "2[6]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-33" : [ "4[6]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-37" : [ "Mute[25]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-39" : [ "1[6]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-49" : [ "MuteCh1[6]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-58" : [ "MuteCh2[6]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-64" : [ "MuteCh3[6]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-70" : [ "MuteCh4[6]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-20" : [ "Freq[18]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-22" : [ "TimeMode[6]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-23" : [ "CV2[18]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-28" : [ "Res[6]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-4" : [ "Offset[18]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-54" : [ "CV1[6]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-55" : [ "power[6]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-63" : [ "CV3[18]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-95" : [ "ResCV[6]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-1" : [ "Attack[6]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-15" : [ "Legato[6]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-20" : [ "Mute[24]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-29" : [ "Decay[6]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-31" : [ "Release[6]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-32" : [ "Sustain[6]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-33" : [ "Quadrants[6]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-55" : [ "Bypass[6]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-80" : [ "Response[6]", "Response", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-106" : [ "CV3[17]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-107" : [ "Linear[11]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-11" : [ "PWM[11]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-129" : [ "CV2[17]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-36" : [ "PW[11]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-4" : [ "Waveform[11]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-45" : [ "FreqMode[11]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-46" : [ "Offset[17]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-51" : [ "Freq[17]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-53" : [ "Mute[23]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-106" : [ "CV3[16]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-107" : [ "Linear[10]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-11" : [ "PWM[10]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-129" : [ "CV2[16]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-36" : [ "PW[10]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-4" : [ "Waveform[10]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-45" : [ "FreqMode[10]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-46" : [ "Offset[16]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-51" : [ "Freq[16]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-53" : [ "Mute[22]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-29" : [ "3[5]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-32" : [ "2[5]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-33" : [ "4[5]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-37" : [ "Mute[21]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-39" : [ "1[5]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-49" : [ "MuteCh1[5]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-58" : [ "MuteCh2[5]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-64" : [ "MuteCh3[5]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-70" : [ "MuteCh4[5]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-20" : [ "Freq[15]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-22" : [ "TimeMode[5]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-23" : [ "CV2[15]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-28" : [ "Res[5]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-4" : [ "Offset[15]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-54" : [ "CV1[5]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-55" : [ "power[5]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-63" : [ "CV3[15]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-95" : [ "ResCV[5]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-1" : [ "Attack[5]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-15" : [ "Legato[5]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-20" : [ "Mute[20]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-29" : [ "Decay[5]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-31" : [ "Release[5]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-32" : [ "Sustain[5]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-33" : [ "Quadrants[5]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-55" : [ "Bypass[5]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-80" : [ "Response[5]", "Response", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-106" : [ "CV3[14]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-107" : [ "Linear[9]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-11" : [ "PWM[9]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-129" : [ "CV2[14]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-36" : [ "PW[9]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-4" : [ "Waveform[9]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-45" : [ "FreqMode[9]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-46" : [ "Offset[14]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-51" : [ "Freq[14]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-53" : [ "Mute[19]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-106" : [ "CV3[13]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-107" : [ "Linear[8]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-11" : [ "PWM[8]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-129" : [ "CV2[13]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-36" : [ "PW[8]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-4" : [ "Waveform[8]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-45" : [ "FreqMode[8]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-46" : [ "Offset[13]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-51" : [ "Freq[13]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-53" : [ "Mute[18]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-29" : [ "3[4]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-32" : [ "2[4]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-33" : [ "4[4]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-37" : [ "Mute[17]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-39" : [ "1[4]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-49" : [ "MuteCh1[4]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-58" : [ "MuteCh2[4]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-64" : [ "MuteCh3[4]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-70" : [ "MuteCh4[4]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-20" : [ "Freq[12]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-22" : [ "TimeMode[4]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-23" : [ "CV2[12]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-28" : [ "Res[4]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-4" : [ "Offset[12]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-54" : [ "CV1[4]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-55" : [ "power[4]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-63" : [ "CV3[12]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-95" : [ "ResCV[4]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-1" : [ "Attack[4]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-15" : [ "Legato[4]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-20" : [ "Mute[16]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-29" : [ "Decay[4]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-31" : [ "Release[4]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-32" : [ "Sustain[4]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-33" : [ "Quadrants[4]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-55" : [ "Bypass[4]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-80" : [ "Response[4]", "Response", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-106" : [ "CV3[11]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-107" : [ "Linear[7]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-11" : [ "PWM[7]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-129" : [ "CV2[11]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-36" : [ "PW[7]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-4" : [ "Waveform[7]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-45" : [ "FreqMode[7]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-46" : [ "Offset[11]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-51" : [ "Freq[11]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-53" : [ "Mute[15]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-106" : [ "CV3[10]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-107" : [ "Linear[6]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-11" : [ "PWM[6]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-129" : [ "CV2[10]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-36" : [ "PW[6]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-4" : [ "Waveform[6]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-45" : [ "FreqMode[6]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-46" : [ "Offset[10]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-51" : [ "Freq[10]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-53" : [ "Mute[14]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-29" : [ "3[3]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-32" : [ "2[3]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-33" : [ "4[3]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-37" : [ "Mute[13]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-39" : [ "1[3]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-49" : [ "MuteCh1[3]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-58" : [ "MuteCh2[3]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-64" : [ "MuteCh3[3]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-70" : [ "MuteCh4[3]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-20" : [ "Freq[9]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-22" : [ "TimeMode[3]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-23" : [ "CV2[9]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-28" : [ "Res[3]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-4" : [ "Offset[9]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-54" : [ "CV1[3]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-55" : [ "power[3]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-63" : [ "CV3[9]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-95" : [ "ResCV[3]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-1" : [ "Attack[3]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-15" : [ "Legato[3]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-20" : [ "Mute[12]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-29" : [ "Decay[3]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-31" : [ "Release[3]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-32" : [ "Sustain[3]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-33" : [ "Quadrants[3]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-55" : [ "Bypass[3]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-80" : [ "Response[3]", "Response", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-106" : [ "CV3[8]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-107" : [ "Linear[5]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-11" : [ "PWM[5]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-129" : [ "CV2[8]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-36" : [ "PW[5]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-4" : [ "Waveform[5]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-45" : [ "FreqMode[5]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-46" : [ "Offset[8]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-51" : [ "Freq[8]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-53" : [ "Mute[11]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-106" : [ "CV3[7]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-107" : [ "Linear[4]", "Linear", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-11" : [ "PWM[4]", "PWM", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-129" : [ "CV2[7]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-36" : [ "PW[4]", "PW", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-4" : [ "Waveform[4]", "Waveform", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-45" : [ "FreqMode[4]", "FreqMode", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-46" : [ "Offset[7]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-51" : [ "Freq[7]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-53" : [ "Mute[10]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-29" : [ "3[2]", "3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-32" : [ "2[2]", "2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-33" : [ "4[2]", "4", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-37" : [ "Mute[9]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-39" : [ "1[2]", "1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-49" : [ "MuteCh1[2]", "MuteCh1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-58" : [ "MuteCh2[2]", "MuteCh2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-64" : [ "MuteCh3[2]", "MuteCh3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-70" : [ "MuteCh4[2]", "MuteCh4", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-20" : [ "Freq[6]", "Freq", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-22" : [ "TimeMode[2]", "TimeMode", 1 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-23" : [ "CV2[6]", "CV2", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-28" : [ "Res[2]", "Res", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-4" : [ "Offset[6]", "Offset", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-54" : [ "CV1[2]", "CV1", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-55" : [ "power[2]", "power", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-63" : [ "CV3[6]", "CV3", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-95" : [ "ResCV[2]", "CV", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-1" : [ "Attack[2]", "Attack", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-15" : [ "Legato[2]", "Legato", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-20" : [ "Mute[8]", "Mute", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-29" : [ "Decay[2]", "Decay", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-31" : [ "Release[2]", "Release", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-32" : [ "Sustain[2]", "Sustain", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-33" : [ "Quadrants[2]", "Quadrants", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-55" : [ "Bypass[2]", "Bypass", 0 ],
			"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-80" : [ "Response[2]", "Response", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-106" : [ "CV3[5]", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-107" : [ "Linear[3]", "Linear", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-11" : [ "PWM[3]", "PWM", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-129" : [ "CV2[5]", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-36" : [ "PW[3]", "PW", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-4" : [ "Waveform[3]", "Waveform", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-45" : [ "FreqMode[3]", "FreqMode", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-46" : [ "Offset[5]", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-51" : [ "Freq[5]", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-53" : [ "Mute[7]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-106" : [ "CV3[4]", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-107" : [ "Linear[2]", "Linear", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-11" : [ "PWM[2]", "PWM", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-129" : [ "CV2[4]", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-36" : [ "PW[2]", "PW", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-4" : [ "Waveform[2]", "Waveform", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-45" : [ "FreqMode[2]", "FreqMode", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-46" : [ "Offset[4]", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-51" : [ "Freq[4]", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-53" : [ "Mute[6]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-29" : [ "3[1]", "3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-32" : [ "2[1]", "2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-33" : [ "4[1]", "4", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-37" : [ "Mute[5]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-39" : [ "1[1]", "1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-49" : [ "MuteCh1[1]", "MuteCh1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-58" : [ "MuteCh2[1]", "MuteCh2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-64" : [ "MuteCh3[1]", "MuteCh3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-70" : [ "MuteCh4[1]", "MuteCh4", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-20" : [ "Freq[3]", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-22" : [ "TimeMode[1]", "TimeMode", 1 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-23" : [ "CV2[3]", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-28" : [ "Res[1]", "Res", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-4" : [ "Offset[3]", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-54" : [ "CV1[1]", "CV1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-55" : [ "power[1]", "power", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-63" : [ "CV3[3]", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-95" : [ "ResCV[1]", "CV", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-1" : [ "Attack[1]", "Attack", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-15" : [ "Legato[1]", "Legato", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-20" : [ "Mute[4]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-29" : [ "Decay[1]", "Decay", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-31" : [ "Release[1]", "Release", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-32" : [ "Sustain[1]", "Sustain", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-33" : [ "Quadrants[1]", "Quadrants", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-55" : [ "Bypass[1]", "Bypass", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-80" : [ "Response[1]", "Response", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-106" : [ "CV3[2]", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-107" : [ "Linear[1]", "Linear", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-11" : [ "PWM[1]", "PWM", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-129" : [ "CV2[2]", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-36" : [ "PW[1]", "PW", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-4" : [ "Waveform[1]", "Waveform", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-45" : [ "FreqMode[1]", "FreqMode", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-46" : [ "Offset[2]", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-51" : [ "Freq[2]", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-53" : [ "Mute[3]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-106" : [ "CV3[1]", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-107" : [ "Linear", "Linear", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-11" : [ "PWM", "PWM", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-129" : [ "CV2[1]", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-36" : [ "PW", "PW", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-4" : [ "Waveform", "Waveform", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-45" : [ "FreqMode", "FreqMode", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-46" : [ "Offset[1]", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-51" : [ "Freq[1]", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-53" : [ "Mute[2]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-29" : [ "3", "3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-32" : [ "2", "2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-33" : [ "4", "4", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-37" : [ "Mute[1]", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-39" : [ "1", "1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-49" : [ "MuteCh1", "MuteCh1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-58" : [ "MuteCh2", "MuteCh2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-64" : [ "MuteCh3", "MuteCh3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-70" : [ "MuteCh4", "MuteCh4", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-20" : [ "Freq", "Freq", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-22" : [ "TimeMode", "TimeMode", 1 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-23" : [ "CV2", "CV2", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-28" : [ "Res", "Res", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-4" : [ "Offset", "Offset", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-54" : [ "CV1", "CV1", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-55" : [ "power", "power", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-63" : [ "CV3", "CV3", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-26::obj-95" : [ "ResCV", "CV", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-1" : [ "Attack", "Attack", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-15" : [ "Legato", "Legato", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-20" : [ "Mute", "Mute", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-29" : [ "Decay", "Decay", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-31" : [ "Release", "Release", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-27::obj-32" : [ "Sustain", "Sustain", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-28::obj-33" : [ "Quadrants", "Quadrants", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-28::obj-55" : [ "Bypass", "Bypass", 0 ],
			"obj-14::obj-7::obj-13.1::obj-5::obj-28::obj-80" : [ "Response", "Response", 0 ],
			"parameterbanks" : 			{
				"0" : 				{
					"index" : 0,
					"name" : "",
					"parameters" : [ "-", "-", "-", "-", "-", "-", "-", "-" ]
				}

			}
,
			"parameter_overrides" : 			{
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-106" : 				{
					"parameter_longname" : "CV3[23]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-107" : 				{
					"parameter_longname" : "Linear[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-11" : 				{
					"parameter_longname" : "PWM[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-129" : 				{
					"parameter_longname" : "CV2[23]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-36" : 				{
					"parameter_longname" : "PW[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-4" : 				{
					"parameter_longname" : "Waveform[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-45" : 				{
					"parameter_longname" : "FreqMode[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-46" : 				{
					"parameter_longname" : "Offset[23]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-51" : 				{
					"parameter_longname" : "Freq[23]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-13::obj-53" : 				{
					"parameter_longname" : "Mute[31]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-106" : 				{
					"parameter_longname" : "CV3[22]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-107" : 				{
					"parameter_longname" : "Linear[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-11" : 				{
					"parameter_longname" : "PWM[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-129" : 				{
					"parameter_longname" : "CV2[22]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-36" : 				{
					"parameter_longname" : "PW[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-4" : 				{
					"parameter_longname" : "Waveform[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-45" : 				{
					"parameter_longname" : "FreqMode[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-46" : 				{
					"parameter_longname" : "Offset[22]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-51" : 				{
					"parameter_longname" : "Freq[22]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-14::obj-53" : 				{
					"parameter_longname" : "Mute[30]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-29" : 				{
					"parameter_longname" : "3[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-32" : 				{
					"parameter_longname" : "2[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-33" : 				{
					"parameter_longname" : "4[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-37" : 				{
					"parameter_longname" : "Mute[29]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-39" : 				{
					"parameter_longname" : "1[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-49" : 				{
					"parameter_longname" : "MuteCh1[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-58" : 				{
					"parameter_longname" : "MuteCh2[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-64" : 				{
					"parameter_longname" : "MuteCh3[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-15::obj-70" : 				{
					"parameter_longname" : "MuteCh4[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-20" : 				{
					"parameter_longname" : "Freq[21]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-22" : 				{
					"parameter_longname" : "TimeMode[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-23" : 				{
					"parameter_longname" : "CV2[21]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-28" : 				{
					"parameter_longname" : "Res[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-4" : 				{
					"parameter_longname" : "Offset[21]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-54" : 				{
					"parameter_longname" : "CV1[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-55" : 				{
					"parameter_longname" : "power[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-63" : 				{
					"parameter_longname" : "CV3[21]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-16::obj-95" : 				{
					"parameter_longname" : "ResCV[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-1" : 				{
					"parameter_longname" : "Attack[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-15" : 				{
					"parameter_longname" : "Legato[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-20" : 				{
					"parameter_longname" : "Mute[28]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-29" : 				{
					"parameter_longname" : "Decay[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-31" : 				{
					"parameter_longname" : "Release[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-17::obj-32" : 				{
					"parameter_longname" : "Sustain[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-33" : 				{
					"parameter_longname" : "Quadrants[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-55" : 				{
					"parameter_longname" : "Bypass[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-18::obj-80" : 				{
					"parameter_longname" : "Response[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-106" : 				{
					"parameter_longname" : "CV3[20]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-107" : 				{
					"parameter_longname" : "Linear[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-11" : 				{
					"parameter_longname" : "PWM[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-129" : 				{
					"parameter_longname" : "CV2[20]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-36" : 				{
					"parameter_longname" : "PW[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-4" : 				{
					"parameter_longname" : "Waveform[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-45" : 				{
					"parameter_longname" : "FreqMode[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-46" : 				{
					"parameter_longname" : "Offset[20]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-51" : 				{
					"parameter_longname" : "Freq[20]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-23::obj-53" : 				{
					"parameter_longname" : "Mute[27]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-106" : 				{
					"parameter_longname" : "CV3[19]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-107" : 				{
					"parameter_longname" : "Linear[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-11" : 				{
					"parameter_longname" : "PWM[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-129" : 				{
					"parameter_longname" : "CV2[19]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-36" : 				{
					"parameter_longname" : "PW[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-4" : 				{
					"parameter_longname" : "Waveform[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-45" : 				{
					"parameter_longname" : "FreqMode[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-46" : 				{
					"parameter_longname" : "Offset[19]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-51" : 				{
					"parameter_longname" : "Freq[19]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-24::obj-53" : 				{
					"parameter_longname" : "Mute[26]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-29" : 				{
					"parameter_longname" : "3[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-32" : 				{
					"parameter_longname" : "2[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-33" : 				{
					"parameter_longname" : "4[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-37" : 				{
					"parameter_longname" : "Mute[25]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-39" : 				{
					"parameter_longname" : "1[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-49" : 				{
					"parameter_longname" : "MuteCh1[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-58" : 				{
					"parameter_longname" : "MuteCh2[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-64" : 				{
					"parameter_longname" : "MuteCh3[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-25::obj-70" : 				{
					"parameter_longname" : "MuteCh4[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-20" : 				{
					"parameter_longname" : "Freq[18]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-22" : 				{
					"parameter_longname" : "TimeMode[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-23" : 				{
					"parameter_longname" : "CV2[18]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-28" : 				{
					"parameter_longname" : "Res[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-4" : 				{
					"parameter_longname" : "Offset[18]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-54" : 				{
					"parameter_longname" : "CV1[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-55" : 				{
					"parameter_longname" : "power[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-63" : 				{
					"parameter_longname" : "CV3[18]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-26::obj-95" : 				{
					"parameter_longname" : "ResCV[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-1" : 				{
					"parameter_longname" : "Attack[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-15" : 				{
					"parameter_longname" : "Legato[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-20" : 				{
					"parameter_longname" : "Mute[24]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-29" : 				{
					"parameter_longname" : "Decay[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-31" : 				{
					"parameter_longname" : "Release[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-27::obj-32" : 				{
					"parameter_longname" : "Sustain[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-33" : 				{
					"parameter_longname" : "Quadrants[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-55" : 				{
					"parameter_longname" : "Bypass[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-23.1::obj-5::obj-28::obj-80" : 				{
					"parameter_longname" : "Response[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-106" : 				{
					"parameter_longname" : "CV3[17]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-107" : 				{
					"parameter_longname" : "Linear[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-11" : 				{
					"parameter_longname" : "PWM[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-129" : 				{
					"parameter_longname" : "CV2[17]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-36" : 				{
					"parameter_longname" : "PW[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-4" : 				{
					"parameter_longname" : "Waveform[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-45" : 				{
					"parameter_longname" : "FreqMode[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-46" : 				{
					"parameter_longname" : "Offset[17]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-51" : 				{
					"parameter_longname" : "Freq[17]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-13::obj-53" : 				{
					"parameter_longname" : "Mute[23]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-106" : 				{
					"parameter_longname" : "CV3[16]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-107" : 				{
					"parameter_longname" : "Linear[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-11" : 				{
					"parameter_longname" : "PWM[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-129" : 				{
					"parameter_longname" : "CV2[16]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-36" : 				{
					"parameter_longname" : "PW[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-4" : 				{
					"parameter_longname" : "Waveform[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-45" : 				{
					"parameter_longname" : "FreqMode[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-46" : 				{
					"parameter_longname" : "Offset[16]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-51" : 				{
					"parameter_longname" : "Freq[16]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-14::obj-53" : 				{
					"parameter_longname" : "Mute[22]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-29" : 				{
					"parameter_longname" : "3[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-32" : 				{
					"parameter_longname" : "2[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-33" : 				{
					"parameter_longname" : "4[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-37" : 				{
					"parameter_longname" : "Mute[21]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-39" : 				{
					"parameter_longname" : "1[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-49" : 				{
					"parameter_longname" : "MuteCh1[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-58" : 				{
					"parameter_longname" : "MuteCh2[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-64" : 				{
					"parameter_longname" : "MuteCh3[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-15::obj-70" : 				{
					"parameter_longname" : "MuteCh4[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-20" : 				{
					"parameter_longname" : "Freq[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-22" : 				{
					"parameter_longname" : "TimeMode[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-23" : 				{
					"parameter_longname" : "CV2[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-28" : 				{
					"parameter_longname" : "Res[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-4" : 				{
					"parameter_longname" : "Offset[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-54" : 				{
					"parameter_longname" : "CV1[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-55" : 				{
					"parameter_longname" : "power[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-63" : 				{
					"parameter_longname" : "CV3[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-16::obj-95" : 				{
					"parameter_longname" : "ResCV[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-1" : 				{
					"parameter_longname" : "Attack[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-15" : 				{
					"parameter_longname" : "Legato[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-20" : 				{
					"parameter_longname" : "Mute[20]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-29" : 				{
					"parameter_longname" : "Decay[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-31" : 				{
					"parameter_longname" : "Release[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-17::obj-32" : 				{
					"parameter_longname" : "Sustain[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-33" : 				{
					"parameter_longname" : "Quadrants[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-55" : 				{
					"parameter_longname" : "Bypass[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-18::obj-80" : 				{
					"parameter_longname" : "Response[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-106" : 				{
					"parameter_longname" : "CV3[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-107" : 				{
					"parameter_longname" : "Linear[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-11" : 				{
					"parameter_longname" : "PWM[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-129" : 				{
					"parameter_longname" : "CV2[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-36" : 				{
					"parameter_longname" : "PW[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-4" : 				{
					"parameter_longname" : "Waveform[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-45" : 				{
					"parameter_longname" : "FreqMode[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-46" : 				{
					"parameter_longname" : "Offset[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-51" : 				{
					"parameter_longname" : "Freq[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-23::obj-53" : 				{
					"parameter_longname" : "Mute[19]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-106" : 				{
					"parameter_longname" : "CV3[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-107" : 				{
					"parameter_longname" : "Linear[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-11" : 				{
					"parameter_longname" : "PWM[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-129" : 				{
					"parameter_longname" : "CV2[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-36" : 				{
					"parameter_longname" : "PW[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-4" : 				{
					"parameter_longname" : "Waveform[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-45" : 				{
					"parameter_longname" : "FreqMode[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-46" : 				{
					"parameter_longname" : "Offset[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-51" : 				{
					"parameter_longname" : "Freq[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-24::obj-53" : 				{
					"parameter_longname" : "Mute[18]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-29" : 				{
					"parameter_longname" : "3[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-32" : 				{
					"parameter_longname" : "2[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-33" : 				{
					"parameter_longname" : "4[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-37" : 				{
					"parameter_longname" : "Mute[17]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-39" : 				{
					"parameter_longname" : "1[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-49" : 				{
					"parameter_longname" : "MuteCh1[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-58" : 				{
					"parameter_longname" : "MuteCh2[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-64" : 				{
					"parameter_longname" : "MuteCh3[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-25::obj-70" : 				{
					"parameter_longname" : "MuteCh4[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-20" : 				{
					"parameter_longname" : "Freq[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-22" : 				{
					"parameter_longname" : "TimeMode[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-23" : 				{
					"parameter_longname" : "CV2[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-28" : 				{
					"parameter_longname" : "Res[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-4" : 				{
					"parameter_longname" : "Offset[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-54" : 				{
					"parameter_longname" : "CV1[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-55" : 				{
					"parameter_longname" : "power[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-63" : 				{
					"parameter_longname" : "CV3[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-26::obj-95" : 				{
					"parameter_longname" : "ResCV[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-1" : 				{
					"parameter_longname" : "Attack[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-15" : 				{
					"parameter_longname" : "Legato[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-20" : 				{
					"parameter_longname" : "Mute[16]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-29" : 				{
					"parameter_longname" : "Decay[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-31" : 				{
					"parameter_longname" : "Release[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-27::obj-32" : 				{
					"parameter_longname" : "Sustain[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-33" : 				{
					"parameter_longname" : "Quadrants[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-55" : 				{
					"parameter_longname" : "Bypass[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-28.1::obj-5::obj-28::obj-80" : 				{
					"parameter_longname" : "Response[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-106" : 				{
					"parameter_longname" : "CV3[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-107" : 				{
					"parameter_longname" : "Linear[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-11" : 				{
					"parameter_longname" : "PWM[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-129" : 				{
					"parameter_longname" : "CV2[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-36" : 				{
					"parameter_longname" : "PW[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-4" : 				{
					"parameter_longname" : "Waveform[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-45" : 				{
					"parameter_longname" : "FreqMode[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-46" : 				{
					"parameter_longname" : "Offset[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-51" : 				{
					"parameter_longname" : "Freq[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-13::obj-53" : 				{
					"parameter_longname" : "Mute[15]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-106" : 				{
					"parameter_longname" : "CV3[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-107" : 				{
					"parameter_longname" : "Linear[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-11" : 				{
					"parameter_longname" : "PWM[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-129" : 				{
					"parameter_longname" : "CV2[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-36" : 				{
					"parameter_longname" : "PW[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-4" : 				{
					"parameter_longname" : "Waveform[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-45" : 				{
					"parameter_longname" : "FreqMode[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-46" : 				{
					"parameter_longname" : "Offset[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-51" : 				{
					"parameter_longname" : "Freq[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-14::obj-53" : 				{
					"parameter_longname" : "Mute[14]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-29" : 				{
					"parameter_longname" : "3[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-32" : 				{
					"parameter_longname" : "2[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-33" : 				{
					"parameter_longname" : "4[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-37" : 				{
					"parameter_longname" : "Mute[13]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-39" : 				{
					"parameter_longname" : "1[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-49" : 				{
					"parameter_longname" : "MuteCh1[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-58" : 				{
					"parameter_longname" : "MuteCh2[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-64" : 				{
					"parameter_longname" : "MuteCh3[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-15::obj-70" : 				{
					"parameter_longname" : "MuteCh4[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-20" : 				{
					"parameter_longname" : "Freq[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-22" : 				{
					"parameter_longname" : "TimeMode[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-23" : 				{
					"parameter_longname" : "CV2[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-28" : 				{
					"parameter_longname" : "Res[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-4" : 				{
					"parameter_longname" : "Offset[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-54" : 				{
					"parameter_longname" : "CV1[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-55" : 				{
					"parameter_longname" : "power[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-63" : 				{
					"parameter_longname" : "CV3[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-16::obj-95" : 				{
					"parameter_longname" : "ResCV[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-1" : 				{
					"parameter_longname" : "Attack[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-15" : 				{
					"parameter_longname" : "Legato[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-20" : 				{
					"parameter_longname" : "Mute[12]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-29" : 				{
					"parameter_longname" : "Decay[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-31" : 				{
					"parameter_longname" : "Release[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-17::obj-32" : 				{
					"parameter_longname" : "Sustain[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-33" : 				{
					"parameter_longname" : "Quadrants[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-55" : 				{
					"parameter_longname" : "Bypass[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-18::obj-80" : 				{
					"parameter_longname" : "Response[3]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-106" : 				{
					"parameter_longname" : "CV3[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-107" : 				{
					"parameter_longname" : "Linear[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-11" : 				{
					"parameter_longname" : "PWM[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-129" : 				{
					"parameter_longname" : "CV2[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-36" : 				{
					"parameter_longname" : "PW[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-4" : 				{
					"parameter_longname" : "Waveform[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-45" : 				{
					"parameter_longname" : "FreqMode[5]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-46" : 				{
					"parameter_longname" : "Offset[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-51" : 				{
					"parameter_longname" : "Freq[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-23::obj-53" : 				{
					"parameter_longname" : "Mute[11]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-106" : 				{
					"parameter_longname" : "CV3[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-107" : 				{
					"parameter_longname" : "Linear[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-11" : 				{
					"parameter_longname" : "PWM[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-129" : 				{
					"parameter_longname" : "CV2[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-36" : 				{
					"parameter_longname" : "PW[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-4" : 				{
					"parameter_longname" : "Waveform[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-45" : 				{
					"parameter_longname" : "FreqMode[4]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-46" : 				{
					"parameter_longname" : "Offset[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-51" : 				{
					"parameter_longname" : "Freq[7]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-24::obj-53" : 				{
					"parameter_longname" : "Mute[10]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-29" : 				{
					"parameter_longname" : "3[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-32" : 				{
					"parameter_longname" : "2[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-33" : 				{
					"parameter_longname" : "4[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-37" : 				{
					"parameter_longname" : "Mute[9]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-39" : 				{
					"parameter_longname" : "1[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-49" : 				{
					"parameter_longname" : "MuteCh1[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-58" : 				{
					"parameter_longname" : "MuteCh2[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-64" : 				{
					"parameter_longname" : "MuteCh3[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-25::obj-70" : 				{
					"parameter_longname" : "MuteCh4[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-20" : 				{
					"parameter_longname" : "Freq[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-22" : 				{
					"parameter_longname" : "TimeMode[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-23" : 				{
					"parameter_longname" : "CV2[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-28" : 				{
					"parameter_longname" : "Res[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-4" : 				{
					"parameter_longname" : "Offset[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-54" : 				{
					"parameter_longname" : "CV1[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-55" : 				{
					"parameter_longname" : "power[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-63" : 				{
					"parameter_longname" : "CV3[6]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-26::obj-95" : 				{
					"parameter_longname" : "ResCV[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-1" : 				{
					"parameter_longname" : "Attack[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-15" : 				{
					"parameter_longname" : "Legato[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-20" : 				{
					"parameter_longname" : "Mute[8]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-29" : 				{
					"parameter_longname" : "Decay[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-31" : 				{
					"parameter_longname" : "Release[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-27::obj-32" : 				{
					"parameter_longname" : "Sustain[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-33" : 				{
					"parameter_longname" : "Quadrants[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-55" : 				{
					"parameter_longname" : "Bypass[2]"
				}
,
				"obj-14::obj-6::obj-19::obj-33.1::obj-5::obj-28::obj-80" : 				{
					"parameter_longname" : "Response[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-106" : 				{
					"parameter_longname" : "CV3[5]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-107" : 				{
					"parameter_longname" : "Linear[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-11" : 				{
					"parameter_longname" : "PWM[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-129" : 				{
					"parameter_longname" : "CV2[5]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-36" : 				{
					"parameter_longname" : "PW[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-4" : 				{
					"parameter_longname" : "Waveform[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-45" : 				{
					"parameter_longname" : "FreqMode[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-46" : 				{
					"parameter_longname" : "Offset[5]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-51" : 				{
					"parameter_longname" : "Freq[5]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-13::obj-53" : 				{
					"parameter_longname" : "Mute[7]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-106" : 				{
					"parameter_longname" : "CV3[4]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-107" : 				{
					"parameter_longname" : "Linear[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-11" : 				{
					"parameter_longname" : "PWM[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-129" : 				{
					"parameter_longname" : "CV2[4]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-36" : 				{
					"parameter_longname" : "PW[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-4" : 				{
					"parameter_longname" : "Waveform[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-45" : 				{
					"parameter_longname" : "FreqMode[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-46" : 				{
					"parameter_longname" : "Offset[4]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-51" : 				{
					"parameter_longname" : "Freq[4]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-14::obj-53" : 				{
					"parameter_longname" : "Mute[6]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-29" : 				{
					"parameter_longname" : "3[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-32" : 				{
					"parameter_longname" : "2[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-33" : 				{
					"parameter_longname" : "4[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-37" : 				{
					"parameter_longname" : "Mute[5]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-39" : 				{
					"parameter_longname" : "1[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-49" : 				{
					"parameter_longname" : "MuteCh1[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-58" : 				{
					"parameter_longname" : "MuteCh2[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-64" : 				{
					"parameter_longname" : "MuteCh3[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-15::obj-70" : 				{
					"parameter_longname" : "MuteCh4[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-20" : 				{
					"parameter_longname" : "Freq[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-22" : 				{
					"parameter_longname" : "TimeMode[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-23" : 				{
					"parameter_longname" : "CV2[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-28" : 				{
					"parameter_longname" : "Res[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-4" : 				{
					"parameter_longname" : "Offset[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-54" : 				{
					"parameter_longname" : "CV1[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-55" : 				{
					"parameter_longname" : "power[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-63" : 				{
					"parameter_longname" : "CV3[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-16::obj-95" : 				{
					"parameter_longname" : "ResCV[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-1" : 				{
					"parameter_longname" : "Attack[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-15" : 				{
					"parameter_longname" : "Legato[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-20" : 				{
					"parameter_longname" : "Mute[4]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-29" : 				{
					"parameter_longname" : "Decay[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-31" : 				{
					"parameter_longname" : "Release[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-17::obj-32" : 				{
					"parameter_longname" : "Sustain[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-33" : 				{
					"parameter_longname" : "Quadrants[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-55" : 				{
					"parameter_longname" : "Bypass[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-18::obj-80" : 				{
					"parameter_longname" : "Response[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-106" : 				{
					"parameter_longname" : "CV3[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-107" : 				{
					"parameter_longname" : "Linear[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-11" : 				{
					"parameter_longname" : "PWM[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-129" : 				{
					"parameter_longname" : "CV2[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-36" : 				{
					"parameter_longname" : "PW[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-4" : 				{
					"parameter_longname" : "Waveform[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-45" : 				{
					"parameter_longname" : "FreqMode[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-46" : 				{
					"parameter_longname" : "Offset[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-51" : 				{
					"parameter_longname" : "Freq[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-23::obj-53" : 				{
					"parameter_longname" : "Mute[3]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-106" : 				{
					"parameter_longname" : "CV3[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-129" : 				{
					"parameter_longname" : "CV2[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-46" : 				{
					"parameter_longname" : "Offset[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-51" : 				{
					"parameter_longname" : "Freq[1]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-24::obj-53" : 				{
					"parameter_longname" : "Mute[2]"
				}
,
				"obj-14::obj-7::obj-13.1::obj-5::obj-25::obj-37" : 				{
					"parameter_longname" : "Mute[1]"
				}

			}
,
			"inherited_shortname" : 1
		}
,
		"dependency_cache" : [ 			{
				"name" : "background_sm.maxpat",
				"bootpath" : "C74:/packages/BEAP/misc",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "cabin_master~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "cabin_rumble~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "drive_simulator_ev.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "engine_controller_ev.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "engine_start_beap~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "engine_start_voice.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_expressive_beap~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_expressive_voice.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_pad_beap~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_powertrain.gendsp",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/gen",
				"patcherrelativepath" : "./gen",
				"type" : "gDSP",
				"implicit" : 1
			}
, 			{
				"name" : "ev_powertrain~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_relax_voice.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_soundscape_host~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_sport_beap~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "ev_sport_voice.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "keyboard_drive_ws.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "mix_master~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "road_air~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "sine.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "square.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "transient_ev~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "transient~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
, 			{
				"name" : "up.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "updown.svg",
				"bootpath" : "C74:/media/max/picts/m4l-picts",
				"type" : "svg",
				"implicit" : 1
			}
, 			{
				"name" : "vehicle_engine_ev~.maxpat",
				"bootpath" : "~/Downloads/VehicleSoundSynth-V4/patchers",
				"patcherrelativepath" : "./patchers",
				"type" : "JSON",
				"implicit" : 1
			}
 ],
		"autosave" : 0
	}

}
