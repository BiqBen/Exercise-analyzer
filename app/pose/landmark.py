"""
- Definition der Landmark-Datenstruktur
- Speicherung von Körperpunkt-Koordinaten (x, y, z)
- Einheitliche Verarbeitung von Pose-Daten
"""

class Landmark:
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Landmark(x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"