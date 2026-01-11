from Scripts.config import *
from Scripts.utils import messages as msg
from Scripts.core.Cleaner import *

import webbrowser

from textual.app import ComposeResult, on
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Static, Tree, Label, Button, Checkbox, Input
from textual.screen import ModalScreen
from rich.text import Text as RichText

class SettingsModal(ModalScreen):
    CSS = """
    Screen {
        background: $background;
    }

    #sidebar {
        dock: left;
        width: 28;
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
    }

    #tasks {
        height: 1fr;
        margin-top: 1;
    }

    #buttons-container {
        dock: bottom;
        height: auto;
    }

    #settings-container {
        height: 100%;
        background: $surface;
        border: tall $accent;
        padding: 1;
    }

    #booleans, #integers {
        background: $panel 70%;
        border: round $primary 60%;
        padding: 2 3;
        margin: 1 2 1 0;
        height: auto;
    }

    #booleans Label, #integers Label {
        margin-bottom: 1;
        text-style: bold;
        color: $accent;
    }

    .setting-row {
        layout: horizontal;
        height: auto;
        margin: 1 0;
        align: center middle;
    }

    .setting-label {
        width: 25;
        min-width: 25;
        content-align: right middle;
        margin-right: 1;
        color: $text;
    }

    Input {
        width: 18;
        min-width: 12;
    }

    Checkbox {
        margin: 0 0 0 1;
    }

    Button {
        margin: 1;
        width: 100%;
    }

    #btn-exit {
        margin-top: 2;
        width: 100%;
        background: $error;
        color: white;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        with Container(id="sidebar"):
            yield Static(id="logo-small")
            yield Label("By N1h1lius", id="credit")
            yield Tree("Tasks", id="tasks")
            with Vertical(id="buttons-container"):
                yield Button("Back", id="btn-back")
                yield Button("Github", id="btn-github")
                yield Button("Twitter", id="btn-twitter")
                yield Button("Exit", id="btn-exit")

        with VerticalScroll(id="settings-container"):
            with Horizontal():
                with Vertical(id="booleans"):
                    yield Label("Boolean Settings")
                    for section in ["Deployment", "MainVars"]:
                        for key in config.options(section):
                            try:
                                val = config.getboolean(section, key)
                                yield Checkbox(
                                    label=f"{section}.{key}",
                                    value=val,
                                    id=f"{section}-{key}"
                                )
                            except ValueError:
                                pass

                with Vertical(id="integers"):
                    yield Label("Integer / Numeric Settings")
                    for section in ["Deployment", "MainVars"]:
                        for key in config.options(section):
                            try:
                                val = config.getint(section, key)
                                with Container(classes="setting-row"):
                                    yield Label(f"{section}.{key}", classes="setting-label")
                                    yield Input(
                                        value=str(val),
                                        id=f"{section}-{key}",
                                        placeholder=str(val),
                                        type="integer"
                                    )
                            except ValueError:
                                pass

        yield Static("Settings - Changes are saved automatically", id="status-bar")

    def on_mount(self) -> None:
        self.query_one("#logo-small", Static).update(RichText(msg.logo_ascii, style="bold magenta"))

    @on(Button.Pressed, "#btn-back")
    def on_back(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#btn-github")
    def open_github(self):
        webbrowser.open("https://github.com/n1h1lius")

    @on(Button.Pressed, "#btn-twitter")
    def open_twitter(self):
        webbrowser.open("https://x.com/N1h1lius")

    @on(Button.Pressed, "#btn-exit")
    def exit_app(self):
        self.app.exit()

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id:
            section, key = event.checkbox.id.split("-")
            config.set(section, key, str(event.value).lower())
            with open(ini_file_path, "w") as configfile:
                config.write(configfile)

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id:
            section, key = event.input.id.split("-")
            value = event.value.strip()
            if value == "":
                return
            try:
                val = int(value)
                config.set(section, key, str(val))
                with open(ini_file_path, "w") as configfile:
                    config.write(configfile)
            except ValueError:
                pass

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.on_input_changed(event)