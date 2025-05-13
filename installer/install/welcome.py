from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container
from textual.events import Key
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label, Static


class HelloScreen(Screen):
    DEFAULT_CSS = """
        HelloScreen {
            align: center middle;
        }
        
        #dialog {
            box_sizing: content-box;
            width: 40%;
            height: 5;
            padding: 2 5;
            background: black;
            border: double yellow;
            align: center middle;
        }
        .close {
            dock: bottom;
            width: 100%;
        }
    """

    def compose(self) -> ComposeResult:
        # yield HelloDialog()
        yield Container(
            Label("欢迎来到Linux Router安装程序！", classes="alert"),
            Button("OK!!", classes="close", variant="success"),
            id="dialog",
        )

    @on(Button.Pressed, ".close")
    def handle_button_click(self, event: Button.Pressed) -> None:
        self.log.info("is clicked ::: " + str(event.button))
        self.dismiss("wow!")

    # def on_mount(self) -> None:
    #     self.screen.styles.align = "center", "middle"
