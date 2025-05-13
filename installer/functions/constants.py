from pathlib import Path

INSTALL_ROOT_DIR = Path("/usr/local/lib")
VENV_PATH = INSTALL_ROOT_DIR / "virtual_env"
PYTHON = VENV_PATH / "bin/python"

INSTALLER_ROOT = Path(__file__).parent.parent
