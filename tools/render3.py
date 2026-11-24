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

pass

def frame_shot(img, shot, box, radius=20):
    """Paste a product screenshot as a rounded, shadowed window."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sh = shot.resize((w * SS, h * SS), Image.LANCZOS)
    card(img, box, radius)
    mask = Image.new('L', sh.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sh.width, sh.height), radius=radius * SS, fill=255)
    img.paste(sh, (x0 * SS, y0 * SS), mask)
    ImageDraw.Draw(img).rounded_rectangle((x0 * SS, y0 * SS, x1 * SS, y1 * SS), radius=radius * SS, outline=(214, 222, 232), width=2 * SS)

def minimap_v2():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, "New in OneDirectory", 28, bg=GREEN, fg=NAVY)
    y = para(d, M * SS, 300 * SS, "Org chart mini map", F(100, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 14 * SS, "See the whole chart, and jump anywhere in one click.", F(42, 'Regular'), SUB, (W - 2 * M) * SS, 1.3, -0.005)
    full = Image.open('shots/orgchart-minimap.jpg').convert('RGB')
    shot = full.crop((64, 62, 1481, 757))
    sw = W - 2 * M; sh_h = int(shot.height * sw / shot.width)
    top = 560
    frame_shot(img, shot, (M, top, M + sw, top + sh_h))
    # zoomed callout of the mini map
    mm = full.crop((1268, 612, 1467, 743))
    cw = 340; chh = int(mm.height * cw / mm.width)
    cx1 = W - M + 30; cy1 = top + sh_h + 70
    box = (cx1 - cw, cy1 - chh, cx1, cy1)
    frame_shot(img, mm, box, 16)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((box[0] * SS, box[1] * SS, box[2] * SS, box[3] * SS), radius=16 * SS, outline=GREEN, width=5 * SS)
    tracked(d, (M * SS, (top + sh_h + 40) * SS), "Drag or click the map to move.", F(32, 'Medium'), NAVY, -0.005)
    tracked(d, (M * SS, (top + sh_h + 86) * SS), "Available now for everyone in your directory.", F(28, 'Regular'), MUTED, 0)
    finish(img, 'out2/org-chart-mini-map.png')

pass

def shot_card(name, shotfile, pill_text, title, sub, crop, foot=None):
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, pill_text, 28, bg=GREEN, fg=NAVY)
    y = para(d, M * SS, 300 * SS, title, F(92, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    y = para(d, M * SS, y + 30 * SS, sub, F(40, 'Regular'), SUB, (W - 2 * M) * SS, 1.3, -0.005)
    full = Image.open(shotfile).convert('RGB'); shot = full.crop(crop)
    sw = W - 2 * M; sh_h = int(shot.height * sw / shot.width)
    top = max(int(y / SS) + 50, 560)
    if top + sh_h > H - 70:
        sh_h = H - 70 - top
        shot = shot.crop((0, 0, shot.width, int(sh_h * shot.width / sw)))
    frame_shot(img, shot, (M, top, M + sw, top + sh_h))
    finish(img, f'out2/{name}.png')

def faq_card():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, "FAQ", 28, bg=GREEN, fg=NAVY)
    y = para(d, M * SS, 310 * SS, "How quickly can we start?", F(92, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    card(img, (M, y / SS + 60, W - M, y / SS + 530), 24); d = ImageDraw.Draw(img)
    yy = y / SS + 120
    bar(d, M + 56, yy)
    yy = para(d, (M + 56) * SS, (yy + 40) * SS, "Most customers have a working directory the same day the first sync finishes.", F(56, 'Bold'), NAVY, (W - 2 * M - 112) * SS, 1.2, -0.02)
    para(d, (M + 56) * SS, yy + 30 * SS, "Profiles sync from Microsoft Entra ID every hour, with no manual imports.", F(36, 'Regular'), SUB, (W - 2 * M - 112) * SS, 1.35, -0.005)
    tracked(d, (M * SS, (H - 96) * SS), "Try it free at onedirectory.com", F(30, 'Medium'), SUB, -0.005)
    finish(img, 'out2/faq-how-quickly.png')

def quote_card():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, "Customer story", 28, bg=GREEN, fg=NAVY)
    tracked(d, (M * SS, 250 * SS), "“", F(260, 'ExtraBold'), GREEN, 0)
    y = para(d, M * SS, 470 * SS, "I couldn't find anything that beat the price and functionality of OneDirectory. I highly recommend the tool.", F(68, 'Bold'), NAVY, (W - 2 * M) * SS, 1.22, -0.02)
    bar(d, M, y / SS + 40)
    tracked(d, (M * SS, (y / SS + 80) * SS), "Chris Clinger", F(40, 'Bold'), NAVY, -0.01)
    tracked(d, (M * SS, (y / SS + 132) * SS), "IT Enterprise Application Team Manager, Mountain View Hospital", F(30, 'Regular'), SUB, -0.005)
    finish(img, 'out2/quote-mountain-view.png')

def types_carousel():
    W, H = 1080, 1350
    slides = []
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300); bar(d, M, 300)
    y = para(d, M * SS, 350 * SS, "4 kinds of org chart software, and the job each one does", F(104, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 50 * SS, "From our analysis of 15,000+ reviews across G2, Capterra and TrustRadius.", F(42, 'Regular'), SUB, (W - 2 * M - 40) * SS, 1.35, -0.005)
    pill(d, M, H - 230, "Swipe for all 4", 38)
    slides.append(img)
    ts = [("Live directory with org chart", "Everyone can look people up and see reporting lines, kept current from your people data.", "$3,500 to $12,000 a year at 250 employees"),
          ("HRIS-connected chart", "Charts published from your HR system, for HR teams that need accurate, controlled org charts.", "$1,260 to $3,150 a year at 100 charted employees"),
          ("Planning platform", "Scenario modeling for reorgs and headcount planning.", "$15,000+ a year at 250 employees"),
          ("Chart builder", "One-off charts you draw and keep up to date by hand.", "Free to $600 a year")]
    for i, (t, a, c) in enumerate(ts, 1):
        img = canvas(W, H); d = ImageDraw.Draw(img)
        logo(img, M, 100, 240)
        cnt = f"{i} / 4"; fc = F(30, 'Medium'); tracked(d, ((W - M) * SS - tw(d, cnt, fc, 0), 106 * SS), cnt, fc, MUTED, 0)
        tracked(d, (M * SS, 270 * SS), f"{i:02d}", F(190, 'ExtraBold'), GREEN, -0.04)
        y = para(d, M * SS, 520 * SS, t, F(84, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
        bar(d, M, y / SS + 30)
        y = para(d, M * SS, y + 90 * SS, a, F(46, 'Regular'), SUB, (W - 2 * M - 20) * SS, 1.42, -0.005)
        card(img, (M, y / SS + 50, W - M, y / SS + 190), 18); d = ImageDraw.Draw(img)
        tracked(d, ((M + 36) * SS, (y / SS + 72) * SS), "Typical cost", F(28, 'Medium'), MUTED, 0)
        sz = 40
        while tw(d, c, F(sz, 'Bold'), -0.015) > (W - 2 * M - 72) * SS: sz -= 1
        tracked(d, ((M + 36) * SS, (y / SS + 112) * SS), c, F(sz, 'Bold'), NAVY, -0.015)
        slides.append(img)
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300); bar(d, M, 380)
    y = para(d, M * SS, 430 * SS, "Start with the job, then pick the tool.", F(92, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 50 * SS, "Pricing verified on vendor sites, Nov 9, 2026. Full guide in the comments.", F(42, 'Regular'), SUB, (W - 2 * M) * SS, 1.4, -0.005)
    slides.append(img)
    out = []
    for n, s in enumerate(slides):
        p = f'out2/types-{n:02d}.png'; finish(s, p); out.append(Image.open(p).convert('RGB'))
    out[0].save('out2/org-chart-types-carousel.pdf', save_all=True, append_images=out[1:], resolution=150)


def gains_card():
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    y = para(d, M * SS, 250 * SS, "Directory data gets better when you work on it", F(78, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
    bar(d, M, y / SS + 26)
    data = [("+37 pts", "employees with a manager recorded, now 79%"), ("+28 pts", "organizations that are directory-ready, now 61%"),
            ("+19 pts", "organizations with 80%+ phone coverage"), ("+10 pts", "organizations with 80%+ photo coverage")]
    gx = 24; cw = (W - 2 * M - gx) / 2; ch = 270; top = y / SS + 84
    for i, (n, lab) in enumerate(data):
        x0 = M + (i % 2) * (cw + gx); y0 = top + (i // 2) * (ch + gx)
        card(img, (x0, y0, x0 + cw, y0 + ch)); d = ImageDraw.Draw(img)
        tracked(d, ((x0 + 36) * SS, (y0 + 34) * SS), n, F(96, 'ExtraBold'), GREEN, -0.035)
        para(d, (x0 + 38) * SS, (y0 + 160) * SS, lab, F(32, 'Regular'), SUB, (cw - 70) * SS, 1.3, -0.005)
    tracked(d, (M * SS, (top + 2 * ch + gx + 40) * SS), "65 Microsoft 365 tenants, first sync vs Aug 2026. Source: OneDirectory study.", F(26, 'Regular'), MUTED, 0)
    finish(img, 'out3/data-gains.png')

def quote_card2(name, quote, who, role, fsize=68):
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, "Customer story", 28, bg=GREEN, fg=NAVY)
    tracked(d, (M * SS, 250 * SS), "“", F(260, 'ExtraBold'), GREEN, 0)
    y = para(d, M * SS, 470 * SS, quote, F(fsize, 'Bold'), NAVY, (W - 2 * M) * SS, 1.22, -0.02)
    bar(d, M, y / SS + 40)
    tracked(d, (M * SS, (y / SS + 80) * SS), who, F(40, 'Bold'), NAVY, -0.01)
    tracked(d, (M * SS, (y / SS + 132) * SS), role, F(30, 'Regular'), SUB, -0.005)
    finish(img, f'out3/{name}.png')

def faq_card2(name, q, a, sub):
    W = H = 1200
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 92, 300)
    pill(d, M, 200, "FAQ", 28, bg=GREEN, fg=NAVY)
    y = para(d, M * SS, 310 * SS, q, F(84, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    top = y / SS + 60
    # measure
    tmp = Image.new('RGB', (10, 10)); td = ImageDraw.Draw(tmp)
    yy = para(td, (M + 56) * SS, (top + 100) * SS, a, F(52, 'Bold'), NAVY, (W - 2 * M - 112) * SS, 1.2, -0.02)
    yy = para(td, (M + 56) * SS, yy + 30 * SS, sub, F(34, 'Regular'), SUB, (W - 2 * M - 112) * SS, 1.35, -0.005)
    card(img, (M, top, W - M, yy / SS + 56), 24); d = ImageDraw.Draw(img)
    bar(d, M + 56, top + 60)
    yy = para(d, (M + 56) * SS, (top + 100) * SS, a, F(52, 'Bold'), NAVY, (W - 2 * M - 112) * SS, 1.2, -0.02)
    para(d, (M + 56) * SS, yy + 30 * SS, sub, F(34, 'Regular'), SUB, (W - 2 * M - 112) * SS, 1.35, -0.005)
    tracked(d, (M * SS, (H - 96) * SS), "Try it free at onedirectory.com", F(30, 'Medium'), SUB, -0.005)
    finish(img, f'out3/{name}.png')

def fields_carousel():
    W, H = 1080, 1350
    slides = []
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300); bar(d, M, 300)
    y = para(d, M * SS, 350 * SS, "5 employee data fields that quietly break your org chart", F(100, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 50 * SS, "Check these before anyone opens the chart this year.", F(42, 'Regular'), SUB, (W - 2 * M - 40) * SS, 1.35, -0.005)
    pill(d, M, H - 230, "Swipe for all 5", 38)
    slides.append(img)
    fs = [("Manager", "A missing or wrong manager puts people under the wrong leader, and the reporting lines stop making sense."),
          ("Department", "Team names spelled differently across systems make grouping and filtering confusing."),
          ("Job title", "Old or vague titles hide who does what, so people guess who to contact."),
          ("Location", "Without office, region or time zone, distributed teams look flat and colleagues are harder to reach."),
          ("Profile photo", "Blank avatars make people harder to recognize and the directory feel impersonal.")]
    for i, (t, a) in enumerate(fs, 1):
        img = canvas(W, H); d = ImageDraw.Draw(img)
        logo(img, M, 100, 240)
        cnt = f"{i} / 5"; fc = F(30, 'Medium'); tracked(d, ((W - M) * SS - tw(d, cnt, fc, 0), 106 * SS), cnt, fc, MUTED, 0)
        tracked(d, (M * SS, 270 * SS), f"{i:02d}", F(190, 'ExtraBold'), GREEN, -0.04)
        y = para(d, M * SS, 520 * SS, t, F(96, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.12)
        bar(d, M, y / SS + 30)
        para(d, M * SS, y + 90 * SS, a, F(48, 'Regular'), SUB, (W - 2 * M - 20) * SS, 1.42, -0.005)
        slides.append(img)
    img = canvas(W, H); d = ImageDraw.Draw(img)
    logo(img, M, 100, 300); bar(d, M, 380)
    y = para(d, M * SS, 430 * SS, "Fix them at the source, in Microsoft Entra ID.", F(92, 'ExtraBold'), NAVY, (W - 2 * M) * SS, 1.1)
    para(d, M * SS, y + 50 * SS, "OneDirectory picks up the change on its next hourly sync. Full guide in the comments.", F(42, 'Regular'), SUB, (W - 2 * M) * SS, 1.4, -0.005)
    slides.append(img)
    out = []
    for n, s in enumerate(slides):
        p = f'out3/fields-{n:02d}.png'; finish(s, p); out.append(Image.open(p).convert('RGB'))
    out[0].save('out3/data-fields-carousel.pdf', save_all=True, append_images=out[1:], resolution=150)

import os; os.makedirs('out3', exist_ok=True)
gains_card()
quote_card2('quote-chesapeake', "If you are looking for a directory that allows for growth, is customizable, and leverages many systems - look no further.", "Jacob Glaser", "IT Specialist, Chesapeake Bank", 62)
faq_card2('faq-data-storage', "Where is our employee data stored?", "In Microsoft Azure, encrypted in transit and at rest.", "Hosted in the United States by default, with other regions available for enterprise customers.")
fields_carousel()
from PIL import Image as I
n=['data-gains.png','quote-chesapeake.png','faq-data-storage.png']
s=I.new('RGB',(1350,450),'white')
for i,x in enumerate(n): s.paste(I.open('out3/'+x).resize((450,450)),(i*450,0))
s.save('out3/_a.png')
n=['fields-%02d.png'%i for i in (0,1,4,6)]
s=I.new('RGB',(1440,450),'white')
for i,x in enumerate(n): s.paste(I.open('out3/'+x).resize((360,450)),(i*360,0))
s.save('out3/_b.png')
