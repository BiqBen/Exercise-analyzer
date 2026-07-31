"""
- Berechnung von Gelenkwinkeln aus Landmark-Koordinaten
- Berechnung biomechanischer Körperwinkel
- Grundlage für Bewegungsbewertung
"""

import math

def calculate_angle(a, b, c, return_visibility=False):
    """
    Berechnet Winkel zwischen 3 Landmarks, gewichtet auf visibility.
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

    #print(a.visibility, b.visibility, c.visibility)
    if return_visibility:
        return math.degrees(math.acos(cos_angle)), min(a.visibility, b.visibility, c.visibility)

    return math.degrees(math.acos(cos_angle))

def calculate_vertical_torso_angle(shoulder, hip):
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


def calculate_horizontal_body_angle(shoulder, ankle):
    """
    Berechnet die Körperneigung relativ zur Horizontalen.

    Schulter -> Knöchel bildet die Körperlinie.

    Rückgabe:
    Winkel in Grad

    0°   = perfekt horizontal (Push-up Position)
    90°  = vertikal stehend
    """

    dx = ankle.x - shoulder.x
    dy = ankle.y - shoulder.y


    angle = math.degrees(
        math.atan2(abs(dy), abs(dx))
    )


    return angle