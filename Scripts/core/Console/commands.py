# commands.py
from colorama import Fore, init

import argparse

from Scripts.config import *
from Scripts.core.Cleaner import detect_and_get_paths

init(autoreset=True)

HEADER = f"{Fore.LIGHTYELLOW_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

def build_tree_box(title: str, items: list, program_names: dict, box_width: int, prefix="", border_color=Fore.LIGHTGREEN_EX, tree_color=Fore.LIGHTYELLOW_EX, element_color=Fore.LIGHTWHITE_EX) -> int:
    """
    Retorna el ancho máximo usado en esta sección (sin contar el prefix)
    para poder alinear correctamente el cierre del recuadro grande.
    """
    if not items:
        return 0

    # Calculamos el ancho necesario según el contenido más largo
    title_len = len(title)
    items_lens = [len(program_names.get(key, key)) for key in items]
    max_item_len = max(items_lens) if items_lens else 0

    # Ancho interno útil (sin contar bordes ni indentación del árbol)
    inner_content_width = max(title_len, max_item_len) + 4   # margen extra

    # ───── Encabezado del bloque ─────
    header_block_line_1 = f"{prefix}{border_color}│{tree_color}   ┌{'─' * inner_content_width}┐"
    header_block_line_2 = f"{prefix}{border_color}│{tree_color}   │{title.center(inner_content_width)}│"
    header_block_line_3 = f"{prefix}{border_color}│{tree_color}   ├{'─' * inner_content_width}┘"

    print(f"{header_block_line_1}{' ' * (4 + box_width - len(header_block_line_1))}{border_color}│")
    print(f"{header_block_line_2}{' ' * (4 + box_width - len(header_block_line_1))}{border_color}│")
    print(f"{header_block_line_3}{' ' * (4 + box_width - len(header_block_line_1))}{border_color}│")


    # Items
    for i, key in enumerate(items):

        connector = "╠════" if i < len(items) - 1 else "╚════"
        name = program_names.get(key, key)

        # Line Builder
        intro = f"{prefix}{border_color}│"
        blank_line = f"{intro}{' ' * 3}{tree_color}│"
        text_line = f"   {tree_color}{connector} {element_color}{name}"
        closer = f"{border_color}│"

        blank_gap = box_width - len(blank_line) + 4

        print(f"{blank_line}{' ' * blank_gap}{closer}")  

        text_gap = box_width - (len(intro) + len(text_line) - len(border_color) - len(tree_color) + 1)

        print(f"{intro}{text_line}{' ' * text_gap}{closer}")

    # Devolvemos el ancho máximo que ocupó esta sección (útil para alinear)
    return inner_content_width + 6  # +6 → espacio │   + borde izquierdo/derecho

def tree_box(box_title, all_sections, border_color=Fore.LIGHTGREEN_EX, tree_color=Fore.LIGHTYELLOW_EX, element_color=Fore.LIGHTWHITE_EX):
    max_section_width = 0

    for title, items in all_sections:
        w = max(len(title), max((len(PROGRAMS_PATH_NAMES.get(k, k)) for k in items), default=0))
        max_section_width = max(max_section_width, w)

    # Ancho total interno del recuadro grande
    BOX_WIDTH = max(60, max_section_width + 20)   # mínimo 60, o más si hay nombres largos

    reference_line = f"{HEADER}{Fore.LIGHTGREEN_EX}╔{'═' * BOX_WIDTH}╗"

    print(f"{HEADER}{border_color}╔{'═' * BOX_WIDTH}╗")
    print(f"{HEADER}{border_color}║{box_title.center(BOX_WIDTH)}║")
    print(f"{HEADER}{border_color}╠{'═' * BOX_WIDTH}╣")
    print(f"{HEADER}{border_color}║{' ' * BOX_WIDTH}║")

    for title, items in all_sections:
        section_width = build_tree_box(title, items, PROGRAMS_PATH_NAMES, len(reference_line), HEADER, border_color, tree_color, element_color)

        # Líneas vacías entre secciones
        print(f"{HEADER}{border_color}│{' ' * BOX_WIDTH}│")

    print(f"{HEADER}{border_color}╚{'═' * BOX_WIDTH}╝")

def list_all_cleaner_scopes():
    # Calculamos el ancho máximo global para que todo el recuadro grande quede bien
    all_sections = [
        ("Browsers", LIST_ALL_SCOPES["Browsers"]),
        ("Software", LIST_ALL_SCOPES["Software"]),
        ("Apps UWP", LIST_ALL_SCOPES["Apps UWP"]),
    ]

    tree_box("ALL CLEANER SCOPES", all_sections)

def list_available_cleaner_scopes():
    # Calculamos el ancho.maxcdn global para que todo el recuadro grande quede bien
    detected = detect_and_get_paths()[1]

    browsers = []
    software = []
    apps_uwp = []


    for item in detected:
        key = next((k for k, v in PROGRAMS_PATH_NAMES.items() if v == item), None)
        if key in LIST_ALL_SCOPES["Browsers"]: browsers.append(key)
        elif key in LIST_ALL_SCOPES["Software"]: software.append(key)
        elif key in LIST_ALL_SCOPES["Apps UWP"]: apps_uwp.append(key)

    all_sections = [
        ("Browsers", browsers),
        ("Software", software),
        ("Apps UWP", apps_uwp),
    ]

    tree_box("AVAILABLE CLEANER SCOPES", all_sections)


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
        help_text = action.help or "(sin descripción)"
        
        # Si es un flag sin valor (store_true/store_false), lo indicamos
        if isinstance(action, argparse._StoreTrueAction):
            cmd_str += f"  [{Fore.LIGHTCYAN_EX}flag{Fore.RESET}]"
        elif isinstance(action, argparse._StoreFalseAction):
            cmd_str += f"  [{Fore.LIGHTCYAN_EX}flag{Fore.RESET}]"
            
        commands.append((cmd_str, help_text))
    
    return commands


    """

    ┌───────────────────────┐
    │       PARAMETRO       │
    ├───────────────────────┘
    │
    │            ┌────────────────────────────────────────┐
    └────────────┤             HELP DESCRIPTION           │
                └────────────────────────────────────────┘

    ┌───────────────────────┐
    │       PARAMETRO       │
    ├───────────────────────┘
    │
    │            ┌────────────────────────────────────────┐
    └────────────┤             HELP DESCRIPTION           │
                └────────────────────────────────────────┘
    """


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