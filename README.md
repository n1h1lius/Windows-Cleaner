# Windows-Cleaner

Aquí tienes el contenido completo del **README.md** listo para copiar y pegar directamente en GitHub. Está formateado en Markdown válido, con badges, secciones claras, tablas, listas y bloques de código.

```markdown
# Windows Cleaner 🧹✨

**A safe, modern, and self-updating Windows cleanup tool with a beautiful terminal UI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org)
[![Textual](https://img.shields.io/badge/UI-Textual-6f42c1?logo=python&logoColor=white)](https://textual.textualize.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/n1h1lius/Windows-Cleaner?color=green)](https://github.com/n1h1lius/Windows-Cleaner/releases)

Windows Cleaner is a lightweight, open-source utility that intelligently removes temporary files, browser caches, and other junk from your Windows system — all from a pleasant terminal interface.

## Features

- Removes temp files from Windows system folders and popular apps (Chrome, Edge, Brave, Discord, Spotify…)
- **Age-based deletion** — only removes files older than a configurable threshold (default: 7 days)
- Beautiful **TUI** built with [Textual](https://textual.textualize.io) — real-time progress, confirmation modals, settings panel
- **Self-updating** from GitHub — automatic or manual, preserves user config via smart merge
- Modular design — legacy CLI mode + modern Textual UI coexist
- Run as admin for maximum cleaning power

## Requirements

- **Windows** 10 / 11
- **Python** 3.8+ (recommended: 3.12)
- Dependencies:
  ```bash
  pip install textual>=0.71.0 rich colorama requests
  ```

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/n1h1lius/Windows-Cleaner.git
   cd Windows-Cleaner
   ```

2. **(Recommended) Create virtual environment**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install textual rich colorama requests
   ```

4. **Run the cleaner**

   - Modern Textual UI (recommended):
     ```bash
     python main.py --main-menu
     ```

   - Direct cleaning (legacy mode):
     ```bash
     python main.py
     ```

   - Using batch wrappers (run as Administrator):
     ```batch
     cleaner.bat          REM → modern UI / main menu
     WindowsCleaner.bat   REM → legacy direct cleaning
     ```


## Development / Roadmap Ideas

- Persistent file logging (`cleaner.log`)


## License

MIT License — see [LICENSE](LICENSE)

## Author

Created with ❤️ by **@Opus_hund** (Marco Aurelio)  
https://github.com/n1h1lius

---

Enjoy a cleaner Windows! 🧹✨

Star the repo if you find it useful! ⭐
```
