"""'AI up, ___ down' series charts, simple versions: one contrast, one punchline each.
Usage: python3 tools/ai_series.py [name ...]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sketch import Sketch, INK, BLUE, RED

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media", "linkedin", "ai-series")
GREY = (120, 120, 130)


def save(s, name):
    os.makedirs(OUT, exist_ok=True)
    s.save(os.path.join(OUT, name + ".png"))


def title(s, text):
    s.text((600, 80), text, "mark", 50, RED, -1)
    s.line([(170, 120), (1030, 117)], RED, 5, 1.2)


def source(s, text):
    s.text((600, 1150), text, size=34, fill=GREY)


def bar(s, x, top, w=260, base=960, fill=GREY):
    s.line([(x - w / 2, base), (x - w / 2, top), (x + w / 2, top), (x + w / 2, base)], w=8, amp=1.2)
    for yy in range(int(top) + 22, base - 6, 22):
        s.line([(x - w / 2 + 12, yy), (x + w / 2 - 12, yy - 9)], fill, 4, 0.8)


def baseline(s, base=960):
    s.line([(150, base), (1050, base)], w=8)


def two_bars(s, left, right, base=960, tall=300):
    """left/right = (label, value_text, height_fraction, colour)."""
    baseline(s, base)
    for x, (lab, val, frac, col) in [(370, left), (830, right)]:
        top = base - (base - tall) * frac
        bar(s, x, top, base=base, fill=col)
        s.text((x, top - 60), val, "mark", 72, col if col != GREY else INK)
        s.text((x, base + 60), lab, "mark", 48)


def arrow_big(s, x, y0, y1, col, w=16):
    s.line([(x, y0), (x, y1)], col, w, 1.0)
    d = 1 if y1 > y0 else -1
    s.line([(x - 60, y1 - d * 60), (x, y1), (x + 60, y1 - d * 60)], col, w, 1.0)


def stack_overflow():
    s = Sketch(seed=1)
    title(s, "AI UP, STACK OVERFLOW DOWN")
    s.text((600, 190), "new questions asked in a year", size=52, fill=GREY)
    two_bars(s, ("2022", "1.34M", 1.0, GREY), ("2025", "109K", 0.08, RED), tall=350)
    s.text((830, 620), "-92%", "mark", 110, RED, -5)
    source(s, "Stack Exchange Data Explorer")
    save(s, "01-stack-overflow")


def google_ctr():
    s = Sketch(seed=2)
    title(s, "AI UP, GOOGLE CLICKS DOWN")
    s.text((600, 190), "clicks on the #1 result", size=52, fill=GREY)
    s.text((600, 245), "when an AI Overview shows up", size=52, fill=GREY)
    two_bars(s, ("2023", "7.3%", 1.0, GREY), ("2025", "1.6%", 0.22, RED), tall=400)
    source(s, "Ahrefs, 150,000 keywords")
    save(s, "02-google-ctr")


def glue():
    s = Sketch(seed=3)
    title(s, "AI UP, COMMON SENSE DOWN")
    x0, y0, x1, y1 = 220, 190, 980, 1060
    s.line([(x0, y0), (x1, y0 + 6), (x1 - 4, y1), (x0 + 4, y1 - 4), (x0, y0)], INK, 7, 1.4)
    s.text((600, 290), "PIZZA", "mark", 90)
    s.text((600, 375), "(recipe by Google's AI, 2024)", size=46, fill=GREY)
    for t, yy in [("dough", 500), ("tomato sauce", 610), ("cheese", 720)]:
        s.line([(310, yy), (330, yy + 20), (365, yy - 24)], BLUE, 7, 0.8)
        s.text((600, yy), t, size=70)
    s.line([(310, 860), (330, 880), (365, 836)], RED, 7, 0.8)
    s.text((600, 860), "glue", "mark", 96, RED)
    s.circle(600, 860, 170, 85)
    s.text((600, 975), "(so the cheese sticks)", size=50, fill=RED)
    source(s, "confirmed real by Google, May 2024")
    save(s, "03-glue-on-pizza")


def reddit():
    s = Sketch(seed=4)
    title(s, "AI UP, REDDIT VISITS DOWN")
    arrow_big(s, 370, 820, 360, BLUE)
    s.text((370, 290), "+39%", "mark", 100, BLUE)
    s.text((370, 900), "Google sends", size=56, fill=BLUE)
    s.text((370, 960), "you to Reddit", size=56, fill=BLUE)
    s.text((370, 1030), "2023-24", "mark", 40, GREY)
    arrow_big(s, 830, 360, 820, RED)
    s.text((830, 290), "-13%", "mark", 100, RED)
    s.text((830, 900), "Google answers", size=56, fill=RED)
    s.text((830, 960), "for Reddit", size=56, fill=RED)
    s.text((830, 1030), "2025-26", "mark", 40, GREY)
    source(s, "Similarweb visit estimates")
    save(s, "04-reddit")


def please():
    s = Sketch(seed=5)
    title(s, "AI UP, MANNERS... EXPENSIVE")
    base = 960
    baseline(s, base)
    bar(s, 370, 720, base=base, fill=BLUE)
    s.text((370, 640), "$10M+", "mark", 72, BLUE)
    s.text((370, 1020), "saying please", size=52)
    s.text((370, 1075), "to ChatGPT", size=52)
    s.line([(700, base), (700, 150)], w=8, amp=1.2)
    s.line([(960, base), (960, 150)], w=8, amp=1.2)
    for yy in range(172, base - 6, 22):
        s.line([(712, yy), (948, yy - 9)], RED, 4, 0.8)
    s.text((830, 1020), "not saying please", size=52)
    s.text((830, 1075), "when AI takes over", size=52)
    s.text((1080, 520), "?", "mark", 120, RED, -8)
    source(s, "Sam Altman: “tens of millions of dollars well spent”")
    save(s, "05-please-thank-you")


def certainly():
    s = Sketch(seed=6)
    title(s, "AI UP, PROOFREADING DOWN")
    s.text((600, 230), "The first line of a published", size=56, fill=GREY)
    s.text((600, 290), "science paper, 2024:", size=56, fill=GREY)
    s.line([(130, 400), (1070, 405), (1068, 820), (132, 815), (130, 400)], INK, 6, 1.2)
    s.text((600, 500), "“Certainly, here is", size=84)
    s.text((600, 600), "a possible introduction", size=84)
    s.text((600, 700), "for your topic:”", size=84)
    s.circle(500, 495, 180, 62)
    s.text((600, 940), "someone forgot to delete", "mark", 52, RED, -2)
    s.text((600, 1005), "the ChatGPT part", "mark", 52, RED, -2)
    save(s, "06-certainly")


def chegg():
    s = Sketch(seed=7)
    title(s, "AI UP, HOMEWORK HELP DOWN")
    s.text((600, 190), "Chegg share price", size=56, fill=GREY)
    def y(p): return 960 - p / 20 * 620
    pts, x = [], 170
    while x < 560:
        pts.append((x, y(18.4 + random.uniform(-0.3, 0.3)))); x += 18
    pts += [(580, y(18.71)), (620, y(13)), (650, y(9.5))]
    x = 670
    while x <= 1040:
        pts.append((x, y(9 + random.uniform(-0.2, 0.2)))); x += 18
    s.line(pts, w=12, amp=1.0)
    s.text((360, y(18.71) - 70), "$18.71", "mark", 64)
    s.text((860, y(9) + 80), "$9", "mark", 64)
    s.text((860, 470), "-49%", "mark", 120, RED, -4)
    s.text((860, 570), "in ONE day", size=62, fill=RED, angle=-4)
    s.text((600, 1060), "the day Chegg blamed ChatGPT (May 2023)", size=44, fill=INK)
    save(s, "07-chegg")


def em_dash():
    s = Sketch(seed=8)
    title(s, "AI UP, EM DASHES UP")
    s.line([(420, 230), (780, 233)], INK, 26, 0.6)
    s.text((600, 300), "the em dash, on the web", size=52, fill=GREY)
    two_bars(s, ("2023", "1x", 0.5, GREY), ("2026", "2x", 1.0, RED), tall=470)
    source(s, "Pew Research Center")
    save(s, "08-em-dash")


def linkedin_slop():
    s = Sketch(seed=9)
    title(s, "AI UP, ORIGINAL THOUGHT DOWN")
    s.text((600, 190), "long LinkedIn posts that look AI-written", size=50, fill=GREY)
    two_bars(s, ("2024", "~50%", 0.5 / 0.85, GREY), ("2026", "81%", 0.812 / 0.85, RED))
    source(s, "Originality.ai")
    save(s, "09-linkedin-slop")


def pickleball():
    s = Sketch(seed=10)
    title(s, "AI UP, PICKLEBALL UP")
    s.line([(180, 960), (1060, 960)], w=8)
    s.line([(200, 900), (450, 760), (700, 580), (950, 380), (1040, 330)], BLUE, 12, 1.2)
    s.line([(540, 950), (640, 820), (760, 560), (900, 330), (1040, 250)], RED, 12, 1.2)
    s.text((330, 650), "pickleball", "mark", 60, BLUE, -18)
    s.text((990, 620), "ChatGPT", "mark", 60, RED, -40)
    s.text((600, 1060), "same shape. zero connection.", "mark", 52, INK)
    s.text((600, 200), "(for fun)", size=56, fill=GREY)
    save(s, "10-pickleball")


ALL = {"stack_overflow": stack_overflow, "google_ctr": google_ctr, "glue": glue, "reddit": reddit,
       "please": please, "certainly": certainly, "chegg": chegg, "em_dash": em_dash,
       "linkedin_slop": linkedin_slop, "pickleball": pickleball}

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        ALL[n]()
        print("rendered", n)
