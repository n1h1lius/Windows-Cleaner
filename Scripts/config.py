import os
import configparser


# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                            INI FILE                                                             ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

ini_file_path = "Data/config.ini"
config = configparser.ConfigParser()
config.read(ini_file_path, encoding="utf-8")

AUTOUPDATE = config.getboolean("MainVars", "AutoUpdate", fallback=True)
DEBUG_MODE = config.getboolean("MainVars", "DebugMode", fallback=False)
INI_SECTIONS = {"Deployment":"Deployment", "Input":"InputVars", "Boolean":"BooleanVars"}

APP_VERSION = int(config["Deployment"]["Version"])

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       GENERAL VARIABLES                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def get_release_version():
    with open(DATA_VERSION_FILE_PATH, "r") as vf:
        return str(vf.read().strip())

# ─────── App Version ─────────
DATA_VERSION_FILE_PATH = "Data/version.txt"
RELEASE_VERSION = get_release_version()

# ─────── App Name ─────────
V1_NAME = "CleanerApp"
V2_NAME = "Windows Cleaner"

# ─────── Environment ─────────
USER_PROFILE = os.environ.get("USERPROFILE")

# ─────── App Basic Vars ─────────
APP_TITLE = ""
DAYS_THRESHOLD = config.getint("MainVars", "DaysThreshold", fallback=3)

# ─────── Updates Checker ─────────
UPDATED = False


# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       CLEANER VARIABLES                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ─────── Folders Vars ─────────
detected_folders = {}
detected_profiles = {}

BROWSER_FOLDERS = ["\\Cache", "\\File System", "\\IndexedDB", "\\Code Cache", "\\Service Worker", "\\GPU_Cache", "\\blob_storage"]
UWP_FOLDERS = ["\\LocalCache", "\\LocalState", "\\TempState"]

LIST_ALL_SCOPES = {
    "Browsers": ["Edge", "Brave", "Chrome", "Firefox", "Vivaldi", "Yandex", "Chromium", "Waterfox", "LibreWolf", "Opera GX Stable", "Opera Stable"],
    "Software": ["discord", "Spotify", "Telegram Desktop", "Code"],
    "Apps UWP": ["SpotifyAB.SpotifyMusic_zpdnekdrzrea0", "5319275A.WhatsAppDesktop_cv1g1gvanyjgm"]
}

PROGRAMS_PATH_NAMES ={
    # ─────── Browsers
    "Edge": "Edge Browser",
    "Brave-Browser": "Brave Browser",
    "Chrome": "Chrome Browser",
    "Firefox": "Firefox Browser",
    "Vivaldi": "Vivaldi Browser",
    "Yandex": "Yandex Browser",
    "Chromium": "Chromium Browser",
    "Waterfox": "Waterfox Browser",
    "LibreWolf": "LibreWolf Browser",
    "Opera GX Stable": "Opera GX Browser",
    "Opera Stable": "Opera Browser",

    # ─────── Software
    "discord": "Discord",
    "Spotify": "Spotify",
    "Telegram Desktop": "Telegram",
    "Code": "VS-Code",

    # ─────── Apps UWP
    "SpotifyAB.SpotifyMusic_zpdnekdrzrea0": "Spotify-App",
    "5319275A.WhatsAppDesktop_cv1g1gvanyjgm": "Whats-App"
}

# ─────── Stats Vars ─────────
stats = {
    "current_files": 0,
    "current_folders": 0,
    "current_mb": 0.0,
    "total_files": 0,
    "total_folders": 0,
    "total_mb": 0.0
}

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       UI-HUD  VARIABLES                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

BOX_MAX_WIDTH = 195

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                         EXTRA VARIABLES                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

QUOTES = [
    "All gates before one goes forward, one ought to look around, one ought to peer around.",
    "'Hail to the hosts!' A guest has come inside. Where shall this one sit?",
    "Fire is a need for those who are come inside, and on the knee cold.",
    "Food and clothes are a need for the man, that one who has traveled over the mountain.",
    "Wit is a need for that one who wanders widely, easy is anything at home.",
    "A laughing-stock becomes he who knows nothing and sits among the wise.",
    "About his thinking mind a man should not be arrogant, rather cautious in his temper.",
    "When a wise and silent one comes to the homestead, seldom does harm befall the watchful.",
    "A man never gets a more unfailing friend than great common sense.",
    "That one is happy who gets for himself praise and words of kindness.",
    "A better burden a man does not carry on the road than great common sense.",
    "Wealth seems better in an unknown place, such is the poor man’s existence.",
    "The greedy fellow, unless he knows his mind, eats himself into life-long misery."
]

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                           LOG SYSTEM                                                            ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def init_logSystem():
    log_files = ["Core-Cleaner.log", "Core-Cleaner-Deleted.log", "Core-Cleaner-Detected.log", "Cleaner-Output.log"]

    for file in log_files:
        with open(f"Logs/{file}", "w") as f:
            f.write("")


def cleanerLogSystem(line, output=False):
    if DEBUG_MODE:

        logs = ["Logs/Cleaner-Output.log", "Logs/Core-Cleaner-Deleted.log"]
        enter = "\n"

        if output is True:
            logs.pop(1)
            enter = "\n\n"

        for log in logs:
            with open(log, "a", encoding="utf-8") as f:
                f.write(line + enter)
