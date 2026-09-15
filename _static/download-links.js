// Make the "Download source file" menu items actually download.
// GitHub Pages serves .ipynb (and .md) as plain text, so a normal link opens the raw file
// in the browser. The same-origin `download` attribute forces a save dialog with the
// correct filename instead.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a.btn-download-source-button, a[href*="_sources/"]').forEach(function (a) {
    a.setAttribute("download", "");
    a.removeAttribute("target");
  });
});
