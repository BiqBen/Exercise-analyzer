"""
- Erkennung einzelner Pushup-Wiederholungen
- Segmentierung in Abwärts- und Aufwärtsphase
- Ermittlung von tatsächlichem Start-, Tief- und Endpunkt
- Separate Ermittlung des maximalen Ellenbogenwinkels
- Robuste Richtungsbestimmung über Trendfenster
- Start einer Wiederholung erst bei bestätigter Abwärtsbewegung
- Erkennung eines stabilen oberen Plateaus
- Abschluss einer offenen Wiederholung am Videoende
- Validierung über Bewegungsumfang und Dauer
- Nutzung eines externen Pose Validators
- Robuste Verarbeitung fehlender Pose-Daten
- Kontinuierliche Erkennung direkt aufeinanderfolgender Wiederholungen
"""

from collections import deque

from app.analysis.repetition_utils import (
    format_frame,
    format_angle,
    get_angle_trend,
    find_descent_start,
    get_top_plateau,
    get_plateau_start,
)

from app.analysis.pushup.pushup_pose_validator import (
    is_pushup_position
)


# ==========================================================
# Konfiguration
# ==========================================================

END_ANGLE = 130

TREND_WINDOW = 10
MIN_TREND_COUNT = 7
ANGLE_TOLERANCE = 0.4

START_MOVEMENT_THRESHOLD = 0.8
READY_BUFFER_SIZE = 30

TOP_END_WINDOW = 6
TOP_END_MAX_RANGE = 2.0

TOP_STABLE_FRAMES = 10
TOP_STABLE_TOLERANCE = 1.0

MIN_ROM = 50
MIN_DURATION = 0.5
MIN_DESCENT_TIME = 0.25


STATE_LABELS = {
    "waiting": "WAIT",
    "ready": "READY",
    "descending": "DOWN",
    "ascending": "UP",
    "ascending_top": "TOP",
}

TREND_LABELS = {
    "neutral": "-",
    "rising": "UP",
    "falling": "DOWN",
}


# ==========================================================
# Debug-Ausgabe
# ==========================================================

def print_frame_debug(
    i,
    fps,
    state_before,
    state,
    elbow_angle,
    trend,
    start,
    bottom,
    end_candidate,
    min_angle,
    max_angle,
    rising_count,
    falling_count,
    neutral_count
):
    before = STATE_LABELS[state_before]
    current = STATE_LABELS[state]

    if state_before != state:
        state_display = f"{before:>5}>{current:<5}"
    else:
        state_display = f"{current:^11}"

    print(
        f"[{i:04d} {i / fps:6.2f}s] "
        f"{state_display} | "
        f"A={elbow_angle:6.1f} | "
        f"T={TREND_LABELS[trend]:<4} | "
        f"S={format_frame(start)} "
        f"B={format_frame(bottom)} "
        f"E={format_frame(end_candidate)} | "
        f"min={format_angle(min_angle)} "
        f"max={format_angle(max_angle)} | "
        f"R/F/N="
        f"{rising_count}/"
        f"{falling_count}/"
        f"{neutral_count}"
    )


# ==========================================================
# Wiederholung validieren und speichern
# ==========================================================

def finalize_repetition(
    repetitions,
    fps,
    start,
    bottom,
    end,
    min_angle,
    max_angle,
    max_angle_frame,
    debug=True,
    reason=""
):
    if (
        start is None
        or bottom is None
        or end is None
        or max_angle is None
        or min_angle == float("inf")
    ):
        return False

    rom = max_angle - min_angle

    duration = (
        end - start
    ) / fps

    descent_time = (
        bottom - start
    ) / fps

    ascend_time = (
        end - bottom
    ) / fps

    valid = True

    if rom < MIN_ROM:
        valid = False

        if debug:
            print(
                f"      INVALID "
                f"ROM={rom:.1f}° "
                f"< {MIN_ROM}°"
            )

    if duration < MIN_DURATION:
        valid = False

        if debug:
            print(
                f"      INVALID "
                f"time={duration:.2f}s "
                f"< {MIN_DURATION:.2f}s"
            )

    if descent_time < MIN_DESCENT_TIME:
        valid = False

        if debug:
            print(
                f"      INVALID "
                f"down={descent_time:.2f}s "
                f"< {MIN_DESCENT_TIME:.2f}s"
            )

    if not valid:
        if debug:
            print(
                f"      DROP   "
                f"S={start:04d} "
                f"B={bottom:04d} "
                f"E={end:04d}"
            )

        return False

    repetitions.append(
        {
            "start": start,
            "bottom": bottom,
            "end": end,
            "rom": rom,
            "duration": duration,
            "descent_time": descent_time,
            "ascend_time": ascend_time,
            "min_angle": min_angle,
            "max_angle": max_angle,
            "max_angle_frame": max_angle_frame,
        }
    )

    if debug:
        reason_display = (
            f" reason={reason}"
            if reason
            else ""
        )

        print(
            f"      REP    "
            f"S={start:04d} "
            f"B={bottom:04d} "
            f"E={end:04d} | "
            f"min={min_angle:5.1f}° "
            f"max={max_angle:5.1f}° "
            f"@{format_frame(max_angle_frame)} | "
            f"ROM={rom:5.1f}° | "
            f"down={descent_time:.2f}s "
            f"up={ascend_time:.2f}s "
            f"total={duration:.2f}s"
            f"{reason_display}"
        )

    return True


