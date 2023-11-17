from datetime import date
from time import time
from typing import Any

from httpx import HTTPError
from jinja2 import Environment, PackageLoader, select_autoescape

from src.core import api, context_vars, filters, pages
from src.core.helpers import duration


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
    print("Creating all static files and folders...")
    prompt_years = api.get("browse", "years")["years"]
    prompt_years_months = [
        {str(year): api.get("browse", "years", str(year))["months"]} for year in prompt_years
    ]
    pages.make.dist(prompt_years_months)

    # Create the search page
    print("Making search page...")
    render_opts = {
        "page_title": "Search #vss365 prompts",
        "hosts": [r["handle"] for r in api.get("hosts/")],
    }
    pages.make.page("search.html", data=pages.make.render("search/search", render_opts, env))

    # Make the root browse page
    print("Making root browse page...")
    try:
        archive_name = api.get("archive/")
    except HTTPError:
        archive_name = None
    pages.make.page(
        "browse.html",
        data=pages.make.render(
            "root/browse", {"years": prompt_years, "archive": archive_name}, env
        ),
    )

    # We're going to be fetching all of the prompts shortly. Might as well be
    # a tiny be efficient and store them so we don't need to refetch it all
    all_prompts: dict[str, list[dict[str, Any]]] = {}

    for item in prompt_years_months:
        for year, months in item.items():
            month_objs = [date(int(year), m, 1) for m in months]

            # Create an index page for each year
            print(f"Making index for {year}...")
            pages.make.page(
                f"browse/{year}/index.html",
                data=pages.make.render(
                    "root/browse-year", {"year": year, "months": month_objs}, env
                ),
            )

            # Create an index for each month in each year
            for date_obj in month_objs:
                print(f"Making index for {year}-{date_obj.month}...")
                prompts_in_month = api.get("browse", str(year), str(date_obj.month))["prompts"]

                # Keep a record of each prompt for further rendering outside this cray cray loop
                for p in prompts_in_month:
                    if p["date"] not in all_prompts:
                        all_prompts[p["date"]] = []
                    all_prompts[p["date"]].append(p)

                # Actually, finally, make the dang page
                pages.make.page(
                    f"browse/{year}/{date_obj.month}/index.html",
                    data=pages.make.render(
                        "root/browse-month",
                        {"date": date_obj, "month_prompts": prompts_in_month},
                        env,
                    ),
                )

    # Next, we are going to generate a site index, which is the newest prompt
    print("Making site index...")
    newest_prompts = all_prompts[max(all_prompts.keys())]
    for p in newest_prompts:
        p["date"] = date.fromisoformat(p["date"])

    render_opts = {
        "prompts": newest_prompts,
        "previous": (
            date.fromisoformat(newest_prompts[0]["navigation"]["previous"])
            if newest_prompts[0]["navigation"]["previous"]
            else None
        ),
        "next": None,
    }
    pages.make.page("index.html", data=pages.make.render("root/index", render_opts, env))

    # Next, pull out the special One Year page, which is different from the rest
    print("Making One Year page...")
    one_year_prompt = api.get("prompts", "date", "2017-09-05")[0]
    del all_prompts["2017-09-05"]
    render_opts = {
        "prompt": one_year_prompt,
        "previous": date.fromisoformat(one_year_prompt["navigation"]["previous"]),
        "next": date.fromisoformat(one_year_prompt["navigation"]["next"]),
    }
    pages.make.page(
        "view/2017-09-05.html", data=pages.make.render("root/one-year", render_opts, env)
    )


    # Provide a basic "how long did it run" recording
    total_time = time() - start_time
    print(f"{total_time}=")


if __name__ == "__main__":
    main()
