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
INI_SECTIONS = ["Deployment", "MainVars"]

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

# ─────── Environment ─────────
USER_PROFILE = os.environ.get("USERPROFILE")

# ─────── App Basic Vars ─────────
APP_TITLE = ""
DAYS_THRESHOLD = config.getint("MainVars", "DaysThreshold", fallback=3)


# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                       CLEANER VARIABLES                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ─────── Folders Vars ─────────
detected_folders = {}

BROWSER_FOLDERS = ["\\Cache", "\\File System", "\\IndexedDB", "\\Code Cache", "\\Service Worker", "\\GPU_Cache", "\\blob_storage"]
UWP_FOLDERS = ["\\LocalCache", "\\LocalState", "\\TempState"]

PROGRAMS_PATH_NAMES ={
    "Edge": "Edge",
    "Brave": "Brave",
    "Chrome": "Chrome Browser",
    "Opera GX Stable": "Opera GX",
    "Opera Stable": "Opera",
    "discord": "Discord",
    "Spotify": "Spotify",
    "SpotifyAB.SpotifyMusic_zpdnekdrzrea0": "Spotify-App"
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