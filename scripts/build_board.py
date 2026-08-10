#!/usr/bin/env python3
"""Generate the homepage project board from taxonomy.yml + projects/*.qmd.

Regenerated on every `quarto render`/`quarto preview` (see `pre-render` in
_quarto.yml) — never hand-edit `_generated/board.qmd`, it's a build
artifact. To add a project to the board, add a projects/*.qmd file; to
change section order or names, edit taxonomy.yml. Nothing here needs
editing when either of those changes.

Project pages are NOT rendered (see `!projects/**` in _quarto.yml's
project.render list) — a project's title/thumbnail link straight to its
external `paper` (or the first entry of `papers`, for a project with more
than one linked paper), not to a page on this site. A project's qmd body
(write-up, figures) is therefore inert — kept only as source material, not
built into anything.
"""
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"
OUT_DIR = ROOT / "_generated"
OUT_FILE = OUT_DIR / "board.qmd"

FINISHED_SLUG = "finished-projects"

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
        # Click-through target for the title/thumbnail: the first (or only)
        # linked paper. A project always has `paper` or `papers` — see
        # projects/_template.qmd.
        fm["_href"] = fm.get("papers", [{}])[0].get("url") or fm.get("paper")
        projects.append(fm)
    return projects


def labels_attr(p):
    return escape("|".join(p.get("labels", [])))


def paper_link_html(p):
    # Most projects link a single paper via `paper:`. A project covering
    # several distinct papers (e.g. one card summarizing a body of work) can
    # instead set `papers:` — a list of {label, url} — to render one labelled
    # link per paper instead of a single generic one.
    papers = p.get("papers")
    if papers:
        return " ".join(
            f'<a class="project-card-paper-link" href="{escape(paper["url"])}">'
            f'Read the paper ({escape(paper["label"])})&nbsp;&rarr;</a>'
            for paper in papers
        )
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
    # Both anchors point at the same external paper as the inline paper
    # link(s) below (see load_projects's `_href`) — not at a page on this
    # site, since project pages aren't rendered at all.
    thumb = p.get("thumbnail") or p.get("image", "")
    thumb_class = "project-card-thumb"
    if p.get("thumbnail_compact"):
        thumb_class += " project-card-thumb--compact"
    thumb_html = (
        f"""
        <a class="project-card-link" href="{escape(p['_href'])}">
          <img class="{thumb_class}" src="/{thumb}" alt="{escape(p['title'])}" loading="lazy">
        </a>"""
        if thumb
        else ""
    )
    link = paper_link_html(p)
    desc = escape(p.get("description", ""))
    desc_html = f"{desc} {link}" if link else desc
    return f"""
      <div class="project-card" data-labels="{labels_attr(p)}">
        <a class="project-card-link" href="{escape(p['_href'])}">
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


def flat_board_html(visible):
    # Shown only while a tag filter is active (see styles.scss and
    # js/board-filter.js) instead of the grouped-by-category columns above —
    # a single flat grid, in the same overall order the columns list them
    # in, so that filtering never leaves category-shaped gaps: non-matches
    # are fully removed from flow here (unlike the grouped board and the
    # Other research grid) so remaining matches pack tightly, first into
    # column 1, then column 2, and so on.
    cards = "".join(card_html(p) for _, cat_projects in visible for p in cat_projects)
    return f"""
    <div class="project-board-flat">{cards}
    </div>"""


def main():
    tax = load_taxonomy()
    projects = load_projects()

    by_category = {}
    for p in projects:
        by_category.setdefault(p["category"], []).append(p)
    for cat_projects in by_category.values():
        cat_projects.sort(key=lambda p: p.get("order", DEFAULT_ORDER))

    # Columns that will actually render (non-finished, non-empty).
    visible = [
        (cat, by_category[cat["slug"]])
        for cat in tax["categories"]
        if cat["slug"] != FINISHED_SLUG and by_category.get(cat["slug"])
    ]

    board_columns = []
    for cat, cat_projects in visible:
        cards = "".join(card_html(p) for p in cat_projects)
        board_columns.append(f"""
    <div class="board-column">
      <h2 class="board-column-title">{escape(cat['name'])}</h2>
      <div class="board-cards">{cards}
      </div>
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
{flat_board_html(visible)}

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
