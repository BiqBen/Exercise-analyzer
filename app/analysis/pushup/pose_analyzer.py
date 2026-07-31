"""
- Analyse der Push-up-Pose eines Frames
- Berechnung biomechanischer Parameter
"""

import math
from app.pose.angle_calculator import calculate_angle
from app.pose.angle_calculator import calculate_horizontal_body_angle


def analyze_pushup_pose(landmarks, use_visibility = False):


    # -----------------------------
    # Ellenbogenwinkel
    # Schulter - Ellenbogen - Hand
    # -----------------------------

    left_elbow_angle = calculate_angle(
        landmarks["left_shoulder"],
        landmarks["left_elbow"],
        landmarks["left_wrist"]
    )

    right_elbow_angle = calculate_angle(
        landmarks["right_shoulder"],
        landmarks["right_elbow"],
        landmarks["right_wrist"]
    )

    left_elbow_visibility = min(
        landmarks["left_shoulder"].visibility,
        landmarks["left_elbow"].visibility,
        landmarks["left_wrist"].visibility
    )

    right_elbow_visibility = min(
        landmarks["right_shoulder"].visibility,
        landmarks["right_elbow"].visibility,
        landmarks["right_wrist"].visibility
    )

    # gewichteter Mittelwert
    average_elbow_angle = (
        left_elbow_angle * left_elbow_visibility +
        right_elbow_angle * right_elbow_visibility
    ) / (
        left_elbow_visibility +
        right_elbow_visibility
    )

    """
    average_elbow_angle = (
        left_elbow_angle + right_elbow_angle
    ) / 2
    """


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

    left_shoulder_angle = calculate_angle(
        landmarks["left_hip"],
        landmarks["left_shoulder"],
        landmarks["left_elbow"]
    )


    right_shoulder_angle = calculate_angle(
        landmarks["right_hip"],
        landmarks["right_shoulder"],
        landmarks["right_elbow"]
    )


    average_shoulder_angle = (
        left_shoulder_angle +
        right_shoulder_angle
    ) / 2



    return {


        "elbow": {

            "measurements": {

                "left_angle": left_elbow_angle,
                "right_angle": right_elbow_angle,
                "average_angle": average_elbow_angle

            }
        },



        "body": {

            "measurements": {

                "left_angle": left_body_angle,
                "right_angle": right_body_angle,
                "average_relative_angle": average_relative_body_angle

            }
        },



        "shoulder": {

            "measurements": {

                "left_shoulder_angle":
                    left_shoulder_angle,

                "right_shoulder_angle":
                    right_shoulder_angle,

                "average_shoulder_angle":
                    average_shoulder_angle

            }
        }

    }