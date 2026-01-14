# commands.py
from colorama import Fore, Style, init

import argparse

from Scripts.config import *
from Scripts.core.Cleaner import detect_and_get_paths
from Scripts.utils.ui_helpers import tree_box
from Scripts.utils.Getters import get_detected_paths

init(autoreset=True)

HEADER = f"{Fore.LIGHTYELLOW_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

def list_all_cleaner_scopes():
    """Returns all possible options that cleaner script is able to detect"""

    all_sections = [
        ("Browsers", LIST_ALL_SCOPES["Browsers"]),
        ("Software", LIST_ALL_SCOPES["Software"]),
        ("Apps UWP", LIST_ALL_SCOPES["Apps UWP"]),
    ]

    tree_box("ALL CLEANER SCOPES", all_sections)

def list_available_cleaner_scopes():
    """Returns all available options that cleaner script has detected on the system"""
    detected = detect_and_get_paths()[1]

    browsers = []
    software = []
    apps_uwp = []


    for item in detected:
        
        for key in PROGRAMS_PATH_NAMES:
            if item in PROGRAMS_PATH_NAMES[key]:
                
                if key in LIST_ALL_SCOPES["Browsers"]: browsers.append(key)
                elif key in LIST_ALL_SCOPES["Software"]: software.append(key)
                elif key in LIST_ALL_SCOPES["Apps UWP"]: apps_uwp.append(key)

    all_sections = [
        ("Browsers", browsers),
        ("Software", software),
        ("Apps UWP", apps_uwp),
    ]

    tree_box("AVAILABLE CLEANER SCOPES", all_sections)

def get_all_detected_paths():
    paths_detected = detect_and_get_paths()
    detected = get_detected_paths(paths_detected[1], paths_detected[0])

    print(f"{Fore.LIGHTYELLOW_EX}  /////\n  ///// {Fore.RESET}")

    for line in detected:
        if line.startswith("Program: "):
            opt = line.split("\n")

            new_line = ""
            flag = False
            for i, item in enumerate(opt[0].split(" ")):
                if item.startswith("Program") or item.startswith("Folders") or item.startswith("Profiles"):
                    item = f"{Fore.YELLOW + Style.BRIGHT}{item}"
                    item2 = f"{Fore.LIGHTRED_EX}[ {Fore.GREEN + Style.BRIGHT}{opt[0].split(" ")[i+1]}{Fore.LIGHTRED_EX} ]{Fore.RESET}"
                    new_line += item + " " + item2 + " "
                    flag = True
                
                elif flag is False:
                    new_line += item


            print(f"{HEADER}{Fore.LIGHTCYAN_EX}{new_line}\n{HEADER}{Fore.LIGHTCYAN_EX}{opt[1]}")
        
        elif line == "\n\n":
            print(f"{Fore.LIGHTYELLOW_EX}  /////\n  ///// {Fore.RESET}")

        else:
            print(f"{HEADER}{Fore.LIGHTWHITE_EX}{line.strip("\n")}")


def get_parser_commands(parser):
    """
    Extrae los comandos/argumentos con sus descripciones del ArgumentParser
    Ignora --help automáticamente
    """
    commands = []
    
    for action in parser._actions:
        if action.dest == 'help':
            continue
        if not action.option_strings:  # ignoramos positional si los hubiera
            continue
            
        cmd_str = ", ".join(action.option_strings)
        help_text = action.help or "[ No Description ]"
        
        # Si es un flag sin valor (store_true/store_false), lo indicamos
        if isinstance(action, argparse._StoreTrueAction):
            cmd_str += f"  [{Fore.LIGHTCYAN_EX}flag{Fore.RESET}]"
        elif isinstance(action, argparse._StoreFalseAction):
            cmd_str += f"  [{Fore.LIGHTCYAN_EX}flag{Fore.RESET}]"
            
        commands.append((cmd_str, help_text))
    
    return commands


