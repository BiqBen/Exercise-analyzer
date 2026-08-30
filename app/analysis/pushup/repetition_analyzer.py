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

    hip_angles = []

    left_hip_angles = []
    right_hip_angles = []

    shoulder_angles = []

    left_shoulder_angles = []
    right_shoulder_angles = []


    for frame in rep_frames:

        analysis = frame["analysis"]

        elbow = analysis["elbow"]["measurements"]
        body = analysis["body"]["measurements"]
        hip = analysis["hip"]["measurements"]
        shoulder = analysis["shoulder"]["measurements"]

        elbow_angles.append(elbow["average_angle"])
        left_elbow_angles.append(elbow["left_angle"])
        right_elbow_angles.append(elbow["right_angle"])

        body_angles.append(body["average_relative_angle"])
        left_body_angles.append(body["left_angle"])
        right_body_angles.append(body["right_angle"])

        hip_angles.append(hip["average_hip_angle"])
        left_hip_angles.append(hip["left_angle"])
        right_hip_angles.append(hip["right_angle"])

        shoulder_angles.append(shoulder["average_shoulder_angle"])
        left_shoulder_angles.append(shoulder["left_shoulder_angle"])
        right_shoulder_angles.append(shoulder["right_shoulder_angle"])

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
    # Schulterwinkel
    # -----------------------------------------

    minimum_shoulder_angle = min(shoulder_angles)
    maximum_shoulder_angle = max(shoulder_angles)

    shoulder_range_of_motion = (
        maximum_shoulder_angle
        - minimum_shoulder_angle
    )

    # -----------------------------------------
    # Hüftwinkel
    # -----------------------------------------

    minimum_hip_angle = min(hip_angles)
    minimum_hip_flexion = 180 - minimum_hip_angle

    maximum_hip_angle = max(hip_angles)
    maximum_hip_flexion = 180 - maximum_hip_angle

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

    #-----------------------------------------
    # Symmetrie
    #-----------------------------------------

    elbow_symmetry = np.mean(
    np.abs(
        np.array(left_elbow_angles)
        - np.array(right_elbow_angles)
        )
    )

    body_symmetry = np.mean(
        np.abs(
            np.array(left_body_angles)
            - np.array(right_body_angles)
        )
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
    # Rückgabe
    # -----------------------------------------

    return {

        "elbow": {
            "minimum_angle": minimum_elbow_angle,
            "maximum_angle": maximum_elbow_angle,
            "range_of_motion": elbow_range_of_motion,
        },

        "body": {
            "minimum_angle": min(body_angles),
            "maximum_angle": max(body_angles),
            "average_relative_angle": np.mean(body_angles),
        },
        "hip": {
            "minimum_flexion": minimum_hip_flexion,
            "maximum_flexion": maximum_hip_flexion,
        },
         "shoulder": {
            "minimum_angle": minimum_shoulder_angle,
            "maximum_angle": maximum_shoulder_angle,
            "range_of_motion": shoulder_range_of_motion,
            "average_angle": np.mean(shoulder_angles),
        },

        "timing": {
            "duration": duration,
            "descent_time": descent_time,
            "ascent_time": ascent_time,
        },
        "symmetry": {
                    "elbow_symmetry": elbow_symmetry,
                    "body_symmetry": body_symmetry,
                },

        "velocity": {
            "descent": descent_velocity,
            "ascent": ascent_velocity,
        },

    }