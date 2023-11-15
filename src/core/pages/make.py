import json
import shutil
from os import fspath
from pathlib import Path

import sys_vars
from jinja2 import Environment


def render(
    name: str,
    render_opts: dict,
    jinja: Environment,
) -> str:
    template = jinja.get_template(f"{name}.jinja2")
    return template.render(**render_opts)


def search_json(data: dict) -> None:
    json_file = sys_vars.get_path("DIST_PATH") / "js" / "search.js"
    str_data = json.dumps(data)

    # After we stringify the JSON data, append the following
    # ES Module export defaults so we can load it as
    # an ES module and search on the data way more easily.
    # This is D U M B but it works
    # TODO: This has been fixed and you can now import json files.
    # Do that instead
    str_data = f"export default {str_data}"
    json_file.write_text(str_data)


def page(*args: str, data: str = ""):
    (sys_vars.get_path("DIST_PATH").joinpath(*args)).write_bytes(data.encode())
