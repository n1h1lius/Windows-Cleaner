import os

import configparser

from colorama import Fore, Style, init

init(autoreset=True)


# INI
ini_file_path = "Data/config.ini"
config = configparser.ConfigParser()
config.read(ini_file_path, encoding="utf-8")



# GENERAL VARIABLES
APP_VERSION = int(config["Deployment"]["Version"])
USER_PROFILE = os.environ.get("USERPROFILE")
DAYS_THRESHOLD = 3


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


