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
import sys
import webbrowser
from io import StringIO
from contextlib import contextmanager

from textual.app import App, ComposeResult, on
from textual.containers import Container, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, RichLog, Tree, Label, Button
from textual.reactive import reactive
from rich.text import Text as RichText

from Versions.Cleaner_v2.SettingsModal import SettingsModal


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
    CSS = """
    Screen {
        background: $background;
    }

    #sidebar {
        dock: left;
        width: 30%;
        max-width: 35;
        min-width: 20;
        height: 100%;
        background: $panel;
        border: tall $primary;
    }

    #logo-small {
        height: 12;
        content-align: center middle;
        background: $panel-darken-1;
        margin-bottom: 2;
    }

    #credit {
        height: 1;
        content-align: center middle;
        color: $text-muted;
        background: $panel-darken-1;
        margin: 0 0 2 0;
        margin-left: 11;
    }

    #tasks {
        height: 40%;
        min-height: 6;
        max-height: 12;
        margin-top: 1;
    }

    #buttons-container {
        dock: bottom;
        height: auto;
        padding: 1;
    }

    #main-log {
        height: 100%;
        background: $surface;
        border: tall $accent;
        overflow-x: hidden;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $primary-darken-2;
        content-align: center middle;
        color: white;
    }

    Button {
        margin: 1;
        width: 100%;
    }

    #btn-exit {
        margin-top: 2;
        margin-bottom: 1;
        margin-left: 1;
        margin-right: 1;
        width: 100%;
        background: $error;
        color: white;
    }
    """

    current_app = reactive("Preparing...")

    def compose(self) -> ComposeResult:
        self.title = f"CleanerApp - v{RELEASE_VERSION}"
        yield Header(show_clock=True)
        yield Footer()

        with Container(id="sidebar"):
            yield Static(id="logo-small")
            yield Label("By N1h1lius", id="credit")
            yield Tree("Tasks", id="tasks")
            with Vertical(id="buttons-container"):
                yield Button("Settings", id="btn-settings", disabled=True)
                yield Button("Github", id="btn-github")
                yield Button("Twitter", id="btn-twitter")
                yield Button("Exit", id="btn-exit")

        yield VerticalScroll(RichLog(highlight=True, markup=True, wrap=False), id="main-log")

        yield Static("Status: Starting...", id="status-bar")

    def on_mount(self) -> None:
        self.query_one("#logo-small", Static).update(RichText(msg.logo_ascii, style="bold magenta"))

        tree = self.query_one(Tree)
        tree.root.expand()
        self.app_nodes = {}
        for cat in folder_categories:
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

        paths, detected = detect_and_get_paths()

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