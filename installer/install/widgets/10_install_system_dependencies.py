from ..common.step_widget import StepWidget


class ThisWidget(StepWidget):
    
    @property
    def title(self) -> str:
        return "安装系统依赖"

    def render(self):
        return "Hello, world!"

def wow():
    pass

a=123
