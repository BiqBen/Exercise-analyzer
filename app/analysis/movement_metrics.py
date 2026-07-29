"""
- Berechnung biomechanischer Bewegungsparameter
- Analyse einer kompletten Squat-Wiederholung
- Keine Bewertung, nur Messwerte
"""


import numpy as np



def extract_movement_metrics(frames, repetition, fps):


    start = repetition["start"]
    end = repetition["end"]


    # Frames der Wiederholung

    rep_frames = frames[start:end+1]


    knee_angles = []
    hip_angles = []
    torso_angles = []

    left_knee_angles = []
    right_knee_angles = []



    for frame in rep_frames:

        analysis = frame["analysis"]


        knee = analysis["knee"]["measurements"]
        hip = analysis["hip"]["measurements"]
        torso = analysis["torso"]["measurements"]



        knee_angles.append(
            knee["average_angle"]
        )


        left_knee_angles.append(
            knee["left_angle"]
        )


        right_knee_angles.append(
            knee["right_angle"]
        )


        hip_angles.append(
            hip["average_angle"]
        )


        torso_angles.append(
            torso["lean_angle"]
        )



    # ==================================================
    # Bewegungsumfang
    # ==================================================


    min_knee_angle = min(knee_angles)



    # Bottom Frame

    bottom_index = repetition["bottom"]

    bottom_analysis = frames[bottom_index]["analysis"]



    bottom_hip_angle = (
        bottom_analysis["hip"]
        ["measurements"]
        ["average_angle"]
    )


    bottom_torso_angle = (
        bottom_analysis["torso"]
        ["measurements"]
        ["lean_angle"]
    )



    max_hip_flexion = (
        180 - bottom_hip_angle
    )


    max_torso_lean = bottom_torso_angle



    # ==================================================
    # Squat Tiefe
    # ==================================================


    depth = bottom_analysis["depth"]["measurements"]


    hip_y = depth["hip_y"]

    knee_y = depth["knee_y"]


    depth_difference = (
        hip_y - knee_y
    )


    # Hüfte unter Knie?

    below_parallel = (
        depth_difference > 0
    )



    # ==================================================
    # Timing
    # ==================================================


    bottom = repetition["bottom"]



    descent_time = (
        bottom - start
    ) / fps



    ascent_time = (
        end - bottom
    ) / fps



    if descent_time > 0:

        descent_velocity = (
            knee_angles[0] - min_knee_angle
        ) / descent_time

    else:

        descent_velocity = 0




    if ascent_time > 0:

        ascent_velocity = (
            knee_angles[-1] - min_knee_angle
        ) / ascent_time

    else:

        ascent_velocity = 0



    # ==================================================
    # Bottom Position halten
    # ==================================================


    bottom_threshold = 5


    bottom_frames = [

        angle for angle in knee_angles

        if angle <= min_knee_angle + bottom_threshold

    ]


    bottom_time = (
        len(bottom_frames) / fps
    )



    # ==================================================
    # Stabilität
    # ==================================================


    differences = []


    for left, right in zip(
        left_knee_angles,
        right_knee_angles
    ):

        differences.append(
            abs(left-right)
        )


    stability_difference = np.mean(
        differences
    )



    # ==================================================
    # Rückgabe
    # ==================================================


    return {


        "knee": {

            "minimum_angle":
                min_knee_angle

        },


        "hip": {

            "maximum_flexion":
                max_hip_flexion

        },


        "torso": {

            "maximum_lean":
                max_torso_lean

        },


        "depth": {

            "hip_y":
                hip_y,

            "knee_y":
                knee_y,

            "difference":
                depth_difference,

            "below_parallel":
                below_parallel

        },


        "timing": {

            "descent_time":
                descent_time,

            "bottom_time":
                bottom_time,

            "ascent_time":
                ascent_time

        },


        "velocity": {

            "descent":
                descent_velocity,

            "ascent":
                ascent_velocity

        },


        "stability": {

            "average_difference":
                stability_difference

        }

    }