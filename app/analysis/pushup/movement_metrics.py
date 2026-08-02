"""
- Berechnung biomechanischer Bewegungsparameter
- Analyse einer kompletten Push-up-Wiederholung
- Keine Bewertung, nur Messwerte
"""

import numpy as np


BOTTOM_THRESHOLD = 5


def extract_pushup_metrics(frames, repetition, fps):

    start = repetition["start"]
    end = repetition["end"]
    bottom = repetition["bottom"]

    # -----------------------------------------
    # Nur gültige Frames der Wiederholung
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

    elbow_angles = []

    left_elbow_angles = []
    right_elbow_angles = []

    body_angles = []

    left_body_angles = []
    right_body_angles = []

    for frame in rep_frames:

        analysis = frame["analysis"]

        elbow = analysis["elbow"]["measurements"]
        body = analysis["body"]["measurements"]

        elbow_angles.append(elbow["average_angle"])
        left_elbow_angles.append(elbow["left_angle"])
        right_elbow_angles.append(elbow["right_angle"])

        body_angles.append(body["average_relative_angle"])
        left_body_angles.append(body["left_angle"])
        right_body_angles.append(body["right_angle"])

    # -----------------------------------------
    # Ellenbogen
    # -----------------------------------------

    minimum_elbow_angle = min(elbow_angles)
    maximum_elbow_angle = max(elbow_angles)

    elbow_range_of_motion = (
        maximum_elbow_angle
        - minimum_elbow_angle
    )

    # -----------------------------------------
    # Bottom Frame
    # -----------------------------------------

    bottom_analysis = None

    for i in range(bottom, start - 1, -1):

        analysis = frames[i].get("analysis")

        if analysis is not None:
            bottom_analysis = analysis
            break

    if bottom_analysis is None:

        for i in range(bottom, end + 1):

            analysis = frames[i].get("analysis")

            if analysis is not None:
                bottom_analysis = analysis
                break

    if bottom_analysis is None:
        return None

    bottom_elbow_angle = (
        bottom_analysis["elbow"]["measurements"]["average_angle"]
    )

    bottom_body_angle = (
        bottom_analysis["body"]["measurements"]["average_relative_angle"]
    )

    # -----------------------------------------
    # Timing
    # -----------------------------------------

    descent_time = (bottom - start) / fps
    ascent_time = (end - bottom) / fps
    duration = (end - start) / fps

    # -----------------------------------------
    # Geschwindigkeit
    # -----------------------------------------

    if descent_time > 0:
        descent_velocity = (
            elbow_angles[0] - minimum_elbow_angle
        ) / descent_time
    else:
        descent_velocity = 0

    if ascent_time > 0:
        ascent_velocity = (
            elbow_angles[-1] - minimum_elbow_angle
        ) / ascent_time
    else:
        ascent_velocity = 0

    # -----------------------------------------
    # Bottom Hold
    # -----------------------------------------

    bottom_frames = [
        angle
        for angle in elbow_angles
        if angle <= minimum_elbow_angle + BOTTOM_THRESHOLD
    ]

    bottom_time = len(bottom_frames) / fps

    # -----------------------------------------
    # Rückgabe
    # -----------------------------------------

    return {

        "elbow": {
            "minimum_angle": minimum_elbow_angle,
            "maximum_angle": maximum_elbow_angle,
            "range_of_motion": elbow_range_of_motion,
            "bottom_angle": bottom_elbow_angle,
        },

        "body": {
            "minimum_angle": min(body_angles),
            "maximum_angle": max(body_angles),
            "average_relative_angle": np.mean(body_angles),
            "bottom_angle": bottom_body_angle,
        },

        "timing": {
            "duration": duration,
            "descent_time": descent_time,
            "bottom_time": bottom_time,
            "ascent_time": ascent_time,
        },

        "velocity": {
            "descent": descent_velocity,
            "ascent": ascent_velocity,
        },

    }