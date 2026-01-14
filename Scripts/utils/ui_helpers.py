# -*- coding: utf-8 -*-
"""
Funciones de ayuda para formateo visual responsive en la consola
"""

import shutil
import re

from Scripts.config import *

from colorama import Fore

ansi_escape = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

HEADER = f"{Fore.LIGHTYELLOW_EX}  ///// {Fore.LIGHTMAGENTA_EX}-> {Fore.RESET}"

# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                    TEXTUAL CONSOLE UTILS                                                        ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

def strip_ansi(text):
    """Elimina códigos ANSI de un string para calcular longitud visible"""
    return ansi_escape.sub('', text)


def truncate_ansi(text, max_width, ellipsis="..."):
    """Trunca texto preservando códigos ANSI, añadiendo ... al final"""
    if not text:
        return ""
        
    plain = strip_ansi(text)
    if len(plain) <= max_width:
        return text
        
    target = max_width - len(ellipsis)
    current_len = 0
    result = []
    in_escape = False
    
    for char in text:
        if char == '\x1b':
            in_escape = True
            result.append(char)
            continue
            
        if in_escape:
            result.append(char)
            if char == 'm':
                in_escape = False
            continue
            
        current_len += 1
        result.append(char)
        
        if current_len >= target:
            break
            
    return ''.join(result) + ellipsis


def get_terminal_width(obj, default=120):
    """Intenta obtener el ancho real del terminal desde diferentes fuentes"""
    try:
        return obj.console.width
    except:
        try:
            return shutil.get_terminal_size(fallback=(default, 24)).columns
        except:
            return default


def make_dynamic_boxed_message(self, state="header", title="", line="", border_color="", content_color=""):
    """
    Genera partes de una caja dinámica que crece línea a línea
    """
    width = get_terminal_width(self, 120) - 4
    width = max(80, min(width, BOX_MAX_WIDTH))
    inner_width = width - 2

    head = f"  [{border_color}]╔{'─' * inner_width}╗[/{border_color}]"
    empty = f"  [{border_color}]│{' ' * inner_width}│[/{border_color}]"
    foot = f"  [{border_color}]╚{'─' * inner_width}╝[/{border_color}]"

    if state == "header":
        lines = [head, empty]
        if title:
            title_clean = strip_ansi(title)
            if len(title_clean) > inner_width - 4:
                title = truncate_ansi(title, inner_width - 6, "...")
            title_padded = title.center(inner_width)
            lines.append(f"  [{border_color}]│{title_padded}│[/{border_color}]")
            lines.append(empty)
            lines.append(foot)
            lines.append(empty)
        return "\n".join(lines)

    elif state == "content":
        full_line = line
        clean_line = strip_ansi(full_line)
        if len(clean_line) > inner_width - 4:
            full_line = truncate_ansi(full_line, inner_width - 7, "...")
            clean_line = strip_ansi(full_line)
        padded = full_line + ' ' * (inner_width - len(clean_line))
        return f"  [{border_color}]│[/{border_color}]{padded}[{border_color}]│[/{border_color}]"

    elif state == "footer":
        return "\n".join([empty, foot, ""])

    return ""


def make_boxed_message(self, title, content_lines, border_color, content_color=""):
    """Genera un cuadro completo y estático adaptado al ancho"""
    width = get_terminal_width(self, 120) - 4
    width = max(80, min(width, BOX_MAX_WIDTH))

    head = f"[{border_color}]╔{'─' * (width - 2)}╗[/{border_color}]"
    foot = f"[{border_color}]╚{'─' * (width - 2)}╝[/{border_color}]"
    body_empty = f"[{border_color}]│{' ' * (width - 2)}│[/{border_color}]"

    lines = [f"  [{border_color}]{head}[/{border_color}]"]
    lines.append(f"  [{border_color}]{body_empty}[/{border_color}]")

    if title:
        title_padded = title.center(width - 2)
        lines.append(f"  [{border_color}]│{title_padded}│[/{border_color}]")
        lines.append(f"  [{border_color}]{body_empty}[/{border_color}]")
        lines.append(f"  [{border_color}]{foot}[/{border_color}]")
        lines.append(f"  [{border_color}]{body_empty}[/{border_color}]")

    for line in content_lines:
        full_line = content_color + line
        clean_line = strip_ansi(full_line)
        if len(clean_line) > width - 4:
            full_line = truncate_ansi(full_line, width - 6, "...")
            clean_line = strip_ansi(full_line)
        padded = full_line + ' ' * ((width - 2) - len(clean_line))
        lines.append(f"  [{border_color}]│{padded}│[/{border_color}]")

    lines.append(f"  [{border_color}]{body_empty}[/{border_color}]")
    lines.append(f"  [{border_color}]{foot}[/{border_color}]")

    return "\n".join(lines)


# ╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                    REGULAR CONSOLE UTILS                                                        ║
# ╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

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