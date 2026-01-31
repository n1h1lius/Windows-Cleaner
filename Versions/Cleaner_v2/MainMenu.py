# -*- coding: utf-8 -*-
"""
Requires: pip install textual pyfiglet colorama
Run as Admin!
"""

import subprocess
from Scripts.config import *
from Scripts.utils import messages as msg
from Scripts.core.Cleaner import *
from Scripts.utils.ui_helpers import make_boxed_message

import random
import sys
import webbrowser
from io import StringIO
from contextlib import contextmanager

from textual.app import App, ComposeResult, on
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Static, Tree, Label, Button
from textual.reactive import reactive
from rich.text import Text as RichText

from Scripts.widgets.MessageBox import MessageBox
from Versions.Cleaner_v2.modals.SettingsModal import SettingsModal
from Versions.Cleaner_v2.modals.CleanerModal import CleanerModal


log_buffer = StringIO()

@contextmanager
def capture_logs():
    old_stdout = sys.stdout
    sys.stdout = log_buffer
    try:
        yield
    finally:
        sys.stdout = old_stdout

class MainMenu(App):

    CSS_PATH = ["css/style.css", "css/MainMenuAppStyle.css"]
    current_app = reactive("Preparing...")

    def __init__(self, updated_status: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.updated = updated_status  # Guardamos el booleano en la instancia

    def compose(self) -> ComposeResult:
        global APP_TITLE

        self.title = f"Windows Cleaner - v{RELEASE_VERSION}"
        APP_TITLE = self.title
        
        yield Header(show_clock=True)
        yield Footer()

        # ================ SIDEBAR CANVAS ================
        with Container(id="sidebar"):
            yield Static(id="logo-small")
            yield Label("By N1h1lius", id="credit")
            
            with VerticalScroll(id="tasks-scroll"): yield Tree("Tasks", id="tasks")

            with Vertical(id="buttons-container"):
                yield Button("Settings", id="btn-settings")
                yield Button("Github", id="btn-github")
                yield Button("Twitter", id="btn-twitter")
                yield Button("Exit", id="btn-exit")



        # ================ MAIN CANVAS ================
        with VerticalScroll(id="actions-container"):

            with Horizontal():
                # ================ SYSTEM COLUMN ================
                with Vertical(id="system"):
                    yield Label("SYSTEM FUNCTIONS", classes="menu-section-title")
                    yield Button("Cleaner", id="btn-cleaner")
                    yield Button("Debloater", id="btn-debloater")

                # ================ SECURITY COLUMN ================
                with Vertical(id="security"):
                    yield Label("SECURITY FUNCTIONS", classes="menu-section-title")

                # ================ SPECIAL ACTIONS COLUMN ================
                with Vertical(id="menu-special-actions"):
                    yield Label("SPECIAL ACTIONS", classes="menu-section-title")



        yield Static("Main Menu Started", id="status-bar")



    # ================ SYSTEM BUTTONS ================
    @on(Button.Pressed, "#btn-cleaner")
    def open_cleaner(self) -> None:
        self.query_one("#status-bar").update(QUOTES[random.randint(0, len(QUOTES)-1)])
        self.push_screen(CleanerModal())

    @on(Button.Pressed, "#btn-debloater")
    def open_debloater(self) -> None:
            self.query_one("#status-bar").update(QUOTES[random.randint(0, len(QUOTES)-1)])
            script_path = os.path.join("Scripts", "utils", "debloater", "W10-11_Debloater.bat")
            
            try:
                subprocess.Popen(f'start "" "{script_path}"', shell=True)            
            except Exception as e:
                self.query_one("#status-bar").update(f"Error: {str(e)}")

    # ================ LEFT COLUMN BUTTONS ================
    @on(Button.Pressed, "#btn-settings")
    def open_settings(self) -> None:
        self.query_one("#status-bar").update(QUOTES[random.randint(0, len(QUOTES)-1)])
        self.push_screen(SettingsModal())

    @on(Button.Pressed, "#btn-github")
    def open_github(self):
        webbrowser.open("https://github.com/n1h1lius")

    @on(Button.Pressed, "#btn-twitter")
    def open_twitter(self):
        webbrowser.open("https://x.com/N1h1lius")

    @on(Button.Pressed, "#btn-exit")
    def exit_app(self):
        self.exit()

    # ================ GENERAL EVENTS ================
    def on_mount(self) -> None:
        self.query_one("#logo-small", Static).update(RichText(msg.logo_ascii, style="bold magenta"))
        self.query_one("#status-bar").update(QUOTES[random.randint(0, len(QUOTES)-1)])

        if self.updated:
            print("UPDATED")
            dialog = MessageBox(f"{V2_NAME} Updated Succesfully to version {RELEASE_VERSION}", mode="success") 
            self.push_screen_wait(dialog)

    def on_resize(self) -> None:
        #self.query_one(RichLog).refresh()
        
        self.query_one("#status-bar").refresh()

    def key_any(self):
        self.exit()

    def key_escape(self):
        self.exit()

    def key_q(self):
        self.exit()