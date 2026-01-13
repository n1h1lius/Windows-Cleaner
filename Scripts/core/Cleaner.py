
from Scripts.config import *
from Scripts.utils.ui_helpers import make_dynamic_boxed_message

import os
import time
import shutil

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       CLEANER CORE (V2)                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def is_file_old(file_path, days_threshold):
    file_age = time.time() - os.path.getmtime(file_path)
    return file_age > days_threshold * 86400


def get_file_size(file_path):
    try:
        return round(os.path.getsize(file_path) / (1024 * 1024), 2)
    except:
        return 0.0

def manage_general_vars(mode, size=0):
    global stats

    if mode == "reset":
        stats["total_files"] += stats["current_files"]
        stats["total_folders"] += stats["current_folders"]
        stats["total_mb"] += stats["current_mb"]
        
        stats["current_files"] = 0
        stats["current_folders"] = 0
        stats["current_mb"] = 0.0

    elif mode == "folder":
        stats["current_folders"] += 1
        stats["current_mb"] += size

    elif mode == "file":
        stats["current_files"] += 1
        stats["current_mb"] += size


def printLog(log, message):
    log.write(message)
    log.refresh()

def cleaner(path, log):

    global stats

    manage_general_vars("reset")

    BORDER = "bright_red"
    CONTENT = "bright_white"

    header = make_dynamic_boxed_message(
        self=log.app,
        state="header",
        title=f" Cleaning {os.path.basename(path)} ",
        border_color=BORDER,
        content_color=CONTENT
    )

    printLog(log, header)

    try:
        list_dir = os.listdir(path)
        for filename in sorted(list_dir):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if not is_file_old(file_path, DAYS_THRESHOLD):
                        continue
                    size = get_file_size(file_path)
                    os.unlink(file_path)
                    
                    content_line = (
                        f" [bright_green][+][bright_red] - Deleting file   "
                        f"[bright_yellow][{size:.2f} Mb] [bright_magenta]-> "
                        f"[bright_cyan]{file_path}"
                    )
                    printLog(log, make_dynamic_boxed_message(
                        self=log.app,
                        state="content",
                        line=content_line,
                        border_color=BORDER,
                        content_color=CONTENT
                    ))
                    manage_general_vars("file", size)

                elif os.path.isdir(file_path):
                    size = get_file_size(file_path)
                    shutil.rmtree(file_path, ignore_errors=True)
                    
                    content_line = (
                        f" [bright_green][+][bright_red] - Deleting folder "
                        f"[bright_yellow][{size:.2f} Mb] [bright_magenta]-> "
                        f"[bright_cyan]{file_path}"
                    )
                    printLog(log, make_dynamic_boxed_message(
                        self=log.app,
                        state="content",
                        line=content_line,
                        border_color=BORDER,
                        content_color=CONTENT
                    ))
                    manage_general_vars("folder", size)

            except Exception as e:
                printLog(log, f" [bright_red][!] Error deleting {file_path} [bright_magenta]-> [bright_cyan]{e}")

    except Exception as e:
        printLog(log, f" [bright_red][!] Error deleting {file_path} [bright_magenta]-> [bright_cyan]{e}")

    footer = make_dynamic_boxed_message(
        self=log.app,
        state="footer",
        border_color=BORDER
    )

    printLog(log, footer)


# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       PROGRAMS DETECTOR                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def get_browser_paths(p, browser, paths, detected):

    detected.append(PROGRAMS_PATH_NAMES[browser])

    paths_counter = 0
    profiles_counter = 0

    # Profile Folders
    user_data = p + "\\User Data"
    if os.path.isdir(user_data):
        for folder in os.listdir(user_data):
            if folder.startswith("Profile"):
                profiles_counter += 1
                for browser_folder in BROWSER_FOLDERS:
                    if os.path.isdir(os.path.join(user_data, folder) + browser_folder): 
                        paths.append(os.path.join(user_data, folder) + browser_folder)
                        paths_counter += 1

    # Default Folder
    default = user_data + "\\Default"
    for browser_folder in BROWSER_FOLDERS:
        if os.path.isdir(default + browser_folder): 
            paths.append(default + browser_folder)
            paths_counter += 1

    # Root Folder
    for browser_folder in BROWSER_FOLDERS:
        if os.path.isdir(p + browser_folder): 
            paths.append(p + browser_folder)
            paths_counter += 1
    
    # Update Counters
    detected_folders[PROGRAMS_PATH_NAMES[browser]] = paths_counter
    detected_profiles[PROGRAMS_PATH_NAMES[browser]] = profiles_counter



