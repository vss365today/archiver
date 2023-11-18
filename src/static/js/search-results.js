// @ts-ignore
import * as searchData from "./prompts.js";

function searchDates(query) {
  let promptDates = Object.keys(searchData.prompts);

  // That date is not recorded
  if (!promptDates.includes(query)) {
    return () => {};
  }

  // Redirect to the view page for this date
  return () => { window.location = `/view/${query}` };
}
function searchHosts(query) {}
function searchPrompts(query) {}


document.addEventListener("DOMContentLoaded", function(e) {
  let qs = new URL(window.location.toString()).searchParams;
  let searchType = qs.get("type");
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
  headline.querySelector(".header-query").textContent = qs.get("query");

  // Determine the correct search function
  let searchFunction = null;
  if (searchType === "host") {
    searchFunction = searchHosts;
  } else if (searchType === "word") {
    searchFunction = searchPrompts;
  } else if (searchType === "date") {
    searchFunction = searchDates;
  } else {
    searchFunction = () => { () => {} };
  }

  console.log(searchData.hosts);
 searchFunction(qs.get("query"))();
});
