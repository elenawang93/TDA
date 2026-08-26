// Workaround for sphinx-book-theme 1.3 + pydata-sphinx-theme 0.17.
// The themes attach their sidebar click handlers to pydata's own header buttons, which the
// book theme hides with CSS, so the visible hamburger and "contents" buttons do nothing:
// on phones the sidebars can't be opened at all, and on desktop the hamburger doesn't
// collapse the sidebar. This forwards clicks from the visible buttons to the hidden ones.
document.addEventListener("DOMContentLoaded", function () {
  [
    [".bd-header-article .primary-toggle", ".bd-header .primary-toggle"],
    [".bd-header-article .secondary-toggle", ".bd-header .secondary-toggle"],
  ].forEach(function (pair) {
    var visible = document.querySelector(pair[0]);
    var hidden = document.querySelector(pair[1]);
    if (!visible || !hidden) return;
    visible.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      hidden.click();
    });
  });
});