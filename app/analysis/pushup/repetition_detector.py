"""
- Erkennung einzelner Pushup-Wiederholungen
- Segmentierung in Abwärts- und Aufwärtsphase
- Validierung über Bewegungsumfang und Dauer
- Nutzung eines externen Pose Validators
- Robuste Verarbeitung fehlender Pose-Daten
"""


from app.analysis.pushup.pushup_pose_validator import is_pushup_position



# ==========================
# Konfiguration
# ==========================

START_ANGLE = 145
# Minimaler Ellenbogenwinkel zum Erkennen der oberen Startposition

END_ANGLE = 145
# Ellenbogenwinkel, der zum Abschluss einer Wiederholung erreicht werden muss

BOTTOM_TOLERANCE = 8
# Erlaubte Winkelabweichung vom Tiefpunkt zur Kompensation von Messrauschen

BOTTOM_CONFIRM_FRAMES = 5
# Anzahl aufeinanderfolgender Frames zur Bestätigung des Tiefpunkts

MIN_ROM = 50
# Minimal erforderlicher Bewegungsumfang (Range of Motion) einer Wiederholung

MIN_DURATION = 0.5
# Minimale Dauer einer gültigen Wiederholung in Sekunden

MIN_DESCENT_TIME = 0.25
# Minimale Dauer der Abwärtsbewegung in Sekunden




def detect_pushup_repetitions(frames, fps):


    repetitions = []


    # Zustände:
    #
    # waiting     -> Startposition suchen
    # descending  -> Abwärtsbewegung
    # ascending   -> Aufwärtsbewegung
    #

    state = "waiting"



    start = None
    bottom = None

    start_angle = None


    min_angle = float("inf")


    bottom_candidate = None
    bottom_counter = 0


    for i, frame in enumerate(frames):


        # ==========================
        # Sicherheitsprüfung
        # ==========================

        analysis = frame.get("analysis")


        if analysis is None:
            continue



        try:

            elbow_angle = (
                analysis["elbow"]
                ["measurements"]
                ["average_angle"]
            )


        except KeyError:

            continue



        # ==========================
        # Startposition prüfen
        #
        # NUR im waiting Zustand!
        # ==========================

        pushup_ready = False


        if state == "waiting":


            pushup_ready = is_pushup_position(
                analysis
            )


            print(
                i,
                "Pushup position:",
                pushup_ready
            )



        # ==========================
        # Start einer Wiederholung
        # ==========================

        if state == "waiting":


            if pushup_ready:

                pushup_active = True

                start = i

                start_angle = elbow_angle

                bottom = None

                min_angle = elbow_angle


                bottom_candidate = None

                bottom_counter = 0


                state = "descending"




        # ==========================
        # Abwärtsbewegung
        # ==========================

        elif state == "descending":



            # neues Minimum suchen

            if elbow_angle < min_angle:


                min_angle = elbow_angle

                bottom_candidate = i

                bottom_counter = 0




            # Tiefpunkt bestätigen

            if bottom_candidate is not None:



                if elbow_angle <= (
                    min_angle
                    + BOTTOM_TOLERANCE
                ):


                    bottom_counter += 1


                else:


                    bottom_counter = 0




                if (
                    bottom_counter
                    >= BOTTOM_CONFIRM_FRAMES
                ):


                    bottom = bottom_candidate




            # Richtungswechsel erkannt

            if bottom is not None:


                if elbow_angle > (
                    min_angle
                    + BOTTOM_TOLERANCE
                ):


                    state = "ascending"





        # ==========================
        # Aufwärtsbewegung
        # ==========================

        elif state == "ascending":



            # Arm wieder gestreckt

            if elbow_angle > END_ANGLE:



                if (
                    start is not None
                    and bottom is not None
                ):



                    rom = (
                        start_angle
                        -
                        min_angle
                    )


                    duration = (
                        i - start
                    ) / fps



                    descent_time = (
                        bottom - start
                    ) / fps




                    valid = True




                    if rom < MIN_ROM:


                        valid = False

                        print(
                            "Pushup verworfen: ROM zu klein"
                        )




                    if duration < MIN_DURATION:


                        valid = False

                        print(
                            "Pushup verworfen: zu kurz"
                        )




                    if descent_time < MIN_DESCENT_TIME:


                        valid = False

                        print(
                            "Pushup verworfen: Abwärtsbewegung zu kurz"
                        )





                    if valid:



                        repetitions.append(
                            {
                                "start": start,
                                "bottom": bottom,
                                "end": i,

                                "rom": rom,

                                "duration": duration
                            }
                        )


                        print(
                            f"Rep erkannt: "
                            f"start={start}, "
                            f"bottom={bottom}, "
                            f"end={i}, "
                            f"ROM={rom:.1f}"
                        )




                # Reset für nächste Wiederholung

                state = "waiting"

                start = None

                bottom = None

                start_angle = None

                min_angle = float("inf")

                bottom_candidate = None

                bottom_counter = 0




    return repetitions