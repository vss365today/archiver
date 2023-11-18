import copy
import json
from datetime import date
from pathlib import Path
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

    # Create error handling pages
    print("Making error handling pages...")
    pages.make.page("404.html", data=pages.make.render("partials/errors/404.html", {}, env))
    pages.make.page("500.html", data=pages.make.render("partials/errors/500.html", {}, env))

    # Create the about page
    print("Making about page...")
    pages.make.page("about/index.html", data=pages.make.render("root/about.html", {}, env))

    # Create the root stats page
    print("Making root stats page...")
    stats_years = sorted(
        int(f.stem) for f in (Path() / "templates" / "stats" / "years").resolve().iterdir()
    )
    pages.make.page(
        "stats/index.html", data=pages.make.render("stats/index.html", {"years": stats_years}, env)
    )

    # Create the individual stats pages
    print("Making individual stats pages...")
    for year in stats_years:
        print(f"Making stats page for {year}...")
        pages.make.page(
            f"stats/{year}.html", data=pages.make.render(f"stats/years/{year}.html", {}, env)
        )

    # Make the root browse page
    print("Making root browse page...")
    try:
        archive_name = api.get("archive/")
    except HTTPError:
        archive_name = None
    pages.make.page(
        "browse/index.html",
        data=pages.make.render(
            "root/browse.html", {"years": prompt_years, "archive": archive_name}, env
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
                    "root/browse-year.html", {"year": year, "months": month_objs}, env
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
                        "root/browse-month.html",
                        {"date": date_obj, "month_prompts": prompts_in_month},
                        env,
                    ),
                )

    # Next, pull out the special One Year page, which is different from the rest
    print("Making One Year page...")
    one_year_prompt = api.get("prompts", "date", "2017-09-05")[0]
    render_opts = {
        "prompt": one_year_prompt,
        "previous": date.fromisoformat(one_year_prompt["navigation"]["previous"]),
        "next": date.fromisoformat(one_year_prompt["navigation"]["next"]),
    }
    pages.make.page(
        "view/2017-09-05.html", data=pages.make.render("root/one-year.html", render_opts, env)
    )

    print("Making individual view pages...")
    for day, prompts in all_prompts.items():
        # Skip One Year
        if day == "2017-09-05":
            continue

        # Create the required date object
        for prompt in prompts:
            prompt["date"] = date.fromisoformat(prompt["date"])

        print(f"Making view page for {day}...")
        render_opts = {
            "prompts": prompts,
            "previous": (
                date.fromisoformat(prompts[0]["navigation"]["previous"])
                if prompts[0]["navigation"]["previous"]
                else None
            ),
            "next": (
                date.fromisoformat(prompts[0]["navigation"]["next"])
                if prompts[0]["navigation"]["next"]
                else None
            ),
        }
        pages.make.page(
            f"view/{day}.html", data=pages.make.render("root/index.html", render_opts, env)
        )

    # Next, we are going to generate a site index, which is the newest prompt
    print("Making site index...")
    newest_prompts = all_prompts[max(all_prompts.keys())]
    render_opts = {
        "prompts": newest_prompts,
        "previous": (
            date.fromisoformat(newest_prompts[0]["navigation"]["previous"])
            if newest_prompts[0]["navigation"]["previous"]
            else None
        ),
        "next": None,
    }
    pages.make.page("index.html", data=pages.make.render("root/index.html", render_opts, env))

    # Create the search pages
    print("Making search and search results pages...")
    render_opts = {
        "hosts": [r["handle"] for r in api.get("hosts/")],
    }
    pages.make.page(
        "search/index.html", data=pages.make.render("search/search.html", render_opts, env)
    )
    pages.make.page(
        "search/results.html", data=pages.make.render("search/results.html", render_opts, env)
    )

    print("Making searchable content...")
    json_prompts = copy.deepcopy(all_prompts)

    # Add a pretty date field to each prompt
    for prompts in json_prompts.values():
        for p in prompts:
            p["date"] = p["date"].isoformat() if isinstance(p["date"], date) else p["date"]
            p["pretty_date"] = filters.format_date_pretty(p["date"])

    render_opts = {"prompts": json.dumps(json_prompts)}
    pages.make.page(
        "static/js/prompts.js", data=pages.make.render("search/prompts.js", render_opts, env)
    )

    # Provide a basic "how long did it run" message
    total_time = time() - start_time
    print(f"Total generation time: {duration(total_time)}")


if __name__ == "__main__":
    main()
