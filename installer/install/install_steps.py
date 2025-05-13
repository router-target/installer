import importlib.util
import re
import sys
from pathlib import Path

from installer.install.common.context import ctx
from installer.install.common.step_widget import Completed, StepWidget
from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal
from textual.events import Key
from textual.reactive import Reactive, reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import Button, Label, ProgressBar, Static

from .widgets_load import import_all

step_widgets = import_all()
print(step_widgets)


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

    current_step: int = -1

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("安装步骤", classes="title")
            for step in step_widgets:
                if self.current_step == step["step"]:
                    classes = "working"
                elif self.current_step > step["step"]:
                    classes = "done"
                else:
                    classes = "todo"

                yield Static(f"{step['step']+1}. {step['name']}", classes=classes)

    async def update(self, step: int) -> None:
        self.current_step = step
        # await self.recompose()


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

    current_step = -1
    steps: list[StepWidget] = []

    left_panel = LeftPanel(classes="left-panel")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for element in step_widgets:
            self.steps.append(element["widget"])

    def compose(self) -> ComposeResult:
        self.log.warning(f"render: {self.current_step} {self.widget.title}")
        with Horizontal():
            yield self.left_panel
            yield Static(" ", classes="divider")
            with Container(classes="right-panel"):
                yield self.widget

    @property
    def widget(self) -> StepWidget:
        index = int(self.current_step)
        if index >= len(self.steps):
            raise ValueError(f"index ({index}) out of range (0, {len(self.steps)})")

        widget = self.steps[index]
        if not widget:
            raise ValueError("widget is None")
        return widget

    async def on_mount(self):
        await self.next_step()

    @on(Completed)
    async def on_complete(self, event: Completed) -> None:
        self.log.warning(f"on_complete {event.success}")
        if event.success:
            await self.next_step()
        else:
            self.log("one step failed")
            self.dismiss(False)

    async def next_step(self) -> None:
        if self.current_step >= len(step_widgets) - 1:
            self.log("all steps completed")
            self.dismiss(True)
        else:
            self.log("run next step")
            self.current_step += 1

            await self.left_panel.update(self.current_step)
            await self.recompose()
