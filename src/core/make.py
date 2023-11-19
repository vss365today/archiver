import shutil
from os import fspath
from pathlib import Path

import sys_vars
from jinja2 import Environment


__all__ = ["dist", "render", "page"]


def dist(dir_names: list[dict[str, list[int]]]) -> None:
    dist_path = sys_vars.get_path("DIST_PATH")

    # Create the prompts years and months folders
    for item in dir_names:
        for year, months in item.items():
            for month in months:
                (dist_path / "browse" / year / str(month)).mkdir(parents=True, exist_ok=True)

    # Create the site static files folders and files
    src_path = Path() / "src" / "static"
    shutil.copytree(fspath(src_path), fspath(dist_path / "static"), dirs_exist_ok=True)
    (dist_path / "static" / "images").mkdir(parents=True, exist_ok=True)

    # Make various static directories
    (dist_path / "about").mkdir(exist_ok=True)
    (dist_path / "search").mkdir(exist_ok=True)
    (dist_path / "stats").mkdir(exist_ok=True)
    (dist_path / "view").mkdir(exist_ok=True)


def render(name: str, render_opts: dict, jinja: Environment) -> str:
    return jinja.get_template(name).render(**render_opts)


def page(*args: str, data: str = "") -> None:
    (sys_vars.get_path("DIST_PATH").joinpath(*args)).write_bytes(data.encode())
