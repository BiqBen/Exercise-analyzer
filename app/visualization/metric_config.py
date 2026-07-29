METRICS = [

    {
        "title": "Minimum Knee Angle",
        "category": "knee",
        "key": "minimum_angle",
        "unit": "°",

        # tiefe Kniebeugung
        # ca. 60-100° gelten als sinnvoller Bereich
        "min": 30,
        "max": 120,
        "optimal": (50, 100),

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
        "min": -0.1,
        "max": 0.05,
        "optimal": (-0.08, -0.01),

        "direction": "range",

        "description":
            "Hip position relative to knee",

        "show_scale": True
    },


    {
        "title": "Maximum Hip Flexion",
        "category": "hip",
        "key": "maximum_flexion",
        "unit": "°",

        # typische Squat-Hüftflexion
        # nicht maximale Flexion im Stand!
        "min": 80,
        "max": 160,
        "optimal": (90, 140),

        "direction": "range",

        "description":
            "Maximum hip flexion during squat",

        "show_scale": True
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
        "optimal": (15, 55),

        "direction": "range",

        "description":
            "Forward torso inclination",

        "show_scale": True
    },


    {
        "title": "Descent Time",
        "category": "timing",
        "key": "descent_time",
        "unit": " s",

        # kontrollierte Abwärtsphase
        "min": 0.2,
        "max": 2.0,
        "optimal": (0.6, 1.2),

        "direction": "range",

        "description":
            "Time spent lowering",

        "show_scale": True
    },


    {
        "title": "Bottom Time",
        "category": "timing",
        "key": "bottom_time",
        "unit": " s",

        # kurze Pause ist technisch sauber
        # aber kein langer Aufenthalt
        "min": 0,
        "max": 1.5,
        "optimal": (0.1, 0.6),

        "direction": "range",

        "description":
            "Time spent at squat depth",

        "show_scale": True
    },


    {
        "title": "Ascent Time",
        "category": "timing",
        "key": "ascent_time",
        "unit": " s",

        "min": 0.2,
        "max": 2.0,
        "optimal": (0.5, 1.0),

        "direction": "range",

        "description":
            "Time spent standing up",

        "show_scale": True
    },


    {
        "title": "Descent Velocity",
        "category": "velocity",
        "key": "descent",
        "unit": "°/s",

        # Geschwindigkeit alleine ist nicht gut/schlecht
        # nur Information
        "min": 50,
        "max": 300,
        "optimal": (100, 220),

        "direction": "range",

        "description":
            "Lowering movement speed",

        "show_scale": True
    },


    {
        "title": "Ascent Velocity",
        "category": "velocity",
        "key": "ascent",
        "unit": "°/s",

        "min": 50,
        "max": 350,
        "optimal": (150, 280),

        "direction": "range",

        "description":
            "Rising movement speed",

        "show_scale": True
    },


    {
        "title": "Stability",
        "category": "stability",
        "key": "average_difference",
        "unit": "°",

        # Differenz linkes/rechtes Knie
        # kleiner = besser
        "min": 0,
        "max": 20,
        "optimal": (0, 7),

        "direction": "lower",

        "description":
            "Left-right knee symmetry",

        "show_scale": True
    }

]