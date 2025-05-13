import importlib.util
import re
import sys
from pathlib import Path
from typing import TypedDict

import textual.widgets
from installer.install.common.context import ctx
from textual.widget import Widget

from ..functions import die
from .common.step_widget import StepWidget


class StepWidgetMeta(TypedDict):
    widget: StepWidget
    name: str
    step: int


internal_widget_names = dir(textual.widgets)


def import_all():
    ret: list[StepWidgetMeta] = []
    index = 0
    for file in Path(__file__).parent.joinpath("widgets").glob("*.py"):
        try:
            lindex = index
            for obj in import_one(file):
                ret.append({"widget": obj, "name": obj.title, "step": index})
                index += 1

            if index == lindex:
                print(f"文件中没有找到任何 StepWidget\n  at {file}")
        except Exception as e:
            die(f"无法导入 {file}: {e}")
    return ret


def import_one(file: Path):
    clean_name = re.sub(r"^[0-9_]+", "", file.stem)
    name = f"installer.install.widgets.{clean_name}"
    # print("importing: ", name)
    spec = importlib.util.spec_from_file_location(name, str(file))
    if spec is None:
        die(f"找不到 {file} 的spec")

    foo = importlib.util.module_from_spec(spec)
    sys.modules[name] = foo
    spec.loader.exec_module(foo)

    for name in dir(foo):
        try:
            if name.startswith("_") or name in internal_widget_names:
                continue

            if name == "Widget":
                print(
                    f"警告: 文件中有一个名为 Widget 的类, 应该继承 StepWidget\n  at {file}"
                )
            if name == "StepWidget":
                continue

            CLS = getattr(foo, name)
            if not isinstance(CLS, type):
                continue
            if not issubclass(CLS, StepWidget):
                continue
            # if not hasattr(CLS, "title"):
            #     continue

            obj = CLS(ctx)

            yield obj
        except Exception as e:
            die(f"无法导入 {name}: {e}\n  at {file}")
