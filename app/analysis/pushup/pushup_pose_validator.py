"""
Validierung der Push-up Ausgangsposition

Kriterien:
- Körperlinie ungefähr horizontal
- Hüfte-Schulter-Ellenbogen Winkel im gültigen Bereich
- Arm zwischen Hand-Ellenbogen-Schulter gestreckt
"""


BODY_MAX_HORIZONTAL = 30


MIN_SHOULDER_HIP_ELBOW = 40
MAX_SHOULDER_HIP_ELBOW = 100


ARM_STRAIGHT_MIN = 140
ARM_STRAIGHT_MAX = 200

MIN_VISIBILITY = 0.85
MIN_COUNTER = 2




def is_pushup_position(analysis):


    try:


        body_angle = (
            analysis["body"]
            ["measurements"]
            ["average_relative_angle"]
        )

        left_body_visibility = (
            analysis["body"]
            ["measurements"]
            ["left_visibility"]
        )

        right_body_visibility = (
            analysis["body"]
            ["measurements"]
            ["right_visibility"]
        )


        shoulder_angle = (
            analysis["shoulder"]
            ["measurements"]
            ["average_shoulder_angle"]
        )

        left_shoulder_visibility = (
            analysis["shoulder"]
            ["measurements"]
            ["left_visibility"]
        )

        right_shoulder_visibility = (
            analysis["shoulder"]
            ["measurements"]
            ["right_visibility"]
        )


        arm_angle = (
            analysis["elbow"]
            ["measurements"]
            ["average_angle"]
        )

        left_elbow_visibility = (
            analysis["elbow"]
            ["measurements"]
            ["left_visibility"]
        )

        right_elbow_visibility = (
            analysis["elbow"]
            ["measurements"]
            ["right_visibility"]
        )
    

        #print(f"body={body_angle:.1f}, average_shoulder_angle={shoulder_angle:.1f}, arm={arm_angle:.1f}")


    except KeyError as e:

        print("Fehlender Key:", e)
        print(analysis.keys())
        return False

    
    # --------------------------------
    # Körperlinie
    # --------------------------------

    if abs(body_angle) > BODY_MAX_HORIZONTAL:
        #print("FALSE: Körper nicht horizontal genug")
        return False



    # --------------------------------
    # Schulter-Hüfte-Ellenbogen
    # --------------------------------

    if not (
        MIN_SHOULDER_HIP_ELBOW
        <=
        shoulder_angle
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

    counter = 0

    if (
        (left_body_visibility > MIN_VISIBILITY or right_body_visibility > MIN_VISIBILITY)
    ):
        counter += 1

    if (left_shoulder_visibility > MIN_VISIBILITY or right_shoulder_visibility > MIN_VISIBILITY):
        counter += 1

    if (left_elbow_visibility > MIN_VISIBILITY or right_elbow_visibility > MIN_VISIBILITY):
        counter += 1


    if counter < MIN_COUNTER:
        print(f"FALSE: Sichtbarkeit zu gering (body(l,r)=({left_body_visibility:.2f}, {right_body_visibility:.2f}), shoulder(l,r)=({left_shoulder_visibility:.2f}, {right_shoulder_visibility:.2f}), elbow(l,r)=({left_elbow_visibility:.2f}, {right_elbow_visibility:.2f}))")
        return False
    

    print(f"Start position valid: body={body_angle:.1f} visibility (l,r)=({left_body_visibility:.2f}, {right_body_visibility:.2f}), average_shoulder_angle={shoulder_angle:.1f} visibility (l,r)=({left_shoulder_visibility:.2f}, {right_shoulder_visibility:.2f}), arm={arm_angle:.1f} visibility (l,r)=({left_elbow_visibility:.2f}, {right_elbow_visibility:.2f})")
    return True
