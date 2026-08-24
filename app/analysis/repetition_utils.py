"""
Übungsunabhängige Hilfsfunktionen für die Wiederholungserkennung.

Enthält:
- Formatierung von Debug-Werten
- Erkennung des Winkeltrends
- Rückwirkende Bestimmung des Bewegungsbeginns
- Erkennung eines stabilen oberen Plateaus
"""

# ==========================================================
# Debug-Hilfsfunktionen
# ==========================================================


def format_frame(value):
    if value is None:
        return "----"

    return f"{value:04d}"


def format_angle(value):
    if value is None or value == float("inf"):
        return " ---.-"

    return f"{value:6.1f}"


# ==========================================================
# Trend bestimmen
# ==========================================================


def get_angle_trend(
    angle_window,
    trend_window,
    min_trend_count,
    angle_tolerance
):
    """
    Bestimmt die Bewegungsrichtung anhand eines
    Fensters aufeinanderfolgender Winkelwerte.

    Rückgabe:
        trend
        rising_count
        falling_count
        neutral_count
    """

    if len(angle_window) < trend_window:
        return "neutral", 0, 0, 0

    rising_count = 0
    falling_count = 0
    neutral_count = 0

    angles = list(angle_window)

    for previous, current in zip(
        angles[:-1],
        angles[1:]
    ):
        difference = current - previous

        if difference > angle_tolerance:
            rising_count += 1

        elif difference < -angle_tolerance:
            falling_count += 1

        else:
            neutral_count += 1

    if rising_count >= min_trend_count:
        trend = "rising"

    elif falling_count >= min_trend_count:
        trend = "falling"

    else:
        trend = "neutral"

    return (
        trend,
        rising_count,
        falling_count,
        neutral_count
    )


# ==========================================================
# Bewegungsbeginn bestimmen
# ==========================================================


def find_descent_start(
    buffer,
    movement_threshold
):
    """
    Bestimmt rückwirkend den tatsächlichen Beginn
    einer bestätigten Abwärtsbewegung.

    buffer:
        Folge von (frame_index, angle)

    Rückgabe:
        frame_index
        angle
    """

    if not buffer:
        return None, None

    if len(buffer) == 1:
        return buffer[0]

    values = list(buffer)

    start_position = len(values) - 1

    significant_falling_found = False

    for j in range(
        len(values) - 1,
        0,
        -1
    ):
        current_angle = values[j][1]
        previous_angle = values[j - 1][1]

        difference = (
            current_angle
            - previous_angle
        )

        # deutliche Abwärtsbewegung
        if difference < -movement_threshold:
            start_position = j - 1
            significant_falling_found = True

        # kleine Schwankung
        elif abs(difference) <= movement_threshold:
            if significant_falling_found:
                continue

        # deutliche Gegenbewegung
        else:
            if significant_falling_found:
                break

    return values[start_position]


# ==========================================================
# Plateau-Erkennung
# ==========================================================


def get_top_plateau(
    top_end_window,
    required_window_size,
    max_range
):
    """
    Prüft, ob die Winkel innerhalb des Fensters
    ausreichend stabil sind.
    """

    if len(top_end_window) < required_window_size:
        return False

    angles = [
        angle
        for _, angle in top_end_window
    ]

    angle_range = (
        max(angles)
        - min(angles)
    )

    return angle_range <= max_range


def get_plateau_start(top_end_window):
    """
    Gibt den ersten Frame des erkannten
    Plateau-Fensters zurück.
    """

    if not top_end_window:
        return None

    return top_end_window[0][0]