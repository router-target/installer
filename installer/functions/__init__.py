# 此文件不能import非核心模块，且不能使用python3.11及以上语法

import sys
import typing
from pathlib import Path


def die(msg: str) -> typing.NoReturn:
    print(msg, file=sys.stderr)
    exit(1)


def is_newer(src: Path, dst: Path) -> bool:
    """
    Check if src is newer than dst.
    """
    if not dst.exists():
        return True
    return src.stat().st_mtime > dst.stat().st_mtime
