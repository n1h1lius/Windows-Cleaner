# -*- coding: utf-8 -*-
"""
Funciones de limpieza y detección de carpetas temporales
"""

from Scripts.config import *
from Scripts.utils.ui_helpers import make_dynamic_boxed_message

import os
import time
import shutil


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


def cleaner(path, log):
    """
    Limpieza con caja dinámica que crece línea a línea
    """
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
    log.write(header)

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
                    log.write(make_dynamic_boxed_message(
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
                    log.write(make_dynamic_boxed_message(
                        self=log.app,
                        state="content",
                        line=content_line,
                        border_color=BORDER,
                        content_color=CONTENT
                    ))
                    manage_general_vars("folder", size)

            except Exception:
                pass

    except Exception:
        pass

    footer = make_dynamic_boxed_message(
        self=log.app,
        state="footer",
        border_color=BORDER
    )
    log.write(footer)
# ── Detección ─────────────────────────────────────────────────────────────────
def detect_and_get_paths():
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

    detected = []

    # ── Microsoft Edge ───────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Microsoft\\Edge"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["Edge"])
        paths.append(p + "\\User Data\\Default")
        counter += 1

        try:
            ud = p + "\\User Data"
            for d in os.listdir(ud):
                if d.startswith("Profile"):
                    prof_path = os.path.join(ud, d)
                    if os.path.isdir(prof_path): 
                        paths.append(prof_path)
                        counter += 1
        except:
            pass

        detected_folders[PROGRAMS_PATH_NAMES["Edge"]] = counter

    # ── Brave Browser ────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\BraveSoftware\\Brave-Browser"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["Brave"])
        ud = p + "\\User Data"
        default = ud + "\\Default"
        for bp in BROWSER_FOLDERS:
            if os.path.isdir(default + bp): 
                paths.append(default + bp)
                counter += 1
        try:
            for d in os.listdir(ud):
                if d.startswith("Profile"):
                    for bp in BROWSER_FOLDERS:
                        if os.path.isdir(os.path.join(ud, d) + bp): 
                            paths.append(os.path.join(ud, d) + bp)
                            counter += 1
        except:
            pass
        detected_folders[PROGRAMS_PATH_NAMES["Brave"]] = counter

    # ── Google Chrome ────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Google\\Chrome"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["Chrome"])
        ud = p + "\\User Data"
        default = ud + "\\Default"

        for bp in BROWSER_FOLDERS:
            if os.path.isdir(default + bp): 
                paths.append(default + bp)
                counter += 1

        try:
            for d in os.listdir(ud):
                if d.startswith("Profile"):
                    for bp in BROWSER_FOLDERS:
                        if os.path.isdir(os.path.join(ud, d) + bp): 
                            paths.append(os.path.join(ud, d) + bp)
                            counter += 1
        except:
            pass

        detected_folders[PROGRAMS_PATH_NAMES["Chrome"]] = counter
    
    # ── Opera (Stable + GX) ────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\Opera Software"):

        opera_paths = [
            USER_PROFILE + "\\AppData\\Roaming\\Opera Software\\Opera Stable",
            USER_PROFILE + "\\AppData\\Roaming\\Opera Software\\Opera GX Stable",
        ]

        for base in opera_paths:
            if os.path.isdir(base):
                counter = 0
                name = "Opera GX Stable" if "GX" in base else "Opera Stable"
                detected.append(PROGRAMS_PATH_NAMES[name])

                for bp in BROWSER_FOLDERS:
                    full = base + bp
                    if os.path.isdir(full):
                        paths.append(full)
                        counter += 1

                detected_folders[PROGRAMS_PATH_NAMES[name]] = counter


    # ── Discord ──────────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\discord"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["discord"])

        for suf in ["\\Cache\\Cache_Data", "\\Code Cache", "\\GPU_Cache"]:
            paths.append(p + suf)
            counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["discord"]] = counter

    # ── Spotify (Official Desktop Version) ────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Spotify"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["Spotify"])

        ud = p + "\\User Data"
        default = p + "\\Default"

        for suf in BROWSER_FOLDERS:

            if os.path.isdir(p + suf): 
                paths.append(p + suf)
                counter += 1
            if os.path.isdir(ud + suf): 
                paths.append(ud + suf)
                counter += 1
            if os.path.isdir(default + suf): 
                paths.append(default + suf)
                counter += 1

        try:
            for d in os.listdir(p):
                if d.startswith("Profile"):
                    for suf in BROWSER_FOLDERS:
                        prof_path = os.path.join(p, d) + suf
                        if os.path.isdir(prof_path): 
                            paths.append(prof_path)
                            counter += 1
        except:
            pass

        detected_folders[PROGRAMS_PATH_NAMES["Spotify"]] = counter

    # ── Spotify (Official UWP Version) ────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Packages\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0"):
        counter = 0
        detected.append(PROGRAMS_PATH_NAMES["SpotifyAB.SpotifyMusic_zpdnekdrzrea0"])

        for suf in UWP_FOLDERS:
            if os.path.isdir(p + suf): 
                paths.append(p + suf)
                counter += 1

        detected_folders[PROGRAMS_PATH_NAMES["SpotifyAB.SpotifyMusic_zpdnekdrzrea0"]] = counter

    return [p for p in paths if os.path.exists(p)], detected