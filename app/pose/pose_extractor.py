"""
- Extraktion relevanter Körperpunkte
- Auswahl benötigter Gelenk-Landmarks
- Umwandlung in eigene Landmark-Struktur
"""

import mediapipe as mp
from app.pose.landmark import Landmark

mp_pose = mp.solutions.pose


def extract_landmarks(results):
    landmarks = results.pose_landmarks.landmark

    def lm(i):
        return Landmark(
            x=landmarks[i].x,
            y=landmarks[i].y,
            z=landmarks[i].z,
            visibility=landmarks[i].visibility
        )

    return {
        # Beine
        "left_hip": lm(23),
        "left_knee": lm(25),
        "left_ankle": lm(27),

        "right_hip": lm(24),
        "right_knee": lm(26),
        "right_ankle": lm(28),

        # Oberkörper
        "left_shoulder": lm(11),
        "right_shoulder": lm(12),

        # Arme
        "left_elbow": lm(13),
        "right_elbow": lm(14),
        "left_wrist": lm(15),
        "right_wrist": lm(16),
    }