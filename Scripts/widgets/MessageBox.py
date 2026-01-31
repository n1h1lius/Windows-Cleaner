from textual.screen import ModalScreen
from rich.text import Text
from textual.widgets import Button, Label, RichLog
from textual.containers import Horizontal, Vertical, VerticalScroll
import os

class MessageBox(ModalScreen[bool]):
    """
    Regular MessageBox
    @param message: Message to show
    @param title: Title to show (Default "Title")
    @param mode: [normal, warning, error, success] (Default "normal")
    @param buttonName: Button text (Default "Accept")
    @param details: List of details to show (Default None)

    """
    CSS_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\css\\MessageBoxStyle.css"

    def __init__(self, message: str, title: str = None, mode: str = "normal", 
                 buttonName: str = "Accept", details: list = None):
        super().__init__()
        self.message = message
        self.title_str = title if title is not None else "INFORMATION" if mode == "normal" else mode.upper()
        self.mode = mode
        self.buttonName = buttonName
        self.details = details # Aquí recibimos la lista (readlines)

    def compose(self):
        with Vertical(classes="mb-dialog", id=f"mb-dialog-{self.mode}"):
            yield Label(self.title_str, classes=f"mb-title-{self.mode}")
            yield Label(self.message, classes="mb-message")
            
            # Si hay detalles, mostramos el RichLog con scroll
            if self.details:
                yield RichLog(highlight=True, markup=True, wrap=False, id="mb-details-area")

            with Horizontal(classes="mb-buttons"):
                yield Button(self.buttonName, classes=f"mb-button-{self.mode}")

    def on_mount(self) -> None:
        if not self.details:
            return

        log: RichLog = self.query_one("#mb-details-area", RichLog)
        log.clear()

        for line in self.details:
            # Preserve leading spaces (indentation), strip only trailing \n/\r
            cleaned = line.rstrip("\r\n")

            if not cleaned.strip():  # skip blank lines
                continue

            log.write(cleaned)
            log.write("\n")  # explicit newline after each line

        # After all writes: force recompute layout & scroll to end
        log.styles.align_horizontal = "left"
        log.styles.scrollbar_visibility = "visible"
        log.refresh(layout=True)
        log.scroll_end(animate=False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)