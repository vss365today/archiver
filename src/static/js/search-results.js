// @ts-ignore
import { searchData } from "./prompts.js";

function searchDates(query) {
  // Redirect to the view page for this date or 404 page if it's not recorded
  return () => {
    window.location = Object.keys(searchData).includes(query)
      ? `/view/${query}`
      : "/404";
  };
}

function searchHosts(query) {
  function render(p) {}

  let foundPrompts = {
    render,
    prompts: [],
  };

  // Find the prompts from this host
  for (let prompts of Object.values(searchData)) {
    prompts.forEach((v) => {
      if (v.host.handle === query) {
        foundPrompts.prompts.push(v);
      }
    });
  }

  return foundPrompts;
}

function searchPrompts(query) {
  function render(p) {}

  let foundPrompts = {
    render,
    prompts: [],
  };

}

document.addEventListener("DOMContentLoaded", function (e) {
  let qs = new URL(window.location.toString()).searchParams;
  let searchType = qs.get("type");
  let searchQuery = qs.get("query")?.toString();
  let headline = null;

  // Show the proper page headline depending on the search type
  if (searchType === "host") {
    headline = document.querySelector("h2.header-host");
  } else {
    headline = document.querySelector("h2.header-not-host");
  }
  headline?.classList.remove("hidden");

  // Display the query in the headline
  // @ts-ignore
  headline.querySelector(".header-query").textContent = searchQuery;

  // Determine the correct search function
  let searchFunction = (query) => {};
  if (searchType === "host") {
    let r = searchHosts(searchQuery);
    console.log(r);
    // @ts-ignore
    headline.querySelector(".header-total").textContent = r.prompts.length.toString();
    // @ts-ignore
    headline.querySelector(".header-plural").textContent = r.prompts.length ? "s": "";

  } else if (searchType === "word") {
    let r = searchPrompts(searchQuery);
    // @ts-ignore
    headline.querySelector(".header-fast").textContent = r.prompts.length ? "times fast": "time";

  } else if (searchType === "date") {
    searchDates(searchQuery)();
  }
});
