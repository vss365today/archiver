// @ts-ignore
import * as searchData from "./prompts.js";


document.addEventListener("DOMContentLoaded", function(e) {
  let qs = new URL(window.location.toString()).searchParams;
  let search_type = qs.get("type");
  let headline = null;

    // Show the proper page headline depending on the search type
  if (search_type === "host") {
    headline = document.querySelector("h2.header-host");
  } else {
    headline = document.querySelector("h2.header-not-host");
  }
  headline?.classList.remove("hidden");

  // Display the query in the headline
  // @ts-ignore
  headline.querySelector(".header-query").textContent = qs.get("query");

  console.log(searchData.prompts);
  console.log(searchData.hosts);
});
