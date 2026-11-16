"""Tiny dual-target canvas: every primitive is written to a python-pptx slide AND
rasterised with PIL, so the layout can be checked visually without PowerPoint.
Units are inches; text sizes are points. Text is measured with the real Arial
metrics and every text box is checked for overflow."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

W, H = 13.333, 7.5
DPI = 110
FONT_DIR = '/System/Library/Fonts/Supplemental/'
_fonts = {}

def font(size, bold=False):
    key = (round(size * DPI / 72), bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_DIR + ('Arial Bold.ttf' if bold else 'Arial.ttf'), key[0])
    return _fonts[key]

def rgb(h):
    h = h.lstrip('#'); return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
def prgb(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK, INK2, MUTED, GRID, BASE = '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'

def parse_runs(s):
    """'plain **bold** plain' -> [(text, bold)]"""
    out = []
    for i, part in enumerate(re.split(r'\*\*', s)):
        if part: out.append((part, i % 2 == 1))
    return out

OVERFLOWS = []

class Slide:
    def __init__(self, deck, idx):
        self.deck = deck
        self.s = deck.prs.slides.add_slide(deck.prs.slide_layouts[6])
        self.img = Image.new('RGB', (int(W * DPI), int(H * DPI)), (255, 255, 255))
        self.d = ImageDraw.Draw(self.img)
        self.idx = idx

    # ---------- shapes ----------
    def rect(self, x, y, w, h, fill, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
        if w <= 0 or h <= 0: return
        sh = self.s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.shadow.inherit = False
        if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else: sh.fill.background()
        if line: sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        else: sh.line.fill.background()
        box = [x * DPI, y * DPI, (x + w) * DPI, (y + h) * DPI]
        if shape == MSO_SHAPE.OVAL:
            self.d.ellipse(box, fill=prgb(fill) if fill else None, outline=prgb(line) if line else None)
        else:
            self.d.rectangle(box, fill=prgb(fill) if fill else None, outline=prgb(line) if line else None,
                             width=max(1, int(lw * DPI / 72)) if line else 0)
        return sh

    def dot(self, cx, cy, r, fill, ring='#ffffff'):
        self.rect(cx - r, cy - r, 2 * r, 2 * r, fill, line=ring, lw=1.5, shape=MSO_SHAPE.OVAL)

    def line(self, x1, y1, x2, y2, color, width=1.0, dash=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(width)
        if dash: c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        px = max(1, round(width * DPI / 72))
        p1, p2 = (x1 * DPI, y1 * DPI), (x2 * DPI, y2 * DPI)
        if not dash:
            self.d.line([p1, p2], fill=prgb(color), width=px)
        else:
            import math
            L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); seg = 4 * px; n = int(L // (2 * seg)) + 1
            for i in range(n):
                a = (2 * i * seg) / L; b = min(1, (2 * i * seg + seg) / L)
                if a >= 1: break
                self.d.line([(p1[0] + (p2[0] - p1[0]) * a, p1[1] + (p2[1] - p1[1]) * a),
                             (p1[0] + (p2[0] - p1[0]) * b, p1[1] + (p2[1] - p1[1]) * b)], fill=prgb(color), width=px)

    # ---------- text ----------
    def text(self, x, y, w, h, paras, size=14, color=INK, bold=False, align='l', valign='t',
             ls=1.18, bullet_indent=0.22, check=True, para_space=None):
        """paras: str or list of str/dict. dict keys: t, size, color, bold, bullet, space (pt before)."""
        if isinstance(paras, str): paras = [paras]
        P = []
        for p in paras:
            if isinstance(p, str): p = {'t': p}
            q = dict(size=size, color=color, bold=bold, bullet=False,
                     space=(para_space if para_space is not None else size * 0.45))
            q.update(p); P.append(q)
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[valign]
        bodyPr = tf._txBody.find(qn('a:bodyPr'))
        for el in list(bodyPr): bodyPr.remove(el)
        # layout in PIL
        layout, total = [], 0
        for i, p in enumerate(P):
            ind = bullet_indent if p['bullet'] else 0
            maxw = (w - ind) * DPI * 0.965
            runs = parse_runs(p['t'])
            words = []
            for t, b in runs:
                for k, tok in enumerate(re.split(r'(\s+)', t)):
                    if tok == '': continue
                    words.append((tok, b or p['bold']))
            lines, cur, curw = [], [], 0
            for tok, b in words:
                f = font(p['size'], b)
                tw = f.getlength(tok)
                if tok.isspace():
                    if cur: cur.append((' ', b, tw)); curw += tw
                    continue
                if cur and curw + tw > maxw:
                    while cur and cur[-1][0] == ' ': curw -= cur[-1][2]; cur.pop()
                    lines.append(cur); cur, curw = [], 0
                cur.append((tok, b, tw)); curw += tw
            while cur and cur[-1][0] == ' ': cur.pop()
            if cur or not lines: lines.append(cur)
            lh = p['size'] * ls / 72
            sp = (p['space'] / 72) if i > 0 else 0
            layout.append((p, ind, lines, lh, sp)); total += sp + lh * len(lines)
        if check and total > h + 0.02:
            OVERFLOWS.append(f'slide {self.idx}: text overflows box by {total - h:.2f}in: {P[0]["t"][:60]!r}')
        y0 = y + {'t': 0, 'm': (h - total) / 2, 'b': h - total}[valign]
        cy = y0
        for p, ind, lines, lh, sp in layout:
            cy += sp
            for li, ln in enumerate(lines):
                lw_ = sum(t[2] for t in ln) / DPI
                if align == 'c': lx = x + ind + ((w - ind) - lw_) / 2
                elif align == 'r': lx = x + w - lw_
                else: lx = x + ind
                f0 = font(p['size'])
                base = cy * DPI + (lh * DPI - p['size'] * DPI / 72 * 1.0) / 2
                if p['bullet'] and li == 0:
                    self.d.text((x * DPI, base), '•', font=f0, fill=prgb(p['color']))
                px = lx * DPI
                for tok, b, tw in ln:
                    self.d.text((px, base), tok, font=font(p['size'], b), fill=prgb(p['color']))
                    px += tw
                cy += lh
        # pptx
        for i, p in enumerate(P):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
            para.line_spacing = Pt(p['size'] * ls)
            if i > 0: para.space_before = Pt(p['space'])
            pPr = para._p.get_or_add_pPr()
            if p['bullet']:
                pPr.set('marL', str(int(Inches(bullet_indent)))); pPr.set('indent', str(-int(Inches(bullet_indent))))
                bf = pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'}); pPr.append(bf)
                bc = pPr.makeelement(qn('a:buChar'), {'char': '•'}); pPr.append(bc)
            else:
                pPr.append(pPr.makeelement(qn('a:buNone'), {}))
            for t, b in parse_runs(p['t']):
                r = para.add_run(); r.text = t
                r.font.size = Pt(p['size']); r.font.bold = b or p['bold']; r.font.name = 'Arial'
                r.font.color.rgb = rgb(p['color'])
        return total

    def notes(self, txt):
        self.s.notes_slide.notes_text_frame.text = txt


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.slides = []
    def new(self):
        s = Slide(self, len(self.slides) + 1); self.slides.append(s); return s
    def save(self, path, preview_dir):
        self.prs.save(path)
        for s in self.slides:
            s.img.save(f'{preview_dir}/slide{s.idx:02d}.png')
