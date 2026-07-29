"""
- MediaPipe Pose Estimation
- Erkennung menschlicher Körperpose
- Verarbeitung von Bilddaten zu Pose-Landmarks
"""

import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self, static=False):

        self.pose = mp.solutions.pose.Pose(
            static_image_mode=static
        )


    def process(self, image):

        image_rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        return self.pose.process(image_rgb)