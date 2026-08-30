SQUAT_METRICS = [

    {
        "title": "Minimum Knee Angle",
        "category": "knee",
        "key": "minimum_angle",
        "unit": "°",

        "min": 45,
        "max": 160,
        "optimal": (45, 90),

        "description":
            "Knee flexion at lowest squat position",

        "show_scale": True
    },


    {
        "title": "Squat Depth",
        "category": "depth",
        "key": "difference",
        "unit": "",

        # negative Werte:
        # Hüfte tiefer als Knie
        "min": -0.3,
        "max": 0.3,
        "optimal": (0, 0.3),

        "direction": "higher",

        "description":
            "Hip position relative to knee",

        "show_scale": True
    },

    {
            "title": "Range of Motion",
            "category":"knee",
            "key":"range_of_motion",
    
            "unit":"°",
            
            "min":50,
            "max":150,
    
            "optimal":(90,150),
    
            "show_scale":True
    },



    {
        "title": "Maximum Torso Lean",
        "category": "torso",
        "key": "maximum_lean",
        "unit": "°",

        # Oberkörpervorlage:
        # zu wenig = Knie wandern extrem nach vorne
        # zu viel = starke Hüftdominanz
        "min": 0,
        "max": 70,
        "optimal": (10, 45),

        "direction": "range",

        "description":
            "Forward torso inclination",

        "show_scale": True
    },
    {
        "title":"Duration",
        "category":"timing",
        "key":"duration",

        "unit":" s",

        "min":1,
        "max":8,

        "optimal":(1.5,6),

        "show_scale":True
    },


    {
        "title": "Descent Time",
        "category": "timing",
        "key": "descent_time",
        "unit": " s",

        # kontrollierte Abwärtsphase
        "min": 0.5,
        "max": 5,
        "optimal": (1, 3),

        "direction": "range",

        "description":
            "Time spent lowering",

        "show_scale": True
    },


    {
        "title": "Ascent Time",
        "category": "timing",
        "key": "ascent_time",
        "unit": " s",

        "min": 0.3,
        "max": 5,
        "optimal": (0.5, 3),

        "direction": "range",

        "description":
            "Time spent standing up",

        "show_scale": True
    },


    {
        "title": "Symmetrie",
        "category": "stability",
        "key": "average_difference",
        "unit": "°",

        # Differenz linkes/rechtes Knie
        # kleiner = besser
        "min": 0,
        "max": 20,
        "optimal": (0, 2),

        "direction": "lower",

        "description":
            "Left-right knee symmetry",

        "show_scale": True
    }

]