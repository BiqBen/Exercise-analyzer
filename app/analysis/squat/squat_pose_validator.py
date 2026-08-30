"""
Validierung der Squat-Ausgangsposition

Kriterien:
- Beine annähernd gestreckt
- Linkes und rechtes Knie ungefähr symmetrisch
- Oberkörper annähernd aufrecht
- Ausreichende Sichtbarkeit
"""


# ==========================================================
# Konfiguration
# ==========================================================

KNEE_MIN = 145
KNEE_MAX = 190

MAX_KNEE_DIFFERENCE = 10

TORSO_MAX_ANGLE = 20

MIN_VISIBILITY = 0.85
MIN_VISIBILITY_GROUPS = 2


# ==========================================================
# Squat-Ausgangsposition prüfen
# ==========================================================

def is_squat_position(analysis):

    try:

        # --------------------------------------------------
        # Knie
        # --------------------------------------------------

        knee = (
            analysis["knee"]
            ["measurements"]
        )

        average_knee_angle = (
            knee["average_angle"]
        )

        left_knee_angle = (
            knee["left_angle"]
        )

        right_knee_angle = (
            knee["right_angle"]
        )


        # --------------------------------------------------
        # Torso
        # --------------------------------------------------

        torso = (
            analysis["torso"]
            ["measurements"]
        )

        torso_angle = (
            torso["average_relative_angle"]
        )


        # --------------------------------------------------
        # Visibility
        # --------------------------------------------------

        left_knee_visibility = (
            knee["left_visibility"]
        )

        right_knee_visibility = (
            knee["right_visibility"]
        )

        left_torso_visibility = (
            torso["left_visibility"]
        )

        right_torso_visibility = (
            torso["right_visibility"]
        )

    except KeyError as e:

        print(
            f"Fehlender Key bei Squat-Validierung: {e}"
        )

        return False


    # ======================================================
    # Knie annähernd gestreckt
    # ======================================================

    if not (
        KNEE_MIN
        <= average_knee_angle
        <= KNEE_MAX
    ):
        return False


    # ======================================================
    # Symmetrie
    # ======================================================

    knee_difference = abs(
        left_knee_angle
        - right_knee_angle
    )

    if knee_difference > MAX_KNEE_DIFFERENCE:
        return False


    # ======================================================
    # Oberkörper annähernd aufrecht
    # ======================================================

    if abs(torso_angle) > TORSO_MAX_ANGLE:
        return False


    # ======================================================
    # Visibility
    # ======================================================

    visibility_counter = 0

    if (
        left_knee_visibility > MIN_VISIBILITY
        or right_knee_visibility > MIN_VISIBILITY
    ):
        visibility_counter += 1

    if (
        left_torso_visibility > MIN_VISIBILITY
        or right_torso_visibility > MIN_VISIBILITY
    ):
        visibility_counter += 1

    if visibility_counter < MIN_VISIBILITY_GROUPS:
        return False


    print(
        f"Squat start position valid: "
        f"knee={average_knee_angle:.1f}° "
        f"knee_diff={knee_difference:.1f}° "
        f"torso={torso_angle:.1f}°"
    )

    return True