def list_all_params(parser):
    """
    Muestra los comandos del parser en formato visual bonito
    Lee dinámicamente de argparse.ArgumentParser
    """
    commands = get_parser_commands(parser)
    
    if not commands:
        print(f"{Fore.LIGHTRED_EX}No se encontraron comandos en el parser.")
        return

    # ───── Cálculo de anchos para alineación perfecta ─────
    max_cmd_len  = max(len(cmd) for cmd, _ in commands)
    max_desc_len = max(len(desc) for _, desc in commands)
    
    # Ancho interno para el bloque de descripción
    desc_inner_width = max(45, max_desc_len + 8)   # mínimo razonable + margen
    
    # Ancho total del recuadro grande
    BOX_WIDTH = max(80, desc_inner_width + 22)     # espacio para conectores + estética

    border = Fore.LIGHTGREEN_EX
    tree   = Fore.LIGHTYELLOW_EX
    titlec = Fore.LIGHTMAGENTA_EX
    elem   = Fore.LIGHTWHITE_EX
    head   = f"{Fore.LIGHTYELLOW_EX}  ///// {titlec}-> {Fore.RESET}"

    # ───── Cabecera principal ─────
    print(f"{head}{border}╔{'═' * BOX_WIDTH}╗")
    print(f"{head}{border}║{' AVAILABLE PARAMETERS '.center(BOX_WIDTH)}║")
    print(f"{head}{border}╠{'═' * BOX_WIDTH}╣")
    print(f"{head}{border}║{' ' * BOX_WIDTH}║")

    # ───── Cada comando ─────
    for i, (cmd, desc) in enumerate(commands):
        is_last = i == len(commands) - 1

        # Bloque superior: nombre del comando
        cmd_box_width = max_cmd_len + 6
        cmd_top    = f"┌{'─' * cmd_box_width}┐"
        cmd_text   = f" {cmd.ljust(max_cmd_len + 2)}   "
        cmd_bottom = f"├{'─' * cmd_box_width}┘"

        if f"  [{Fore.LIGHTCYAN_EX}flag{Fore.RESET}]" in cmd:
            cmd_text += ' ' * 10
            cmd_text_offset = -5

        else:
            cmd_text_offset = 5

        # Bloque inferior: descripción
        desc_top    = f"┌{'─' * desc_inner_width}┐"
        desc_text   = f" {desc.center(desc_inner_width - 2)} "
        desc_bottom = f"└{'─' * desc_inner_width}┘"

        # ─── Impresión ───
        # Línea 1: bloque superior del comando
        print(f"{head}{border}║{tree}   {cmd_top}{' ' * (BOX_WIDTH - len(cmd_top) - 3)}{border}║")

        # Línea 2: texto del comando
        print(f"{head}{border}║{tree}   │{elem}{cmd_text}{tree}│{' ' * (BOX_WIDTH - len(cmd_text) - cmd_text_offset)}{border}║")

        # Línea 3: cierre superior + conector descendente
        print(f"{head}{border}║{tree}   {cmd_bottom}{' ' * (BOX_WIDTH - len(cmd_bottom) - 3)}{border}║")

        # Linea que baja
        print(f"{head}{border}║{tree}   │         {' ' * (desc_inner_width)}   {border} {' ' * (BOX_WIDTH - desc_inner_width - 17)}{border}║")
        print(f"{head}{border}║{tree}   │         {' ' * (desc_inner_width)}   {border} {' ' * (BOX_WIDTH - desc_inner_width - 17)}{border}║")

        # Línea con bloque descripción
        print(f"{head}{border}║{tree}   │         {desc_top}{' ' * (BOX_WIDTH - desc_inner_width - 15)}{border}║")

        # Línea con texto descripción
        print(f"{head}{border}║{tree}   └─────────│{elem}{desc_text}{tree}│{' ' * (BOX_WIDTH - desc_inner_width - 15)}{border}║")

        # Cierre descripción
        print(f"{head}{border}║{tree}             {desc_bottom}{' ' * (BOX_WIDTH - desc_inner_width - 15)}{border}║")

        # Separador entre comandos
        if not is_last:
            print(f"{head}{border}║{' ' * BOX_WIDTH}║")
            print(f"{head}{border}║{' ' * BOX_WIDTH}║")

    # Cierre final
    print(f"{head}{border}╚{'═' * BOX_WIDTH}╝")
    print()