# ==========================================================
# Push-up-Wiederholungen erkennen
# ==========================================================

def detect_pushup_repetitions(frames, fps):

    repetitions = []
    debug = True

    state = "waiting"

    start = None
    start_angle = None

    bottom = None
    bottom_candidate = None

    end_candidate = None

    min_angle = float("inf")

    max_angle = None
    max_angle_frame = None

    angle_window = deque(
        maxlen=TREND_WINDOW
    )

    ready_buffer = deque(
        maxlen=READY_BUFFER_SIZE
    )

    top_end_window = deque(
        maxlen=TOP_END_WINDOW
    )

    next_descent_angles = []

    top_stable_count = 0


    # ======================================================
    # Frames verarbeiten
    # ======================================================

    for i, frame in enumerate(frames):

        state_before = state

        analysis = frame.get("analysis")

        if analysis is None:

            if debug:
                print(
                    f"[{i:04d} {i / fps:6.2f}s] "
                    f"{STATE_LABELS[state]:^11} | "
                    f"NO ANALYSIS"
                )

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

            if debug:
                print(
                    f"[{i:04d} {i / fps:6.2f}s] "
                    f"{STATE_LABELS[state]:^11} | "
                    f"NO ELBOW ANGLE"
                )

            continue


        # ==================================================
        # Trend
        # ==================================================

        angle_window.append(
            elbow_angle
        )

        (
            trend,
            rising_count,
            falling_count,
            neutral_count
        ) = get_angle_trend(
            angle_window,
            TREND_WINDOW,
            MIN_TREND_COUNT,
            ANGLE_TOLERANCE
        )


        # ==================================================
        # WAITING
        # ==================================================

        if state == "waiting":

            if is_pushup_position(analysis):

                ready_buffer.clear()

                ready_buffer.append(
                    (i, elbow_angle)
                )

                angle_window.clear()

                angle_window.append(
                    elbow_angle
                )

                state = "ready"


        # ==================================================
        # READY
        # ==================================================

        elif state == "ready":

            ready_buffer.append(
                (i, elbow_angle)
            )

            if trend == "falling":

                (
                    start,
                    start_angle
                ) = find_descent_start(
                    ready_buffer,
                    START_MOVEMENT_THRESHOLD
                )

                if start is None:
                    start = i
                    start_angle = elbow_angle

                descent_values = [
                    value
                    for value in ready_buffer
                    if value[0] >= start
                ]

                if descent_values:

                    (
                        bottom_candidate,
                        min_angle
                    ) = min(
                        descent_values,
                        key=lambda value: value[1]
                    )

                else:
                    bottom_candidate = i
                    min_angle = elbow_angle

                bottom = None
                end_candidate = None

                max_angle = None
                max_angle_frame = None

                next_descent_angles.clear()

                top_end_window.clear()

                top_stable_count = 0

                state = "descending"

                if debug:
                    print(
                        f"      START  "
                        f"frame={start:04d} "
                        f"angle={start_angle:6.1f}° "
                        f"confirmed={i:04d}"
                    )


        # ==================================================
        # DESCENDING
        # ==================================================

        elif state == "descending":

            if elbow_angle < min_angle:
                min_angle = elbow_angle
                bottom_candidate = i

            if trend == "rising":

                bottom = bottom_candidate

                if debug:
                    print(
                        f"      BOTTOM "
                        f"frame={bottom:04d} "
                        f"angle={min_angle:6.1f}° "
                        f"confirmed={i:04d}"
                    )

                max_angle = elbow_angle
                max_angle_frame = i

                angle_window.clear()

                angle_window.append(
                    elbow_angle
                )

                state = "ascending"


        # ==================================================
        # ASCENDING
        # ==================================================

        elif state == "ascending":

            if (
                max_angle is None
                or elbow_angle > max_angle
            ):
                max_angle = elbow_angle
                max_angle_frame = i

            if (
                max_angle is not None
                and max_angle >= END_ANGLE
            ):

                state = "ascending_top"

                angle_window.clear()

                angle_window.append(
                    elbow_angle
                )

                top_end_window.clear()

                top_end_window.append(
                    (i, elbow_angle)
                )

                next_descent_angles = [
                    (i, elbow_angle)
                ]

                top_stable_count = 0


        # ==================================================
        # ASCENDING TOP
        # ==================================================

        elif state == "ascending_top":

            if elbow_angle > max_angle:
                max_angle = elbow_angle
                max_angle_frame = i
                top_stable_count = 0

            top_end_window.append(
                (i, elbow_angle)
            )


            # ----------------------------------------------
            # oberes Plateau
            # ----------------------------------------------

            if (
                end_candidate is None
                and get_top_plateau(
                    top_end_window,
                    TOP_END_WINDOW,
                    TOP_END_MAX_RANGE
                )
            ):

                end_candidate = (
                    get_plateau_start(
                        top_end_window
                    )
                )

                if debug:
                    print(
                        f"      END    "
                        f"frame={end_candidate:04d} "
                        f"confirmed={i:04d}"
                    )


            # ----------------------------------------------
            # mögliche nächste Abwärtsbewegung
            # ----------------------------------------------

            next_descent_angles.append(
                (i, elbow_angle)
            )


            # ----------------------------------------------
            # Stabilität oben
            # ----------------------------------------------

            if (
                abs(
                    elbow_angle
                    - max_angle
                )
                <= TOP_STABLE_TOLERANCE
            ):
                top_stable_count += 1

            else:
                top_stable_count = 0


            # ==================================================
            # nächste Wiederholung beginnt
            # ==================================================

            if trend == "falling":

                if end_candidate is None:
                    end_candidate = (
                        max_angle_frame
                    )

                finalize_repetition(
                    repetitions=repetitions,
                    fps=fps,
                    start=start,
                    bottom=bottom,
                    end=end_candidate,
                    min_angle=min_angle,
                    max_angle=max_angle,
                    max_angle_frame=max_angle_frame,
                    debug=debug,
                    reason="falling"
                )

                valid_next_angles = [
                    value
                    for value in next_descent_angles
                    if (
                        max_angle_frame is not None
                        and value[0] >= max_angle_frame
                    )
                ]

                (
                    start,
                    start_angle
                ) = find_descent_start(
                    valid_next_angles,
                    START_MOVEMENT_THRESHOLD
                )

                if start is None:
                    start = max_angle_frame
                    start_angle = max_angle

                descent_values = [
                    value
                    for value in valid_next_angles
                    if value[0] >= start
                ]

                if descent_values:

                    (
                        bottom_candidate,
                        min_angle
                    ) = min(
                        descent_values,
                        key=lambda value: value[1]
                    )

                else:
                    bottom_candidate = start
                    min_angle = start_angle

                bottom = None

                end_candidate = None

                max_angle = None
                max_angle_frame = None

                state = "descending"

                angle_window.clear()

                for _, angle in (
                    descent_values[-TREND_WINDOW:]
                ):
                    angle_window.append(
                        angle
                    )

                ready_buffer.clear()

                top_end_window.clear()

                next_descent_angles.clear()

                top_stable_count = 0


            # ==================================================
            # stabiles Top
            # ==================================================

            elif (
                top_stable_count
                >= TOP_STABLE_FRAMES
            ):

                if end_candidate is None:
                    end_candidate = (
                        max_angle_frame
                    )

                saved = finalize_repetition(
                    repetitions=repetitions,
                    fps=fps,
                    start=start,
                    bottom=bottom,
                    end=end_candidate,
                    min_angle=min_angle,
                    max_angle=max_angle,
                    max_angle_frame=max_angle_frame,
                    debug=debug,
                    reason="stable_top"
                )

                if saved:

                    ready_buffer.clear()

                    ready_buffer.append(
                        (i, elbow_angle)
                    )

                    angle_window.clear()

                    angle_window.append(
                        elbow_angle
                    )

                    top_end_window.clear()

                    next_descent_angles.clear()

                    start = None
                    start_angle = None

                    bottom = None
                    bottom_candidate = None

                    end_candidate = None

                    min_angle = float("inf")

                    max_angle = None
                    max_angle_frame = None

                    top_stable_count = 0

                    state = "ready"


        # ==================================================
        # Debug
        # ==================================================

        if debug:

            print_frame_debug(
                i=i,
                fps=fps,
                state_before=state_before,
                state=state,
                elbow_angle=elbow_angle,
                trend=trend,
                start=start,
                bottom=bottom,
                end_candidate=end_candidate,
                min_angle=min_angle,
                max_angle=max_angle,
                rising_count=rising_count,
                falling_count=falling_count,
                neutral_count=neutral_count
            )


    # ======================================================
    # Videoende
    # ======================================================

    if (
        state == "ascending_top"
        and start is not None
        and bottom is not None
        and max_angle is not None
        and max_angle >= END_ANGLE
    ):

        if end_candidate is None:
            end_candidate = max_angle_frame

        if debug:
            print(
                "      EOF    "
                "offene TOP-Wiederholung wird geprüft"
            )

        finalize_repetition(
            repetitions=repetitions,
            fps=fps,
            start=start,
            bottom=bottom,
            end=end_candidate,
            min_angle=min_angle,
            max_angle=max_angle,
            max_angle_frame=max_angle_frame,
            debug=debug,
            reason="video_end"
        )


    return repetitions