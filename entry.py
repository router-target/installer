#!/usr/bin/env python3

from os import environ

from installer.functions import die, is_newer, constants


def ensure_python():
    import platform

    versions = platform.python_version_tuple()
    maj = int(versions[0])
    min = int(versions[1])
    if maj < 3 or (maj == 3 and min < 10):
        die("当前Python版本过低，请使用Python 3.10或更高版本")


def ensure_platform():
    import platform
    import sys

    if sys.platform != "linux" or platform.architecture()[0] != "64bit":
        die("此系统仅支持64位Linux系统.")


def create_environment_and_respawn():
    import subprocess
    import sys

    if constants.PYTHON.exists():
        print(f"虚拟环境存在 ({constants.VENV_PATH.as_posix()})")
    else:
        print(f"创建虚拟环境中... ({constants.VENV_PATH.as_posix()})")
        r = subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                "--prompt",
                "router.target",
                "--upgrade-deps",
                constants.VENV_PATH.as_posix(),
            ],
            check=False,
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        if r.returncode != 0:
            die("创建虚拟环境失败！")
        print(f"虚拟环境创建成功！")

    SRC = constants.INSTALLER_ROOT / "requirements.txt"
    DST = constants.VENV_PATH / "requirements.txt"
    if is_newer(SRC, DST):
        print("安装依赖……")
        r = subprocess.run(
            [
                constants.PYTHON.as_posix(),
                "-m",
                "pip",
                "install",
                "-r",
                SRC.as_posix(),
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if r.returncode != 0:
            print(r.stdout.strip(), file=sys.stderr)
            die("安装依赖失败！")
        DST.write_text(SRC.read_text())
    else:
        print("依赖已安装")

    # respawn
    print(f"+ {constants.PYTHON} {__file__} {' '.join(sys.argv[1:])}")

    proxy = ""
    no_proxy = ""
    for pname in ["http_proxy", "https_proxy", "all_proxy"]:
        proxy = environ.get(pname, "")
        if proxy:
            break
        proxy = environ.get(pname.upper(), "")
        if proxy:
            break

    if proxy:
        no_proxy = environ.get("no_proxy", environ.get("NO_PROXY", ""))
        print("使用代理:", proxy)
    else:
        print("不使用代理")

    r = subprocess.run(
        [
            constants.PYTHON.as_posix(),
            __file__,
            *sys.argv[1:],
        ],
        env={
            "http_proxy": proxy,
            "no_proxy": no_proxy,
            "_RESPAWNED_": "1",
            "VIRTUAL_ENV": constants.VENV_PATH.as_posix(),
        },
        check=False,
        stdin=sys.stdin,
        stdout=sys.stderr,
        stderr=sys.stderr,
    )
    sys.exit(r.returncode)


def main():
    current_venv = environ.get("VIRTUAL_ENV", None)
    if current_venv != constants.VENV_PATH.as_posix():
        ensure_python()
        ensure_platform()
        if environ.get("_RESPAWNED_", None) == "1":
            die(
                f"未知异常，当前环境变量VIRTUAL_ENV不正确\n\t应为: {constants.VENV_PATH.as_posix()}\n\t实际为: {current_venv}"
            )
        else:
            create_environment_and_respawn()
    else:
        from installer.main import main

        print("启动router.target安装")
        main()
        print("退出！")


print(f"当前Python: {constants.PYTHON.as_posix()} <{__name__}>")
if __name__ == "__main__":
    main()
else:
    die("这是可执行脚本。" + __name__)
