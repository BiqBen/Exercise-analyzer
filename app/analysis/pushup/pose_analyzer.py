"""
- Analyse der Push-up-Pose eines Frames
- Berechnung biomechanischer Parameter
"""

import math
from app.pose.angle_calculator import calculate_angle
from app.pose.angle_calculator import calculate_horizontal_body_angle


def analyze_pushup_pose(landmarks):


    # -----------------------------
    # Ellenbogenwinkel
    # Schulter - Ellenbogen - Hand
    # -----------------------------

    left_elbow = calculate_angle(
        landmarks["left_shoulder"],
        landmarks["left_elbow"],
        landmarks["left_wrist"]
    )


    right_elbow = calculate_angle(
        landmarks["right_shoulder"],
        landmarks["right_elbow"],
        landmarks["right_wrist"]
    )


    average_elbow = (
        left_elbow + right_elbow
    ) / 2



    # -----------------------------
    # Körperlinie relativ horizontal
    # Schulter -> Knöchel
    # -----------------------------

    left_body_angle = calculate_horizontal_body_angle(
        landmarks["left_shoulder"],
        landmarks["left_ankle"]
    )


    right_body_angle = calculate_horizontal_body_angle(
        landmarks["right_shoulder"],
        landmarks["right_ankle"]
    )

    average_relative_body_angle = (
        left_body_angle +
        right_body_angle
    ) / 2



    # -----------------------------
    # Schulter-Hüfte-Ellenbogen
    # Schulter als Vertex
    #
    # Hüfte ---- Schulter ---- Ellenbogen
    # -----------------------------

    left_hip_shoulder_elbow = calculate_angle(
        landmarks["left_hip"],
        landmarks["left_shoulder"],
        landmarks["left_elbow"]
    )


    right_hip_shoulder_elbow = calculate_angle(
        landmarks["right_hip"],
        landmarks["right_shoulder"],
        landmarks["right_elbow"]
    )


    average_hip_shoulder_elbow = (
        left_hip_shoulder_elbow +
        right_hip_shoulder_elbow
    ) / 2



    return {


        "elbow": {

            "measurements": {

                "left_angle": left_elbow,
                "right_angle": right_elbow,
                "average_angle": average_elbow

            }
        },



        "body": {

            "measurements": {

                "left_angle": left_body_angle,
                "right_angle": right_body_angle,
                "average_relative_angle": average_relative_body_angle

            }
        },



        "pushup": {

            "measurements": {

                "left_hip_shoulder_elbow":
                    left_hip_shoulder_elbow,

                "right_hip_shoulder_elbow":
                    right_hip_shoulder_elbow,

                "hip_shoulder_elbow":
                    average_hip_shoulder_elbow

            }
        }

    }