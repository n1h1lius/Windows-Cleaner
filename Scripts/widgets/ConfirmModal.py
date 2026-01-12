from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical
import os


class ConfirmModal(ModalScreen[bool]):
    """
    Modal de confirmación profesional que devuelve:

    """
    CSS_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\css\\ConfirmModalStyle.css"

    def __init__(self, message: str, title: str = "Confirm Action"):
        super().__init__()
        self.message = message
        self.title_str = title

    def compose(self):
        yield Vertical(
            Label(self.title_str, classes="title"),
            Label(self.message, classes="message"),
            Horizontal(
                Button("Yes", id="yes", variant="success"),
                Button("No", id="no", variant="error"),
                classes="buttons",
            ),
            classes="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Cierra el modal y devuelve el resultado"""
        self.dismiss(event.button.id == "yes")