"""
- Visualisierung von Videoanalysen
- Erzeugung von Frames mit Pose Overlay
"""

import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



def create_overlay_frame(data):

    frame = data["frame"].copy()


    results = data["results"]


    # -----------------------------
    # Skeleton
    # -----------------------------

    if results.pose_landmarks:

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    return frame