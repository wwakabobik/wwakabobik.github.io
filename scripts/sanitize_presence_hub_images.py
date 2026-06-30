#!/usr/bin/env python3
"""Strip metadata and redact visible dates/times in chat & tracking screenshots."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, PngImagePlugin

DIR = Path(__file__).resolve().parents[1] / "content/assets/images/articles/iot/presence_hub"

# x0, y0, x1, y1, fill RGB
REDACT: dict[str, list[tuple]] = {
    "telegram_gift_dm.png": [
        (400, 0, 620, 44, (198, 218, 178)),
        (275, 112, 375, 151, (255, 255, 255)),
    ],
    "telegram_power_strip.png": [
        (360, 48, 660, 108, (198, 218, 178)),
        (360, 168, 660, 228, (198, 218, 178)),
        (100, 95, 270, 160, (255, 255, 255)),
        (820, 235, 1015, 320, (220, 248, 198)),
        (100, 385, 270, 460, (255, 255, 255)),
        (820, 485, 1015, 570, (220, 248, 198)),
        (100, 580, 270, 655, (255, 255, 255)),
    ],
    "usps_delivered.png": [
        (25, 165, 780, 255, (232, 245, 233)),
        (540, 145, 1010, 265, (255, 255, 255)),
    ],
}


def cover_region(im: Image.Image, spec: tuple) -> None:
    x0, y0, x1, y1, fill = spec
    ImageDraw.Draw(im).rectangle((x0, y0, x1, y1), fill=fill)


def strip_and_save(path: Path) -> None:
    im = Image.open(path)
    if path.suffix.lower() == ".gif":
        frames = []
        for frame in range(getattr(im, "n_frames", 1)):
            im.seek(frame)
            frames.append(im.convert("RGBA"))
        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=im.info.get("duration", 100),
            loop=im.info.get("loop", 0),
            optimize=True,
        )
        return

    if path.name in REDACT:
        im = im.convert("RGB")
        for spec in REDACT[path.name]:
            cover_region(im, spec)
    elif path.suffix.lower() in {".jpg", ".jpeg"}:
        im = im.convert("RGB")
    else:
        im = im.convert("RGBA")

    if path.suffix.lower() in {".jpg", ".jpeg"}:
        im.save(path, format="JPEG", quality=92, optimize=True)
    else:
        im.save(path, format="PNG", optimize=True, pnginfo=PngImagePlugin.PngInfo())


def main() -> None:
    for path in sorted(DIR.iterdir()):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif"}:
            continue
        strip_and_save(path)
        print(f"sanitized {path.name}")


if __name__ == "__main__":
    main()
