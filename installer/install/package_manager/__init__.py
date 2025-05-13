from pathlib import Path


def get_package_manager():
    for file in Path("/etc").glob("*-release"):
        print("--", file)
    raise NotImplementedError("Package manager detection is not implemented yet.")
