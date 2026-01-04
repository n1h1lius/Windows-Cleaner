import os
import shutil
import time
import msvcrt
from colorama import Fore, Style, init

init(autoreset=True)

numVars = {
    "TotalFiles": 0,
    "TotalFolders": 0,
    "TotalMB": 0,
    "Del_Files": 0,
    "Del_Folders": 0,
    "MB": 0
}

VERBOSE_MODE = False

USER_PROFILE = os.environ.get("USERPROFILE")
APPDATA_LOCAL = "\\AppData\\Local"
APPDATA_LOCALLOW = "\\AppData\\LocalLow"
APPDATA_ROAMING = "\\AppData\\Roaming"

EDGE_PATH = USER_PROFILE + APPDATA_LOCAL + "\\Microsoft\\Edge"
BRAVE_PATH = USER_PROFILE + APPDATA_LOCAL + "\\BraveSoftware\\Brave-Browser"
CHROME_PATH = USER_PROFILE + APPDATA_LOCAL + "\\Google\\Chrome"

DISCORD_PATH = USER_PROFILE +  APPDATA_ROAMING + "\\discord"

# Configuración avanzada
DAYS_THRESHOLD = 3  # Antigüedad máxima en días para eliminar archivos None for none
SIZE_THRESHOLD_MB = None  # Tamaño máximo permitido en MB para archivos None for none

# =================================================================================================================
#                                                   UTILITIES
# =================================================================================================================

def wait_before_continue(timeout=10):
    for remaining in range(timeout, 0, -1):
        print(Fore.MAGENTA + Style.BRIGHT + f"\n///// -> \rAll set. Press any key to continue or wait {remaining} seconds...", end="", flush=True)
        time.sleep(1)

        if msvcrt.kbhit():  # Si el usuario pulsa una tecla
            msvcrt.getch()  # Consumir la tecla
            return

def is_file_old(file_path, days_threshold):
    """Verifica si un archivo no se ha modificado en un tiempo específico."""
    file_age = time.time() - os.path.getmtime(file_path)
    return file_age > days_threshold * 86400  # Convertir días a segundos


