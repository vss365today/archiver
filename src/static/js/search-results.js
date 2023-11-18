// @ts-ignore
import { searchData } from "./prompts.js";

function renderPrompts(prompts) {
  let finalHTML = ['<div class="wrapper">'];
  prompts.forEach((prompt, i) => {
    let t = `<dl>
      <dd><a href="{{ url_for('root.view_date', d=prompt.date) }}">${prompt.word}</a></dd>
      <dt>${prompt.pretty_date}</dt>
      <dt>${prompt.host.handle}</dt>
    </dl>`;
    finalHTML.push(t);

    // Only five items per column
    if ((i + 1) % 5 === 0) {
      finalHTML.push('</div><div class="wrapper">');
    }
  });
  return finalHTML.join("");
}

function searchDates(query) {
  // Redirect to the view page for this date or 404 page if it's not recorded
  return () => {
    window.location = Object.keys(searchData).includes(query)
      ? `/view/${query}`
      : "/404";
  };
}

function searchHosts(query) {
  let foundPrompts = [];

  // Find the prompts from this host
  for (let prompts of Object.values(searchData)) {
    prompts.forEach((v) => {
      if (v.host.handle === query) {
        foundPrompts.push(v);
      }
    });
  }

  return foundPrompts;
}

function searchPrompts(query) {
  let foundPrompts = [];
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
    headline.querySelector(".header-total").textContent = r.length.toString();
    // @ts-ignore
    headline.querySelector(".header-plural").textContent = r.length ? "s" : "";

    let content = renderPrompts(r);
    document
      .querySelector(".page .prompts-here")
      ?.insertAdjacentHTML("afterbegin", content);
  } else if (searchType === "word") {
    let r = searchPrompts(searchQuery);
    // @ts-ignore
    headline.querySelector(".header-fast").textContent = r.length
      ? "times fast"
      : "time";

    let content = renderPrompts(r);
    document
      .querySelector(".page .prompts-here")
      ?.insertAdjacentHTML("afterbegin", content);
  } else if (searchType === "date") {
    searchDates(searchQuery)();
  }
});
