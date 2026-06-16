print("squat_analyzer loaded")

from app.angle_calculator import calculate_angle


def analyze_squat(landmarks):
    """
    Beidseitige Squat-Analyse (links + rechts + Stabilität)
    """

    # --- linkes Bein ---
    left_hip = landmarks["left_hip"]
    left_knee = landmarks["left_knee"]
    left_ankle = landmarks["left_ankle"]

    left_angle = calculate_angle(left_hip, left_knee, left_ankle)

    # --- rechtes Bein ---
    right_hip = landmarks["right_hip"]
    right_knee = landmarks["right_knee"]
    right_ankle = landmarks["right_ankle"]

    right_angle = calculate_angle(right_hip, right_knee, right_ankle)

    # --- Durchschnitt ---
    avg_angle = (left_angle + right_angle) / 2

    # --- Status (Tiefe) ---
    if avg_angle > 160:
        status = "stehend"
    elif avg_angle > 120:
        status = "leicht gebeugt"
    elif avg_angle > 90:
        status = "gute Squat-Tiefe"
    else:
        status = "sehr tief"

    # --- Stabilität (Asymmetrie) ---
    diff = abs(left_angle - right_angle)

    if diff < 5:
        stability = "sehr stabil"
    elif diff < 10:
        stability = "leicht asymmetrisch"
    else:
        stability = "instabil (Asymmetrie erkannt)"

    return {
        "left_angle": left_angle,
        "right_angle": right_angle,
        "average_angle": avg_angle,
        "status": status,
        "stability": stability,
        "difference": diff
    }