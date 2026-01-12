import os
import asyncio
import time
import datetime
import requests
import zipfile
import shutil
import tempfile
import configparser
import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from textual.containers import Vertical, VerticalScroll
from textual import work  # ← Importante para @work decorator

from Scripts.utils import messages as msg
from Scripts.widgets.ConfirmModal import ConfirmModal

# Constantes
REPO_URL = "https://github.com/n1h1lius/Windows-Cleaner/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = Path("Data/version.txt")
CONFIG_FILE = Path("Data/config.ini")

async def merge_configs(local_ini: Path, remote_ini: Path):
    local_config = configparser.ConfigParser()
    local_config.read(local_ini)
    
    remote_config = configparser.ConfigParser()
    remote_config.read(remote_ini)
    
    for section in remote_config.sections():
        if not local_config.has_section(section):
            local_config.add_section(section)
        for key in remote_config.options(section):
            if not local_config.has_option(section, key) or local_config.get(section, key) == remote_config.get(section, key):
                local_config.set(section, key, remote_config.get(section, key))
    
    with open(local_ini, "w") as f:
        local_config.write(f)

async def get_remote_version() -> str | None:
    url = "https://raw.githubusercontent.com/n1h1lius/Windows-Cleaner/main/Data/version.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        return None
    except Exception:
        return None

class UpdateLog(RichLog):
    """Custom log with nice border"""
    BORDER_TITLE = "Updater Log"
    BORDER_SUBTITLE = "Updating..."

    def __init__(self):
        super().__init__(
            highlight=True,
            markup=True,
            wrap=True,
        )

class UpdaterApp(App):
    CSS = """
    Screen {
        background: $surface;
    }

    Header {
        background: $primary-darken-2;
        color: white;
        height: 3;
        content-align: center middle;
    }

    Footer {
        background: $primary-darken-2;
        color: white;
        height: 1;
        content-align: center middle;
    }

    #logo-container {
        height: 6;
        content-align: center middle;
    }

    #main-log {
        height: 100%;
        background: $panel;
        border: tall $accent;
        padding: 1;
        margin: 1 2;
    }

    #status {
        height: 3;
        content-align: center middle;
        text-style: bold;
        color: $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        with Vertical(id="main"):
            yield VerticalScroll(UpdateLog(), id="main-log")

    def print(self, text: str):
        log = self.query_one(UpdateLog)
        log.write(text)
        log.refresh()               # ← Fuerza redraw inmediato
        self.refresh()              # ← Refresca toda la app (opcional pero útil)

    def on_mount(self) -> None:
        self.print(msg.updater_intro)
        self.print("[cyan]Checking for updates...[/]")
        self.check_for_updates()    # ← Llamada directa (no worker aquí)

    @work(thread=True, exclusive=True)
    async def check_for_updates(self):
        await asyncio.sleep(1.5)

        if not LOCAL_VERSION_FILE.exists():
            self.call_from_thread(self.print, "[yellow]Local version file not found. Skipping update.[/]")
            self.call_from_thread(self.after_update_check, False)
            return

        with open(LOCAL_VERSION_FILE, "r") as f:
            local_version = f.read().strip()

        self.call_from_thread(self.print, f"[cyan]Local Version:[/] [white]{local_version}[/]")

        remote_version = await get_remote_version()

        if remote_version is None:
            self.call_from_thread(self.print, "[yellow]Could not fetch remote version. Skipping.[/]")
            self.call_from_thread(self.after_update_check, False)
            return

        self.call_from_thread(self.print, f"[cyan]Remote Version:[/] [white]{remote_version}[/]")

        if remote_version != local_version:
            self.call_from_thread(self.print, f"[green]New version available: {remote_version}[/]")

            # Confirmación modal (síncrona)
            confirmed = await self.push_screen_wait(ConfirmModal("Do you want to update?", title="UPDATE"))
            
            if confirmed:
                self.call_from_thread(self.print, "[bold green]Starting update...[/]")
                await self.perform_update()
            else:
                self.call_from_thread(self.print, "[yellow]Update cancelled by user.[/]")
                self.call_from_thread(self.after_update_check, False)
        else:
            self.call_from_thread(self.print, "[green]You are already up to date![/]")
            self.call_from_thread(self.after_update_check, False)

    async def after_update_check(self, updated: bool):
        await asyncio.sleep(1.5)
        
        if updated:
            self.print("[bold green]Update completed successfully![/]")
            self.print("[yellow]Restarting application...[/]")
            await asyncio.sleep(2)
        else:
            self.print("[dim]No update performed. Exiting...[/]")
            await asyncio.sleep(2)
        
        self.exit(updated)

    @work(thread=True, exclusive=True)
    async def perform_update(self):
        self.print("[cyan]Downloading update package...[/]")
        response = requests.get(REPO_URL)
        if response.status_code != 200:
            self.print("[bold red]Failed to download update package.[/]")
            self.after_update_check(False)
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "repo.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)

            extract_dir = os.path.join(tmp_dir, "extract")
            os.makedirs(extract_dir)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            repo_dir = os.path.join(extract_dir, "Windows-Cleaner-main")

            if CONFIG_FILE.exists():
                shutil.copy(CONFIG_FILE, str(CONFIG_FILE) + ".bak")
                self.print("[cyan]Config backup created[/]")

            remote_config = os.path.join(repo_dir, str(CONFIG_FILE))
            if os.path.exists(remote_config):
                await merge_configs(CONFIG_FILE, Path(remote_config))
                self.print("[green]Config merged successfully[/]")

            self.print("[cyan]Copying files...[/]")
            for item in os.listdir(repo_dir):
                src = os.path.join(repo_dir, item)
                dst = os.path.join(os.getcwd(), item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

        remote_version = await get_remote_version()
        if remote_version:
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(remote_version)
            self.print("[green]Local version updated[/]")

        self.after_update_check(True)


if __name__ == "__main__":
    app = UpdaterApp()
    app.run()