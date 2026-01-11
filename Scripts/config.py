import os

import configparser


# INI
ini_file_path = "Data/config.ini"
config = configparser.ConfigParser()
config.read(ini_file_path, encoding="utf-8")


RELEASE_VERSION = "1.1"
APP_TITLE = ""

with open("Data/version.txt", "r") as vf:
    RELEASE_VERSION = str(vf.read().strip())

AUTOUPDATE = config.getboolean("MainVars", "AutoUpdate", fallback=True)
DEBUG_MODE = config.getboolean("MainVars", "DebugMode", fallback=False)
INI_SECTIONS = ["Deployment", "MainVars"]


# GENERAL VARIABLES

APP_VERSION = int(config["Deployment"]["Version"])
USER_PROFILE = os.environ.get("USERPROFILE")
DAYS_THRESHOLD = config.getint("MainVars", "DaysThreshold", fallback=3)


# Folder Categories

folder_categories = ["System Temps", "Edge", "Brave", "Chrome", "Discord", "Spotify"]

BROWSER_FOLDERS = ["\\Cache", "\\File System", "\\IndexedDB", "\\Code Cache", "\\Service Worker", "\\GPU_Cache", "\\blob_storage"]

PROGRAMS_PATH_NAMES ={
    "Edge": "Edge",
    "Brave": "Brave",
    "Chrome": "Chrome",
    "discord": "Discord",
    "Spotify": "Spotify"
}

detected_folders = {}


# Cleaner Stats

stats = {
    "current_files": 0,
    "current_folders": 0,
    "current_mb": 0.0,
    "total_files": 0,
    "total_folders": 0,
    "total_mb": 0.0
}

# UI Variables

BOX_MAX_WIDTH = 195

# EXTRA

QUOTES = [
    "All gates before one goes forward, one ought to look around, one ought to peer around.",
    "'Hail to the hosts!' A guest has come inside. Where shall this one sit?"
]