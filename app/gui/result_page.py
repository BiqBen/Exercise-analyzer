import customtkinter as ctk
import cv2
import time

from PIL import Image

from app.visualization.video_visualizer import create_overlay_frame
from app.analysis.squat.metrics import SQUAT_METRICS
from app.analysis.pushup.metrics import PUSHUP_METRICS
from app.visualization.metric_widgets import create_metric_row



class ResultPage(ctk.CTkFrame):

    def __init__(
            self,
            parent,
            controller,
            results,
            frames,
            fps,
            exercise
    ):

        super().__init__(parent)


        self.controller = controller

        self.results = results

        self.exercise = exercise

        self.frames = frames

        self.fps = fps


        self.current_frame = 0


        self.create_widgets()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self,
            text=f"{self.exercise.upper()} ANALYSIS RESULTS",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        title.pack(
            pady=20
        )


        # Hauptbereich links/rechts

        self.main_frame = ctk.CTkFrame(
            self
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        # linke Seite Video

        self.video_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.video_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )


        # rechte Seite Ergebnisse

        self.result_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=500
        )

        self.result_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10
        )


        # Video Label

        self.video_label = ctk.CTkLabel(
            self.video_frame,
            text=""
        )

        self.video_label.pack(
            pady=20
        )

        # -------------------------------------
        # Live Analyse
        # -------------------------------------

        self.info_frame = ctk.CTkFrame(
            self.video_frame
        )

        self.info_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )


        self.frame_label = ctk.CTkLabel(
            self.info_frame,
            text="Frame: 0"
        )

        self.frame_label.pack(
            anchor="w",
            padx=10,
            pady=3
        )


        self.rep_label = ctk.CTkLabel(
            self.info_frame,
            text="Repetition: -"
        )

        self.rep_label.pack(
            anchor="w",
            padx=10,
            pady=3
        )


        self.phase_label = ctk.CTkLabel(
            self.info_frame,
            text="Phase: Idle"
        )

        self.phase_label.pack(
            anchor="w",
            padx=10,
            pady=3
        )


        self.update_video()


        self.create_results()




    # -------------------------------------
    # Video Wiedergabe
    # -------------------------------------

    def update_video(self):


        if len(self.frames) == 0:

            return



        if self.current_frame >= len(self.frames):

            self.current_frame = 0

        start_time = time.perf_counter()  # Startzeitpunkt für die Frame-Dauer



        data = self.frames[
            self.current_frame
        ]



        frame = create_overlay_frame(
            data
        )



        # OpenCV BGR -> RGB

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )



        image = Image.fromarray(
            frame
        )



        image.thumbnail(
            (700, 500)
        )



        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )



        self.video_label.configure(
            image=photo
        )


        self.video_label.image = photo



        # -------------------------------------
        # Live Bewegungsstatus aktualisieren
        # -------------------------------------

        self.update_status()



        # Nächster Frame

        self.current_frame += 1

        # -------------------------------------
        # Timing
        # -------------------------------------

        frame_duration = 1000 / self.fps

        processing_time = (
            time.perf_counter() - start_time
        ) * 1000

        delay = max(
            1,
            int(frame_duration - processing_time)
        )
        

        self.after(
            delay,
            self.update_video
        )

    def update_status(self):


        current = self.current_frame


        repetition = "-"
        phase = "Idle"



        for i, result in enumerate(self.results):


            start = result["frames"]["start"]
            bottom = result["frames"]["bottom"]
            end = result["frames"]["end"]



            if start <= current <= end:


                repetition = (
                    f"{i+1}/{len(self.results)}"
                )


                if current < bottom:

                    phase = "Descending"


                else:

                    phase = "Ascending"



                break



        self.frame_label.configure(
            text=(
                f"Frame: "
                f"{current}/{len(self.frames)-1}"
            )
        )


        self.rep_label.configure(
            text=(
                f"Repetition: "
                f"{repetition}"
            )
        )


        self.phase_label.configure(
            text=(
                f"Phase: "
                f"{phase}"
            )
        )




    # -------------------------------------
    # Ergebnisse
    # -------------------------------------

    def create_results(self):


        for i, result in enumerate(self.results):


            rep_frame = ctk.CTkFrame(
                self.result_frame
            )


            rep_frame.pack(
                fill="x",
                padx=10,
                pady=10
            )



            ctk.CTkLabel(
                rep_frame,
                text=f"Repetition {i+1}",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=10,
                pady=10
            )



            frames = result["frames"]



            ctk.CTkLabel(
                rep_frame,
                text=(
                    f"Start: {frames['start']}\n"
                    f"Bottom: {frames['bottom']}\n"
                    f"End: {frames['end']}"
                )
            ).pack(
                anchor="w",
                padx=10
            )



            self.create_metrics(
                rep_frame,
                result["metrics"]
            )




    def create_metrics(
            self,
            parent,
            metrics
    ):


        title = ctk.CTkLabel(
            parent,
            text="Movement Metrics",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )


        title.pack(
            anchor="w",
            padx=10,
            pady=10
        )


        if self.exercise == "Squat":

            metrics_config = SQUAT_METRICS


        elif self.exercise == "Push Up":

            metrics_config = PUSHUP_METRICS


        else:

            metrics_config = []

        for metric in metrics_config:


            create_metric_row(
                parent,
                metric,
                metrics
            )