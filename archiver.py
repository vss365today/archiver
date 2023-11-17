from time import time

from jinja2 import Environment, PackageLoader, select_autoescape

from src.core import api, context_vars, filters, pages


def main() -> None:
    start_time = time()

    # Start by creating a Jinja2 renderer
    env = Environment(
        loader=PackageLoader("archiver", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    # Register any custom filters and context vals
    env.filters.update(filters.ALL_FILTERS)
    env.globals.update(context_vars.ALL_CONTEXT_VARS)

    # Set up the prompt years and months directories in the dist folder
    prompt_years = api.get("browse", "years")["years"]
    prompt_years_months = [
        {str(year): api.get("browse", "years", str(year))["months"]} for year in prompt_years
    ]
    pages.make.dist(prompt_years_months)

    # Create the search page
    render_opts = {
        "page_title": "Search #vss365 prompts",
        "hosts": [r["handle"] for r in api.get("hosts/")],
    }
    pages.make.page("search.html", data=pages.make.render("search/search", render_opts, env))

    # Provide a basic "how long did it run" recording
    total_time = time() - start_time
    print(f"{total_time}=")


if __name__ == "__main__":
    main()
