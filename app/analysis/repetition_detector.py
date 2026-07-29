"""
- Erkennung einzelner Squat-Wiederholungen
- Segmentierung der Bewegung in Abwärts- und Aufwärtsphase
- Robuste Verarbeitung fehlender Pose-Daten
"""


# Konfiguration
START_ANGLE = 150        # Winkel kleiner -> Squat beginnt
STANDING_ANGLE = 150     # Winkel größer -> wieder aufrecht
BOTTOM_TOLERANCE = 10    # Winkelanstieg nach Tiefpunkt


def detect_repetitions(frames):

    repetitions = []

    state = "standing"

    start = None
    bottom = None
    min_angle = float("inf")


    for i, frame in enumerate(frames):

        # -----------------------------------
        # Sicherheitsprüfung
        # -----------------------------------

        analysis = frame.get("analysis")

        if analysis is None:
            continue


        try:

            knee_angle = (
                analysis
                ["knee"]
                ["measurements"]
                ["average_angle"]
            )

        except KeyError:
            continue



        # -----------------------------------
        # Start Abwärtsbewegung
        # -----------------------------------

        if state == "standing":

            if knee_angle < START_ANGLE:

                start = i
                bottom = None
                min_angle = knee_angle

                state = "descending"



        # -----------------------------------
        # Abwärtsbewegung
        # -----------------------------------

        elif state == "descending":


            if knee_angle < min_angle:

                min_angle = knee_angle
                bottom = i



            # Umkehrpunkt erkannt
            if knee_angle > min_angle + BOTTOM_TOLERANCE:

                state = "ascending"



        # -----------------------------------
        # Aufwärtsbewegung
        # -----------------------------------

        elif state == "ascending":


            if knee_angle > STANDING_ANGLE:


                # Nur gültige Wiederholung speichern

                if start is not None and bottom is not None:

                    repetitions.append(
                        {
                            "start": start,
                            "bottom": bottom,
                            "end": i
                        }
                    )


                # Reset

                state = "standing"

                start = None
                bottom = None
                min_angle = float("inf")


    return repetitions