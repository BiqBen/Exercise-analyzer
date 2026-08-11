PUSHUP_METRICS = [

    {
        "title": "Minimum Elbow Angle",
        "category": "elbow",
        "key": "minimum_angle",
        "unit": "°",

        "min": 35,
        "max": 160,

        "optimal": (35,60),

        "description":
            "Maximum elbow flexion during push-up",

        "show_scale": True
    },


    {
        "title": "Hip Angle",
        "category": "hip",
        "key": "average_angle",
        "unit": "°",

        "min":140,
        "max":200,

        "optimal":(165,185),

        "description":
            "Hip angle during push-up",

        "show_scale":True
    },


    {
        "title": "Range of Motion",
        "category":"elbow",
        "key":"range_of_motion",

        "unit":"°",
        
        "min":50,
        "max":150,

        "optimal":(90,150),

        "show_scale":True
    },


    {
        "title":"Descent Time",
        "category":"timing",
        "key":"descent_time",

        "unit":" s",

        "min":0.2,
        "max":3,

        "optimal":(1,3),

        "show_scale":True
    },


    {
        "title":"Ascent Time",
        "category":"timing",
        "key":"ascent_time",

        "unit":" s",

        "min":0.2,
        "max":3,

        "optimal":(0.4,2),

        "show_scale":True
    },

    {
        "title": "Shoulder Angle (not accurate)",
        "category": "shoulder",
        "key": "average_angle",
        "unit": "°",

        "min": 30,
        "max": 100,

        "optimal": (35,65),

        "description":
            "Average shoulder angle during push-up, not accurate due to side view limitations",

        "show_scale": True
    }

]