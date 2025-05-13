import importlib.util
import re
import sys
from pathlib import Path

from installer.install.common import step_widget
from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Button, Label, ProgressBar, Static

from .widgets_load import import_all

step_widgets = import_all()
print(step_widgets)
current_step = 0


class LeftPanel(Widget):
    DEFAULT_CSS = """
        .title {
            padding: 0 0 1 0;
        }
        .working {
            color: yellow;
        }
        .done {
            color: green;
        }
        .todo {
            color: grey;
        }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("安装步骤", classes="title")
            for step in step_widgets:
                if current_step == step["step"]:
                    classes = "working"
                elif current_step > step["step"]:
                    classes = "done"
                else:
                    classes = "todo"

                yield Static(f"{step['step']+1}. {step['name']}", classes=classes)


class InstallStepsScreen(Screen):
    DEFAULT_CSS = """
        .left-panel {
            width: 2fr;
            min-width: 20;
        }
        .divider {
            width: 1;
            height: 100%;
            background: green;
            margin: 0 1 0 0;
        }
        .right-panel {
            width: 7fr;
        }
    """

    def compose(self) -> ComposeResult:
        self.log.warning(f"render: {current_step} {step_widgets[current_step]['name']}")
        with Horizontal():
            yield LeftPanel(classes="left-panel")
            yield Static(" ", classes="divider")
            with Container(classes="right-panel"):
                yield step_widgets[current_step]["widget"]
