from typing import Any

import httpx
import sys_vars


__all__ = ["get"]


def __create_api_url(*args: str) -> str:
    """Construct a URL to the given API endpoint."""
    endpoint = "/".join(args)
    return f"{sys_vars.get('API_DOMAIN')}/v2/{endpoint}"


def get(*args: str, **kwargs: Any) -> dict | list:
    """Helper function for performing a GET request."""
    url = __create_api_url(*args)
    r = httpx.get(url, **kwargs)
    r.raise_for_status()
    return r.json() if r.text else {}
