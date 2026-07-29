"""
- Berechnung von Gelenkwinkeln aus Landmark-Koordinaten
- Berechnung biomechanischer Körperwinkel
- Grundlage für Bewegungsbewertung
"""

import math

def calculate_angle(a, b, c):
    """
    Berechnet Winkel zwischen 3 Landmarks
    a, b, c = Landmark-Objekte
    """

    ba_x = a.x - b.x
    ba_y = a.y - b.y

    bc_x = c.x - b.x
    bc_y = c.y - b.y

    dot = ba_x * bc_x + ba_y * bc_y

    mag_ba = (ba_x**2 + ba_y**2) ** 0.5
    mag_bc = (bc_x**2 + bc_y**2) ** 0.5

    if mag_ba * mag_bc == 0:
        return 0.0

    cos_angle = dot / (mag_ba * mag_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.degrees(math.acos(cos_angle))

def calculate_torso_angle(shoulder, hip):
    """
    Berechnet die Oberkörperneigung relativ zur Vertikalen.

    shoulder: Schulter Landmark
    hip: Hüfte Landmark

    Rückgabe:
    Winkel in Grad
    """

    # Vektor Hüfte -> Schulter
    dx = shoulder.x - hip.x
    dy = shoulder.y - hip.y

    # Winkel zur vertikalen Achse
    angle = math.degrees(
        math.atan2(abs(dx), abs(dy))
    )

    return angle