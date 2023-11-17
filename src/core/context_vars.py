from datetime import date
from typing import Any

import sys_vars

from src.core.helpers import get_static_url


__all__ = ["ALL_CONTEXT_VARS"]

ALL_CONTEXT_VARS: dict[str, Any] = {
    "current_date": date.today(),
    "get_site_domain": sys_vars.get("DIST_DOMAIN"),
    "get_static_url": get_static_url,
    "nav_cur_page": lambda title, has: ("active" if has.strip() in title.strip().lower() else ""),
}
