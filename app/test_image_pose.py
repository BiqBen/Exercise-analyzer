import cv2
import os
import mediapipe as mp

from app.pose_extractor import extract_landmarks
from app.squat_analyzer import analyze_squat

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#IMAGE_PATH = os.path.join(BASE_DIR, "data", "squat_test.png")
IMAGE_PATH = os.path.join(BASE_DIR, "data", "squat_high.png")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(static_image_mode=True)


def run(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Bild nicht gefunden!")
        return

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print("Keine Pose erkannt")
        return

    # 1. Landmarks extrahieren
    landmarks = extract_landmarks(results)

    # 2. Analyse
    result = analyze_squat(landmarks)

    print(f"Left Knee: {result['left_angle']:.2f}°")
    print(f"Right Knee: {result['right_angle']:.2f}°")
    print(f"Average: {result['average_angle']:.2f}°")
    print(f"Status: {result['status']}")
    print(f"Stability: {result['stability']}")
    print(f"Difference: {result['difference']:.2f}°")


    # Visualisierung
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    cv2.imshow("Squat Analysis", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run(IMAGE_PATH)