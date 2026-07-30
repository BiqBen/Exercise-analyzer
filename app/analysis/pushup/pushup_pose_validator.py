"""
Validierung der Push-up Ausgangsposition

Kriterien:
- Körperlinie ungefähr horizontal
- Hüfte-Schulter-Ellenbogen Winkel im gültigen Bereich
- Arm zwischen Hand-Ellenbogen-Schulter gestreckt
"""


BODY_MAX_HORIZONTAL = 20


MIN_SHOULDER_HIP_ELBOW = 40
MAX_SHOULDER_HIP_ELBOW = 120


ARM_STRAIGHT_MIN = 145
ARM_STRAIGHT_MAX = 200



def is_pushup_position(analysis):


    try:


        body_angle = (
            analysis["body"]
            ["measurements"]
            ["average_relative_angle"]
        )


        hip_shoulder_elbow = (
            analysis["pushup"]
            ["measurements"]
            ["hip_shoulder_elbow"]
        )


        arm_angle = (
            analysis["elbow"]
            ["measurements"]
            ["average_angle"]
        )

        print(
            f"body={body_angle:.1f}, hip_shoulder_elbow={hip_shoulder_elbow:.1f}, arm={arm_angle:.1f}"
        )


    except KeyError as e:

        print("Fehlender Key:", e)
        print(analysis.keys())
        return False

    
    # --------------------------------
    # Körperlinie
    # --------------------------------

    if abs(body_angle) > BODY_MAX_HORIZONTAL:
        print("FALSE: Körper nicht horizontal genug")
        return False



    # --------------------------------
    # Schulter-Hüfte-Ellenbogen
    # --------------------------------

    if not (
        MIN_SHOULDER_HIP_ELBOW
        <=
        hip_shoulder_elbow
        <=
        MAX_SHOULDER_HIP_ELBOW
    ):

        return False



    # --------------------------------
    # Arm gestreckt
    # --------------------------------

    if not (
        ARM_STRAIGHT_MIN
        <=
        arm_angle
        <=
        ARM_STRAIGHT_MAX
    ):

        return False



    return True