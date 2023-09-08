'use strict';


function applyFilter(event, parameterName) {
  const prefix = getPrefixFromElement(event.target);
  const value = document.getElementById(`${prefix}-${parameterName}`).value;
  const newSearchParam = `${parameterName}=${value}`;
  const stringToReplace = new RegExp(`([\\?|&])${parameterName}=[^&]*(&)?`);

  if (stringToReplace.test(window.location.search)) {
    // $1 will be the preceding question mark or ampersand and $2 the ampersand after if any
    window.location.search = window.location.search.replace(stringToReplace, `$1${newSearchParam}$2`);
  } else {
    const joiner = window.location.search.includes("?") ? "&" : "?";
    window.location.search += `${joiner}${newSearchParam}`;
  }
}


function getPrefixFromElement(element) {
  if (!element) return;
  return element.getAttribute("data-input-filter-prefix") || getPrefixFromElement(element.parentElement);
}
