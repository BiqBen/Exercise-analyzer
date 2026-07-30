PUSHUP_METRICS = [

    {
        "title": "Minimum Elbow Angle",
        "category": "elbow",
        "key": "minimum_angle",
        "unit": "°",

        "min": 40,
        "max": 160,

        "optimal": (70,110),

        "description":
            "Maximum elbow flexion during push-up",

        "show_scale": True
    },


    {
        "title": "Body Line Angle",
        "category": "body",
        "key": "maximum_deviation",
        "unit": "°",

        "min":0,
        "max":40,

        "optimal":(0,15),

        "direction":"lower",

        "description":
            "Hip alignment during push-up",

        "show_scale":True
    },


    {
        "title": "Push-up Depth",
        "category":"depth",
        "key":"difference",

        "unit":"",
        
        "min":0,
        "max":1,

        "optimal":(0.3,0.7),

        "show_scale":True
    },


    {
        "title":"Descent Time",
        "category":"timing",
        "key":"descent_time",

        "unit":" s",

        "min":0.2,
        "max":2,

        "optimal":(0.5,1.2),

        "show_scale":True
    },


    {
        "title":"Ascent Time",
        "category":"timing",
        "key":"ascent_time",

        "unit":" s",

        "min":0.2,
        "max":2,

        "optimal":(0.5,1),

        "show_scale":True
    }

]