"""
- Verarbeitung von Videodaten
- Frameweise Pose Estimation
- Extraktion von Bewegungsdaten
- Berechnung biomechanischer Parameter pro Frame
"""

import cv2

from app.pose.pose_detector import PoseDetector
from app.pose.pose_extractor import extract_landmarks


def analyze_video(video_path, analyzer_function):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    detector = PoseDetector(static=False)

    frames = []


    while True:

        ret, frame = cap.read()

        if not ret:
            break


        results = detector.process(frame)


        analysis = None
        landmarks = None


        if results.pose_landmarks:

            landmarks = extract_landmarks(results)

            analysis = analyzer_function(
                landmarks
            )


        frames.append(
            {
                "frame_index": len(frames),
                "frame": frame,
                "results": results,
                "landmarks": landmarks,
                "analysis": analysis
            }
        )


    cap.release()


    return frames, fps