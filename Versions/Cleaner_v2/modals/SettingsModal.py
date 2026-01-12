from Scripts.config import *
from Scripts.utils import messages as msg
from Scripts.core.Cleaner import *

import webbrowser
import win32com.client
import os

from textual.app import ComposeResult, on
from textual.containers import Container, Vertical, VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Static, Tree, Label, Button, Checkbox, Input
from textual.screen import ModalScreen
from rich.text import Text as RichText


from Versions.Cleaner_v2.modals.UpdaterModal import UpdaterModal

from Scripts.widgets.MessageBox import MessageBox

class SettingsModal(ModalScreen):
    CSS_PATH = ["../css/style.css", "../css/SettingsModalStyle.css"]

    def compose(self) -> ComposeResult:
        self.title = f"[ SETTINGS ] - {APP_TITLE}"
        yield Header(show_clock=True)
        yield Footer()

        with Container(id="sidebar"):
            yield Static(id="logo-small")
            yield Label("By N1h1lius", id="credit")
            with VerticalScroll(id="tasks-scroll"): yield Tree("Tasks", id="tasks")
            with Vertical(id="buttons-container"):
                yield Button("Back", id="btn-back")
                yield Button("Github", id="btn-github")
                yield Button("Twitter", id="btn-twitter")
                yield Button("Exit", id="btn-exit")

        with VerticalScroll(id="settings-container"):
            with Horizontal():
                with Vertical(id="booleans"):
                    yield Label("BOOLEAN SETTINGS", classes="section-title")

                    for section in INI_SECTIONS:
                        for key in config.options(section):

                            if section == "Deployment" and key == "runonstart":
                                continue  # ← EVITA EL DUPLICADO

                            try:
                                val = config.getboolean(section, key)
                                yield Checkbox(
                                    label=f"{section}.{key}",
                                    value=val,
                                    id=f"{section}-{key}"
                                )
                            except ValueError:
                                pass

                    yield Checkbox(
                        label="Deployment.runonstart",
                        value=False,
                        id="Deployment-runonstart",
                        disabled=True
                    )


                with Vertical(id="integers"):
                    yield Label("INPUT SETTINGS", classes="section-title")
                    for section in INI_SECTIONS:
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

                with Vertical(id="special-actions"):
                    yield Label("SPECIAL ACTIONS", classes="section-title")
                    yield Button("Check for Updates", id="btn-updater")
                    yield Button("Create Shortcut", id="btn-shortcut")
                    yield Button("Run on Start", id="btn-runstart")

        yield Static("Settings - Changes are saved automatically", id="status-bar")

    def on_mount(self) -> None:
        self.query_one("#logo-small", Static).update(RichText(msg.logo_ascii, style="bold magenta"))
        # Cargar estado de runonstart
        try:
            runonstart_val = config.getboolean("Deployment", "runonstart")
            self.query_one("#Deployment-runonstart").value = runonstart_val
        except:
            pass

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
        if event.checkbox.id and event.checkbox.id != "Deployment-runonstart":
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

    # ── Create Shortcut Button ───────────────────────────────────────────────────────
    @on(Button.Pressed, "#btn-shortcut")
    async def create_shortcut(self) -> None:
        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = shell.SpecialFolders("Desktop")
        project_root = os.path.dirname(os.path.abspath(__file__ + "/../../../"))
        bat_path = os.path.join(project_root, "WindowsCleaner.bat")
        icon_path = os.path.join(project_root, "Data", "Icon.ico")
        shortcut_path = os.path.join(desktop, "Cleaner.lnk")

        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = bat_path
        shortcut.IconLocation = icon_path
        shortcut.WorkingDirectory = project_root
        shortcut.save()

        dialog = MessageBox("Shortcut Created", mode="success") 
        await self.app.push_screen(dialog)

    # ── Run On Start Button ───────────────────────────────────────────────────────
    @on(Button.Pressed, "#btn-runstart")
    async def toggle_run_on_start(self) -> None:
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        bat_name = "[N1h1lius]-Cleaner.bat"
        startup_bat_path = os.path.join(startup_folder, bat_name)
        project_root = os.path.dirname(os.path.abspath(__file__ + "/../../../"))
        target_bat_path = os.path.join(project_root, "cleaner.bat")

        if os.path.exists(startup_bat_path):
            os.remove(startup_bat_path)
            runonstart_val = False
        else:
            with open(target_bat_path, 'r') as f:
                template_content = f.readlines()
            
            with open(startup_bat_path, 'w') as f:
                for line in template_content:
                    if "python main.py" in line:
                        f.write(f'{project_root[0]}: \n')  # Change drive if necessary
                        f.write(f'cd "{project_root}"\n')
                        f.write(line)
                    else:
                        f.write(line)

            runonstart_val = True

        config.set("Deployment", "runonstart", str(runonstart_val).lower())

        with open(ini_file_path, "w") as configfile:
            config.write(configfile)

        self.query_one("#Deployment-runonstart").value = runonstart_val

        message = "Run on Start Disabled" if runonstart_val else "Run on Start Enabled"
        dialog = MessageBox(message, mode="success") 
        await self.app.push_screen(dialog)

    # ── Updater Button ───────────────────────────────────────────────────────
    @on(Button.Pressed, "#btn-updater")
    async def open_updater(self) -> None:
        self.app.push_screen(UpdaterModal())
    
    def on_unmount(self) -> None:
        # Restore main app title when modal is dismissed
        self.title = APP_TITLE