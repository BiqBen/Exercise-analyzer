"""
- Analyse einzelner Squat-Wiederholungen
- Extraktion biomechanischer Bewegungsmetriken
- Übergabe an Bewertungssystem
"""


from app.analysis.squat.movement_metrics import extract_squat_metrics



def analyze_squat_repetition(frames, repetition, fps):


    # Bewegungsmetriken der gesamten Wiederholung
    metrics = extract_squat_metrics(
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