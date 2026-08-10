#!/usr/bin/env python3
"""Generate the homepage project board from taxonomy.yml + projects/*.qmd.

Regenerated on every `quarto render`/`quarto preview` (see `pre-render` in
_quarto.yml) — never hand-edit `_generated/board.qmd`, it's a build
artifact. To add a project to the board, add a projects/*.qmd file; to
change section order or names, edit taxonomy.yml. Nothing here needs
editing when either of those changes.
"""
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"
OUT_DIR = ROOT / "_generated"
OUT_FILE = OUT_DIR / "board.qmd"

FINISHED_SLUG = "finished-projects"
SCHOLAR_URL = "https://scholar.google.com/citations?user=HwK5iiEAAAAJ&hl=en&oi=ao"

# Cards within a category sort by this optional frontmatter field (ascending),
# ties broken by filename (see load_projects — the list it returns is already
# filename-sorted, and Python's sort is stable, so untouched projects keep
# today's alphabetical order for free). Only set `order:` on a project when
# it needs to jump the queue for a specific reason (e.g. a new paper that
# should lead its column) — most projects should never need it.
DEFAULT_ORDER = 1000


def load_taxonomy():
    with open(ROOT / "taxonomy.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_projects():
    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.qmd")):
        if path.name == "_template.qmd":
            continue
        text = path.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        fm = yaml.safe_load(text[3:end])
        fm["_href"] = f"/projects/{path.stem}.html"
        projects.append(fm)
    return projects


def labels_attr(p):
    return escape("|".join(p.get("labels", [])))


def paper_link_html(p):
    if not p.get("paper"):
        return ""
    return (
        f'<a class="project-card-paper-link" href="{escape(p["paper"])}">'
        f"Read the paper&nbsp;&rarr;</a>"
    )


def card_html(p):
    # The paper link sits inline at the end of the description text, which
    # means the description can't be inside the card-wide title/thumbnail
    # <a> (HTML doesn't allow nesting an <a> inside another <a>) — so only
    # the title and thumbnail are wrapped in project-card-link, and the
    # description (plain text, not a link target) sits beside them.
    # The thumbnail <a> is omitted entirely for a project with no image
    # (image/thumbnail are both optional — see projects/_template.qmd).
    thumb = p.get("thumbnail") or p.get("image", "")
    thumb_html = (
        f"""
        <a class="project-card-link" href="{p['_href']}">
          <img class="project-card-thumb" src="/{thumb}" alt="{escape(p['title'])}" loading="lazy">
        </a>"""
        if thumb
        else ""
    )
    link = paper_link_html(p)
    desc = escape(p.get("description", ""))
    desc_html = f"{desc} {link}" if link else desc
    return f"""
      <div class="project-card" data-labels="{labels_attr(p)}">
        <a class="project-card-link" href="{p['_href']}">
          <h3 class="project-card-title">{escape(p['title'])}</h3>
        </a>
        <p class="project-card-desc">{desc_html}</p>
        {thumb_html}
      </div>"""


def filter_bar_html(projects):
    tags = sorted({l for p in projects for l in p.get("labels", [])})
    buttons = "".join(
        f'<button type="button" class="filter-tag" data-tag="{escape(t)}">{escape(t)}</button>'
        for t in tags
    )
    return f"""
    <p class="filter-bar-label">Or filter by topic</p>
    <div class="board-filter-bar" aria-label="Filter projects by tag">
      <button type="button" class="filter-tag is-active" data-tag="__all__">All</button>{buttons}
    </div>"""


def link_block_html():
    return f"""
      <div class="board-link-block">
        <p class="board-link-block-label">More</p>
        <a href="/publications.html">All publications &rarr;</a>
        <a href="{SCHOLAR_URL}">Google Scholar &rarr;</a>
      </div>"""


def main():
    tax = load_taxonomy()
    projects = load_projects()

    by_category = {}
    for p in projects:
        by_category.setdefault(p["category"], []).append(p)
    for cat_projects in by_category.values():
        cat_projects.sort(key=lambda p: p.get("order", DEFAULT_ORDER))

    # Columns that will actually render (non-finished, non-empty). The
    # shortest one gets a quiet link block at its foot instead of being
    # left to dangle — recomputed on every render, so it moves on its own
    # as project counts per category shift over time.
    visible = [
        (cat, by_category[cat["slug"]])
        for cat in tax["categories"]
        if cat["slug"] != FINISHED_SLUG and by_category.get(cat["slug"])
    ]
    shortest_slug = (
        min(visible, key=lambda pair: len(pair[1]))[0]["slug"] if visible else None
    )

    board_columns = []
    for cat, cat_projects in visible:
        cards = "".join(card_html(p) for p in cat_projects)
        extra = link_block_html() if cat["slug"] == shortest_slug else ""
        board_columns.append(f"""
    <div class="board-column">
      <h2 class="board-column-title">{escape(cat['name'])}</h2>
      <div class="board-cards">{cards}
      </div>{extra}
    </div>""")

    finished_cat = next(
        (c for c in tax["categories"] if c["slug"] == FINISHED_SLUG), None
    )
    finished_name = finished_cat["name"] if finished_cat else "Other research"
    finished_projects = by_category.get(FINISHED_SLUG, [])
    finished_cards = "".join(card_html(p) for p in finished_projects)

    html = f"""```{{=html}}
{filter_bar_html(projects)}

<div class="project-board">{''.join(board_columns)}
</div>

<section class="finished-section">
  <h2 class="finished-title">{escape(finished_name)}</h2>
  <div class="finished-grid">{finished_cards}
  </div>
</section>
```
"""

    OUT_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")
    print(
        f"Generated {OUT_FILE.relative_to(ROOT)}: "
        f"{len(board_columns)} columns, {len(finished_projects)} finished projects"
    )


if __name__ == "__main__":
    main()
