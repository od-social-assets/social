"""LinkedIn visuals for Greg Bennett's personal posts.

Usage (set LI_THEME=dark or LI_THEME=light; default dark):
  python3 tools/li_card.py card OUT.png "Main line one|Main line two" "Subline"
  python3 tools/li_card.py carousel OUT.pdf "Slide 1 title|line" "Slide 2|line" ...

Card: 1080x1080 PNG. Carousel: PDF of 1080x1350 pages (one per argument),
plus OUT-cover.png (page 1) for the Buffer document thumbnail.
In every argument, "|" starts a new line; the first line of a carousel slide is
the headline, the rest is body text.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

import os
THEMES = {
    # dark: near-black background, warm white text, gold accent
    "dark": ("#111110", "#F2F0EA", "#C9C6BD", "#9A978F", "#E8B04A"),
    # light: off-white background, near-black text, high-contrast orange accent
    "light": ("#FAF8F3", "#111110", "#3A3936", "#6B6964", "#D9480F"),
}
BG, FG, SUB, MUTED, ACCENT = THEMES[os.environ.get("LI_THEME", "dark")]
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FOOTER = "Greg Bennett  ·  SEO & GEO, tested in public"
MARGIN = 90


def wrap(draw, text, font, width):
    out = []
    for para in text.split("|"):
        words, line = para.split(), ""
        for w in words:
            test = (line + " " + w).strip()
            if draw.textlength(test, font=font) <= width:
                line = test
            else:
                if line:
                    out.append(line)
                line = w
        out.append(line)
    return out


def fit(draw, text, path, start, width, max_lines):
    size = start
    while size > 36:
        f = ImageFont.truetype(path, size)
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 4
    f = ImageFont.truetype(path, size)
    return f, wrap(draw, text, f, width)


def page(w, h, head, body=None, counter=None):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    width = w - 2 * MARGIN
    hf, hl = fit(d, head, BOLD, 84, width, 5)
    lh = int(hf.size * 1.28)
    blines, bf = [], None
    if body:
        bf, blines = fit(d, body, REG, 48, width, 7)
    total = len(hl) * lh + (80 + len(blines) * int(bf.size * 1.4) if body else 0)
    y = max(MARGIN + 40, (h - total) // 2 - 40)
    for line in hl:
        d.text((MARGIN, y), line, font=hf, fill=FG)
        y += lh
    d.rectangle((MARGIN, y + 24, MARGIN + 160, y + 34), fill=ACCENT)
    y += 80
    for line in blines:
        d.text((MARGIN, y), line, font=bf, fill=SUB)
        y += int(bf.size * 1.4)
    ff = ImageFont.truetype(REG, 32)
    d.text((MARGIN, h - 110), FOOTER, font=ff, fill=MUTED)
    if counter:
        tw = d.textlength(counter, font=ff)
        d.text((w - MARGIN - tw, h - 110), counter, font=ff, fill=MUTED)
    return img


def main():
    kind, out, *args = sys.argv[1:]
    if kind == "card":
        head = args[0]
        body = args[1] if len(args) > 1 else None
        page(1080, 1080, head, body).save(out)
    elif kind == "carousel":
        pages = []
        for i, a in enumerate(args, 1):
            head, _, body = a.partition("|")
            pages.append(page(1080, 1350, head, body or None, f"{i}/{len(args)}"))
        pages[0].save(out, save_all=True, append_images=pages[1:], resolution=150)
        pages[0].save(out.rsplit(".", 1)[0] + "-cover.png")
    else:
        sys.exit("kind must be card or carousel")


if __name__ == "__main__":
    main()
