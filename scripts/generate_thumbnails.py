#!/usr/bin/env python3
"""Generate 600px-wide card thumbnails into images/thumbs/ from images/.

This is a curatorial step, not a mechanical one: dense multi-panel figures
need a crop (or a simplified region) chosen by eye rather than a blind
downscale, or they turn into unreadable soup at card size. Run by hand
whenever a project image changes or a new one is added — see CLAUDE.md.

    python3 scripts/generate_thumbnails.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images"
DST = ROOT / "images" / "thumbs"
THUMB_WIDTH = 600

# filename -> crop box (left, top, right, bottom) in ORIGINAL pixel
# coordinates, or None for a straight aspect-preserving downscale.
# See the Phase 3 check-in message for the reasoning behind each crop.
CROPS = {
    "llm-agents-financial-markets.jpg": (0, 0, 950, 736),
    "misinformation-resharing-vlms.jpeg": (0, 0, 1337, 300),
    "seshat-benchmark-results.png": None,
    "chatgpt-freelancer-skills-demand.png": None,
    "chatgpt-stackoverflow-impact.png": (1900, 0, 3695, 1541),
    "labour-market-network-model.png": (0, 478, 975, 1674),
    "us-decarbonisation-employment.jpg": (0, 0, 996, 828),
    "brazil-skill-mismatch.png": None,
    "great-resignation-reddit-topics.png": (0, 0, 676, 330),
    "covid-nyc-health-economy-tradeoff.png": None,
    "financial-contagion-multiplex-network.png": (0, 0, 1772, 1700),
    "machine-spirits-bubbles.png": None,
    "self-building-benchmarks-occupation-performance.png": None,
}


def make_thumb(filename, crop_box):
    src_path = SRC / filename
    img = Image.open(src_path)
    if img.mode in ("RGBA", "LA", "P"):
        # flatten transparency onto white — plain .convert("RGB") keeps
        # whatever RGB values sit under the alpha channel, often black
        img = img.convert("RGBA")
        flattened = Image.new("RGB", img.size, (255, 255, 255))
        flattened.paste(img, mask=img.split()[-1])
        img = flattened
    else:
        img = img.convert("RGB")
    if crop_box is not None:
        img = img.crop(crop_box)
    w, h = img.size
    new_h = round(h * THUMB_WIDTH / w)
    img = img.resize((THUMB_WIDTH, new_h), Image.LANCZOS)
    out_path = DST / (Path(filename).stem + ".jpg")
    img.save(out_path, "JPEG", quality=85)
    print(f"{out_path.name}: {img.size} (crop={'yes' if crop_box else 'no'})")


def main():
    DST.mkdir(parents=True, exist_ok=True)
    for filename, crop_box in CROPS.items():
        make_thumb(filename, crop_box)


if __name__ == "__main__":
    main()
