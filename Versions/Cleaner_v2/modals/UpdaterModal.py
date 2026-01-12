import os
import asyncio
import time
import requests
import zipfile
import shutil
import tempfile
import configparser
import subprocess
from pathlib import Path

from textual.app import App, ComposeResult, work
from textual.widgets import Header, Footer, RichLog, Static
from textual.containers import Vertical, VerticalScroll
from textual import on

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
    
    changes = False
    for section in remote_config.sections():
        if not local_config.has_section(section):
            local_config.add_section(section)
            changes = True
        for key in remote_config.options(section):
            remote_val = remote_config.get(section, key)
            if not local_config.has_option(section, key):
                local_config.set(section, key, remote_val)
                changes = True
    
    if changes:
        with open(local_ini, "w", encoding="utf-8") as f:
            local_config.write(f)
        return True
    return False

def get_remote_version() -> str | None:
    url = "https://raw.githubusercontent.com/n1h1lius/Windows-Cleaner/main/Data/version.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        return None
    except Exception:
        return None

class UpdateLog(RichLog):
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
        yield Header("Updater - Windows Cleaner", show_clock=True)
        yield Footer()

        with Vertical():
            yield Static(id="status", markup=True)
            yield VerticalScroll(UpdateLog(), id="main-log")

    def on_mount(self) -> None:
        self.query_one("#status").update("[cyan]Inicializando comprobación...[/]")
        self.check_updates()

    def print(self, text: str):
        try:
            log = self.query_one(UpdateLog)
            log.write(text)
            log.scroll_end(animate=False)
            log.refresh()
            self.refresh()
        except:
            pass

    @work(thread=True, exclusive=True)
    async def check_updates(self):
        await asyncio.sleep(1)

        self.call_from_thread(self.print, msg.updater_intro)
        self.call_from_thread(self.print, "[cyan]Comprobando actualizaciones...[/]")

        if not LOCAL_VERSION_FILE.exists():
            self.call_from_thread(self.print, "[yellow]Archivo de versión local no encontrado.[/]")
            self.call_from_thread(self.after_check, False)
            return

        local_version = LOCAL_VERSION_FILE.read_text(encoding="utf-8").strip()
        self.call_from_thread(self.print, f"[cyan]Versión local:[/] [white]{local_version}[/]")

        remote_version = get_remote_version()
        if remote_version is None:
            self.call_from_thread(self.print, "[yellow]No se pudo obtener versión remota.[/]")
            self.call_from_thread(self.after_check, False)
            return

        self.call_from_thread(self.print, f"[cyan]Versión remota:[/] [white]{remote_version}[/]")

        if remote_version == local_version:
            self.call_from_thread(self.print, "[bold green]Estás al día.[/]")
            self.call_from_thread(self.after_check, False)
            return

        # Delegamos la pregunta al hilo principal
        self.call_from_thread(self._ask_for_update, remote_version)

    def _ask_for_update(self, remote_version: str):
        """Método llamado desde el hilo principal para mostrar el modal"""
        self.print(f"[bold green]¡Nueva versión disponible! {remote_version}[/]")

        async def show_modal():
            await asyncio.sleep(0.2)  # Pequeño retraso para estabilizar contexto
            confirmed = await self.push_screen_wait(ConfirmModal(
                message="¿Quieres actualizar ahora?",
                title="Actualización disponible"
            ))
            if confirmed:
                self.print("[bold green]Iniciando actualización...[/]")
                await self.perform_update(remote_version)
            else:
                self.print("[yellow]Actualización cancelada.[/]")
                self.after_check(False)

        self.run_worker(show_modal, exclusive=True)

    async def perform_update(self, new_version: str):
        self.print("[cyan]Descargando paquete...[/]")

        try:
            response = requests.get(REPO_URL, timeout=30)
            if response.status_code != 200:
                self.print("[bold red]Fallo al descargar.[/]")
                self.after_check(False)
                return

            with tempfile.TemporaryDirectory() as tmp_dir:
                zip_path = Path(tmp_dir) / "repo.zip"
                zip_path.write_bytes(response.content)

                extract_dir = Path(tmp_dir) / "extract"
                extract_dir.mkdir(exist_ok=True)

                with zipfile.ZipFile(zip_path) as z:
                    z.extractall(extract_dir)

                repo_dir = extract_dir / "Windows-Cleaner-main"
                if not repo_dir.exists():
                    self.print("[bold red]Carpeta no encontrada en ZIP.[/]")
                    self.after_check(False)
                    return

                if CONFIG_FILE.exists():
                    backup_path = CONFIG_FILE.with_suffix(".bak")
                    shutil.copy(CONFIG_FILE, backup_path)
                    self.print(f"[cyan]Backup creado: {backup_path.name}[/]")

                remote_config_path = repo_dir / CONFIG_FILE.name
                if remote_config_path.exists():
                    if await merge_configs(CONFIG_FILE, remote_config_path):
                        self.print("[green]Config fusionada[/]")
                    else:
                        self.print("[dim]No había cambios nuevos en config[/]")

                self.print("[cyan]Copiando archivos...[/]")
                for item in repo_dir.iterdir():
                    if item.name == Path(__file__).name:  # No sobrescribir este updater
                        continue
                    dest = Path.cwd() / item.name
                    if item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)

            LOCAL_VERSION_FILE.write_text(new_version, encoding="utf-8")
            self.print("[green]Versión local actualizada[/]")

            self.after_check(True)

        except Exception as e:
            self.print(f"[bold red]Error: {str(e)}[/]")
            self.after_check(False)

    def after_check(self, updated: bool):
        if updated:
            self.print("[bold green]¡Actualización completada![/]")
            self.print("[yellow]Reiniciando en 3 segundos...[/]")
            time.sleep(3)
            subprocess.Popen(["cleaner.bat"])  # Ajusta según tu launcher
        else:
            self.print("[dim]Saliendo...[/]")
            time.sleep(2)

        self.exit(updated)


if __name__ == "__main__":
    app = UpdaterApp()
    app.run()