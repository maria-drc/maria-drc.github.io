#!/usr/bin/env python3
"""Pre-render check: every project's category/labels must exist in taxonomy.yml.

Fails the build (non-zero exit) on the first unknown category or label so
typos are caught instead of silently creating a new tag. Run automatically
by Quarto (see `project.pre-render` in _quarto.yml); can also be run by hand:

    python3 scripts/validate_taxonomy.py
"""
import glob
import sys

import yaml

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent


def load_taxonomy():
    with open(ROOT / "taxonomy.yml", encoding="utf-8") as f:
        tax = yaml.safe_load(f)
    slugs = {c["slug"] for c in tax["categories"]}
    labels = set(tax["labels"])
    return slugs, labels


def load_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end])


def main():
    valid_slugs, valid_labels = load_taxonomy()
    errors = []

    project_files = sorted(
        p for p in glob.glob(str(ROOT / "projects" / "*.qmd"))
        if not p.endswith("_template.qmd")
    )

    for path_str in project_files:
        path = __import__("pathlib").Path(path_str)
        fm = load_frontmatter(path)
        if fm is None:
            errors.append(f"{path.name}: no YAML frontmatter found")
            continue

        category = fm.get("category")
        if category is None:
            errors.append(f"{path.name}: missing 'category' field")
        elif category not in valid_slugs:
            errors.append(
                f"{path.name}: unknown category '{category}' "
                f"(not in taxonomy.yml categories: {sorted(valid_slugs)})"
            )

        labels = fm.get("labels")
        if not labels:
            errors.append(f"{path.name}: missing or empty 'labels' field")
        else:
            for label in labels:
                if label not in valid_labels:
                    errors.append(
                        f"{path.name}: unknown label '{label}' "
                        f"(not in taxonomy.yml labels)"
                    )

    if errors:
        print("Taxonomy validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Taxonomy validation OK ({len(project_files)} projects checked).")


if __name__ == "__main__":
    main()
