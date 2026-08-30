"""
- Analyse der Push-up-Pose eines Frames
- Berechnung biomechanischer Parameter
"""

from app.pose.angle_calculator import calculate_angle, calculate_angle_xz
from app.pose.angle_calculator import calculate_horizontal_body_angle


def analyze_pushup_pose(landmarks):

    visibility_threshold = 0.5

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

    left_body_visibility = min(
        landmarks["left_shoulder"].visibility,  
        landmarks["left_ankle"].visibility
    )

    right_body_visibility = min(
        landmarks["right_shoulder"].visibility,
        landmarks["right_ankle"].visibility
    )

    average_relative_body_angle = (
        left_body_angle * left_body_visibility +    
        right_body_angle * right_body_visibility
    ) / (
        left_body_visibility + right_body_visibility
    )

    # -----------------------------
    # Hüftwinkel
    # Schulter - Hüfte - Knöchel
    # -----------------------------

    left_hip_angle = calculate_angle(
        landmarks["left_shoulder"],
        landmarks["left_hip"],
        landmarks["left_ankle"]
    )

    right_hip_angle = calculate_angle(
        landmarks["right_shoulder"],
        landmarks["right_hip"],
        landmarks["right_ankle"]
    )

    left_hip_visibility = min(
        landmarks["left_shoulder"].visibility,  
        landmarks["left_hip"].visibility,
        landmarks["left_ankle"].visibility
    )

    right_hip_visibility = min(
        landmarks["right_shoulder"].visibility,
        landmarks["right_hip"].visibility,
        landmarks["right_ankle"].visibility
    )

    average_hip_angle = (
        left_hip_angle * left_hip_visibility +    
        right_hip_angle * right_hip_visibility
    ) / (
        left_hip_visibility + right_hip_visibility
    )


    # -----------------------------
    # Schulter-Hüfte-Ellenbogen
    # Schulter als Vertex
    #
    # Hüfte ---- Schulter ---- Ellenbogen
    # -----------------------------

    left_shoulder_angle = calculate_angle_xz(
        landmarks["left_hip"],
        landmarks["left_shoulder"],
        landmarks["left_elbow"]
    )


    right_shoulder_angle = calculate_angle_xz(
        landmarks["right_hip"],
        landmarks["right_shoulder"],
        landmarks["right_elbow"]
    )
    
    left_shoulder_visibility = min(
        landmarks["left_hip"].visibility,
        landmarks["left_shoulder"].visibility,
        landmarks["left_elbow"].visibility  
    )

    right_shoulder_visibility = min(
        landmarks["right_hip"].visibility,
        landmarks["right_shoulder"].visibility,
        landmarks["right_elbow"].visibility
    )
    
    average_shoulder_angle = (
        left_shoulder_angle * left_shoulder_visibility +
        right_shoulder_angle * right_shoulder_visibility
    ) / (
        left_shoulder_visibility + right_shoulder_visibility
    )

    if(left_shoulder_visibility > visibility_threshold and right_shoulder_visibility > visibility_threshold):
        shoulder_angle_difference = abs(
            left_shoulder_angle - right_shoulder_angle
        )
    else:
        shoulder_angle_difference = None



    return {


        "elbow": {

            "measurements": {

                "left_angle": left_elbow_angle,
                "left_visibility": left_elbow_visibility,
                "right_angle": right_elbow_angle,
                "right_visibility": right_elbow_visibility,
                "average_angle": average_elbow_angle

            }
        },



        "body": {

            "measurements": {

                "left_angle": left_body_angle,
                "left_visibility": left_body_visibility,
                "right_angle": right_body_angle,
                "right_visibility": right_body_visibility,
                "average_relative_angle": average_relative_body_angle

            }
        },

        "hip": {

            "measurements": {

                "left_angle": left_hip_angle,
                "right_angle": right_hip_angle,
                "average_hip_angle": average_hip_angle

            }
        },


        "shoulder": {

            "measurements": {

                "left_shoulder_angle":
                    left_shoulder_angle,

                "left_visibility":
                    left_shoulder_visibility,

                "right_shoulder_angle":
                    right_shoulder_angle,

                "right_visibility":
                    right_shoulder_visibility,

                "average_shoulder_angle":
                    average_shoulder_angle,

                "shoulder_angle_difference":
                    shoulder_angle_difference

            }
        }

    }