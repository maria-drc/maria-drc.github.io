# Current site style reference (WordPress.com, "Maywood" theme)

Documented from the live site's HTML/CSS on 2026-07-21, as a starting
reference for Phase 5 design discussion — not a spec to reproduce exactly.

## Typography

- **Single typeface throughout, no serif anywhere**: IBM Plex Sans
  (weights loaded: 300, 300 italic, 500, 500 italic, 700). Headings use
  700 (bold), body copy uses 300/400.
- No display/accent font — section titles, project titles, and body text
  all share the same grotesque sans.
- Type scale (theme presets): small 16.6px, normal/medium 20px,
  large 28.8px, huge 34.56px, x-large 42px. Body paragraph text sits at
  the "normal" 20px step — noticeably larger than a typical 16px web
  body, which is part of why the page reads as spacious/uncluttered even
  with dense project lists.

## Color

Near-monochrome. Color is used sparingly, almost never for decoration:

| Role | Hex | Usage |
|---|---|---|
| Background | `#FFFFFF` | page background, no off-white/tint |
| Body text | `#181818` | near-black, not pure black |
| Muted text | `#686868` | secondary/lighter text (not heavily used on homepage) |
| Primary / link color | `#897248` | muted brown-gold — used for links like "Read more" and "List of publications" |
| Secondary (rare accent) | `#C4493F` | muted brick red, barely visible on homepage, likely a button/hover color |

No gradients, no card backgrounds, no borders, no shadows anywhere in the
content area. All the visual color on the page comes from the embedded
research figures themselves (charts, network diagrams, screenshots) —
the surrounding page is deliberately quiet so the figures pop.

## Layout patterns

- **Header**: site title as plain text link (not a logo), tagline
  directly below it in regular weight. No styled nav bar — "About me /
  Podcasts & Talks / Blog" is literally a 3-column row of plain text
  links placed as the first thing in the page content, equal-width,
  no underline/pill/button styling until hovered.
- **Section dividers**: a plain `<hr>` rule, then a centered, bold `<h2>`
  ("Current Research", "Finished Research Projects"). No background
  tint, no icon — just a horizontal rule + centered heading as the only
  section-break device on the whole page.
- **Research sections are 3-column, not stacked**: each of the "Current
  Research" and "Finished Research Projects" sections is laid out as
  a 3-column grid (WordPress/Jetpack layout grid, 12 cols split into
  three 4-col columns) where **each column is one category**, and every
  project belonging to that category is stacked vertically inside its
  column (heading → description paragraph → figure → next project's
  heading → …, repeated down the column). This is different from the
  "grid of cards + full sections below" structure agreed for the new
  site — worth flagging explicitly for the Phase 5 conversation since
  it's the single biggest structural difference from the new spec.
- **Per-project block**: a bold lead-in phrase (often the project name,
  sometimes with an emoji or two 📈💸), then a plain paragraph of
  findings in regular weight, then an inline "Read more" link to the
  paper, then the figure image below at natural aspect ratio (no crop,
  no frame, no caption styling, no rounded corners/shadow).
- **Images**: always full column width, never cropped to a fixed
  aspect ratio, so column heights vary a lot project to project
  (this is what gives the "newspaper column" look in the screenshots
  rather than an even card grid).

## Spacing

- Theme spacing scale (rem): 0.44 / 0.67 / 1 / 1.5 / 2.25 / 3.38 / 5.06
- Default block gap: 24px between stacked blocks (headings, paragraphs,
  images) — this, combined with the larger 20px body font, is most of
  why the page feels airy despite having ~11 project entries on one
  page.

## Overall impression to carry into Phase 5

Restrained, editorial, text-first. No boxes/cards/borders/shadows
anywhere — hierarchy comes entirely from bold vs. regular weight, rule
dividers, and generous spacing. Color is reserved for links and for the
research figures themselves. This lines up well with the "clean and
academic... restrained, no gradients or animation" brief already agreed
for Phase 5 — the main open question for that phase isn't the palette or
type approach (both are worth keeping close to as-is), but whether to
keep the **3-columns-of-categories** layout or move to the **grid-of-cards
+ stacked full sections** layout specified for the new site. Something to
decide explicitly when we get to Phase 5, rather than defaulting either
way.
