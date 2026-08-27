"""Small site tweaks, loaded as a local Sphinx extension via `sphinx: local_extensions:` in _config.yml.

1. Label the home-page link at the top of the sidebar "Homepage" instead of the page's H1
   (requires `html: home_page_in_navbar: true`). Change HOME_LABEL to use another label.
2. Remove the second search bar across the top of every page. pydata-sphinx-theme 0.17 fills
   in its `navbar_persistent` option with a search field unless the option is set explicitly,
   and Jupyter Book offers no clean way to set it in _config.yml without losing its other
   theme settings, so it is set here instead.
"""

HOME_LABEL = "Homepage"


def _set_home_title(app, pagename, templatename, context, doctree):
    context["root_title"] = HOME_LABEL


def _no_top_search_bar(app, config):
    # runs before the theme fills in its defaults (which happens at builder-inited)
    config.html_theme_options.setdefault("navbar_persistent", [])


def setup(app):
    app.connect("config-inited", _no_top_search_bar)
    # priority > 500 so this runs after sphinx-book-theme sets root_title
    app.connect("html-page-context", _set_home_title, priority=900)
    return {"parallel_read_safe": True, "parallel_write_safe": True}