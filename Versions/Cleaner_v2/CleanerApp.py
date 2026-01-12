# -*- coding: utf-8 -*-
"""
Requires: pip install textual pyfiglet colorama
Run as Admin!
"""

from Scripts.config import *
from Scripts.utils import messages as msg
from Scripts.core.Cleaner import *
from Scripts.utils.ui_helpers import make_boxed_message

import asyncio
import random
import sys
import webbrowser
from io import StringIO
from contextlib import contextmanager

from textual.app import App, ComposeResult, on
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, RichLog, Tree, Label, Button
from textual.reactive import reactive
from rich.text import Text as RichText

from Versions.Cleaner_v2.modals.SettingsModal import SettingsModal


log_buffer = StringIO()

@contextmanager
def capture_logs():
    old_stdout = sys.stdout
    sys.stdout = log_buffer
    try:
        yield
    finally:
        sys.stdout = old_stdout

class CleanerApp(App):

    CSS_PATH = ["css/style.css", "css/CleanerAppStyle.css"]
    current_app = reactive("Preparing...")

    def compose(self) -> ComposeResult:
        global APP_TITLE

        self.title = f"CleanerApp - v{RELEASE_VERSION}"
        self.paths, self.detected = detect_and_get_paths()
        APP_TITLE = self.title

        yield Header(show_clock=True)
        yield Footer()

        with Container(id="sidebar"):
            yield Static(id="logo-small")
            yield Label("By N1h1lius", id="credit")
            
            with VerticalScroll(id="tasks-scroll"): yield Tree("Tasks", id="tasks")

            with Vertical(id="buttons-container"):
                yield Button("Settings", id="btn-settings", disabled=True)
                yield Button("Github", id="btn-github")
                yield Button("Twitter", id="btn-twitter")
                yield Button("Exit", id="btn-exit")

        yield VerticalScroll(RichLog(highlight=True, markup=True, wrap=False), id="main-log")

        yield Static("Status: Starting...", id="status-bar")

    def on_mount(self) -> None:

        self.query_one("#logo-small", Static).update(RichText(msg.logo_ascii, style="bold magenta"))
        self.query_one("#status-bar").update(QUOTES[random.randint(0, len(QUOTES)-1)])

        tree = self.query_one(Tree)
        tree.root.expand()
        self.app_nodes = {}
        for cat in self.detected:
            node = tree.root.add(f"[bright_red][ - ][/] {cat}")
            self.app_nodes[cat] = node

        self.run_worker(self.do_cleaning, exclusive=True)

    @on(Button.Pressed, "#btn-settings")
    def open_settings(self) -> None:
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

    def on_resize(self) -> None:
        log = self.query_one(RichLog)
        log.refresh()
        self.query_one("#status-bar").refresh()

    async def do_cleaning(self):
        self.current_app = "Initializing..."
        self.query_one("#status-bar").update("Status: Analyzing...")

        await asyncio.sleep(1.2)

        log = self.query_one(RichLog)

        log.write(msg.starting_message)
        log.refresh()
        await asyncio.sleep(1.0)

        paths, detected = self.paths, self.detected

        detected_lines = []
        for m in detected:
            detected_lines.append(
                f"   [bright_green][+] [bright_magenta]-> "
                f"[bright_cyan]{m} [bright_green]"
                f"Detected - [{detected_folders[m]}] Folders"
            )
        log.write(make_boxed_message(self, "DETECTING INSTALLED PROGRAMS", detected_lines, "bright_white"))
        log.refresh()

        await asyncio.sleep(1.0)

        for path in paths:
            app_name = "System Temps"
            for key in PROGRAMS_PATH_NAMES.keys():
                if key in path:
                    app_name = PROGRAMS_PATH_NAMES[key]
                    break

            self.current_app = app_name
            self.query_one("#status-bar").update(f"Status: Cleaning {app_name}...")

            cleaning_lines = [f"     CLEANING: {path}"]
            log.write(make_boxed_message(self, "", cleaning_lines, "bright_cyan"))
            log.refresh()

            cleaner(path, log)

            cleaned_line = (
                f"     CLEANED || Deleted Files [{stats['current_files']}] || "
                f"Deleted Folders [{stats['current_folders']}] || "
                f"Deleted Size in Mb [{stats['current_mb']:.2f}]"
            )
            log.write(make_boxed_message(self, "", [cleaned_line], "bright_green"))
            log.refresh()

            tree = self.query_one(Tree)
            if app_name in self.app_nodes:
                node = self.app_nodes[app_name]
                label = RichText(f"[ + ] {app_name}")
                label.stylize("green", 0, 5)
                node.label = label
                tree.refresh()

        self.current_app = "Finished"
        self.query_one("#status-bar").update("Process Finished Successfully")

        await asyncio.sleep(1.5)

        final_lines = []
        final_lines.append(
            f"TOTAL CLEANED || Files [{stats['total_files']}] || "
            f"Folders [{stats['total_folders']}] || Size [{stats['total_mb']:.2f} Mb]"
        )
        final_lines.append(f"[bright_white]PRESS ANY KEY TO EXIT[/bright_white]")
        log.write(make_boxed_message(self, "PROCESS COMPLETED", final_lines, "bright_yellow"))
        log.refresh()

        self.query_one("#btn-settings", Button).disabled = False

    def key_any(self):
        self.exit()

    def key_escape(self):
        self.exit()

    def key_q(self):
        self.exit()