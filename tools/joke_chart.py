"""Hand-drawn joke chart, simple version: best-of listicles over time."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont

random.seed(11)
W = H = 1200
S = 2
img = Image.new("RGB", (W * S, H * S), (251, 249, 243))
d = ImageDraw.Draw(img)
MARK = "/home/claude/fonts/PermanentMarker.ttf"
CAV = "/home/claude/fonts/Caveat.ttf"
def F(p, s): return ImageFont.truetype(p, s * S)

# faint graph paper
for i in range(0, W * S, 40 * S):
    d.line([(i, 0), (i, H * S)], fill=(226, 234, 242), width=S)
    d.line([(0, i), (W * S, i)], fill=(226, 234, 242), width=S)

INK, BLUE, RED = (24, 24, 30), (28, 72, 196), (214, 58, 36)

def wob(pts, amp, step=6):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * i / n + random.uniform(-amp, amp),
                 y0 + (y1 - y0) * i / n + random.uniform(-amp, amp)) for i in range(n)]
    return out + [pts[-1]]

def line(pts, fill=INK, w=7, amp=1.4):
    d.line([(x * S, y * S) for x, y in wob(pts, amp)], fill=fill, width=w * S, joint="curve")

def arrowhead(tip, frm, fill, w=5, size=26):
    a = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    for da in (2.6, -2.6):
        line([tip, (tip[0] + size * math.cos(a + da), tip[1] + size * math.sin(a + da))], fill, w, 0.8)

def text(xy, s, font, fill=INK, angle=0):
    b = d.textbbox((0, 0), s, font=font)
    lay = Image.new("RGBA", (b[2] - b[0] + 60 * S, b[3] - b[1] + 60 * S), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((30 * S, 30 * S - b[1]), s, font=font, fill=fill)
    lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(xy[0] * S - lay.width / 2), int(xy[1] * S - lay.height / 2)), lay)

# axes
ox, oy, top, right = 190, 1000, 150, 1100
line([(ox, oy + 10), (ox, top)], w=7); arrowhead((ox, top), (ox, top + 50), INK, 7, 30)
line([(ox - 10, oy), (right, oy)], w=7); arrowhead((right, oy), (right - 50, oy), INK, 7, 30)
text((118, (oy + top) / 2), "“BEST X SOFTWARE” LISTS", F(MARK, 44), angle=90)
text(((ox + right) / 2, 1062), "TIME", F(MARK, 48))

# data: boring flat years, then straight up
pts, x = [], ox + 25
while x < 760:
    pts.append((x, 930 + 12 * math.sin(x / 41) + random.uniform(-6, 6))); x += 20
pts += [(778, 915), (792, 860), (800, 700), (806, 480), (812, 300), (820, 250)]
line(pts, w=10, amp=1.0)

# annotation: the trigger
text((480, 610), "AI STARTS", F(CAV, 62), BLUE, 4)
text((485, 672), "PICKING WINNERS", F(CAV, 62), BLUE, 4)
text((490, 734), "FROM THESE LISTS", F(CAV, 62), BLUE, 4)
line([(620, 790), (700, 845), (772, 880)], BLUE, 5)
arrowhead((772, 880), (705, 850), BLUE)

# annotation: the punchline
text((1010, 385), "always written by", F(CAV, 58), RED, -4)
text((1010, 445), "the #1 pick", F(CAV, 58), RED, -4)
line([(890, 330), (860, 290), (838, 262)], RED, 5)
arrowhead((838, 262), (860, 290), RED)

img.resize((W, H), Image.LANCZOS).save(sys.argv[1])
