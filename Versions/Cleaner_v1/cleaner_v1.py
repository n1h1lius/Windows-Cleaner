import os
import shutil
import time
import msvcrt

from Scripts.core.Cleaner import detect_and_get_paths
from Scripts.config import DAYS_THRESHOLD
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

SIZE_THRESHOLD_MB = None  # Max size threshold in MB

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
    """Verifies if a file has not been modified in a specific time."""
    file_age = time.time() - os.path.getmtime(file_path)
    return file_age > days_threshold * 86400  # Convertir días a segundos


def is_file_large(file_path, size_threshold_mb):
    """Verifies if a file exceeds the specified size in MB."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convertir bytes a MB
    return file_size_mb > size_threshold_mb


def get_file_size(file_path):
    return round(os.path.getsize(file_path) / (1024 * 1024), 2)  # Convertir bytes a MB

# =================================================================================================================
#                                                   CLEANER
# =================================================================================================================

def cleaner(path, days_threshold=None, size_threshold_mb=None):
    """Deletes files and folders based on age or size."""
    global numVars
    global VERBOSE_MODE
    try:
        list_dir = os.listdir(path)
        for filename in list_dir:
            file_path = os.path.join(path, filename)

            try:
                # Delete Files
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

                # Delete Folders
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
    
    global numVars

    print(Fore.GREEN + Style.BRIGHT + "\n///// -> STARTING WINDOWS CLEANER\n\n///// - **********************************************************")

    paths_to_clean = detect_and_get_paths()[0]

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

