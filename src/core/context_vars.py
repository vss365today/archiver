from datetime import date
from pathlib import PurePath
from typing import Any

import sys_vars


__all__ = ["ALL_CONTEXT_VARS"]


def url_for(
    endpoint: str,
    *,
    _anchor: str | None = None,
    _method: str | None = None,
    _scheme: str | None = None,
    _external: bool | None = None,
    **values: Any,
) -> str:
    """Generate a URL to the given static file.

    Source: https://gist.github.com/le717/c87e87eb8419c6ba82a8c18c3e635f8f
    """
    # The `_method` param doesn't work in this context
    if _method:
        raise NotImplementedError("Standalone `url_for` does not support the `_method` parameter.")

    # If we're not given a URL scheme, default
    if _scheme is None:
        _scheme = "https"

    # We must a have file name to work with static files
    endpoint = endpoint.lower()
    if endpoint.lower() == "static":
        if "filename" not in values:
            raise KeyError("A `filename` parameter and path must be provided.")

        # Build up the relative URL to this static file, making sure
        # to prepend the leading slash
        final_url = (PurePath("static") / values.pop("filename")).as_posix()
        final_url = f"/{final_url}"
    else:
        mapping = {
            "root": {
                "index": "/",
                "browse": "/browse",
                "about": "/about",
                "view_date": "/view/{d}",
                "browse_by_year": "/browse/{year}",
                "browse_by_year_month": "/browse/{year}/{month}",
            },
            "search": {
                "index": "/search",
                "results": "/search/results",
                "do_search": "/search/results",
            },
            "stats": {
                "index": "/stats",
                "year": "/stats/{year}",
            },
        }

        # Handle non-static routing
        if "." in endpoint:
            root, page = endpoint.split(".")

            # We don't have that endpoint mapped
            if root not in mapping:
                raise NotImplementedError(f"Unsupported endpoint: {endpoint!r}")

            # Get the resulting URL
            final_url = mapping[root][page]

            # HACK way to determine if this URL has variable data. If so,
            # render it in and reset `values` so we don't end up with query strings too
            if "{" in final_url and "}" in final_url:
                final_url = final_url.format_map(values)
                values = {}

        # We don't support this non-static route
        else:
            raise NotImplementedError(f"Unsupported endpoint: {endpoint!r}")

    # If any values remaining, convert them into a query string.
    # Yes, I know supporting `values` and `_anchor` doesn't make sense
    # if only static files are supported, but I wanted to do it anyway
    if values:
        qs = "&".join(f"{k}={v}" for k, v in values.items())
        final_url = f"{final_url}?{qs}"

    # Add the URL anchor if it was provided
    if _anchor:
        final_url = f"{final_url}#{_anchor}"

    # As the very last step, check if this is supposed to be an external URL
    # and prefix the URL scheme and app domain
    if _external:
        url_domain = sys_vars.get("APP_DOMAIN")
        final_url = f"{_scheme}://{url_domain}{final_url}"
    return final_url


ALL_CONTEXT_VARS: dict[str, Any] = {
    "current_date": date.today(),
    "app_domain": sys_vars.get("APP_DOMAIN"),
    "nav_cur_page": lambda title, has: ("active" if has.strip() in title.strip().lower() else ""),
    "url_for": url_for,
}
