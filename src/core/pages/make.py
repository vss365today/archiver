import json
import shutil
from os import fspath
from pathlib import Path

import sys_vars
from jinja2 import Environment


__all__ = ["dist", "render", "page", "search_json"]


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


def search_json(data: dict) -> None:
    json_file = sys_vars.get_path("DIST_PATH") / "js" / "prompts.js"
    str_data = json.dumps(data)

    # After we stringify the JSON data, append the following
    # ES Module export defaults so we can load it as
    # an ES module and search on the data way more easily.
    # This is D U M B but it works
    # TODO: This has been fixed and you can now import json files.
    # Do that instead
    str_data = f"export default {str_data}"
    json_file.write_text(str_data)
