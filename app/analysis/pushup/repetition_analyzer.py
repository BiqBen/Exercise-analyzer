"""
- Analyse einzelner Push-up-Wiederholungen
- Extraktion biomechanischer Bewegungsmetriken
- Übergabe an Bewertungssystem
"""


from app.analysis.pushup.movement_metrics import extract_pushup_metrics



def analyze_pushup_repetition(frames, repetition, fps):


    # Bewegungsmetriken der gesamten Push-up-Wiederholung
    metrics = extract_pushup_metrics(
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