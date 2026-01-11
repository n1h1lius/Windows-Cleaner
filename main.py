import sys

CURRENT_VERSION = 1.1

def cleaner_v1():
    from Versions.cleaner_v1 import main
    main()

def cleaner_v2():
    from Versions.cleaner_v2 import CleanerApp
    
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        SW_MAXIMIZE = 3
        hWnd = kernel32.GetConsoleWindow()
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

    app = CleanerApp()
    app.run()

if __name__ == "__main__":


    from Scripts.config import APP_VERSION

    if APP_VERSION == 1:
        cleaner_v1()

    elif APP_VERSION == 2:
        cleaner_v2()
