# Course website (Jupyter Book)

A course site built with [Jupyter Book 1.x](https://jupyterbook.org) and the Sphinx Book Theme: left sidebar with Course Info + Lectures, right-hand page contents, `.md`/`.pdf` download buttons, and Jupyter notebooks rendered as pages. Hosted for free on GitHub Pages.

## Preview locally

```bash
pip install -r requirements.txt
jupyter-book build .
open _build/html/index.html        # or just open the file in a browser
```

Rebuild after every edit. If the sidebar looks stale, run `jupyter-book clean .` first.

## Where things live

| You want to change...          | Edit this                                   |
| ------------------------------ | ------------------------------------------- |
| Course title, author, logo     | `_config.yml` (top four lines), `_static/logo.svg` |
| Sidebar order and labels       | `_toc.yml`                                  |
| Home page (where/when/instructor) | `index.md`                               |
| Schedule table, office hours   | `Course_Info/Schedule.md`                   |
| Syllabus, textbook             | `Course_Info/Syllabus/Syllabus.md`, `Course_Info/Textbook.md` |
| A lecture page                 | `Lectures/NN-ShortName/index.md`            |
| Small style tweaks             | `_static/custom.css`                        |

## Add a lecture

1. Copy `Lectures/02-Topic/` to `Lectures/04-ShortName/` and edit `index.md`.
2. Drop slides (`.pdf`) or notebooks (`.ipynb`) into that folder. Link a PDF from `index.md` with `[Lecture 4 slides](Lec04-Slides.pdf)`; Jupyter Book copies it into the site and makes it downloadable.
3. Register it in `_toc.yml`:

   ```yaml
   - file: Lectures/04-ShortName/index
     title: "Day 04 (Th 9/10)"
     sections:                                   # optional: nest notebooks under the lecture
       - file: Lectures/04-ShortName/Lec04-Notebook
         title: "Jupyter Notebook"
   ```

4. Add a row to the table in `Course_Info/Schedule.md`.

Notebooks are published exactly as committed (`execute_notebooks: "off"`), so run them locally and save with outputs before pushing. Switch to `"auto"` in `_config.yml` if you would rather have GitHub run them at build time.

## Publish on GitHub Pages

1. Create a GitHub repo (e.g. `COURSE000-Fall2026`) and push this folder to the `main` branch.
2. In the repo: **Settings -> Pages -> Build and deployment -> Source: GitHub Actions**.
3. Every push to `main` now runs `.github/workflows/deploy.yml` and publishes to `https://USERNAME.github.io/COURSE000-Fall2026/`.
4. Put that URL in `html.baseurl` and the repo URL in `repository.url` inside `_config.yml`. Set `use_repository_button: true` if you want the GitHub button in the header.

Prefer to deploy by hand? `jupyter-book build . && ghp-import -n -p -f _build/html` pushes the site to a `gh-pages` branch (then set Pages -> Source to that branch).

## Useful MyST syntax

- Admonitions: `:::{note}`, `:::{warning}`, `:::{tip}` ... `:::`
- Math: `$inline$` and `$$ display $$`
- Downloadable file: `` {download}`file.pdf` `` or a plain link to the file
- Link to another page: `[Schedule](Course_Info/Schedule.md)` (relative to the current file)

Full reference: <https://jupyterbook.org/reference/cheatsheet.html>
