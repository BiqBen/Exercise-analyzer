"""
- Erkennung einzelner Pushup-Wiederholungen
- Segmentierung in Abwärts- und Aufwärtsphase
- Validierung über Bewegungsumfang und Dauer
- Nutzung eines externen Pose Validators
- Robuste Verarbeitung fehlender Pose-Daten
- Mehrframe-Bestätigung der initialen Push-up-Position
- Erkennung des tatsächlichen Bewegungsbeginns
"""

from app.analysis.pushup.pushup_pose_validator import (
    is_pushup_position
)


# ==========================================================
# Konfiguration
# ==========================================================

START_ANGLE = 145

# Ellenbogenwinkel der oberen Startposition


END_ANGLE = 145

# Ellenbogenwinkel zum Abschluss einer Wiederholung


BOTTOM_TOLERANCE = 8

# Erlaubte Winkelabweichung vom Tiefpunkt


BOTTOM_CONFIRM_FRAMES = 5

# Anzahl Frames zur Bestätigung des Tiefpunkts


MIN_ROM = 50

# Minimal erforderlicher Bewegungsumfang


MIN_DURATION = 0.4

# Minimale Dauer einer Wiederholung in Sekunden


MIN_DESCENT_TIME = 0.25

# Minimale Dauer der Abwärtsbewegung


# ==========================================================
# Startposition
# ==========================================================

START_CONFIRM_FRAMES = 3


# ==========================================================
# Bewegungsbeginn
# ==========================================================

MOVEMENT_CONFIRM_FRAMES = 3

# Abwärtsbewegung muss über mehrere Frames
# bestätigt werden.


MOVEMENT_THRESHOLD = 5

# Mindeständerung des Ellenbogenwinkels.


# ==========================================================
# Obere Position
# ==========================================================

TOP_TOLERANCE = 5

# Toleranz für die obere Position.


TOP_CONFIRM_FRAMES = 3

# Anzahl Frames zur Bestätigung der oberen Position.


# ==========================================================
# Repetition Detector
# ==========================================================

