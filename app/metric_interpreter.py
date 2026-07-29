"""
- Interpretation biomechanischer Messwerte
- Umwandlung numerischer Werte in verständliche Kategorien
"""


def interpret_knee_angle(angle):
    """
    Kniewinkel im tiefsten Punkt
    kleiner Winkel = größere Flexion
    """

    if angle < 60:
        return "Sehr tief (hohe Knieflexion)"

    elif angle < 90:
        return "Tief (gute Squat-Tiefe)"

    elif angle < 120:
        return "Mittel"

    else:
        return "Geringe Beugung"


def interpret_hip_flexion(flexion):

    if flexion > 120:
        return "Sehr starke Hüftbeugung"

    elif flexion > 90:
        return "Starke Hüftbeugung"

    elif flexion > 60:
        return "Moderate Hüftbeugung"

    else:
        return "Geringe Hüftbeugung"



def interpret_torso(angle):

    if angle < 20:
        return "Aufrechter Oberkörper"

    elif angle < 40:
        return "Moderate Vorneigung"

    elif angle < 60:
        return "Starke Vorneigung"

    else:
        return "Sehr starke Vorneigung"



def interpret_velocity(speed):

    if speed < 80:
        return "Langsame Bewegung"

    elif speed < 180:
        return "Kontrollierte Geschwindigkeit"

    else:
        return "Schnelle Bewegung"



def interpret_stability(angle_difference):

    if angle_difference < 5:
        return "Sehr stabil"

    elif angle_difference < 10:
        return "Leichte Asymmetrie"

    else:
        return "Deutliche Asymmetrie"