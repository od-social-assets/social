"""Hand-drawn joke chart on graph paper: 'best X tools' listicles over time."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(7)
W = H = 1200
S = 2  # supersample
img = Image.new("RGB", (W * S, H * S), (250, 247, 238))
d = ImageDraw.Draw(img)

MARK = "/home/claude/fonts/PermanentMarker.ttf"
CAV = "/home/claude/fonts/Caveat.ttf"
def F(path, size): return ImageFont.truetype(path, size * S)

# graph paper
for x in range(0, W * S, 30 * S):
    d.line([(x, 0), (x, H * S)], fill=(214, 228, 240), width=1 * S)
for y in range(0, H * S, 30 * S):
    d.line([(0, y), (W * S, y)], fill=(214, 228, 240), width=1 * S)
for x in range(0, W * S, 150 * S):
    d.line([(x, 0), (x, H * S)], fill=(190, 210, 230), width=2 * S)
for y in range(0, H * S, 150 * S):
    d.line([(0, y), (W * S, y)], fill=(190, 210, 230), width=2 * S)

INK = (28, 28, 34)
BLUE = (30, 70, 190)
RED = (214, 64, 40)

def wobble(pts, amp=2.0, step=6):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            t = i / n
            out.append((x0 + (x1 - x0) * t + random.uniform(-amp, amp),
                        y0 + (y1 - y0) * t + random.uniform(-amp, amp)))
    out.append(pts[-1])
    return out

def line(pts, fill=INK, w=6, amp=1.6):
    p = [(x * S, y * S) for x, y in wobble(pts, amp)]
    d.line(p, fill=fill, width=w * S, joint="curve")

def text(xy, s, font, fill=INK, angle=0, anchor="la"):
    if angle == 0:
        d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)
        return
    bbox = d.textbbox((0, 0), s, font=font)
    tw, th = bbox[2] - bbox[0] + 40 * S, bbox[3] - bbox[1] + 40 * S
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((20 * S, 20 * S - bbox[1]), s, font=font, fill=fill)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(xy[0] * S - layer.width / 2), int(xy[1] * S - layer.height / 2)), layer)

# title
text((80, 70), "A BRIEF HISTORY OF", F(MARK, 34), fill=INK)
text((80, 112), "“THE 9 BEST TOOLS FOR 2027”", F(MARK, 52), fill=INK)

# axes
ox, oy, top, right = 170, 1010, 260, 1110
line([(ox, oy + 8), (ox, top)], w=6)
line([(ox, top), (ox - 16, top + 26)], w=6)
line([(ox, top), (ox + 16, top + 26)], w=6)
line([(ox - 8, oy), (right, oy)], w=6)
line([(right, oy), (right - 26, oy - 16)], w=6)
line([(right, oy), (right - 26, oy + 16)], w=6)
text((112, (oy + top) / 2), "HOW MANY EXIST", F(MARK, 34), angle=90)
text(((ox + right) / 2, 1065), "TIME", F(MARK, 40), anchor="ma")

# data: flat wobble, then a cliff straight up
pts = []
x = ox + 20
while x < 720:
    pts.append((x, 940 + 14 * math.sin(x / 37) + random.uniform(-8, 8)))
    x += 18
pts += [(735, 925), (752, 880), (762, 760), (770, 600), (778, 460), (790, 400)]
line(pts, w=8, amp=1.2)

# annotation 1: the spike
text((515, 640), "AI SEARCH STARTS", F(CAV, 54), fill=BLUE, angle=6)
text((515, 692), "CITING THEM", F(CAV, 54), fill=BLUE, angle=6)
line([(640, 735), (700, 790), (748, 830)], fill=BLUE, w=4)
line([(748, 830), (722, 826)], fill=BLUE, w=4)
line([(748, 830), (742, 805)], fill=BLUE, w=4)

# annotation 2: the old era
text((380, 800), "the guest post era", F(CAV, 44), fill=BLUE, angle=-3)
line([(380, 830), (385, 880), (392, 905)], fill=BLUE, w=4)
line([(392, 905), (378, 888)], fill=BLUE, w=4)
line([(392, 905), (402, 886)], fill=BLUE, w=4)

# sticky note
note = Image.new("RGBA", (360 * S, 260 * S), (255, 226, 92, 255))
nd = ImageDraw.Draw(note)
nd.rectangle([0, 0, note.width, 34 * S], fill=(245, 208, 70, 255))
nd.text((26 * S, 62 * S), "Fun fact:", font=F(CAV, 50), fill=INK)
nd.text((26 * S, 118 * S), "every single one", font=F(CAV, 44), fill=INK)
nd.text((26 * S, 168 * S), "ranks itself #1", font=F(CAV, 44), fill=RED)
shadow = Image.new("RGBA", note.size, (0, 0, 0, 70)).filter(ImageFilter.GaussianBlur(8 * S))
note = note.rotate(-5, expand=True, resample=Image.BICUBIC)
shadow = shadow.rotate(-5, expand=True, resample=Image.BICUBIC)
nx, ny = 800 * S, 470 * S
img.paste(shadow, (nx + 10 * S, ny + 14 * S), shadow)
img.paste(note, (nx, ny), note)

# circle the peak in red
cx, cy, r = 790, 400, 46
circ = [(cx + r * math.cos(a) * 1.15, cy + r * math.sin(a)) for a in [i / 20 * 2 * math.pi + 0.3 for i in range(23)]]
line(circ, fill=RED, w=5, amp=2.5)

out = img.resize((W, H), Image.LANCZOS)
out.save(sys.argv[1] if len(sys.argv) > 1 else "joke_chart.png")
