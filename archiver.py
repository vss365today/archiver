from time import time

from jinja2 import Environment, PackageLoader, select_autoescape

from src.core import pages
from src.helpers import api, filters


def main() -> None:
    start_time = time()

    # Start by creating a Jinja2 renderer
    env = Environment(
        loader=PackageLoader("archiver", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    # Register any custom filters
    for f in filters.ALL_FILTERS:
        env.filters[f.__name__] = f
    # Provide a basic "how long did it run" recording
    total_time = time() - start_time
    print(f"{total_time}=")


if __name__ == "__main__":
    main()
