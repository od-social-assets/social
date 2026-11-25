"""Charts for the 'AI up, ___ down' series. Usage: python3 tools/ai_series.py [name ...]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sketch import Sketch, INK, BLUE, RED

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media", "linkedin", "ai-series")
GREY = (120, 120, 130)


def save(s, name):
    os.makedirs(OUT, exist_ok=True)
    s.save(os.path.join(OUT, name + ".png"))


def stamp(s, text):
    s.text((600, 70), text, "mark", 40, RED, -1)
    s.line([(260, 102), (940, 100)], RED, 4, 1.2)


def bars(s, xs, vals, vmax, labels, base=1000, top=220, w=150, fills=None, vlabels=None, lsize=44):
    for i, (x, v) in enumerate(zip(xs, vals)):
        h = (base - top) * v / vmax
        y = base - h
        s.line([(x - w / 2, base), (x - w / 2, y), (x + w / 2, y), (x + w / 2, base)], w=7, amp=1.2)
        fill = (fills or [GREY] * len(xs))[i]
        for yy in range(int(y) + 20, base - 6, 20):
            s.line([(x - w / 2 + 10, yy), (x + w / 2 - 10, yy - 8)], fill, 3, 0.8)
        s.text((x, base + 45), labels[i], "mark", 32)
        if vlabels:
            s.text((x, y - 38), vlabels[i], "mark", lsize, fill if fill != GREY else INK)


def stack_overflow():
    s = Sketch(seed=1)
    stamp(s, "AI UP, STACK OVERFLOW DOWN")
    s.axes("NEW QUESTIONS PER YEAR", "", top=170, ysize=40)
    bars(s, [330, 550, 770, 990], [1336, 789, 399, 109], 1400, ["2022", "2023", "2024", "2025"],
         top=230, vlabels=["1.34M", "789K", "399K", "109K"])
    s.text((690, 300), "ChatGPT launches", size=48, fill=BLUE, angle=-3)
    s.text((690, 350), "Nov 30, 2022", size=48, fill=BLUE, angle=-3)
    s.arrow([(540, 320), (470, 300), (418, 290)])
    s.text((900, 500), "all of 2025 =", "mark", 34, RED, -3)
    s.text((900, 550), "less than 2 months", size=46, fill=RED, angle=-3)
    s.text((900, 595), "of 2016", size=46, fill=RED, angle=-3)
    s.arrow([(1010, 625), (1030, 760), (1010, 880)], RED)
    save(s, "01-stack-overflow")


def google_ctr():
    s = Sketch(seed=2)
    stamp(s, "AI UP, GOOGLE CLICKS DOWN")
    s.axes("POSITION #1 CLICK-THROUGH RATE", "", top=170, ysize=34)
    def y(v): return 1000 - v / 8.5 * 780
    x0, x1 = 340, 900
    s.line([(x0, y(7.6)), (x1, y(3.9))], INK, 8, 1.0)
    s.line([(x0, y(7.3)), (x1, y(1.6))], RED, 9, 1.0)
    for x, v in [(x0, 7.6), (x1, 3.9)]:
        s.dot(x, y(v), 13)
    for x, v in [(x0, 7.3), (x1, 1.6)]:
        s.dot(x, y(v), 13, RED)
    s.text((x0, 1045), "DEC 2023", "mark", 34); s.text((x1, 1045), "DEC 2025", "mark", 34)
    s.text((x0 - 10, y(7.6) - 55), "7.6% / 7.3%", "mark", 38)
    s.text((x1 + 95, y(3.9) - 10), "3.9%", "mark", 40)
    s.text((x1 + 95, y(1.6) + 5), "1.6%", "mark", 44, RED)
    s.text((720, 360), "keywords with no AI Overview", size=42, fill=INK, angle=0)
    s.text((520, 760), "keywords WITH an AI Overview", size=44, fill=RED, angle=0)
    s.text((690, 1110), "Ahrefs: 58% lower clicks with an AI Overview", size=40, fill=BLUE)
    save(s, "02-google-ctr")


def glue():
    s = Sketch(seed=3)
    stamp(s, "AI UP, COMMON SENSE DOWN")
    x0, y0, x1, y1 = 230, 190, 970, 1060
    s.line([(x0, y0), (x1, y0 + 6), (x1 - 4, y1), (x0 + 4, y1 - 4), (x0, y0)], INK, 7, 1.4)
    s.text((600, 270), "PIZZA", "mark", 70)
    s.text((600, 345), "(according to AI, May 2024)", size=44, fill=GREY)
    items = ["dough", "tomato sauce", "mozzarella", "non-toxic glue", "(so the cheese sticks)"]
    ys = [460, 560, 660, 760, 818]
    for i, (t, yy) in enumerate(zip(items, ys)):
        if i < 4:
            s.line([(300, yy), (318, yy + 18), (350, yy - 22)], BLUE if i < 3 else RED, 6, 0.8)
        s.text((560 if i < 4 else 600, yy), t, size=60 if i < 4 else 42, fill=RED if i >= 3 else INK)
    s.circle(560, 790, 230, 78)
    s.text((600, 920), "side: one small rock a day", size=46, fill=INK)
    s.text((600, 990), "sources: a forum joke + satire", size=40, fill=BLUE)
    s.text((600, 1130), "both confirmed real by Google", size=40, fill=GREY)
    save(s, "03-glue-on-pizza")


def reddit():
    s = Sketch(seed=4)
    stamp(s, "AI UP, REDDIT VISITS DOWN")
    s.axes("REDDIT VISITS", "2023                                   2026", top=170, ysize=44)
    pts, x = [], 215
    while x <= 1080:
        if x < 520:   yv = 820 - 380 * ((x - 215) / 305) ** 1.2
        elif x < 760: yv = 440 + random.uniform(-25, 25)
        else:         yv = 440 + 200 * ((x - 760) / 320) ** 1.1
        pts.append((x, yv + random.uniform(-6, 6))); x += 16
    s.line(pts, w=10, amp=1.0)
    s.text((420, 300), "ACT 1:", "mark", 36, BLUE)
    s.text((420, 350), "Google loves Reddit", size=50, fill=BLUE)
    s.text((420, 405), "+39% (May 23 to May 24)", size=40, fill=BLUE)
    s.text((900, 760), "ACT 2:", "mark", 36, RED)
    s.text((900, 810), "Google summarizes", size=48, fill=RED)
    s.text((900, 860), "Reddit instead", size=48, fill=RED)
    s.text((900, 915), "-13% (Oct 25 to Oct 26)", size=40, fill=RED)
    s.text((640, 1140), "(shape not to scale. percentages: Similarweb)", size=36, fill=GREY)
    save(s, "04-reddit")


def please():
    s = Sketch(seed=5)
    stamp(s, "AI UP, MANNERS... EXPENSIVE")
    s.axes("COST", "", top=170, ysize=48)
    base = 1000
    x, w = 420, 200
    s.line([(x - w / 2, base), (x - w / 2, 760), (x + w / 2, 760), (x + w / 2, base)], w=7)
    for yy in range(780, base - 6, 20):
        s.line([(x - w / 2 + 10, yy), (x + w / 2 - 10, yy - 8)], BLUE, 3, 0.8)
    s.text((x, 700), "tens of millions", size=50, fill=BLUE)
    s.text((x, 1050), "saying please", size=42)
    s.text((x, 1095), "and thank you", size=42)
    x2 = 800
    s.line([(x2 - w / 2, base), (x2 - w / 2, 120)], w=7, amp=1.2)
    s.line([(x2 + w / 2, base), (x2 + w / 2, 120)], w=7, amp=1.2)
    for yy in range(140, base - 6, 20):
        s.line([(x2 - w / 2 + 10, yy), (x2 + w / 2 - 10, yy - 8)], RED, 3, 0.8)
    s.text((x2, 1050), "being rude when", size=42)
    s.text((x2, 1095), "the robots take over", size=42)
    s.text((1010, 420), "???", "mark", 64, RED, -8)
    s.text((430, 520), "per Sam Altman:", size=40, fill=GREY)
    s.text((430, 565), "“well spent... you never know”", size=40, fill=GREY)
    save(s, "05-please-thank-you")


def certainly():
    s = Sketch(seed=6)
    stamp(s, "AI UP, PROOFREADING DOWN")
    s.line([(150, 150), (1050, 155), (1048, 330), (152, 326), (150, 150)], RED, 5, 1.2)
    s.text((600, 205), "“Certainly, here is a possible", size=56)
    s.text((600, 270), "introduction for your topic:”", size=56)
    s.text((600, 360), "the opening line of a published lithium battery paper, 2024", size=34, fill=GREY)
    bars(s, [300, 520, 740, 960], [137, 117, 83, 59], 150, ["meticulously", "intricate", "commendable", "meticulous"],
         top=470, w=150, vlabels=["+137%", "+117%", "+83%", "+59%"], lsize=42,
         fills=[RED, GREY, GREY, GREY])
    s.text((600, 1120), "rise in 2023 papers (Andrew Gray, UCL)", size=40, fill=BLUE)
    save(s, "06-certainly")


def chegg():
    s = Sketch(seed=7)
    stamp(s, "AI UP, HOMEWORK HELP DOWN")
    s.axes("CHEGG SHARE PRICE", "", top=170, ysize=44)
    def y(p): return 1000 - p / 21 * 780
    pts, x = [], 215
    while x < 620:
        pts.append((x, y(18.2 + random.uniform(-0.4, 0.5)))); x += 18
    pts += [(640, y(18.71)), (680, y(14)), (700, y(10.5)), (720, y(9.2))]
    x = 740
    while x <= 1060:
        pts.append((x, y(9 + random.uniform(-0.25, 0.25)))); x += 18
    s.line(pts, w=10, amp=1.0)
    s.text((420, 1045), "MAY 1, 2023", "mark", 32); s.text((880, 1045), "MAY 2, 2023", "mark", 32)
    s.text((520, y(18.71) - 60), "$18.71", "mark", 44)
    s.text((900, y(9) + 70), "about $9", "mark", 44)
    s.text((900, 430), "-49%", "mark", 90, RED, -4)
    s.text((900, 520), "in one day", size=54, fill=RED, angle=-4)
    s.text((420, 820), "“We now believe it’s", size=42, fill=BLUE, angle=-2)
    s.text((420, 865), "having an impact on our", size=42, fill=BLUE, angle=-2)
    s.text((420, 910), "new customer growth”", size=42, fill=BLUE, angle=-2)
    s.text((420, 955), "Chegg CEO, on ChatGPT", size=34, fill=GREY, angle=-2)
    save(s, "07-chegg")


def em_dash():
    s = Sketch(seed=8)
    stamp(s, "AI UP, EM DASHES... UP")
    s.axes("EM DASHES PER 10,000 WORDS", "", top=170, ysize=36)
    base = 1000
    for x, h, lab, col in [(420, 330, "2023", GREY), (800, 660, "2026", RED)]:
        s.line([(x - 100, base), (x - 100, base - h), (x + 100, base - h), (x + 100, base)], w=7)
        for yy in range(base - h + 20, base - 6, 20):
            s.line([(x - 90, yy), (x + 90, yy - 8)], col, 3, 0.8)
        s.text((x, base + 45), lab, "mark", 36)
    s.text((420, 620), "5.79", "mark", 50)
    s.text((800, 290), "about 2x", "mark", 50, RED)
    s.line([(330, 210), (520, 212)], INK, 16, 0.6)
    s.text((430, 270), "this little guy", size=44)
    s.text((1000, 600), "the dash", size=48, fill=BLUE, angle=-6)
    s.text((1000, 650), "was here", size=48, fill=BLUE, angle=-6)
    s.text((1000, 700), "first.", size=48, fill=BLUE, angle=-6)
    s.text((620, 1120), "pages published after ChatGPT (Pew Research Center)", size=36, fill=GREY)
    save(s, "08-em-dash")


def linkedin_slop():
    s = Sketch(seed=9)
    stamp(s, "AI UP, ORIGINAL THOUGHT DOWN")
    s.axes("LONG LINKEDIN POSTS LIKELY AI", "", top=170, ysize=32)
    base = 1000
    def h(p): return (base - 230) * p / 100
    for x, p, lab, col, vl in [(420, 50, "LATE 2024", GREY, "about half"), (800, 81.2, "JULY 2026", RED, "81.2%")]:
        s.line([(x - 110, base), (x - 110, base - h(p)), (x + 110, base - h(p)), (x + 110, base)], w=7)
        for yy in range(int(base - h(p)) + 20, base - 6, 20):
            s.line([(x - 100, yy), (x + 100, yy - 8)], col, 3, 0.8)
        s.text((x, base + 45), lab, "mark", 34)
        s.text((x, base - h(p) - 42), vl, "mark", 48, RED if col == RED else INK)
    s.text((520, 300), "the other 18.8%?", size=52, fill=BLUE, angle=-3)
    s.text((520, 355), "humans. or very", size=48, fill=BLUE, angle=-3)
    s.text((520, 405), "good prompts.", size=48, fill=BLUE, angle=-3)
    s.text((620, 1120), "Originality.ai samples of public posts, 100+ words", size=36, fill=GREY)
    save(s, "09-linkedin-slop")


def pickleball():
    s = Sketch(seed=10)
    stamp(s, "AI UP, PICKLEBALL UP (FOR FUN)")
    s.axes("UP AND TO THE RIGHT", "2020                                   2026", top=170, ysize=40)
    pk = [(230, 900), (420, 760), (620, 600), (820, 430), (1000, 320)]
    gp = [(560, 970), (640, 820), (760, 560), (900, 330), (1050, 250)]
    s.line(pk, BLUE, 9, 1.2)
    s.line(gp, RED, 9, 1.2)
    s.text((380, 470), "US pickleball players", size=46, fill=BLUE, angle=-14)
    s.text((380, 525), "4.2M to 24.3M", size=46, fill=BLUE, angle=-14)
    s.text((900, 720), "ChatGPT", size=50, fill=RED, angle=-30)
    s.text((935, 780), "0 to 900M a week", size=42, fill=RED, angle=-30)
    s.line([(240, 190), (740, 186), (742, 290), (242, 294), (240, 190)], INK, 5, 1.2)
    s.text((491, 240), "FOR FUN. NOT A FINDING.", "mark", 32, INK, 0)
    s.text((620, 1120), "correlation: yes. causation: absolutely not.", size=40, fill=GREY)
    save(s, "10-pickleball")


ALL = {"stack_overflow": stack_overflow, "google_ctr": google_ctr, "glue": glue, "reddit": reddit,
       "please": please, "certainly": certainly, "chegg": chegg, "em_dash": em_dash,
       "linkedin_slop": linkedin_slop, "pickleball": pickleball}

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        ALL[n]()
        print("rendered", n)
