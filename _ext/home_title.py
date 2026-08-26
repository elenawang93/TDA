"""Label the home-page link at the top of the sidebar "Homepage" instead of the page's H1.

Loaded via `sphinx: local_extensions:` in _config.yml. Requires html.home_page_in_navbar: true.
"""

HOME_LABEL = "Homepage"


def _set_home_title(app, pagename, templatename, context, doctree):
    context["root_title"] = HOME_LABEL


def setup(app):
    # priority > 500 so this runs after sphinx-book-theme sets root_title
    app.connect("html-page-context", _set_home_title, priority=900)
    return {"parallel_read_safe": True, "parallel_write_safe": True}