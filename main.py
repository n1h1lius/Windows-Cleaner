import sys, os
import argparse

from Scripts.utils import messages as msg
from Scripts.core.Console.actions import RunCommand
from Scripts.core.Console import commands as cmd

from colorama import Fore, init

init(autoreset=True)

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       ARGUMENTS HANDLING                                                        ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

HEADER = f"{Fore.LIGHTRED_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

def parse_args():
    parser = argparse.ArgumentParser()

    # ───────── Arguments ─────────
    parser.add_argument("--debug-mode", action="store_true", help="Enable debug mode")

    parser.add_argument("--update-check", action="store_true", help="Check for updates without launching the application")
    parser.add_argument("--main-menu", action="store_false", help="Launch the Main Windows Cleaner App")
    parser.add_argument("--no-update-check", action="store_true", help="Disable update checking")
    parser.add_argument("--no-force-maximize", action="store_true", help="Do not force maximize the console window on start")

    parser.add_argument("--list-all-cleaner-scopes", action=RunCommand, function=cmd.list_all_cleaner_scopes, help="List all cleaner scopes")
    parser.add_argument("--list-available-cleaner-scopes", action=RunCommand, function=cmd.list_available_cleaner_scopes, help="List available cleaner scopes")
    parser.add_argument("--list-all-detected-paths", action=RunCommand, function=cmd.get_all_detected_paths, help="List all detected paths")
    parser.add_argument("--list-all-params", action=RunCommand, function=lambda: cmd.list_all_params(parser), help="List all params")

    return parser.parse_args()

def handle_args():
    mode = "default"
    args = parse_args()

    # ─────── Debug Mode ─────────
    if args.debug_mode:
        from Scripts.config import DEBUG_MODE
        DEBUG_MODE = True

    # ─────── Force Small Resolution ─────────
    if check_resolution(): msg.updater_intro = msg.small_res_updater_intro

    # ─────── Force Maximize ─────────
    if args.no_force_maximize is False:
        force_maximize()
    
    # ─────── Update Check ─────────
    if args.update_check:
        update()
        sys.exit(0)
    
    # ─────── Shell:Startup ─────────
    if args.main_menu:
        mode = "CleanerApp"

    # ─────── No Update Check ─────────
    from Scripts.config import AUTOUPDATE
    if args.no_update_check is False and AUTOUPDATE:

        if mode == "CleanerApp": # Cleaner Mode
            bat_path = os.path.abspath("cleaner.bat")
        elif mode == "default":  # Main Menu Mode
            bat_path = os.path.abspath("WindowsCleaner.bat")

        update(bat_path)
    
    return mode

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       CLEANER VERSIONS                                                          ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def cleaner_v1():
    from Versions.Cleaner_v1.cleaner_v1 import main
    main()

def cleaner_v2():
    from Versions.Cleaner_v2.CleanerApp import CleanerApp

    app = CleanerApp()
    app.run()

def cleaner_v2_1():
    from Versions.Cleaner_v2.MainMenu import MainMenu

    app = MainMenu()
    app.run()

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       MAIN FUNCTIONS                                                            ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def update(bat_path=None):

    from Scripts.config import APP_VERSION

    if APP_VERSION == 1:

        from Scripts.core.update import main as check_for_updates

        if check_for_updates(bat_path) == False:
            print(f"{HEADER}\n{HEADER}{Fore.LIGHTCYAN_EX}No new updates available. Continuing without update...\n")

    elif APP_VERSION == 2:
        from Versions.Cleaner_v2.UpdaterApp import UpdaterApp
        app = UpdaterApp()
        app.run()

def force_maximize():
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        SW_MAXIMIZE = 3
        hWnd = kernel32.GetConsoleWindow()
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

def check_resolution(max_width=1920, max_height=1024):

    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()  # No mostrar ventana

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.destroy()

        return width < max_width or height < max_height

    except Exception:
        return False

def launch_app(mode):
    from Scripts import config

    if config.DEBUG_MODE:
        config.init_logSystem()

    if config.APP_VERSION == 1:
        cleaner_v1()

    elif config.APP_VERSION == 2:
        if mode == "CleanerApp":
            config.APP_TITLE = f"CleanerApp - v{config.get_release_version()}"
            os.system(f"title {config.APP_TITLE}")
            cleaner_v2()
        elif mode == "default":
            config.APP_TITLE = f"Windows Cleaner - v{config.get_release_version()}"
            os.system(f"title {config.APP_TITLE}")
            cleaner_v2_1()


if __name__ == "__main__":

    mode = handle_args()
    
    launch_app(mode)


