"""Greg Bennett personal LinkedIn visuals, built on the design system v2 in render2.py
(soft gradient canvas, tight-tracked Roboto display type, accent bar, numbered slides,
slide counter, Swipe pill, stat cards). Personal header instead of the OneDirectory logo,
personal accent instead of OneDirectory green, so posts never read as OneDirectory ads.

Usage:
  LI_THEME=light|dark python3 tools/li_card.py SPEC.json OUT_BASE

SPEC.json is either a quote card:
  {"kind": "card", "head": "Big line", "sub": "Optional smaller line"}
or a carousel (6 to 8 slides works best):
  {"kind": "carousel", "slides": [
     {"type": "cover", "head": "Hook headline", "sub": "Optional line", "swipe": "Swipe for the fix"},
     {"type": "point", "head": "Point headline", "body": "One or two sentences"},
     {"type": "stats", "head": "Headline", "stats": [["514,602", "label"], ...], "source": "Source line"},
     {"type": "end", "head": "Takeaway", "body": "The post's question"}]}

Writes OUT_BASE.png (card) or OUT_BASE.pdf + OUT_BASE-cover.png (carousel).
Point slides are numbered 01, 02, ... automatically.
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = '/usr/share/fonts/truetype/google-fonts/ofl/roboto/Roboto[wdth,wght].ttf'
SS = 2
M = 96

THEMES = {
    "light": dict(base=(255, 255, 255), glow1=(255, 222, 200), glow2=(214, 222, 255), line=(255, 255, 255, 150),
                  text=(30, 34, 45), sub=(52, 58, 72), muted=(96, 104, 120), accent=(240, 88, 32),
                  pill_bg=(30, 34, 45), pill_fg=(255, 255, 255), mono_fg=(255, 255, 255),
                  card=(255, 255, 255), card_edge=(226, 232, 238)),
    "dark": dict(base=(15, 17, 24), glow1=(78, 48, 20), glow2=(24, 40, 86), line=(255, 255, 255, 22),
                 text=(246, 244, 239), sub=(204, 208, 218), muted=(140, 146, 160), accent=(255, 178, 62),
                 pill_bg=(255, 178, 62), pill_fg=(15, 17, 24), mono_fg=(15, 17, 24),
                 card=(30, 33, 44), card_edge=(52, 57, 72)),
}
T = THEMES[os.environ.get("LI_THEME", "light")]


def F(size, weight='Bold'):
    f = ImageFont.truetype(FONT, int(size * SS)); f.set_variation_by_name(weight); return f


def tracked(d, xy, text, f, fill, track=-0.025):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track * f.size
    return x


def tw(d, text, f, track=-0.025):
    return sum(d.textlength(c, font=f) + track * f.size for c in text) - track * f.size


def wrap(d, text, f, maxw, track=-0.025):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tw(d, t, f, track) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, maxw, lead=1.15, track=-0.025):
    for ln in wrap(d, text, f, maxw, track):
        tracked(d, (x, y), ln, f, fill, track); y += f.size * lead
    return y


def fit_size(d, text, start, weight, maxw, max_lines, track=-0.025, floor=56):
    s = start
    while s > floor and len(wrap(d, text, F(s, weight), maxw * SS, track)) > max_lines:
        s -= 4
    return s


def canvas(w, h):
    W, H = w * SS, h * SS
    base = Image.new('RGB', (W, H), T['base'])
    g = Image.new('RGB', (W, H), T['base']); d = ImageDraw.Draw(g)
    d.ellipse((-W * 0.5, -H * 0.45, W * 0.55, H * 0.6), fill=T['glow1'])
    d.ellipse((W * 0.35, H * 0.25, W * 1.5, H * 1.4), fill=T['glow2'])
    g = g.filter(ImageFilter.GaussianBlur(min(W, H) * 0.2))
    img = Image.blend(base, g, 0.9)
    ln = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(ln)
    for k in range(4):
        pts = [(x, H * (0.18 + 0.07 * k) + H * 0.06 * math.sin(x / W * math.pi * 1.3 + k)) for x in range(0, W + 10, 10)]
        ld.line(pts, fill=T['line'], width=3 * SS)
    img.paste(ln, (0, 0), ln)
    return img


def header(img, y=100, counter=None, W=1080):
    """Personal mark: GB monogram, name and topic, in place of a company logo."""
    d = ImageDraw.Draw(img)
    r = 30
    d.ellipse((M * SS, y * SS, (M + 2 * r) * SS, (y + 2 * r) * SS), fill=T['accent'])
    fm = F(24, 'ExtraBold'); mono = "GB"
    tracked(d, ((M + r) * SS - tw(d, mono, fm, -0.02) / 2, (y + r - 15) * SS), mono, fm, T['mono_fg'], -0.02)
    tracked(d, ((M + 2 * r + 18) * SS, (y + 4) * SS), "Greg Bennett", F(30, 'SemiBold'), T['text'], -0.01)
    tracked(d, ((M + 2 * r + 18) * SS, (y + 38) * SS), "SEO & GEO, tested in public", F(22, 'Regular'), T['muted'], 0)
    if counter:
        fc = F(30, 'Medium')
        tracked(d, ((W - M) * SS - tw(d, counter, fc, 0), (y + 16) * SS), counter, fc, T['muted'], 0)


def bar(d, x, y, w=120, h=8):
    d.rounded_rectangle((x * SS, y * SS, (x + w) * SS, (y + h) * SS), radius=h * SS // 2, fill=T['accent'])


def pill(d, x, y, text, size=36):
    f = F(size, 'SemiBold'); w = tw(d, text, f, -0.01) / SS
    h = size * 2.1
    d.rounded_rectangle((x * SS, y * SS, (x + w + size * 1.8) * SS, (y + h) * SS), radius=int(h * SS / 2), fill=T['pill_bg'])
    tracked(d, ((x + size * 0.9) * SS, (y + (h - size * 1.17) / 2) * SS), text, f, T['pill_fg'], -0.01)


def card(img, box, radius=18):
    x0, y0, x1, y1 = [v * SS for v in box]
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0, y0 + 6 * SS, x1, y1 + 6 * SS), radius=radius * SS, fill=(0, 0, 0, 30))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * SS))
    img.paste(sh, (0, 0), sh)
    ImageDraw.Draw(img).rounded_rectangle((x0, y0, x1, y1), radius=radius * SS, fill=T['card'], outline=T['card_edge'], width=2 * SS)


def finish(img):
    return img.resize((img.width // SS, img.height // SS), Image.LANCZOS)


def quote_card(spec):
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    header(img, 92, W=W)
    size = fit_size(d, spec['head'], 110, 'ExtraBold', W - 2 * M, 4)
    y = para(d, M * SS, 330 * SS, spec['head'], F(size, 'ExtraBold'), T['text'], (W - 2 * M) * SS, 1.1, -0.03)
    bar(d, M, y / SS + 30)
    if spec.get('sub'):
        para(d, M * SS, y + 90 * SS, spec['sub'], F(46, 'Regular'), T['sub'], (W - 2 * M) * SS, 1.38, -0.005)
    return finish(img)


def carousel(spec):
    W, H = 1080, 1350
    slides, n, num = [], len(spec['slides']), 0
    for i, s in enumerate(spec['slides'], 1):
        img = canvas(W, H); d = ImageDraw.Draw(img)
        t = s['type']
        header(img, 100, None if t == 'cover' else f"{i} / {n}", W)
        maxw = W - 2 * M
        if t == 'cover':
            bar(d, M, 300)
            size = fit_size(d, s['head'], 112, 'ExtraBold', maxw, 5)
            y = para(d, M * SS, 350 * SS, s['head'], F(size, 'ExtraBold'), T['text'], maxw * SS, 1.1, -0.03)
            if s.get('sub'):
                para(d, M * SS, y + 50 * SS, s['sub'], F(42, 'Regular'), T['sub'], (maxw - 40) * SS, 1.35, -0.005)
            pill(d, M, H - 230, s.get('swipe', 'Swipe'), 38)
        elif t == 'point':
            num += 1
            tracked(d, (M * SS, 270 * SS), f"{num:02d}", F(190, 'ExtraBold'), T['accent'], -0.04)
            size = fit_size(d, s['head'], 84, 'ExtraBold', maxw, 3)
            y = para(d, M * SS, 520 * SS, s['head'], F(size, 'ExtraBold'), T['text'], maxw * SS, 1.12, -0.03)
            bar(d, M, y / SS + 30)
            if s.get('body'):
                para(d, M * SS, y + 90 * SS, s['body'], F(46, 'Regular'), T['sub'], (maxw - 20) * SS, 1.42, -0.005)
        elif t == 'stats':
            size = fit_size(d, s['head'], 78, 'ExtraBold', maxw, 3)
            y = para(d, M * SS, 270 * SS, s['head'], F(size, 'ExtraBold'), T['text'], maxw * SS, 1.12, -0.03)
            bar(d, M, y / SS + 26)
            gx = 24; cw = (maxw - gx) / 2; ch = 250; top = y / SS + 84
            for k, (val, lab) in enumerate(s['stats'][:4]):
                x0 = M + (k % 2) * (cw + gx); y0 = top + (k // 2) * (ch + gx)
                card(img, (x0, y0, x0 + cw, y0 + ch)); d = ImageDraw.Draw(img)
                vs = fit_size(d, val, 100, 'ExtraBold', cw - 60, 1, -0.035, 48)
                tracked(d, ((x0 + 36) * SS, (y0 + 36) * SS), val, F(vs, 'ExtraBold'), T['text'], -0.035)
                para(d, (x0 + 38) * SS, (y0 + 162) * SS, lab, F(32, 'Regular'), T['sub'], (cw - 70) * SS, 1.2, -0.005)
            if s.get('source'):
                para(d, M * SS, (top + 2 * ch + gx + 44) * SS, s['source'], F(26, 'Regular'), T['muted'], maxw * SS, 1.3, 0)
        elif t == 'end':
            bar(d, M, 380)
            size = fit_size(d, s['head'], 84, 'ExtraBold', maxw, 4)
            y = para(d, M * SS, 430 * SS, s['head'], F(size, 'ExtraBold'), T['text'], maxw * SS, 1.12, -0.03)
            if s.get('body'):
                para(d, M * SS, y + 50 * SS, s['body'], F(46, 'Regular'), T['sub'], maxw * SS, 1.4, -0.005)
        else:
            sys.exit(f"unknown slide type {t}")
        slides.append(finish(img))
    return slides


def main():
    spec_path, out = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    if spec['kind'] == 'card':
        quote_card(spec).save(out + '.png', optimize=True)
    else:
        s = carousel(spec)
        s[0].save(out + '-cover.png', optimize=True)
        s[0].save(out + '.pdf', save_all=True, append_images=s[1:], resolution=150)


if __name__ == '__main__':
    main()
