"""
- Analyse einer Squat-Pose eines Frames
- Berechnung biomechanischer Parameter
- Bewertung von Knie, Hüfte, Tiefe und Stabilität
"""


from app.pose.angle_calculator import (
    calculate_angle,
    calculate_vertical_torso_angle
)

def analyze_squat_pose(landmarks):
    """
    Analysiert die Pose eines Squats anhand der extrahierten Landmarks.
    """
    visibility_threshold = 0.5

    # --------------------------
    # Kniewinkel
    # --------------------------

    left_knee_angle = calculate_angle(
        landmarks["left_hip"],
        landmarks["left_knee"],
        landmarks["left_ankle"]
    )

    right_knee_angle = calculate_angle(
        landmarks["right_hip"],
        landmarks["right_knee"],
        landmarks["right_ankle"]
    )

    left_knee_visibility = min(
        landmarks["left_hip"].visibility,
        landmarks["left_knee"].visibility,
        landmarks["left_ankle"].visibility)

    right_knee_visibility = min(
        landmarks["right_hip"].visibility,
        landmarks["right_knee"].visibility,
        landmarks["right_ankle"].visibility)
    
    # gewichteter Mittelwert
    avg_knee_angle = (
        left_knee_angle * left_knee_visibility +
        right_knee_angle * right_knee_visibility
    ) / (
        left_knee_visibility +
        right_knee_visibility
    )

    """
    avg_knee_angle = (
        left_knee_angle +
        right_knee_angle
    ) / 2
    """

    if(left_knee_visibility > visibility_threshold and right_knee_visibility > visibility_threshold):
        knee_angle_diff = abs(
            left_knee_angle -
            right_knee_angle
        )
    else:
        knee_angle_diff = None
    

    # --------------------------
    # Squat-Tiefe
    # --------------------------

    avg_hip_y = (
        landmarks["left_hip"].y +
        landmarks["right_hip"].y
    ) / 2

    avg_knee_y = (
        landmarks["left_knee"].y +
        landmarks["right_knee"].y
    ) / 2

    depth_difference = (
        avg_hip_y -
        avg_knee_y
    )


    # --------------------------
    # Hüftwinkel
    # --------------------------

    left_hip_angle = calculate_angle(
        landmarks["left_shoulder"],
        landmarks["left_hip"],
        landmarks["left_knee"]
    )

    right_hip_angle = calculate_angle(
        landmarks["right_shoulder"],
        landmarks["right_hip"],
        landmarks["right_knee"]
    )

    avg_hip_angle = (
        left_hip_angle +
        right_hip_angle
    ) / 2


    # --------------------------
    # Oberkörperneigung
    # --------------------------

    left_torso_angle = calculate_vertical_torso_angle(
        landmarks["left_shoulder"],
        landmarks["left_hip"]
    )

    right_torso_angle = calculate_vertical_torso_angle(
        landmarks["right_shoulder"],
        landmarks["right_hip"]
    )

    avg_torso_angle = (
        left_torso_angle +
        right_torso_angle
    ) / 2

    # --------------------------
    # Ergebnisse
    # --------------------------

    return {

        "depth": {
            "measurements": {
                "hip_y": avg_hip_y,
                "knee_y": avg_knee_y,
                "difference": depth_difference
            }
        },

        "knee": {
            "measurements": {
                "left_angle": left_knee_angle,
                "right_angle": right_knee_angle,
                "average_angle": avg_knee_angle
            }
        },

        "hip": {
            "measurements": {
                "left_angle": left_hip_angle,
                "right_angle": right_hip_angle,
                "average_angle": avg_hip_angle
            }
        },

        "torso": {
            "measurements": {
                "lean_angle": avg_torso_angle
            }
        },

        "stability": {
            "measurements": {
                "angle_difference": knee_angle_diff
            }
        }
    }