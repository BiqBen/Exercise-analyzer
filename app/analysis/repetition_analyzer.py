"""
- Analyse einzelner Squat-Wiederholungen
- Extraktion biomechanischer Bewegungsmetriken
- Übergabe an Bewertungssystem
"""


from app.analysis.movement_metrics import extract_movement_metrics



def analyze_repetition(frames, repetition, fps):


    # Bewegungsmetriken der gesamten Wiederholung
    metrics = extract_movement_metrics(
        frames,
        repetition,
        fps
    )


    return {

        "frames": {
            "start": repetition["start"],
            "bottom": repetition["bottom"],
            "end": repetition["end"]
        },


        "metrics": metrics

    }