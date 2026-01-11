import sys
from Scripts.utils import messages as msg
from Scripts.core.update import main as check_for_updates

CURRENT_VERSION = 1.1

def cleaner_v1():
    from Versions.cleaner_v1 import main
    main()

def cleaner_v2():
    from Versions.cleaner_v2 import CleanerApp

    app = CleanerApp()
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

def launch_app():
    from Scripts.config import APP_VERSION

    if APP_VERSION == 1:
        cleaner_v1()

    elif APP_VERSION == 2:
        cleaner_v2()


if __name__ == "__main__":

    force_maximize()

    if check_resolution(): msg.updater_intro = msg.small_res_updater_intro

    from Scripts.config import AUTOUPDATE
    if AUTOUPDATE:
        if check_for_updates() == False:
            print("  ///// Continuing without update... /////\n")
    
    launch_app()


