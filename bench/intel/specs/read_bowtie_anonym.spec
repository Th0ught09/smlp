{
    "version": "1.2",
    "variables": [
        {
            "label": "p0",
            "interface": "input",
            "type": "real"
        },
        {
            "label": "p1",
            "interface": "input",
            "type": "int"
        },
        {
            "label": "p2",
            "interface": "input",
            "type": "int"
        },
        {
            "label": "p3",
            "interface": "input",
            "type": "int"
        },
        {
            "label": "p4",
            "interface": "knob",
            "type": "real",
            "grid": [
                0.85,
                0.87,
                0.89,
                0.91,
                0.93,
                0.95
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p5",
            "interface": "knob",
            "type": "int",
            "grid": [
                -1,
                0,
                1
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p6",
            "interface": "knob",
            "type": "int",
            "grid": [
                -1,
                0,
                1
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p7",
            "interface": "knob",
            "type": "real",
            "grid": [
                6.7,
                12.3,
                17.900000000000002,
                23.5,
                29.1,
                34.7
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p8",
            "interface": "knob",
            "type": "real",
            "grid": [
                3.3,
                5.5,
                7.7,
                9.9,
                12.100000000000001,
                14.3
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p9",
            "interface": "knob",
            "type": "int",
            "grid": [
                -1,
                0,
                1
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p10",
            "interface": "knob",
            "type": "real",
            "grid": [
                2.6,
                2.83,
                3.06,
                3.29,
                3.52,
                3.75
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p11",
            "interface": "knob",
            "type": "int",
            "grid": [
                -1,
                0,
                1
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p12",
            "interface": "knob",
            "type": "real",
            "grid": [
                8.6,
                11.68,
                14.76,
                17.84,
                20.92,
                24.0
            ],
            "rad-rel": 0.05
        },
        {
            "label": "p13",
            "interface": "knob",
            "type": "real",
            "rad-rel": 0.05
        },
        {
            "label": "p14",
            "interface": "knob",
            "type": "real",
            "rad-rel": 0.05
        },
        {
            "label": "p15",
            "interface": "knob",
            "type": "real",
            "rad-rel": 0.05
        },
        {
            "label": "o0",
            "interface": "output",
            "type": "real"
        },
        {
            "label": "o1",
            "interface": "output",
            "type": "real"
        },
        {
            "label": "o2",
            "interface": "output",
            "type": "real"
        },
        {
            "label": "o3",
            "interface": "output",
            "type": "real"
        }
    ],
    "alpha": "p0 < 10",
    "assertions": {
        "o0_lower": "o0 >= 0.015",
        "o0_upper": "o0 <= 0.055",
        "o1_lower": "o1 >= 12",
        "o1_upper": "o1 <= 38",
        "o2_lower": "o2 >= 0.06",
        "o2_upper": "o2 <= 0.32",
        "o3_lower": "o3 >= 42",
        "o3_upper": "o3 <= 63",
        "o0_o1_trade": "o0 < 0.025 and o1 > 20",
        "o2_o3_constraint": "o2 + (o3 / 100) <= 0.4",
        "o1_o3_ratio": "o1 / (o3 - 40) > 0.5",
        "output_stability": "(o0 + o1 / 100) <= 0.5",
        "combined_metric": "(o0 * o1) + (o2 * o3 / 100) <= 1.0",
        "knob_p4_tight": "p4 > 0.88 and p4 < 0.94",
        "knob_p13_tight": "p13 >= 0.55 and p13 <= 0.75"
    },
    "objectives": {
        "objv_o0": "(o0 + o1)",
        "objv_o1": "o1",
        "objv_o2": "o2",
        "objv_o3": "o3"
    }
}
