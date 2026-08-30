"""
- Berechnung biomechanischer Bewegungsparameter
- Analyse einer kompletten Squat-Wiederholung
- Keine Bewertung, nur Messwerte
"""

import numpy as np


BOTTOM_THRESHOLD = 5


def extract_squat_metrics(frames, repetition, fps):

    start = repetition["start"]
    end = repetition["end"]
    bottom = repetition["bottom"]

    # -----------------------------------------
    # Nur gültige Analyse-Frames
    # -----------------------------------------

    rep_frames = []

    for frame in frames[start:end + 1]:

        analysis = frame.get("analysis")

        if analysis is not None:
            rep_frames.append(frame)

    if len(rep_frames) == 0:
        return None

    # -----------------------------------------
    # Winkel sammeln
    # -----------------------------------------

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
            torso["average_relative_angle"]
        )

    # -----------------------------------------
    # Bottom-Frame suchen
    # -----------------------------------------

    bottom_analysis = None

    # zuerst rückwärts suchen

    for i in range(bottom, start - 1, -1):

        analysis = frames[i].get("analysis")

        if analysis is not None:

            bottom_analysis = analysis
            break

    # falls nichts gefunden wurde vorwärts suchen

    if bottom_analysis is None:

        for i in range(bottom, end + 1):

            analysis = frames[i].get("analysis")

            if analysis is not None:

                bottom_analysis = analysis
                break

    if bottom_analysis is None:
        return None

    # -----------------------------------------
    # Bewegungsumfang
    # -----------------------------------------

    min_knee_angle = min(knee_angles)
    max_knee_angle = max(knee_angles)

    knee_range_of_motion = (
        max_knee_angle
        - min_knee_angle
    )


    bottom_hip_angle = (
        bottom_analysis["hip"]["measurements"]["average_angle"]
    )

    bottom_torso_angle = (
        bottom_analysis["torso"]["measurements"]["average_relative_angle"]
    )

    max_hip_flexion = (
        180 - bottom_hip_angle
    )

    max_torso_lean = bottom_torso_angle

    # -----------------------------------------
    # Squattiefe
    # -----------------------------------------

    depth = bottom_analysis["depth"]["measurements"]

    hip_y = depth["hip_y"]
    knee_y = depth["knee_y"]

    depth_difference = hip_y - knee_y

    below_parallel = (
        depth_difference > 0
    )

    # -----------------------------------------
    # Timing
    # -----------------------------------------

    descent_time = (
        bottom - start
    ) / fps

    ascent_time = (
        end - bottom
    ) / fps

    duration = (end - start) / fps

    # -----------------------------------------
    # Stabilität
    # -----------------------------------------

    differences = [

        abs(left - right)

        for left, right in zip(
            left_knee_angles,
            right_knee_angles
        )

    ]

    stability_difference = np.mean(
        differences
    )

    # -----------------------------------------
    # Rückgabe
    # -----------------------------------------

    return {

        "knee": {

            "minimum_angle": min_knee_angle,
            "maximum_angle": max_knee_angle,
            "range_of_motion": knee_range_of_motion,

        },

        "hip": {

            "maximum_flexion": max_hip_flexion

        },

        "torso": {

            "maximum_lean": max_torso_lean

        },

        "depth": {

            "hip_y": hip_y,

            "knee_y": knee_y,

            "difference": depth_difference,

            "below_parallel": below_parallel

        },

        "timing": {
            "duration": duration,

            "descent_time": descent_time,

            "ascent_time": ascent_time

        },


        "stability": {

            "average_difference": stability_difference

        }

    }