def detect_and_get_paths():

    detected = []

    # ── Windows 10 + 11 Temp Directories ───────────────────────────────────────────────────────
    paths = [
        "C:\\Windows\\Temp",
        "C:\\Windows\\Prefetch",
        "C:\\$Recycle.Bin",
        USER_PROFILE + "\\AppData\\Local\\Temp",
        USER_PROFILE + "\\AppData\\LocalLow\\Temp",
        USER_PROFILE + "\\AppData\\Local\\CrashDumps",
        USER_PROFILE + "\\AppData\\Local\\D3DSCache",
        USER_PROFILE + "\\AppData\\Local\\Microsoft\\Windows\\Explorer"
    ]

    # ─────────────────────────────────────────────────────────────── BROWSERS ────────────────────────────────────────────────────────────────────────

    # ────── Microsoft Edge
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Microsoft\\Edge"): get_browser_paths(p, "Edge", paths, detected)

    # ────── Brave Browser 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\BraveSoftware\\Brave-Browser"): get_browser_paths(p, "Brave", paths, detected)

    # ────── Google Chrome 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Google\\Chrome"): get_browser_paths(p, "Chrome", paths, detected)

    # ────── Firefox
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Mozilla\\Firefox\\Profiles"): get_browser_paths(p, "Firefox", paths, detected)

    # ────── Vivaldi  
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Vivaldi"): get_browser_paths(p, "Vivaldi", paths, detected)

    # ────── Yandex Browser 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Yandex\\YandexBrowser"): get_browser_paths(p, "Yandex", paths, detected)
    
    # ────── Chromium 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Chromium"): get_browser_paths(p, "Chromium", paths, detected)

    # ────── Waterfox  
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Waterfox"): get_browser_paths(p, "Waterfox", paths, detected)

    # ───── LibreWolf 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\LibreWolf"): get_browser_paths(p, "LibreWolf", paths, detected)

    # ────── Opera (Stable + GX) 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\Opera Software"):

        opera_paths = [
            USER_PROFILE + "\\AppData\\Roaming\\Opera Software\\Opera Stable",
            USER_PROFILE + "\\AppData\\Roaming\\Opera Software\\Opera GX Stable",
        ]

        for base in opera_paths:
            if os.path.isdir(base):
                name = "Opera GX Stable" if "GX" in base else "Opera Stable"
                get_browser_paths(base, name, paths, detected)


    # ─────────────────────────────────────────────────────────────── SOFTWARE ────────────────────────────────────────────────────────────────────────

    # ────── Discord 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\discord"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["discord"])

        for suf in ["\\Cache\\Cache_Data", "\\Code Cache", "\\GPU_Cache"]:
            paths.append(p + suf)
            counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["discord"]] = counter
        detected_profiles[PROGRAMS_PATH_NAMES["discord"]] = 0

    # ────── Spotify (Official Desktop Version) 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Spotify"): get_browser_paths(p, "Spotify", paths, detected)

    # ────── Telegram Desktop
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\Telegram Desktop"):
        telegram_paths = [
            p + "\\tupdates",
            p + "\\tdata\\dumps",
            p + "\\tdata\\emoji",
            p + "\\tdata\\temp",
            p + "\\tdata\\user_data",
        ]

        paths_counter = 0

        detected.append(PROGRAMS_PATH_NAMES["Telegram Desktop"])

        for folder in telegram_paths:
            if os.path.isdir(folder):
                paths.append(folder)
                paths_counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["Telegram Desktop"]] = paths_counter
        detected_profiles[PROGRAMS_PATH_NAMES["Telegram Desktop"]] = 0

    # ────── VS-Code
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\Code"): 
        paths_counter = 0

        get_browser_paths(p, "Code", paths, detected)

        extra_folders = ["\\CachedData", "\\DawnCache", "\\DawnGraphiteCache", "\\DawnWebGPUCache", "\\CachedExtensionVSIXs", "\\CachedExtensions", "\\Service Worker", "\\Backups"]

        for folder in extra_folders:
            if os.path.isdir(p + folder):
                paths.append(p + folder)
                paths_counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["Code"]] += paths_counter


    # ─────────────────────────────────────────────────────────────── APPS (UWP) ────────────────────────────────────────────────────────────────────────

    # ────── Spotify (Official UWP Version) 
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Packages\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["SpotifyAB.SpotifyMusic_zpdnekdrzrea0"])

        for suf in UWP_FOLDERS:
            if os.path.isdir(p + suf): 
                paths.append(p + suf)
                counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["SpotifyAB.SpotifyMusic_zpdnekdrzrea0"]] = counter
        detected_profiles[PROGRAMS_PATH_NAMES["SpotifyAB.SpotifyMusic_zpdnekdrzrea0"]] = 0

    # ────── What's App (Official UWP Version)
    if os.path.isdir(p := USER_PROFILE + "AppData\\Local\\Packages\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\\LocalCache\\EBWebView\\Default"): get_browser_paths(p, "5319275A.WhatsAppDesktop_cv1g1gvanyjgm", paths, detected)
    
    
    # ─────────────────────────────────────────────────────────────── Debug Output Log ───────────────────────────────────────────────────────────────
    if DEBUG_MODE:
        with open("Logs/Core-Cleaner.log", "w") as f:
            f.write("Detected:\n-------------------------------------\n")
            for line in detected:
                f.write(line + "\n")
            
            f.write("\nPrograms_path_names:\n-------------------------------------\n")
            for key in PROGRAMS_PATH_NAMES:
                f.write(f"{key}: {PROGRAMS_PATH_NAMES[key]}\n")
            
            f.write("\nDetected_Folders:\n-------------------------------------\n")
            for key in detected_folders:
                f.write(f"{key}: {detected_folders[key]}\n")
            
            f.write("\nDetected_Profiles:\n-------------------------------------\n")
            for key in detected_profiles:
                f.write(f"{key}: {detected_profiles[key]}\n")

    return [p for p in paths if os.path.exists(p)], detected