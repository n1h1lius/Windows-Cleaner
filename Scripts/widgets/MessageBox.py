from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical
import os


class MessageBox(ModalScreen[bool]):
    """
    Regular MessageBox
    @param message: Message to show
    @param title: Title to show (Default "Title")
    @param mode: [normal, warning, error, success] (Default "normal")

    """
    CSS_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\css\\MessageBoxStyle.css"

    def __init__(self, message: str, title: str = None, mode: str = "normal", buttonName: str = "Accept"):
        super().__init__()
        self.message = message
        self.title_str = title if title is not None else "INFORMATION" if mode == "normal" else mode.upper()
        self.mode = mode
        self.buttonName = buttonName

    def compose(self):
        yield Vertical(
            Label(self.title_str, classes=f"mb-title-{self.mode}"),
            Label(self.message, classes="mb-message"),
            Horizontal(
                Button(self.buttonName, classes=f"mb-button-{self.mode}"),
                classes="mb-buttons",
            ),
            classes="mb-dialog", id=f"mb-dialog-{self.mode}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Cierra el modal y devuelve el resultado"""
        self.dismiss()