def detect_pushup_repetitions(frames, fps):

    repetitions = []


    # ======================================================
    # Zustände
    # ======================================================

    # waiting
    #     Initiale Push-up-Position suchen.
    #
    # ready
    #     Obere Position bestätigt.
    #     Auf tatsächliche Abwärtsbewegung warten.
    #
    # descending
    #     Abwärtsbewegung.
    #
    # ascending
    #     Aufwärtsbewegung.

    state = "waiting"


    # ======================================================
    # Wiederholungsdaten
    # ======================================================

    start = None

    bottom = None

    start_angle = None

    min_angle = float("inf")

    bottom_candidate = None

    bottom_counter = 0


    # ======================================================
    # Startposition
    # ======================================================

    start_confirm_counter = 0

    start_candidate = None


    # ======================================================
    # Bewegungsbeginn
    # ======================================================

    movement_counter = 0


    # ======================================================
    # Obere Position
    # ======================================================

    top_counter = 0


    # ======================================================
    # Reset nach abgeschlossener Wiederholung
    # ======================================================

    def reset_repetition():

        nonlocal start
        nonlocal bottom
        nonlocal min_angle
        nonlocal bottom_candidate
        nonlocal bottom_counter
        nonlocal movement_counter
        nonlocal top_counter

        start = None

        bottom = None

        # WICHTIG:
        #
        # start_angle wird hier NICHT zurückgesetzt.
        #
        # Der aktuelle obere Winkel wird benötigt,
        # um im "ready"-Zustand die nächste
        # Abwärtsbewegung zu erkennen.

        min_angle = float("inf")

        bottom_candidate = None

        bottom_counter = 0

        movement_counter = 0

        top_counter = 0


    # ======================================================
    # Hauptschleife
    # ======================================================

    for i, frame in enumerate(frames):


        # ==================================================
        # Analyse vorhanden?
        # ==================================================

        analysis = frame.get("analysis")


        if analysis is None:

            if state == "waiting":

                start_confirm_counter = 0

                start_candidate = None

            continue


        # ==================================================
        # Ellenbogenwinkel
        # ==================================================

        try:

            elbow_angle = (
                analysis["elbow"]
                ["measurements"]
                ["average_angle"]
            )

        except KeyError:

            if state == "waiting":

                start_confirm_counter = 0

                start_candidate = None

            continue


        # ==================================================
        # WAITING
        # ==================================================

        if state == "waiting":

            pushup_ready = is_pushup_position(
                analysis
            )


            print(
                i,
                "Pushup position:",
                pushup_ready
            )


            # ----------------------------------------------
            # Position gültig
            # ----------------------------------------------

            if pushup_ready:

                if start_candidate is None:

                    start_candidate = i


                start_confirm_counter += 1


                print(
                    f"Startposition: "
                    f"{start_confirm_counter}/"
                    f"{START_CONFIRM_FRAMES}"
                )


            # ----------------------------------------------
            # Position ungültig
            # ----------------------------------------------

            else:

                start_confirm_counter = 0

                start_candidate = None


            # ----------------------------------------------
            # Position bestätigt
            # ----------------------------------------------

            if (
                start_confirm_counter
                >= START_CONFIRM_FRAMES
            ):

                start = start_candidate

                start_angle = elbow_angle

                min_angle = elbow_angle

                bottom = None

                bottom_candidate = None

                bottom_counter = 0

                movement_counter = 0

                top_counter = 0


                state = "ready"


                start_confirm_counter = 0

                start_candidate = None


                print(
                    f"[{i}] "
                    f"Push-up position confirmed "
                    f"(angle={start_angle:.1f})"
                )


        # ==================================================
        # READY
        # ==================================================

        elif state == "ready":

            """
            Die Person befindet sich oben.

            Wichtig:
            start_angle bleibt erhalten.

            Dadurch kann geprüft werden, ob sich der
            Ellenbogenwinkel tatsächlich verändert.
            """

            # --------------------------------------------------
            # Sicherheitsprüfung
            # --------------------------------------------------

            if start_angle is None:

                # Falls aus irgendeinem Grund kein
                # Referenzwinkel vorhanden ist, wird
                # der aktuelle Winkel verwendet.

                start_angle = elbow_angle


            # --------------------------------------------------
            # Winkeländerung bestimmen
            # --------------------------------------------------

            angle_change = (
                start_angle
                -
                elbow_angle
            )


            print(
                f"[{i}] "
                f"READY | "
                f"start={start_angle:.1f} | "
                f"current={elbow_angle:.1f} | "
                f"change={angle_change:.1f}"
            )


            # --------------------------------------------------
            # Abwärtsbewegung
            # --------------------------------------------------

            if angle_change >= MOVEMENT_THRESHOLD:

                movement_counter += 1


            else:

                movement_counter = 0


            # --------------------------------------------------
            # Bewegung bestätigt
            # --------------------------------------------------

            if (
                movement_counter
                >= MOVEMENT_CONFIRM_FRAMES
            ):

                # Start der tatsächlichen Bewegung.
                #
                # Die letzten Frames werden einbezogen,
                # damit die Wiederholung nicht erst
                # mehrere Frames nach Bewegungsbeginn
                # startet.

                start = (
                    i
                    -
                    MOVEMENT_CONFIRM_FRAMES
                    +
                    1
                )


                # Der Winkel am tatsächlichen Beginn
                # wird als Startwinkel verwendet.

                try:

                    start_analysis = frames[
                        start
                    ].get("analysis")


                    start_angle = (
                        start_analysis["elbow"]
                        ["measurements"]
                        ["average_angle"]
                    )

                except (
                    KeyError,
                    TypeError,
                    AttributeError
                ):

                    start_angle = elbow_angle


                min_angle = elbow_angle

                bottom = None

                bottom_candidate = None

                bottom_counter = 0

                movement_counter = 0


                state = "descending"


                print(
                    f"[{i}] "
                    f"DESCENDING | "
                    f"start={start} | "
                    f"start_angle="
                    f"{start_angle:.1f}"
                )


        # ==================================================
        # DESCENDING
        # ==================================================

        elif state == "descending":


            # ----------------------------------------------
            # Neues Minimum
            # ----------------------------------------------

            if elbow_angle < min_angle:

                min_angle = elbow_angle

                bottom_candidate = i

                bottom_counter = 0


            # ----------------------------------------------
            # Tiefpunkt bestätigen
            # ----------------------------------------------

            if bottom_candidate is not None:

                if elbow_angle <= (
                    min_angle
                    +
                    BOTTOM_TOLERANCE
                ):

                    bottom_counter += 1

                else:

                    bottom_counter = 0


                if (
                    bottom_counter
                    >= BOTTOM_CONFIRM_FRAMES
                ):

                    bottom = bottom_candidate


                    print(
                        f"[{i}] "
                        f"BOTTOM confirmed: "
                        f"{bottom}"
                    )


            # ----------------------------------------------
            # Aufwärtsbewegung
            # ----------------------------------------------

            if bottom is not None:

                if elbow_angle > (
                    min_angle
                    +
                    BOTTOM_TOLERANCE
                ):

                    state = "ascending"

                    top_counter = 0


                    print(
                        f"[{i}] "
                        f"ASCENDING"
                    )


        # ==================================================
        # ASCENDING
        # ==================================================

        elif state == "ascending":


            # ----------------------------------------------
            # Obere Position
            # ----------------------------------------------

            if start_angle is None:

                top_threshold = (
                    END_ANGLE
                    -
                    TOP_TOLERANCE
                )

            else:

                top_threshold = max(
                    END_ANGLE
                    -
                    TOP_TOLERANCE,

                    start_angle
                    -
                    TOP_TOLERANCE
                )


            # ----------------------------------------------
            # Winkel erreicht?
            # ----------------------------------------------

            if elbow_angle >= top_threshold:

                top_counter += 1


                print(
                    f"[{i}] "
                    f"TOP "
                    f"{top_counter}/"
                    f"{TOP_CONFIRM_FRAMES} "
                    f"| angle="
                    f"{elbow_angle:.1f}"
                )


            else:

                top_counter = 0


            # ----------------------------------------------
            # Obere Position bestätigt
            # ----------------------------------------------

            if (
                top_counter
                >= TOP_CONFIRM_FRAMES
            ):


                if (
                    start is not None
                    and bottom is not None
                    and start_angle is not None
                ):


                    # ======================================
                    # ROM
                    # ======================================

                    rom = (
                        start_angle
                        -
                        min_angle
                    )


                    # ======================================
                    # Gesamtdauer
                    # ======================================

                    duration = (
                        i
                        -
                        start
                    ) / fps


                    # ======================================
                    # Abwärtsdauer
                    # ======================================

                    descent_time = (
                        bottom
                        -
                        start
                    ) / fps


                    # ======================================
                    # Validierung
                    # ======================================

                    valid = True


                    # --------------------------------------
                    # ROM
                    # --------------------------------------

                    if rom < MIN_ROM:

                        valid = False

                        print(
                            "Pushup verworfen: "
                            "ROM zu klein | "
                            f"ROM={rom:.1f}"
                        )


                    # --------------------------------------
                    # Gesamtdauer
                    # --------------------------------------

                    if duration < MIN_DURATION:

                        valid = False

                        print(
                            "Pushup verworfen: "
                            "zu kurz | "
                            f"duration="
                            f"{duration:.2f}s"
                        )


                    # --------------------------------------
                    # Abwärtsdauer
                    # --------------------------------------

                    if (
                        descent_time
                        <
                        MIN_DESCENT_TIME
                    ):

                        valid = False

                        print(
                            "Pushup verworfen: "
                            "Abwärtsbewegung "
                            "zu kurz | "
                            f"{descent_time:.2f}s"
                        )


                    # ======================================
                    # Wiederholung speichern
                    # ======================================

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
                            f"ROM={rom:.1f}, "
                            f"duration="
                            f"{duration:.2f}s"
                        )


                # ==========================================
                # Reset
                # ==========================================

                reset_repetition()


                # Wichtig:
                #
                # Nicht zurück zu "waiting".
                #
                # Die Person befindet sich bereits in der
                # Push-up-Position. Deshalb direkt wieder
                # auf eine neue Abwärtsbewegung warten.

                state = "ready"


                print(
                    f"[{i}] "
                    f"READY FOR NEXT REP"
                )


    return repetitions