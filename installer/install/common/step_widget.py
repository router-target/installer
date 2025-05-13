from abc import ABC, ABCMeta, abstractmethod

from textual.widget import Widget


class CombinedMeta(ABCMeta, type(Widget)):
    pass


class StepWidget(ABC, Widget, metaclass=CombinedMeta):
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = ctx

    @property
    @abstractmethod
    def title(self) -> str:
        pass
