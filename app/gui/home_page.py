import customtkinter as ctk
from tkinter import filedialog

from app.analysis.video_analyzer import analyze_video
from app.analysis.squat.pose_analyzer import analyze_squat_pose
from app.analysis.pushup.pose_analyzer import analyze_pushup_pose
from app.analysis.squat.repetition_detector import detect_squat_repetitions
from app.analysis.pushup.repetition_detector import detect_pushup_repetitions
from app.analysis.squat.repetition_analyzer import analyze_squat_repetition
from app.analysis.pushup.repetition_analyzer import analyze_pushup_repetition



class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.video_path = None

        self.create_widgets()


    def create_widgets(self):

        # Titel
        self.title = ctk.CTkLabel(
            self,
            text="Exercise Analyzer",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title.pack(pady=30)


        # Beschreibung
        self.description = ctk.CTkLabel(
            self,
            text="Wähle eine Übung und lade ein Video zur Analyse hoch.",
            font=ctk.CTkFont(size=16)
        )
        self.description.pack(pady=10)


        # Übungsauswahl
        self.exercise_label = ctk.CTkLabel(
            self,
            text="Übung auswählen:",
            font=ctk.CTkFont(size=18)
        )
        self.exercise_label.pack(pady=(30,5))


        self.exercise_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "Squat",
                "Deadlift",
                "Push Up"
            ],
            command=self.update_instruction
        )

        self.exercise_menu.pack()


        # Anleitung
        self.instruction_box = ctk.CTkTextbox(
            self,
            width=500,
            height=150
        )
        self.instruction_box.pack(pady=30)

        self.instruction_box.insert(
            "0.0",
            "Wähle eine Übung aus, um Hinweise zu sehen."
        )

        self.instruction_box.configure(
            state="disabled"
        )


        # Video auswählen
        self.video_button = ctk.CTkButton(
            self,
            text="Video auswählen",
            command=self.select_video
        )

        self.video_button.pack(pady=10)


        self.video_label = ctk.CTkLabel(
            self,
            text="Kein Video ausgewählt"
        )

        self.video_label.pack()


        # Analyse starten
        self.start_button = ctk.CTkButton(
            self,
            text="Analyse starten",
            command=self.start_analysis,
            height=40,
            width=200
        )

        self.start_button.pack(pady=40)



    def update_instruction(self, exercise):

        instructions = {

            "Squat":
            """
            Squat:
            - Kamera seitlich positionieren
            - Ganze Bewegung sichtbar
            - Knie und Hüfte müssen erkennbar sein
            - Aufrechte Körperhaltung
            """,

            "Deadlift":
            """
            Deadlift:
            - Seitliche Ansicht
            - Stange und Körper vollständig sichtbar
            - Rückenposition beachten
            """,

            "Push Up":
            """
            Push Up:
            - Körper vollständig sichtbar
            - Seitliche Kamera empfohlen
            - Arme und Schulterbewegung erfassen
            """
        }


        self.instruction_box.configure(
            state="normal"
        )

        self.instruction_box.delete(
            "0.0",
            "end"
        )

        self.instruction_box.insert(
            "0.0",
            instructions[exercise]
        )

        self.instruction_box.configure(
            state="disabled"
        )



    def select_video(self):

        file = filedialog.askopenfilename(
            filetypes=[
                (
                    "Video Files",
                    "*.mp4 *.avi *.mov"
                )
            ]
        )

        if file:

            self.video_path = file

            self.video_label.configure(
                text=file.split("/")[-1]
            )



    def start_analysis(self):

        if self.video_path is None:
            print("Kein Video ausgewählt")
            return


        exercise = self.exercise_menu.get()


        if exercise == "Squat":

            frames, fps = analyze_video(
                self.video_path,
                analyze_squat_pose
            )


            print("Analyse abgeschlossen")
            print(f"Frames analysiert: {len(frames)}")
            print(f"FPS: {fps}")


            repetitions = detect_squat_repetitions(
                frames
            )


            print(
                f"Wiederholungen erkannt: {len(repetitions)}"
            )


            results = []


            for repetition in repetitions:

                result = analyze_squat_repetition(
                    frames,
                    repetition,
                    fps
                )

                results.append(result)


            self.controller.show_results(
                results,
                frames,
                fps,
                exercise
            )

        elif exercise == "Push Up":
        
                    frames, fps = analyze_video(
                        self.video_path,
                        analyze_pushup_pose
                    )
        
        
                    print("Analyse abgeschlossen")
                    print(f"Frames analysiert: {len(frames)}")
                    print(f"FPS: {fps}")
        
        
                    repetitions = detect_pushup_repetitions(
                        frames,
                        fps
                    )
        
                    for i, result in enumerate(repetitions):

                        print(
                            i,
                            frames[result["start"]]["frame_index"],
                            frames[result["bottom"]]["frame_index"],    
                        )

                    print(
                        f"Wiederholungen erkannt: {len(repetitions)}"
                    )
        
        
                    results = []
        
        
                    for repetition in repetitions:
        
                        result = analyze_pushup_repetition(
                            frames,
                            repetition,
                            fps
                        )
        
                        results.append(result)
        
        
                    self.controller.show_results(
                        results,
                        frames,
                        fps,
                        exercise
                    )