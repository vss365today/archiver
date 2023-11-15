from datetime import date
from math import floor
from typing import Callable

import sys_vars


def current_year(_: str) -> str:
    return date.today().year


def get_site_domain(_: str) -> str:
    return sys_vars.get("SITE_DOMAIN")


ALL_FILTERS: list[Callable] = [
    current_year,
    get_site_domain,
]
