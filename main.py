import sys, os, time
import argparse


from Scripts.utils import messages as msg
from Scripts.core.update import main as check_for_updates

from colorama import Fore, init

init(autoreset=True)

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       ARGUMENTS HANDLING                                                        ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

HEADER = f"{Fore.LIGHTRED_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

def parse_args():
    parser = argparse.ArgumentParser()

    # ───────── Arguments ─────────
    parser.add_argument("--update-check", action="store_true", help="Check for updates without launching the application")
    parser.add_argument("--main-menu", action="store_false", help="Launch just cleaner App")
    parser.add_argument("--no-update-check", action="store_true", help="Disable update checking")
    parser.add_argument("--no-force-maximize", action="store_true", help="Do not force maximize the console window on start")

    return parser.parse_args()

def handle_args():
    args = parse_args()

    if check_resolution(): msg.updater_intro = msg.small_res_updater_intro

    if args.no_force_maximize is False:
        force_maximize()
    
    # ─────── Update Check ─────────
    if args.update_check:
        if check_for_updates() == False:
            print(f"{HEADER}{Fore.LIGHTCYAN_EX}No new updates available\n")
            time.sleep(3)
        sys.exit(0)

    # ─────── No Update Check ─────────
    from Scripts.config import AUTOUPDATE
    if args.no_update_check is False and AUTOUPDATE:
        if check_for_updates() == False:
            print(f"{HEADER}{Fore.LIGHTCYAN_EX}No new updates available. Continuing without update...\n")
    
    # ─────── Shell:Startup ─────────
    if args.main_menu:
        return "CleanerApp"

    # ─────── Standard Mode ─────────
    return "default"

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
    from Scripts.config import APP_VERSION, RELEASE_VERSION

    if APP_VERSION == 1:
        cleaner_v1()

    elif APP_VERSION == 2:
        if mode == "CleanerApp":
            config.APP_TITLE = f"CleanerApp - v{RELEASE_VERSION}"
            os.system(f"title {config.APP_TITLE}")
            cleaner_v2(os.path.abspath("cleaner.bat"))
        elif mode == "default":
            config.APP_TITLE = f"Windows Cleaner - v{RELEASE_VERSION}"
            os.system(f"title {config.APP_TITLE}")
            cleaner_v2_1(os.path.abspath("WindowsCleaner.bat"))


if __name__ == "__main__":

    mode = handle_args()
    
    launch_app(mode)


