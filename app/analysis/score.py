"""
- Berechnung einzelner Qualitäts-Scores
- Bewertung biomechanischer Kriterien
- Berechnung des Gesamtscores
"""

import math


def knee_score(avg_angle):
    """
    Bewertung der Kniebeugung.
    """

    if avg_angle >= 160:
        return 0

    elif avg_angle >= 130:
        return 20

    elif avg_angle >= 100:
        return 40

    elif avg_angle >= 70:
        return 100

    else:
        # sehr tiefer Squat
        return 85



def symmetry_score(diff):
    """
    Bewertung der Links-Rechts-Symmetrie
    """

    if diff <= 5:
        return 100

    elif diff <= 10:
        return 80

    elif diff <= 15:
        return 60

    else:
        return 30



def depth_score(depth_difference):
    """
    Bewertung der Squat-Tiefe.
    """

    return int(100 * (1 / (1 + math.exp(-80 * depth_difference))))



def hip_score(hip_angle):
    """
    Bewertung des Hüftwinkels.
    """

    if 45 <= hip_angle <= 90:
        return 100

    elif 90 < hip_angle <= 120:
        return 80

    elif 120 < hip_angle <= 160:
        return 50

    elif hip_angle > 160:
        return 20

    else:
        # extreme Hüftflexion
        return 30



def torso_score(lean_angle):
    """
    Bewertung der Oberkörperneigung.
    """

    if 15 <= lean_angle <= 35:
        return 100

    elif 35 < lean_angle <= 45:
        return 80

    elif 45 < lean_angle <= 60:
        return 50

    elif lean_angle < 15:
        return 80

    else:
        return 30



def overall_score(
        knee_score,
        symmetry_score,
        depth_score,
        hip_score,
        torso_score
):


    return round(
        0.25 * knee_score +
        0.25 * depth_score +
        0.15 * symmetry_score +
        0.20 * hip_score +
        0.15 * torso_score,
        1
    )