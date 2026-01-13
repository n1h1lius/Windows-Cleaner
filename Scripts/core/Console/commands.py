# commands.py
from colorama import Fore, init

from Scripts.config import *
from Scripts.core.Cleaner import detect_and_get_paths

init(autoreset=True)

HEADER = f"{Fore.LIGHTYELLOW_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

# ┌───────────────────────────────────────────────────────────────┐
# │                   AVAILABLE CLEANER SCOPES                    │
# ├───────────────────────────────────────────────────────────────┤
# │                                                               │
# │   ┌───────────────┐                                           │
# │   │    Browsers   │                                           │
# │   ├───────────────┘                                           │
# │   │                                                           │
# │   ╠════ Edge Browser                                          │
# │   ╠════ Chrome Browser                                        │
# │   ╚════ Firefox Browser                                       │
# │                                                               │
# └───────────────────────────────────────────────────────────────┘

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

def tree_box(box_title, all_sections):
    max_section_width = 0

    for title, items in all_sections:
        w = max(len(title), max((len(PROGRAMS_PATH_NAMES.get(k, k)) for k in items), default=0))
        max_section_width = max(max_section_width, w)

    # Ancho total interno del recuadro grande
    BOX_WIDTH = max(60, max_section_width + 20)   # mínimo 60, o más si hay nombres largos

    reference_line = f"{HEADER}{Fore.LIGHTGREEN_EX}╔{'═' * BOX_WIDTH}╗"

    print(f"{HEADER}{Fore.LIGHTGREEN_EX}╔{'═' * BOX_WIDTH}╗")
    print(f"{HEADER}{Fore.LIGHTGREEN_EX}║{box_title.center(BOX_WIDTH)}║")
    print(f"{HEADER}{Fore.LIGHTGREEN_EX}╠{'═' * BOX_WIDTH}╣")
    print(f"{HEADER}{Fore.LIGHTGREEN_EX}║{' ' * BOX_WIDTH}║")

    for title, items in all_sections:
        section_width = build_tree_box(title, items, PROGRAMS_PATH_NAMES, len(reference_line), HEADER)

        # Líneas vacías entre secciones
        print(f"{HEADER}{Fore.LIGHTGREEN_EX}│{' ' * BOX_WIDTH}│")

    print(f"{HEADER}{Fore.LIGHTGREEN_EX}╚{'═' * BOX_WIDTH}╝")

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