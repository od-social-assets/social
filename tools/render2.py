"""OneDirectory social graphics, design system v2 (layout set from ChatGPT reference designs, 24 Nov 2026)."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = '/usr/share/fonts/truetype/google-fonts/ofl/roboto/Roboto[wdth,wght].ttf'
NAVY = (30, 34, 45)
SUB = (52, 58, 72)
MUTED = (96, 104, 120)
GREEN = (9, 211, 76)
BLUE = (38, 132, 255)
SS = 2  # supersample factor for crisp edges

def F(size, weight='Bold'):
    f = ImageFont.truetype(FONT, int(size * SS)); f.set_variation_by_name(weight); return f

def tracked(d, xy, text, f, fill, track=-0.025):
    """Draw text with tight tracking (negative letter spacing), like modern SaaS display type."""
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

def canvas(w, h):
    W, H = w * SS, h * SS
    base = Image.new('RGB', (W, H), (255, 255, 255))
    g = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(g)
    d.ellipse((-W * 0.5, -H * 0.45, W * 0.55, H * 0.6), fill=(205, 245, 220))
    d.ellipse((W * 0.35, H * 0.25, W * 1.5, H * 1.4), fill=(212, 231, 252))
    g = g.filter(ImageFilter.GaussianBlur(min(W, H) * 0.2))
    img = Image.blend(base, g, 0.9)
    # faint flowing white lines, as on onedirectory.com
    ln = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(ln)
    for k in range(4):
        pts = [(x, H * (0.18 + 0.07 * k) + H * 0.06 * math.sin(x / W * math.pi * 1.3 + k)) for x in range(0, W + 10, 10)]
        ld.line(pts, fill=(255, 255, 255, 150), width=3 * SS)
    img.paste(ln, (0, 0), ln)
    return img

def finish(img, path):
    img = img.resize((img.width // SS, img.height // SS), Image.LANCZOS)
    img.save(path, optimize=True)

def logo(img, x, y, width, white=False):
    lg = Image.open('logo_white.png' if white else 'logo.png').convert('RGBA')
    r = width * SS / lg.width
    lg = lg.resize((int(lg.width * r), int(lg.height * r)), Image.LANCZOS)
    img.paste(lg, (int(x * SS), int(y * SS)), lg)

def card(img, box, radius=18):
    x0, y0, x1, y1 = [v * SS for v in box]
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0, y0 + 6 * SS, x1, y1 + 6 * SS), radius=radius * SS, fill=(30, 34, 45, 22))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * SS))
    img.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y0, x1, y1), radius=radius * SS, fill=(255, 255, 255), outline=(226, 232, 238), width=2 * SS)

def bar(d, x, y, w=120, h=8):
    d.rounded_rectangle((x * SS, y * SS, (x + w) * SS, (y + h) * SS), radius=h * SS // 2, fill=GREEN)

def pill(d, x, y, text, size=36, bg=NAVY, fg=(255, 255, 255)):
    f = F(size, 'SemiBold'); w = tw(d, text, f, -0.01) / SS
    h = size * 2.1
    d.rounded_rectangle((x * SS, y * SS, (x + w + size * 1.8) * SS, (y + h) * SS), radius=int(h * SS / 2), fill=bg)
    tracked(d, ((x + size * 0.9) * SS, (y + (h - size * 1.17) / 2) * SS), text, f, fg, -0.01)

M = 96  # outer margin

def stats():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    y = para(d, M * SS, 250 * SS, "What 16,267 employees did in their directory in 90 days", F(78, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
    bar(d, M, y / SS + 26)
    data = [("514,602", "directory searches"), ("395,450", "profile views"), ("54,894", "department views"), ("39,854", "org chart views")]
    gx = 24; cw = (W - 2 * M - gx) / 2; ch = 250; top = y / SS + 84
    for i, (n, lab) in enumerate(data):
        x0 = M + (i % 2) * (cw + gx); y0 = top + (i // 2) * (ch + gx)
        card(img, (x0, y0, x0 + cw, y0 + ch)); d = ImageDraw.Draw(img)
        tracked(d, ((x0 + 36) * SS, (y0 + 36) * SS), n, F(104, 'ExtraBold'), NAVY, -0.035)
        tracked(d, ((x0 + 38) * SS, (y0 + 168) * SS), lab, F(36, 'Regular'), SUB, -0.005)
    tracked(d, (M * SS, (top + 2 * ch + gx + 44) * SS), "65 organizations, 90 days to Aug 14, 2026. Source: OneDirectory usage study.", F(26, 'Regular'), MUTED, 0)
    finish(img, 'out2/directory-activity-chart.png')

def carousel():
    W, H = 1080, 1350
    slides = []
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300)
    bar(d, M, 300)
    y = para(d, M * SS, 350 * SS, "5 questions to ask before you buy employee directory software", F(108, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 50 * SS, "From our analysis of 15,000+ reviews across G2, Capterra and TrustRadius.", F(42, 'Regular'), SUB, (W - 2 * M - 40) * SS, 1.35, -0.005)
    pill(d, M, H - 230, "Swipe for all 5", 38)
    slides.append(img)
    qs = [
        ("Where does your people data live?", "Pick a tool that syncs from your source of truth, like Microsoft Entra ID, instead of one that runs on CSV imports and manual updates."),
        ("Directory, org chart, or both?", "Directories serve everyone looking someone up. Org chart tools serve HR planning. Decide who will use it most."),
        ("How will people get to it?", "If it's hard to open on a phone or missing from the tools people use all day, like Teams, they won't use it."),
        ("What does it cost at your headcount?", "Per-user fees grow with you. Price it at today's size and at the size you plan to reach, and get renewal pricing in writing."),
        ("Is the vendor stable?", "Check for layoffs, pricing changes and acquisitions. Ask about customer retention and renewal terms."),
    ]
    for i, (q, a) in enumerate(qs, 1):
        img = canvas(W, H); d = ImageDraw.Draw(img)
        logo(img, M, 100, 240)
        cnt = f"{i} / 5"; fc = F(30, 'Medium')
        tracked(d, ((W - M) * SS - tw(d, cnt, fc, 0), 106 * SS), cnt, fc, MUTED, 0)
        tracked(d, (M * SS, 270 * SS), f"{i:02d}", F(190, 'ExtraBold'), GREEN, -0.04)
        y = para(d, M * SS, 520 * SS, q, F(84, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
        bar(d, M, y / SS + 30)
        para(d, M * SS, y + 90 * SS, a, F(46, 'Regular'), SUB, (W - 2 * M - 20) * SS, 1.42, -0.005)
        slides.append(img)
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300)
    bar(d, M, 380)
    y = para(d, M * SS, 430 * SS, "The full guide covers pricing by tool type and what to test in a trial.", F(84, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
    para(d, M * SS, y + 50 * SS, "Link in the comments.", F(46, 'Regular'), SUB, (W - 2 * M) * SS, 1.4, -0.005)
    slides.append(img)
    out = []
    for n, s in enumerate(slides):
        p = f'out2/carousel-{n:02d}.png'; finish(s, p); out.append(Image.open(p).convert('RGB'))
    out[0].save('out2/five-questions-carousel.pdf', save_all=True, append_images=out[1:], resolution=150)

def minimap():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 210, "New in OneDirectory", 28, bg=GREEN, fg=NAVY)
    y = para(d, M * SS, 320 * SS, "Org chart mini map", F(100, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 20 * SS, "Find your way around big org charts.", F(44, 'Regular'), SUB, (W - 2 * M) * SS, 1.3, -0.005)
    # panel
    px0, py0, px1, py1 = M, 610, W - M, 1010
    card(img, (px0, py0, px1, py1), 24); d = ImageDraw.Draw(img)
    S = lambda v: int(v * SS)
    cx = (px0 + px1) / 2
    rows = [(1, 660), (5, 760), (9, 860), (12, 950)]
    pos = []
    for n, yy in rows:
        span = min(n * 70, px1 - px0 - 140); xs = [cx - span / 2 + (span / max(n - 1, 1)) * k if n > 1 else cx for k in range(n)]
        pos.append([(x, yy) for x in xs])
    for a, b in zip(pos, pos[1:]):
        for j, (x, yy) in enumerate(b):
            px, py = a[min(int(j * len(a) / len(b)), len(a) - 1)]
            d.line((S(px), S(py + 16), S(x), S(yy - 16)), fill=(200, 208, 220), width=S(3))
    hi = {(1, 3), (2, 5), (3, 7)}
    for r, row in enumerate(pos):
        for j, (x, yy) in enumerate(row):
            d.rounded_rectangle((S(x - 26), S(yy - 16), S(x + 26), S(yy + 16)), radius=S(6), fill=BLUE if (r, j) in hi else (232, 237, 244))
    vx0 = pos[2][4][0] - 50; vx1 = pos[3][8][0] + 50
    d.rounded_rectangle((S(vx0), S(820), S(vx1), S(985)), radius=S(10), outline=BLUE, width=S(6))
    tracked(d, (M * SS, (H - 120) * SS), "Drag or click to jump anywhere. People you find show up in blue.", F(30, 'Medium'), SUB, -0.005)
    tracked(d, (M * SS, (H - 76) * SS), "Available now for everyone in your directory.", F(26, 'Regular'), MUTED, 0)
    finish(img, 'out2/org-chart-mini-map.png')

def waves(W, H):
    img = Image.new('RGB', (W, H), (12, 70, 104)); d = ImageDraw.Draw(img)
    bands = [(9, 211, 76), (130, 222, 70), (0, 176, 150), (0, 148, 205), (38, 132, 255), (18, 98, 158), (225, 244, 110)]
    for i, col in enumerate(bands * 2):
        off = i * H / 9 - H * 0.25; amp = H * (0.08 + 0.03 * (i % 3))
        pts = [(x, off + amp * math.sin(x / W * math.pi * 1.6 + i * 0.9) + x * 0.35) for x in range(0, W + 20, 20)]
        d.polygon(pts + [(W, H * 2), (0, H * 2)], fill=col)
    return img.filter(ImageFilter.GaussianBlur(3 * SS))

def seasonal(name, l1, l2):
    W = H = 1200
    img = waves(W * SS, H * SS)
    card(img, (150, 330, 1050, 870), 36); d = ImageDraw.Draw(img)
    f1 = F(110, 'ExtraBold'); w1 = tw(d, l1, f1, -0.03)
    tracked(d, ((W * SS - w1) / 2, 420 * SS), l1, f1, NAVY, -0.03)
    f2 = F(44, 'Regular'); yy = 590
    for ln in wrap(d, l2, f2, 700 * SS, -0.005):
        w2 = tw(d, ln, f2, -0.005); tracked(d, ((W * SS - w2) / 2, yy * SS), ln, f2, SUB, -0.005); yy += 60
    logo(img, (W - 300) / 2, 770, 300)
    finish(img, f'out2/{name}.png')

if __name__ == '__main__':
    os.makedirs('out2', exist_ok=True)
    stats(); carousel(); minimap()
    pass  # seasonal('festive-season', 'Happy holidays', 'Wishing you a restful break and a great start to 2027.')
    pass  # seasonal('new-year', 'Happy New Year', "Here's to 2027.")
    print('done')

import random
def confetti(img, seed, area, n=46):
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    cols = [GREEN, BLUE, (150, 228, 180), (170, 205, 255), (30, 34, 45)]
    x0, y0, x1, y1 = area
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); s = rnd.choice([10, 14, 18, 24])
        c = rnd.choices(cols, weights=[4, 3, 3, 3, 1])[0]
        if rnd.random() < 0.6:
            d.rounded_rectangle((x * SS, y * SS, (x + s * 1.6) * SS, (y + s) * SS), radius=int(s * SS / 4), fill=c)
        else:
            d.ellipse((x * SS, y * SS, (x + s * 0.7) * SS, (y + s * 0.7) * SS), fill=c)

def festive_v2():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    confetti(img, 7, (80, 70, 1100, 300), 26); confetti(img, 9, (60, 900, 300, 1120), 8); confetti(img, 11, (900, 900, 1120, 1120), 8)
    d = ImageDraw.Draw(img)
    f1 = F(140, 'ExtraBold'); t = "Happy holidays"; w = tw(d, t, f1, -0.035)
    tracked(d, ((W * SS - w) / 2, 420 * SS), t, f1, NAVY, -0.035)
    bar(d, (W - 120) / 2, 610)
    f2 = F(46, 'Regular')
    for k, ln in enumerate(["From all of us at OneDirectory.", "See you in 2027."]):
        w2 = tw(d, ln, f2, -0.005); tracked(d, ((W * SS - w2) / 2, (660 + k * 64) * SS), ln, f2, SUB, -0.005)
    logo(img, (W - 300) / 2, 1040 - 40, 300)
    finish(img, 'out2/festive-season.png')

def newyear_v2():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    confetti(img, 21, (80, 60, 1100, 240), 24); confetti(img, 23, (60, 930, 300, 1120), 8); confetti(img, 25, (900, 930, 1120, 1120), 8)
    d = ImageDraw.Draw(img)
    f0 = F(44, 'SemiBold'); t0 = "Happy New Year"; w0 = tw(d, t0, f0, -0.01)
    tracked(d, ((W * SS - w0) / 2, 300 * SS), t0, f0, (6, 150, 55), -0.01)
    f1 = F(330, 'ExtraBold'); t = "2027"; w = tw(d, t, f1, -0.045)
    tracked(d, ((W * SS - w) / 2, 360 * SS), t, f1, NAVY, -0.045)
    bar(d, (W - 120) / 2, 760)
    f2 = F(44, 'Regular'); t2 = "From all of us at OneDirectory."; w2 = tw(d, t2, f2, -0.005)
    tracked(d, ((W * SS - w2) / 2, 810 * SS), t2, f2, SUB, -0.005)
    logo(img, (W - 300) / 2, 1000, 300)
    finish(img, 'out2/new-year.png')

festive_v2(); newyear_v2()
