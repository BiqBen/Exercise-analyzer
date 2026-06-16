import mediapipe as mp

mp_pose = mp.solutions.pose


def extract_landmarks(results):
    """
    Gibt wichtige Gelenke als (x, y) zurück.
    """

    landmarks = results.pose_landmarks.landmark

    return {
        "left_hip": (landmarks[23].x, landmarks[23].y),
        "left_knee": (landmarks[25].x, landmarks[25].y),
        "left_ankle": (landmarks[27].x, landmarks[27].y),

        "right_hip": (landmarks[24].x, landmarks[24].y),
        "right_knee": (landmarks[26].x, landmarks[26].y),
        "right_ankle": (landmarks[28].x, landmarks[28].y),
    }