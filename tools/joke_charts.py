"""Joke charts for Greg's personal LinkedIn. Usage: python3 tools/joke_charts.py [name ...]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sketch import Sketch, INK, BLUE, RED

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media", "linkedin")


def out(date, name):
    os.makedirs(os.path.join(ROOT, date), exist_ok=True)
    return os.path.join(ROOT, date, name)


def listicles():
    s = Sketch(seed=11)
    s.axes("COMPANIES PUBLISHING “BEST OF” LISTS", "TIME", ysize=36)
    pts, x = [], 215
    while x < 760:
        pts.append((x, 930 + 12 * math.sin(x / 41) + random.uniform(-6, 6))); x += 20
    pts += [(778, 915), (792, 860), (800, 700), (806, 480), (812, 300), (820, 250)]
    s.line(pts, w=10, amp=1.0)
    s.text((480, 610), "AI STARTS", size=62, fill=BLUE, angle=4)
    s.text((485, 672), "PICKING WINNERS", size=62, fill=BLUE, angle=4)
    s.text((490, 734), "FROM THESE LISTS", size=62, fill=BLUE, angle=4)
    s.arrow([(620, 790), (700, 845), (772, 880)])
    s.text((495, 270), "NOW: EVERYONE", "mark", 50, RED, -3)
    s.text((500, 335), "(all ranking themselves #1)", size=44, fill=RED, angle=-3)
    s.arrow([(715, 260), (758, 257), (798, 254)], RED)
    s.save(out("2027-01-12", "listicles-joke-chart.png"))


def coin_flip():
    s = Sketch(seed=5)
    s.axes("DID CHATGPT NAME US?", "SAME QUESTION, NEW CHAT, AGAIN...", ysize=36)
    s.text((240, 330), "YES", "mark", 30); s.text((240, 880), "NO", "mark", 30)
    pattern = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    pts, x0, step = [], 230, 72
    for i, v in enumerate(pattern):
        x = x0 + i * step
        y = 330 if v else 930
        if v:
            pts += [(x - 16, 930), (x, y), (x + 16, 930)]
        else:
            pts.append((x, y + random.uniform(-4, 4)))
    s.line(pts, w=9, amp=1.0)
    peak = x0 + 2 * step
    s.text((peak + 260, 230), "THE ONE I SCREENSHOTTED", "mark", 40, RED, -2)
    s.arrow([(peak + 120, 255), (peak + 50, 280), (peak + 14, 318)], RED)
    s.text((555, 680), "every other time:", size=52, fill=BLUE, angle=3)
    s.text((552, 735), "not even mentioned", size=48, fill=BLUE, angle=3)
    s.arrow([(555, 780), (558, 850), (560, 912)])
    s.save(out("2027-01-06", "coin-flip-joke-chart.png"))


def impressions():
    s = Sketch(seed=21)
    s.axes("OUR BLOG IN GOOGLE", "28 DAYS", ysize=40)
    imp, clk, x = [], [], 215
    while x <= 1000:
        t = (x - 215) / 785
        imp.append((x, 930 - 640 * t ** 1.3 + random.uniform(-14, 14)))
        clk.append((x, 945 + random.uniform(-5, 5)))
        x += 25
    s.line(imp, w=9, amp=1.0)
    s.line(clk, fill=BLUE, w=9, amp=1.0)
    s.text((960, 190), "152K", "mark", 54)
    s.text((960, 245), "impressions", size=46)
    s.text((960, 890), "0.29% clicks", size=50, fill=BLUE)
    s.text((860, 690), "THIS GAP =", "mark", 42, RED, -3)
    s.text((865, 750), "image packs + AI Overview", size=44, fill=RED, angle=-3)
    s.text((865, 800), "slots nobody clicks", size=44, fill=RED, angle=-3)
    s.line([(650, 690), (650, 925)], RED, 4, 1.0)
    s.arrowhead((650, 690), (650, 750), RED, 4)
    s.arrowhead((650, 925), (650, 865), RED, 4)
    s.save(out("2026-12-04", "impressions-joke-chart.png"))


def detector():
    s = Sketch(seed=33)
    s.axes("HOW OFTEN AI CITED THE PAGE", "HOW “AI-WRITTEN” A DETECTOR SAID IT WAS", ysize=36)
    random.seed(4)
    dots = [(300, 880), (380, 800), (470, 900), (540, 760), (620, 870), (700, 820),
            (790, 900), (860, 780), (960, 880)]
    for x, y in dots:
        s.dot(x, y)
    s.dot(820, 300, 18)
    s.circle(820, 300, 52, 46)
    s.text((520, 230), "OUR MOST CITED PAGE", "mark", 42, RED, -2)
    s.text((520, 290), "(written with AI help)", size=48, fill=RED, angle=-2)
    s.arrow([(722, 296), (745, 300), (764, 302)], RED)
    s.text((560, 560), "correlation:", size=64, fill=BLUE, angle=4)
    s.text((560, 630), "basically zero", size=64, fill=BLUE, angle=4)
    s.save(out("2026-12-11", "detector-joke-chart.png"))


def copilot():
    s = Sketch(seed=41)
    s.axes("SHARE OF OUR COPILOT CITATIONS", "", ysize=36)
    base = 1000
    def bar(x0, x1, top, fill=None):
        s.line([(x0, base), (x0, top), (x1, top), (x1, base)], w=8, amp=1.2)
        for k in range(int(x0) + 18, int(x1), 26):
            s.line([(k, base - 8), (min(k + 60, x1 - 6), max(top + 8, base - 8 - (x1 - k) * 1.0))],
                   fill or (120, 120, 130), 3, 0.8) if False else None
        if fill:
            for yy in range(int(top) + 22, base, 22):
                s.line([(x0 + 10, yy), (x1 - 10, yy - 10)], fill, 3, 1.0)
    bar(300, 520, 200, (90, 90, 100))
    bar(720, 940, 1000 - 800 * 8.9 / 28.6, BLUE)
    s.text((410, 150), "28.6%", "mark", 54)
    s.text((830, 700), "8.9%", "mark", 54, BLUE)
    s.text((410, 1060), "one old Excel", size=50)
    s.text((410, 1110), "tutorial", size=50)
    s.text((830, 1060), "all our product", size=50, fill=BLUE)
    s.text((830, 1110), "pages combined", size=50, fill=BLUE)
    s.text((850, 400), "the pages we", "mark", 40, RED, -3)
    s.text((850, 455), "actually want cited", "mark", 40, RED, -3)
    s.arrow([(850, 500), (848, 580), (846, 640)], RED)
    s.save(out("2027-01-11", "copilot-joke-chart.png"))


def tiktok():
    s = Sketch(seed=8)
    s.axes("DAILY VIEWS", "TIME", ysize=44)
    fyp, srch, x = [], [], 215
    while x <= 1060:
        if x < 300:   y = 950 - (x - 215) * 0.4
        elif x < 560: y = 916 - 620 * ((x - 300) / 260) ** 1.4
        elif x < 690: y = 296 + random.uniform(-45, 45)
        elif x < 760: y = 296 + 640 * ((x - 690) / 70) ** 0.8
        else:         y = 945
        fyp.append((x, min(950, y + random.uniform(-6, 6))))
        srch.append((x, 905 + random.uniform(-6, 6) - (8 if x > 760 else 0)))
        x += 14
    s.line(fyp, w=10, amp=1.0)
    s.line(srch, fill=BLUE, w=8, amp=1.0)
    s.text((530, 195), "ALGORITHM: \u201cWE LOVE YOU\u201d", "mark", 38, RED, -2)
    s.arrow([(600, 225), (615, 245), (622, 268)], RED, 4)
    s.text((900, 360), "I STOP", "mark", 38, INK, -3)
    s.text((900, 405), "POSTING", "mark", 38, INK, -3)
    s.arrow([(820, 370), (760, 345), (708, 320)], INK, 4)
    s.text((925, 710), "ALGORITHM:", "mark", 34, RED, -3)
    s.text((925, 760), "\u201cwho?\u201d", size=58, fill=RED, angle=-3)
    s.text((925, 840), "search: \u201cstill here.\u201d", size=46, fill=BLUE, angle=-2)
    s.text((700, 1150), "(98.9% of today\u2019s views come from search)", size=38, fill=BLUE)
    s.save(out("tiktok", "tiktok-joke-chart.png"))

ALL = {"listicles": listicles, "coin_flip": coin_flip, "impressions": impressions,
       "detector": detector, "copilot": copilot, "tiktok": tiktok}

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        ALL[n]()
        print("rendered", n)
