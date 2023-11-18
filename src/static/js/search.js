// TODO: Change this to a JSON import
// import { default as prompts } from "./prompts.js";


function findParentElement(element, selector) {
  // The desired element was not found on the page
  if (element === null) {
    return null;
  }

  // We found the desired element
  if (element.matches(selector)) {
    return element;

    // Keep searching for the element
  } else {
    return findParentElement(element.parentElement, selector);
  }
}

// Create the ability to toggle among search tabs
document.querySelector(".form-search-tabs")?.addEventListener("click", function (e) {
  // Find the clicked tab
  let ele = findParentElement(e.target, ".form-search-tabs .tab:not(.active)");
  if (ele) {
    // Switch the active tab
    document.querySelector(".form-search-tabs .tab.active")?.classList.remove("active");
    ele.classList.add("active");

    // Show the desired search form
    let searchType = ele.classList[1];
    document.querySelector(".form-search.active")?.classList.remove("active");
    document.querySelector(`.form-search.${searchType}`)?.classList.add("active");
  }
});

// Create a prettier select element
// @ts-ignore
tail.select(document.querySelector("#input-search-host"), {
  search: true,
  // placeholder: "ArthurUnkTweets",
});



const qForm = document.querySelector(".page-search form");
const qSearchQuery = document.querySelector(".search-input");
const qSearchResults = document.querySelector(".search-results");

// qForm?.addEventListener("submit", function(e) {
//   e.preventDefault();

//   // No blank or one character input
//   let input = qSearchQuery?.value.trim();
//   if (!input || input.length === 1) {
//     return false;
//   }

//   // Search for the input in the film data
//   let query = new RegExp(input, "i");
//   prompts.forEach(prompt => {
//     if (query.test(prompt.title)) {
//       let filmYear = prompt.date.split("-")[0];
//       let html = `<a href="films/${filmYear}/${prompt.id}.html">${prompt.title}</a>`;
//       qSearchResults?.insertAdjacentHTML("beforebegin", html);
//     }
//   });
// });
