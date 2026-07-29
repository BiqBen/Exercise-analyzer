"""
- Visualisierung von Videoanalysen
- Overlay von Pose und Bewertung
- Endloswiedergabe des Videos
"""

import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def show_video_with_overlay(video_path, frames):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Video konnte nicht geöffnet werden")
        return


    frame_index = 0


    while True:

        ret, frame = cap.read()


        # Videoende erreicht
        if not ret:

            # zurück zum Anfang springen
            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

            frame_index = 0

            continue



        # passende Analyse suchen
        if frame_index < len(frames):

            data = frames[frame_index]


            results = data["results"]


            # Pose zeichnen
            if results.pose_landmarks:

                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )


            # Werte aus Analyse
            analysis = data["analysis"]


            knee = analysis["knee"]["measurements"]["average_angle"]
            hip = analysis["hip"]["measurements"]["average_angle"]
            torso = analysis["torso"]["measurements"]["lean_angle"]


            # Overlay Text

            cv2.putText(
                frame,
                f"Knee: {knee:.1f} deg",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )


            cv2.putText(
                frame,
                f"Hip: {hip:.1f} deg",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2
            )


            cv2.putText(
                frame,
                f"Torso: {torso:.1f} deg",
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )


        cv2.imshow(
            "Squat Analysis",
            frame
        )


        frame_index += 1



        # ESC beendet Programm
        key = cv2.waitKey(30)


        if key == 27:
            break



    cap.release()
    cv2.destroyAllWindows()