"""
Validierung der Squat-Ausgangsposition

Kriterien:
- Beide Beine befinden sich annähernd in einer gestreckten Position
- Durchschnittlicher Kniewinkel entspricht einer stehenden Position
- Linkes und rechtes Bein weisen keine zu starke Asymmetrie auf
"""


# ==========================================================
# Konfiguration
# ==========================================================

STANDING_KNEE_MIN = 145
STANDING_KNEE_MAX = 195

MAX_KNEE_DIFFERENCE = 20


# ==========================================================
# Squat-Ausgangsposition prüfen
# ==========================================================

def is_squat_position(analysis):
    """
    Prüft, ob sich die Person in einer geeigneten
    Ausgangsposition für einen Squat befindet.

    Rückgabe:
        True  -> gültige Ausgangsposition
        False -> keine gültige Ausgangsposition
    """

    try:

        measurements = (
            analysis["knee"]
            ["measurements"]
        )

        average_angle = (
            measurements["average_angle"]
        )

        left_angle = (
            measurements["left_angle"]
        )

        right_angle = (
            measurements["right_angle"]
        )

    except KeyError as e:

        print(
            f"Fehlender Key bei Squat-Validierung: {e}"
        )

        return False


    # ======================================================
    # Durchschnittlicher Kniewinkel
    # ======================================================

    if not (
        STANDING_KNEE_MIN
        <= average_angle
        <= STANDING_KNEE_MAX
    ):

        return False


    # ======================================================
    # Linkes Bein
    # ======================================================

    if not (
        STANDING_KNEE_MIN
        <= left_angle
        <= STANDING_KNEE_MAX
    ):

        return False


    # ======================================================
    # Rechtes Bein
    # ======================================================

    if not (
        STANDING_KNEE_MIN
        <= right_angle
        <= STANDING_KNEE_MAX
    ):

        return False


    # ======================================================
    # Symmetrie
    # ======================================================

    knee_difference = abs(
        left_angle
        - right_angle
    )

    if knee_difference > MAX_KNEE_DIFFERENCE:

        return False


    print(
        f"Start position valid: "
        f"knee={average_angle:.1f}° "
        f"left={left_angle:.1f}° "
        f"right={right_angle:.1f}° "
        f"difference={knee_difference:.1f}°"
    )

    return True