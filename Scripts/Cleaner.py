from Scripts.config import *

import shutil

# ── Cleaner original ──────────────────────────────────────────────────────────
def is_file_old(file_path, days_threshold):
    file_age = time.time() - os.path.getmtime(file_path)
    return file_age > days_threshold * 86400

def get_file_size(file_path):
    return round(os.path.getsize(file_path) / (1024 * 1024), 2)

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

def cleaner(path):
    global stats

    manage_general_vars("reset")

    print(f"\n{Fore.LIGHTRED_EX}     ╔──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╗")
    print(f"{Fore.LIGHTRED_EX}     │                                                                                                                                                                                                  │")

    try:
        list_dir = os.listdir(path)
        for filename in list_dir:
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if not is_file_old(file_path, DAYS_THRESHOLD):
                        continue
                    size = get_file_size(file_path)
                    os.unlink(file_path)
                    total = 38
                    total += 1 if size >= 0 else 2 if size >= 10 else 3 if size >= 100 else 0
                    print(f"{Fore.LIGHTRED_EX}     │ {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTRED_EX} - Deleting file  ///// {Fore.LIGHTYELLOW_EX}[{size} Mb] {Fore.LIGHTMAGENTA_EX}-> {Fore.CYAN}{file_path}{' ' * (170 - (total + len(file_path)))}{Fore.LIGHTRED_EX}│")
                    manage_general_vars("file", size)

                elif os.path.isdir(file_path):
                    size = get_file_size(file_path)
                    shutil.rmtree(file_path, ignore_errors=True)
                    total = 40
                    total += 1 if size >= 0 else 2 if size >= 10 else 3 if size >= 100 else 0
                    print(f"{Fore.LIGHTRED_EX}     │ {Fore.LIGHTGREEN_EX}[+]{Fore.LIGHTRED_EX} - Deleting Folder  ///// {Fore.LIGHTYELLOW_EX}[{size} Mb] {Fore.LIGHTMAGENTA_EX}-> {Fore.CYAN}{file_path}{' ' * (170 - (total + len(file_path)))}{Fore.LIGHTRED_EX}│")
                    manage_general_vars("folder", size)
            except:
                pass
    except:
        pass
    print(f"{Fore.LIGHTRED_EX}     │                                                                                                                                                                                                  │")
    print(f"{Fore.LIGHTRED_EX}     ╚──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╝\n")


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
        detected.append("Edge")
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

        detected_folders["Edge"] = counter

    # ── Brave Browser ────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\BraveSoftware\\Brave-Browser"):
        counter = 0
        detected.append("Brave")
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
        detected_folders["Brave"] = counter

    # ── Google Chrome ────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Google\\Chrome"):
        counter = 0
        detected.append("Chrome")
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

        detected_folders["Chrome"] = counter

    # ── Discord ──────────────────────────────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Roaming\\discord"):
        counter = 0
        detected.append("Discord")
        for suf in ["\\Cache\\Cache_Data", "\\Code Cache", "\\GPU_Cache"]:
            paths.append(p + suf)
            counter += 1
        detected_folders["Discord"] = counter

    # ── Spotify (Official Desktop Version) ────────────────────────────────────
    if os.path.isdir(p := USER_PROFILE + "\\AppData\\Local\\Spotify"):
        counter = 0
        detected.append("Spotify")

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

        detected_folders["Spotify"] = counter

    return [p for p in paths if os.path.exists(p)], detected