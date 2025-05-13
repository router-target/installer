from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Button

from .install.install_steps import InstallStepsScreen
from .install.welcome import HelloScreen


class TheApp(App):
    theme = "dracula"  # Default theme
    BINDINGS = [("c", "quit_application", "Quit")]

    CSS = """
    """

    def render(self):
        return ""

    @work
    async def on_mount(self):
        await self.push_screen_wait(HelloScreen())
        await self.push_screen_wait(InstallStepsScreen())

        self.exit(None, 0)


def main():
    app = TheApp()
    return app.run()
