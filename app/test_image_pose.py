import cv2
import os
import mediapipe as mp


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "data", "squat_test.png")


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(static_image_mode=True)


def run(image_path):
    # Bild laden
    image = cv2.imread(image_path)

    if image is None:
        print(f"Bild nicht gefunden: {image_path}")
        return

    # BGR → RGB (wichtig für MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pose Detection
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print("Keine Pose erkannt")
        return

    # Anzahl Landmarks ausgeben
    print("\nLandmarks erkannt:", len(results.pose_landmarks.landmark))

    # Skelett zeichnen
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    # Ergebnis anzeigen
    cv2.imshow("Pose Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run(IMAGE_PATH)