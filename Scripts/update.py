import os
import sys
import requests
import zipfile
import shutil
import tempfile
import configparser
import subprocess

REPO_URL = "https://github.com/n1h1lius/Windows-Cleaner/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = "Data/version.txt"  # Crea este archivo local con "1.1"
CONFIG_FILE = "Data/config.ini"
BAT_FILE = "cleaner.bat"  # Ajusta si se llama diferente o path

def merge_configs(local_path, remote_path):
    local = configparser.ConfigParser(allow_no_value=True)
    local.optionxform = str
    local.read(local_path)

    remote = configparser.ConfigParser(allow_no_value=True)
    remote.optionxform = str
    remote.read(remote_path)

    updated = False

    # Añadir secciones nuevas
    for section in remote.sections():
        if not local.has_section(section):
            local.add_section(section)
            updated = True

    # Añadir solo keys que no existen en local
    for section in remote.sections():
        for key in remote.options(section):
            if not local.has_option(section, key):
                value = remote.get(section, key, raw=True)
                local.set(section, key, value)
                updated = True
                print(f"[Merge] Nueva clave añadida: [{section}] {key} = {value}")

    if updated:
        with open(local_path, 'w', encoding='utf-8') as f:
            local.write(f)
        print("Config.ini actualizado con nuevas claves (valores antiguos preservados)")
    else:
        print("No se añadieron claves nuevas al config.ini")

def update_app():
    # Descarga ZIP
    response = requests.get(REPO_URL)
    if response.status_code != 200:
        print("Error descargando actualización.")
        return False
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "repo.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)
        
        extract_dir = os.path.join(tmp_dir, "extract")
        os.makedirs(extract_dir)
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # El ZIP extrae a una subcarpeta como "Windows-Cleaner-main"
        repo_dir = os.path.join(extract_dir, "Windows-Cleaner-main")  # Ajusta si el nombre cambia
        
        # Backup config.ini
        if os.path.exists(CONFIG_FILE):
            shutil.copy(CONFIG_FILE, CONFIG_FILE + ".bak")
        
        # Merge config si hay nuevo
        remote_config_path = os.path.join(repo_dir, CONFIG_FILE)
        if os.path.exists(remote_config_path):
            merge_configs(CONFIG_FILE, remote_config_path)
        
        # Copia todo excepto updater.py
        for item in os.listdir(repo_dir):
            if item == "updater.py":
                continue
            src = os.path.join(repo_dir, item)
            dst = os.path.join(os.getcwd(), item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    print("Actualización completada.")
    return True

def get_remote_version():
    url = "https://raw.githubusercontent.com/n1h1lius/Windows-Cleaner/main/Data/version.txt"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception:
        return None
    
def main():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return False
    
    with open(LOCAL_VERSION_FILE, "r") as f:
        local_version = f.read().strip()
    
    remote_version = get_remote_version()

    if remote_version is None:
        print("No se pudo comprobar versión remota. Continuando con versión local.")
        return False
    
    elif remote_version != local_version:
        print(f"Nueva versión disponible: {remote_version} (local: {local_version})")
        # Opcional: Preguntar al usuario
        if input("¿Actualizar? [Y/n]: ").lower() != "n":
            if update_app():
                # Actualiza la versión local
                with open(LOCAL_VERSION_FILE, "w") as f:
                    f.write(remote_version)
                # Relanza el bat
                subprocess.call(BAT_FILE)
                sys.exit(0)
                return True
            else:
                print("Actualización fallida. Continuando con versión actual.")
                return False
    
    # Si no actualiza o ya está al día, lanza main.py (o el bat si prefieres)
    return False