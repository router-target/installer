from asyncio import sleep

from textual.widgets import Log
from ..common.step_widget import StepWidget
from textual.worker import Worker, get_current_worker


class ThisWidget(StepWidget):
    output = Log()
    
    @property
    def title(self) -> str:
        return "安装系统依赖"

    def compose(self):
        yield self.output
        
    def line(self, l:str):
        self.output.write_line(l)
        print(l)
        
    async def work(self):
        self.line("Im Working!!!")
        await sleep(1)
        self.line("Im still Working!!!")
        await sleep(1)
        self.line("Im done!!!")
        
        self.dismiss()


class ThisWidget2(StepWidget):
    output = Log()
    
    @property
    def title(self) -> str:
        return "安装系统依赖2"

    def compose(self):
        yield self.output
        
    def line(self, l:str):
        self.output.write_line(l)
        print(l)
        
    async def work(self):
        self.line("Im Working!!!")
        await sleep(1)
        self.line("Im still Working!!!")
        await sleep(1)
        self.line("Im done!!!")
        
        self.dismiss()
