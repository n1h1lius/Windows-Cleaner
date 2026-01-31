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
    @param details: List of details to show. Intended for Logging purposes and such (Default None)
    @param wrapText: Wrap text from RichLog (Default False)
    @param minWidthForWrapping: Minimum width for wrapping the text (Default 100)

    """
    CSS_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\css\\MessageBoxStyle.css"

    def __init__(self, message: str, title: str = None, mode: str = "normal", 
                 buttonName: str = "Accept", details: list = None, 
                 wrapText: bool = False, minWidthForWrapping: int = 100):
        
        super().__init__()
        self.message = message
        self.title_str = title if title is not None else "INFORMATION" if mode == "normal" else mode.upper()
        self.mode = mode
        self.buttonName = buttonName
        self.details = details
        self.wrapText = wrapText
        self.minWidthForWrapping = minWidthForWrapping

    def compose(self):
        with Vertical(classes="mb-dialog", id=f"mb-dialog-{self.mode}"):
            yield Label(self.title_str, classes=f"mb-title-{self.mode}")
            yield Label(self.message, classes="mb-message")
            
            if self.details:
                yield Label("─────────────────────────────────────────────────────────────────────────────", classes=f"mb-separator-{self.mode}")
                yield RichLog(highlight=True, markup=True, wrap=self.wrapText, id="mb-details-area")
                yield Label("─────────────────────────────────────────────────────────────────────────────", classes=f"mb-separator-{self.mode}")

            with Horizontal(classes="mb-buttons"):
                yield Button(self.buttonName, classes=f"mb-button-{self.mode}")

    def on_mount(self) -> None:
        if not self.details:
            return

        log: RichLog = self.query_one("#mb-details-area", RichLog)
        log.auto_scroll = False
        log.styles.min_width = self.minWidthForWrapping

        log.clear()

        for line in self.details:
            cleaned = line.rstrip("\n")
            if cleaned.strip():  # skip completely empty lines
                log.write(cleaned + "\n")

        log.scroll_home(animate=False)
        log.refresh(layout=True, repaint=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(True)