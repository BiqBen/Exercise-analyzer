PUSHUP_METRICS = [

    {
        "title": "Minimum Elbow Angle",
        "category": "elbow",
        "key": "minimum_angle",
        "unit": "°",

        "min": 40,
        "max": 140,

        "optimal": (40,90),

        "description":
            "minimum elbow angle during push-up",

        "show_scale": True
    },


    {
        "title": "Maximum Hip Flexion",
        "category": "hip",
        "key": "maximum_flexion",
        "unit": "°",

        "min":0,
        "max":50,

        "optimal":(0,10),

        "description":
            "Maximum hip flexion during push-up",

        "show_scale":True
    },


    {
        "title": "Range of Motion",
        "category":"elbow",
        "key":"range_of_motion",

        "unit":"°",
        
        "min":40,
        "max":150,

        "optimal":(90,150),

        "show_scale":True
    },

{
        "title":"Duration",
        "category":"timing",
        "key":"duration",

        "unit":" s",

        "min":0.6,
        "max":8,

        "optimal":(1.5,6),

        "show_scale":True
    },

    {
        "title":"Descent Time",
        "category":"timing",
        "key":"descent_time",

        "unit":" s",

        "min":0.2,
        "max":4,

        "optimal":(1,3),

        "show_scale":True
    },


    {
        "title":"Ascent Time",
        "category":"timing",
        "key":"ascent_time",

        "unit":" s",

        "min":0.2,
        "max":4,

        "optimal":(0.5,3),

        "show_scale":True
    },

    {
        "title": "Shoulder Angle (not accurate)",
        "category": "shoulder",
        "key": "average_angle",
        "unit": "°",

        "min": 20,
        "max": 100,

        "optimal": (20,60),

        "description":
            "Average shoulder angle during push-up, not accurate due to side view limitations",

        "show_scale": True
    }

]