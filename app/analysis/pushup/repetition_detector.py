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

RISING_CONFIRM_FRAMES = 5
# Anzahl aufeinanderfolgender steigender Frames,
# um den Richtungswechsel zu bestätigen

MIN_ROM = 50
# Minimal erforderlicher Bewegungsumfang

MIN_DURATION = 0.5
# Minimale Dauer einer gültigen Wiederholung in Sekunden

MIN_DESCENT_TIME = 0.25
# Minimale Dauer der Abwärtsbewegung in Sekunden


def detect_pushup_repetitions(frames, fps):

    repetitions = []

    # Debug-Ausgabe aktivieren/deaktivieren
    debug = True

    # ==========================
    # Zustände
    # ==========================

    # waiting     -> Startposition suchen
    # descending  -> Abwärtsbewegung
    # ascending   -> Aufwärtsbewegung

    state = "waiting"

    # ==========================
    # Wiederholungsdaten
    # ==========================

    start = None
    bottom = None

    start_angle = None

    # Aktuell niedrigster gemessener Winkel
    min_angle = float("inf")

    # Frame des aktuell niedrigsten Winkels
    bottom_candidate = None

    # Anzahl aufeinanderfolgender steigender Frames
    rising_counter = 0

    # Winkel des vorherigen Frames
    previous_angle = None

    # ==========================
    # Frames verarbeiten
    # ==========================

    for i, frame in enumerate(frames):

        state_before = state

        # ==========================
        # Sicherheitsprüfung
        # ==========================

        analysis = frame.get("analysis")

        if analysis is None:

            if debug:
                print(
                    f"[Frame {i:4d} | "
                    f"{i / fps:6.2f}s] "
                    f"State={state:<10} | "
                    f"NO ANALYSIS"
                )

            # previous_angle NICHT verändern,
            # da kein gültiger Winkel vorhanden ist
            continue

        # ==========================
        # Ellenbogenwinkel
        # ==========================

        try:

            elbow_angle = (
                analysis["elbow"]
                ["measurements"]
                ["average_angle"]
            )

        except KeyError:

            if debug:
                print(
                    f"[Frame {i:4d} | "
                    f"{i / fps:6.2f}s] "
                    f"State={state:<10} | "
                    f"NO ELBOW ANGLE"
                )

            continue

        # ==========================
        # Push-up Position prüfen
        # ==========================

        pushup_ready = False

        if state == "waiting":

            pushup_ready = is_pushup_position(
                analysis
            )

        # ==========================
        # Start einer Wiederholung
        # ==========================

        if state == "waiting":

            if pushup_ready:

                start = i

                start_angle = elbow_angle

                bottom = None

                # Startwinkel ist zunächst
                # auch das aktuelle Minimum
                min_angle = elbow_angle

                bottom_candidate = i

                # Steigende Frames zurücksetzen
                rising_counter = 0

                # Vorherigen Winkel setzen
                previous_angle = elbow_angle

                state = "descending"

        # ==========================
        # Abwärtsbewegung
        # ==========================

        elif state == "descending":

            # ----------------------------------
            # Neues Minimum gefunden
            # ----------------------------------

            if elbow_angle < min_angle:

                min_angle = elbow_angle

                bottom_candidate = i

                # Die bisherige steigende Bewegung
                # ist damit unterbrochen
                rising_counter = 0

            # ----------------------------------
            # Winkel steigt gegenüber
            # dem vorherigen Frame
            # ----------------------------------

            elif (
                previous_angle is not None
                and elbow_angle > previous_angle
            ):

                rising_counter += 1

            # ----------------------------------
            # Winkel steigt nicht mehr
            # ----------------------------------

            else:

                rising_counter = 0

            # ----------------------------------
            # Richtungswechsel bestätigen
            # ----------------------------------

            if (
                rising_counter
                >= RISING_CONFIRM_FRAMES
            ):

                bottom = bottom_candidate

                state = "ascending"

                rising_counter = 0

        # ==========================
        # Aufwärtsbewegung
        # ==========================

        elif state == "ascending":

            # Arm wieder ausreichend gestreckt
            if elbow_angle > END_ANGLE:

                if (
                    start is not None
                    and bottom is not None
                ):

                    # --------------------------
                    # Bewegungsumfang
                    # --------------------------

                    rom = (
                        start_angle
                        - min_angle
                    )

                    # --------------------------
                    # Gesamtdauer
                    # --------------------------

                    duration = (
                        i - start
                    ) / fps

                    # --------------------------
                    # Abwärtsdauer
                    # --------------------------

                    descent_time = (
                        bottom - start
                    ) / fps

                    valid = True

                    # ==========================
                    # Validierung
                    # ==========================

                    # ROM
                    if rom < MIN_ROM:

                        valid = False

                        if debug:
                            print(
                                f"  -> ROM zu klein: "
                                f"{rom:.1f}° < "
                                f"{MIN_ROM}°"
                            )

                    # Gesamtdauer
                    if duration < MIN_DURATION:

                        valid = False

                        if debug:
                            print(
                                f"  -> Dauer zu kurz: "
                                f"{duration:.2f}s < "
                                f"{MIN_DURATION}s"
                            )

                    # Abwärtsdauer
                    if (
                        descent_time
                        < MIN_DESCENT_TIME
                    ):

                        valid = False

                        if debug:
                            print(
                                f"  -> Abwärtsbewegung "
                                f"zu kurz: "
                                f"{descent_time:.2f}s < "
                                f"{MIN_DESCENT_TIME}s"
                            )

                    # ==========================
                    # Ergebnis
                    # ==========================

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

                        if debug:
                            print(
                                f"  -> REP ERKANNT | "
                                f"start={start}, "
                                f"bottom={bottom}, "
                                f"end={i}, "
                                f"ROM={rom:.1f}°, "
                                f"duration={duration:.2f}s"
                            )

                    else:

                        if debug:
                            print(
                                "  -> REP VERWORFEN"
                            )

                # ==========================
                # Reset
                # ==========================

                state = "waiting"

                start = None
                bottom = None
                start_angle = None

                min_angle = float("inf")

                bottom_candidate = None

                rising_counter = 0

                previous_angle = None

        # ==========================
        # DEBUG FÜR JEDEN FRAME
        # ==========================

        if debug:

            if min_angle == float("inf"):
                min_display = "None"
            else:
                min_display = f"{min_angle:.1f}°"

            print(
                f"[Frame {i:4d} | "
                f"{i / fps:6.2f}s] "
                f"{state_before:<10} -> "
                f"{state:<10} | "
                f"angle={elbow_angle:6.1f}° | "
                f"ready={str(pushup_ready):5} | "
                f"start={str(start):>4} | "
                f"min={min_display:>7} | "
                f"bottom={str(bottom):>4} | "
                f"candidate={str(bottom_candidate):>4} | "
                f"rising={rising_counter}/{RISING_CONFIRM_FRAMES}"
            )

        # ==========================
        # Vorherigen Winkel speichern
        # ==========================

        previous_angle = elbow_angle

    return repetitions