from abc import ABC, ABCMeta, abstractmethod

from textual import on, work
from textual.events import Mount
from textual.message import Message
from textual.widget import Widget
from textual.worker import Worker, get_current_worker


class CombinedMeta(ABCMeta, type(Widget)):
    pass


class Completed(Message):
    def __init__(self, success: bool):
        super().__init__()
        self.success = success


class StepWidget(ABC, Widget, metaclass=CombinedMeta):
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = ctx

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    async def work(self) -> None:
        pass

    @on(Mount)
    def on_mount_run_work(self):
        if getattr(self, "work", None) is not None:
            self.log.info(f"run work {self.title}")
            self.run_worker(self.work, name=self.title, exclusive=True)

    @on(Worker.StateChanged)
    def on_worker_change(self, event: Worker.StateChanged) -> None:
        self.log(event)

    def dismiss(self, success=True):
        self.log.info(f"dismiss {self.title}")
        self.post_message(Completed(success))
