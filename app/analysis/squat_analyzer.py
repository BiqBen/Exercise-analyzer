"""
- Analyse einer Squat-Pose
- Berechnung biomechanischer Parameter
- Bewertung von Knie, Hüfte, Tiefe und Stabilität
"""


from app.pose.angle_calculator import (calculate_angle, calculate_torso_angle)

from app.analysis.score import (
    knee_score,
    symmetry_score,
    depth_score,
    hip_score,
    torso_score,
    overall_score
)


def analyze_squat(landmarks):
    """
    Analysiert die Pose eines Squats anhand der extrahierten Landmarks.
    """

    # Landmarks

    left_hip = landmarks["left_hip"]
    left_knee = landmarks["left_knee"]
    left_ankle = landmarks["left_ankle"]

    right_hip = landmarks["right_hip"]
    right_knee = landmarks["right_knee"]
    right_ankle = landmarks["right_ankle"]

    left_shoulder = landmarks["left_shoulder"]
    right_shoulder = landmarks["right_shoulder"]


    # Kniewinkel

    left_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = calculate_angle(right_hip, right_knee, right_ankle)

    avg_angle = (left_angle + right_angle) / 2
    angle_diff = abs(left_angle - right_angle)


    # Squat-Tiefe

    avg_hip_y = (left_hip.y + right_hip.y) / 2
    avg_knee_y = (left_knee.y + right_knee.y) / 2

    depth_difference = avg_hip_y - avg_knee_y

    # --------------------------
    # Hüftwinkel
    # --------------------------

    left_hip_angle = calculate_angle(
        left_shoulder,
        left_hip,
        left_knee
    )

    right_hip_angle = calculate_angle(
        right_shoulder,
        right_hip,
        right_knee
    )

    avg_hip_angle = (
        left_hip_angle +
        right_hip_angle
    ) / 2

    # Oberkörperneigung
    # --------------------------

    left_torso_angle = calculate_torso_angle(
        left_shoulder,
        left_hip
    )

    right_torso_angle = calculate_torso_angle(
        right_shoulder,
        right_hip
    )

    avg_torso_angle = (
        left_torso_angle +
        right_torso_angle
    ) / 2

    # Scores berechnen

    knee = knee_score(avg_angle)

    symmetry = symmetry_score(angle_diff)

    depth = depth_score(depth_difference)

    hip = hip_score(avg_hip_angle)

    torso = torso_score(avg_torso_angle)

    total = overall_score(
    knee_score=knee,
    symmetry_score=symmetry,
    depth_score=depth,
    hip_score=hip,
    torso_score=torso
)


    # Ergebnisse

    return {

    "overall": {
        "score": total
    },

    "depth": {
        "score": depth,
        "measurements": {
            "hip_y": avg_hip_y,
            "knee_y": avg_knee_y,
            "difference": depth_difference
        }
    },

    "knee": {
        "score": knee,
        "measurements": {
            "left_angle": left_angle,
            "right_angle": right_angle,
            "average_angle": avg_angle
        }
    },

    "hip": {
        "score": hip,
        "measurements": {
            "left_angle": left_hip_angle,
            "right_angle": right_hip_angle,
            "average_angle": avg_hip_angle
        }
    },

    "torso": {
        "score": torso,
        "measurements": {
            "lean_angle": avg_torso_angle
        }
    },

    "stability": {
        "score": symmetry,
        "measurements": {
            "angle_difference": angle_diff
        }
    }

}