def is_file_large(file_path, size_threshold_mb):
    """Verifica si un archivo supera el tamaño especificado en MB."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convertir bytes a MB
    return file_size_mb > size_threshold_mb


def get_file_size(file_path):
    return round(os.path.getsize(file_path) / (1024 * 1024), 2)  # Convertir bytes a MB

def get_paths_to_clean():
    
    paths = [
        "C:\\Windows\\Temp",
        "C:\\Windows\\Prefetch",
        "C:\\$Recycle.Bin",
        USER_PROFILE + APPDATA_LOCAL + "\\Temp",
        USER_PROFILE + APPDATA_LOCALLOW + "\\Temp",
        USER_PROFILE + APPDATA_LOCAL + "\\CrashDumps",
        USER_PROFILE + APPDATA_LOCAL + "\\D3DSCache",
        USER_PROFILE + APPDATA_LOCAL + "\\Microsoft\\Windows\\Explorer"
    ]

    browsers_paths = [
            "\\Cache",
            "\\File System",
            "\\IndexedDB",
            "\\Code Cache",
            "\\Service Worker"
        ]

    print(Fore.CYAN + f"\n///// -> DETECTING INSTALLED PROGRAMS\n")
    
    # Microsoft Edge

    if os.path.isdir(EDGE_PATH):
        default_path = EDGE_PATH + "\\User Data\\Default"
        
        paths.append(default_path)
        
        for path in browsers_paths:
            paths.append(default_path + path)

        print(Fore.LIGHTGREEN_EX + "///// -> Microsoft Edge Detected")
    
    # Brave

    if os.path.isdir(BRAVE_PATH):
        userData_path = BRAVE_PATH + "\\User Data"
        
        counter = 0

        for dir in os.listdir(userData_path):
            if dir.startswith("Profile"):
                profile_path = userData_path + f"\\{dir}"

                for path in browsers_paths:
                    paths.append(profile_path + path)

                counter += 1
        
        print(Fore.LIGHTGREEN_EX + f"///// -> Brave Browser Detected - [{counter}] Profiles Detected")
    
    # Google Chrome

    if os.path.isdir(CHROME_PATH):
        userData_path = CHROME_PATH + "\\User Data\\Default"

        for path in browsers_paths:
            paths.append(userData_path + path)

    # Discord

    if os.path.isdir(DISCORD_PATH):
        discord_delete_folders = [
            "\\Cache\\Cache_Data",
            "\\Code Cache",
            "\\GPU_Cache"
        ]

        for path in discord_delete_folders:
            paths.append(DISCORD_PATH + path)
        
        print(Fore.LIGHTGREEN_EX + "///// -> Discord Detected")
    
    wait_before_continue(5)
    return paths


# =================================================================================================================
#                                                   CLEANER
# =================================================================================================================

def cleaner(path, days_threshold=None, size_threshold_mb=None):
    """Elimina archivos y carpetas basándose en antigüedad o tamaño."""
    global numVars
    global VERBOSE_MODE
    try:
        list_dir = os.listdir(path)
        for filename in list_dir:
            file_path = os.path.join(path, filename)

            try:
                # Limpiar archivos
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if days_threshold and not is_file_old(file_path, days_threshold):
                        continue  # Saltar archivos recientes
                    if size_threshold_mb and not is_file_large(file_path, size_threshold_mb):
                        continue  # Saltar archivos pequeños

                    size = get_file_size(file_path)
                    os.unlink(file_path)

                    print(Fore.RED + Style.BRIGHT + f"///// [+] - Deleting file  ///// " + Fore.LIGHTYELLOW_EX + f"[{size} Mb] " + Fore.RED + Style.BRIGHT + "-> " + Fore.CYAN, file_path)
                    numVars["Del_Files"] += 1
                    numVars["MB"] += size

                # Limpiar carpetas
                elif os.path.isdir(file_path):
                    size = get_file_size(file_path)
                    shutil.rmtree(file_path)
                    print(Fore.RED + Style.BRIGHT + "///// [+] - Deleting Folder  ///// " + Fore.LIGHTYELLOW_EX + f"[{size} Mb] " +  Fore.RED + Style.BRIGHT + "-> " + Fore.BLUE, file_path)

                    numVars["Del_Folders"] += 1
                    numVars["MB"] += size

            except PermissionError:
                if VERBOSE_MODE:
                    print(Fore.YELLOW + "///// [-] - Skipped (Permission Denied) ->" + Fore.MAGENTA, file_path)
            except Exception as e:
                if VERBOSE_MODE:
                    print(Fore.YELLOW + "///// [!] - Error -> " + Fore.MAGENTA, ":", e)

    except FileNotFoundError:
        if VERBOSE_MODE:
            print(Fore.YELLOW + "///// [-] - Path not found -> " + Fore.MAGENTA, path)       

# =================================================================================================================
#                                                      MAIN
# =================================================================================================================

def main():
    """Limpia carpetas temporales comunes con configuraciones avanzadas."""
    
    global numVars

    print(Fore.GREEN + Style.BRIGHT + "\n///// -> STARTING WINDOWS CLEANER\n\n///// - **********************************************************")

    paths_to_clean = get_paths_to_clean()

    for path in paths_to_clean:

        if path:
            print(Fore.CYAN + f"\n///// -> CLEANING: {path}\n")

            cleaner(path, days_threshold=DAYS_THRESHOLD, size_threshold_mb=SIZE_THRESHOLD_MB)

            print(Fore.LIGHTGREEN_EX + f"\n///// - **********************************************************\n///// -> CLEANED || Deleted Files [{numVars['Del_Files']}] || Deleted Folders [{numVars['Del_Folders']}] || Deleted Size in Mb [{numVars['MB']}]\n///// - **********************************************************")

            numVars['TotalFiles'] += numVars['Del_Files']
            numVars['TotalFolders'] += numVars['Del_Folders']
            numVars['TotalMB'] += numVars['MB']
            numVars['Del_Files'] = 0
            numVars['Del_Folders'] = 0
            numVars['MB'] = 0

        else:
            print(Fore.RED + "\n///// - **********************************************************\n///// [!] - Invalid path, skipping...\n///// - **********************************************************\n")

    print(Fore.YELLOW + f"\n///// - **********************************************************\n///// -> CLEANED || Total Deleted Files [{numVars['TotalFiles']}] || Total Deleted Folders [{numVars['TotalFolders']}] || Total Deleted Size in Mb [{numVars['TotalMB']}]\n///// - **********************************************************\n")
    print(Fore.MAGENTA + Style.BRIGHT + "\n///// -> PROCESS COMPLETED, PRESS ANY KEY TO CLOSE")

    input("")


if __name__ == "__main__":
    main()
