"""
Hauptfenster der Anwendung.

Verantwortlichkeiten:
- Erzeugt das Hauptfenster
- Verwaltet die verschiedenen Seiten
- Wechselt zwischen Home-, Analyse- und Ergebnisansicht
"""

import customtkinter as ctk

from app.gui.home_page import HomePage
from app.gui.result_page import ResultPage


class ExerciseAnalyzerApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # -------------------------------------------------
        # Fenster
        # -------------------------------------------------

        self.title("Exercise Analyzer")

        self.geometry("1200x800")

        self.minsize(1000, 700)

        # -------------------------------------------------
        # Theme
        # -------------------------------------------------

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # -------------------------------------------------
        # Container
        # -------------------------------------------------

        self.container = ctk.CTkFrame(self)

        self.container.pack(
            fill="both",
            expand=True
        )

        # aktuell angezeigte Seite
        self.current_page = None

        # Home anzeigen
        self.show_home()

    # =====================================================
    # Seitenwechsel
    # =====================================================

    def clear_page(self):

        if self.current_page is not None:
            self.current_page.destroy()

    def show_home(self):

        self.clear_page()

        self.current_page = HomePage(
            self.container,
            self
        )

        self.current_page.pack(
            fill="both",
            expand=True
        )

    def show_loading(self):

        print("Loading Page folgt später...")

    def show_results(
            self,
            results,
            frames,
            fps
    ):

        self.clear_page()


        self.current_page = ResultPage(
            self.container,
            self,
            results,
            frames,
            fps
        )


        self.current_page.pack(
            fill="both",
            expand=True
        )