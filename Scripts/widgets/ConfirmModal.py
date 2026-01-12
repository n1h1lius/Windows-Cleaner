from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical


class ConfirmModal(ModalScreen[bool]):
    """
    Modal de confirmación profesional que devuelve:
        - True  → usuario eligió "Sí"
        - False → usuario eligió "No"
    """

    CSS = """
    ConfirmModal {
        align: center middle;               /* Esto centra TODO el contenido del modal */
        background: $background 45%;        /* Dim suave y elegante */
    }

    ConfirmModal Vertical.dialog {
        width: auto;
        height: auto;
        min-width: 40;
        max-width: 70;
        max-height: 20;
        padding: 2 3;
        background: $panel;
        border: tall $primary;
        border-title-align: center;
        border-title-color: $text;
        box-sizing: border-box;
    }

    .dialog Label.title {
        width: 100%;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        color: $text;
    }

    .dialog Label.message {
        width: 100%;
        height: auto;
        text-align: center;
        margin-bottom: 2;
        color: $text-muted;
    }

    .dialog .buttons {
        width: 100%;
        height: auto;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }

    .dialog Button {
        width: 14;
        margin: 0 2;
    }

    .dialog Button#yes {
        background: $success;
    }

    .dialog Button#no {
        background: $error;
    }
    """

    def __init__(self, message: str, title: str = "Confirmar acción"):
        super().__init__()
        self.message = message
        self.title_str = title

    def compose(self):
        yield Vertical(
            Label(self.title_str, classes="title"),
            Label(self.message, classes="message"),
            Horizontal(
                Button("Sí", id="yes", variant="success"),
                Button("No", id="no", variant="error"),
                classes="buttons",
            ),
            classes="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Cierra el modal y devuelve el resultado"""
        self.dismiss(event.button.id == "yes")