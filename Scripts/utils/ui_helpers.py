# -*- coding: utf-8 -*-
"""
Funciones de ayuda para formateo visual responsive en la consola
"""

import shutil
import re

from Scripts.config import *

ansi_escape = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

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