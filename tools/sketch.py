"""Hand-drawn chart helpers (graph paper, wobbly marker lines, handwritten notes).

Fonts: Permanent Marker and Caveat from Google Fonts, kept in tools/fonts/.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = os.path.join(HERE, "fonts", "PermanentMarker.ttf")
CAV = os.path.join(HERE, "fonts", "Caveat.ttf")
INK, BLUE, RED = (24, 24, 30), (28, 72, 196), (214, 58, 36)
S = 2  # supersampling


class Sketch:
    def __init__(self, w=1200, h=1200, seed=11):
        random.seed(seed)
        self.W, self.H = w, h
        self.img = Image.new("RGB", (w * S, h * S), (251, 249, 243))
        self.d = ImageDraw.Draw(self.img)
        for i in range(0, max(w, h) * S, 40 * S):
            self.d.line([(i, 0), (i, h * S)], fill=(226, 234, 242), width=S)
            self.d.line([(0, i), (w * S, i)], fill=(226, 234, 242), width=S)

    @staticmethod
    def font(kind, size):
        return ImageFont.truetype(MARK if kind == "mark" else CAV, size * S)

    def _wob(self, pts, amp, step=6):
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
            out += [(x0 + (x1 - x0) * i / n + random.uniform(-amp, amp),
                     y0 + (y1 - y0) * i / n + random.uniform(-amp, amp)) for i in range(n)]
        return out + [pts[-1]]

    def line(self, pts, fill=INK, w=7, amp=1.4):
        self.d.line([(x * S, y * S) for x, y in self._wob(pts, amp)], fill=fill, width=w * S, joint="curve")

    def arrowhead(self, tip, frm, fill=INK, w=5, size=26):
        a = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
        for da in (2.6, -2.6):
            self.line([tip, (tip[0] + size * math.cos(a + da), tip[1] + size * math.sin(a + da))], fill, w, 0.8)

    def arrow(self, pts, fill=BLUE, w=5):
        self.line(pts, fill, w)
        self.arrowhead(pts[-1], pts[-2], fill, w)

    def text(self, xy, s, kind="cav", size=60, fill=INK, angle=0):
        f = self.font(kind, size)
        b = self.d.textbbox((0, 0), s, font=f)
        lay = Image.new("RGBA", (b[2] - b[0] + 60 * S, b[3] - b[1] + 60 * S), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((30 * S, 30 * S - b[1]), s, font=f, fill=fill)
        lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
        self.img.paste(lay, (int(xy[0] * S - lay.width / 2), int(xy[1] * S - lay.height / 2)), lay)

    def axes(self, ylabel, xlabel, ox=190, oy=1000, top=150, right=1100, ysize=40):
        self.line([(ox, oy + 10), (ox, top)]); self.arrowhead((ox, top), (ox, top + 50), INK, 7, 30)
        self.line([(ox - 10, oy), (right, oy)]); self.arrowhead((right, oy), (right - 50, oy), INK, 7, 30)
        self.text((118, (oy + top) / 2), ylabel, "mark", ysize, angle=90)
        self.text(((ox + right) / 2, oy + 62), xlabel, "mark", 44)

    def dot(self, x, y, r=14, fill=INK):
        pts = [(x + r * math.cos(a), y + r * math.sin(a)) for a in [i / 12 * 2 * math.pi for i in range(13)]]
        self.d.polygon([(px * S, py * S) for px, py in self._wob(pts, 1.2, 4)], fill=fill)

    def circle(self, x, y, rx, ry, fill=RED, w=5):
        pts = [(x + rx * math.cos(a), y + ry * math.sin(a)) for a in [0.3 + i / 20 * 2 * math.pi for i in range(23)]]
        self.line(pts, fill, w, 2.2)

    def save(self, path):
        self.img.resize((self.W, self.H), Image.LANCZOS).save(path)
