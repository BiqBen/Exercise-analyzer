import customtkinter as ctk
import cv2

from PIL import Image

from app.visualization.video_visualizer import create_overlay_frame
from app.visualization.metric_config import METRICS
from app.visualization.metric_widgets import create_metric_row



class ResultPage(ctk.CTkFrame):

    def __init__(
            self,
            parent,
            controller,
            results,
            frames,
            fps
    ):

        super().__init__(parent)


        self.controller = controller

        self.results = results

        self.frames = frames

        self.fps = fps


        self.current_frame = 0


        self.create_widgets()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self,
            text="SQUAT ANALYSIS RESULTS",
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
            (700,500)
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

        self.current_frame += 1

        delay = int(
            1000 / self.fps
        )


        self.after(
            delay,
            self.update_video
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



        for metric in METRICS:


            create_metric_row(
                parent,
                metric,
                metrics
            )