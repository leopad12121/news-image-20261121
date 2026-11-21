#!/usr/bin/env python3
"""Round 2: one image summing up the world news of Saturday 21 November 2026.

Draws a 1024x1024 newspaper front page with Pillow only. No network, no
randomness, no timestamps: running it twice writes byte-identical PNGs.
Output: $MAKEFUN_OUTPUT_DIR/entry.png, else /output/entry.png when /output
exists, else ./entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30

PAPER = (248, 244, 234)
INK = (26, 26, 26)
GREY = (96, 92, 84)
RED = (163, 22, 33)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    """Load a DejaVu font, falling back to Pillow's built-in bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def serif_b(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_font("DejaVuSerif.ttf", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill=INK, spacing=4):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- panels
def panel_gulf(draw, x, y, w, h):
    """Strait of Hormuz at dusk: sea, sun, tanker, missile trails, burst."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 42, 66))
    draw.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(214, 122, 54))
    draw.ellipse([x + w - 92, y + 14, x + w - 28, y + 78], fill=(255, 196, 90))
    draw.rectangle([x, y + int(h * 0.42), x + w, y + h], fill=(16, 42, 66))
    # tanker silhouette
    tx, ty = x + 24, y + int(h * 0.62)
    draw.polygon([(tx, ty), (tx + 150, ty), (tx + 138, ty + 26),
                  (tx + 12, ty + 26)], fill=(8, 22, 36))
    draw.rectangle([tx + 20, ty - 26, tx + 46, ty], fill=(8, 22, 36))
    draw.rectangle([tx + 56, ty - 18, tx + 130, ty], fill=(140, 40, 30))
    for i in range(4):
        draw.rectangle([tx + 60 + i * 18, ty - 34, tx + 72 + i * 18, ty - 18],
                       fill=(200, 90, 60))
    # missile streaks slanting down toward the sea
    for sx, ex in ((x + 30, x + 108), (x + 130, x + 208), (x + 224, x + 296)):
        draw.line([(sx, y + 14), (ex, y + 92)], fill=(255, 220, 130), width=3)
        draw.ellipse([ex - 4, y + 88, ex + 4, y + 96], fill=(255, 220, 130))
    # explosion burst over the sea
    cx, cy = x + w - 70, y + int(h * 0.58)
    pts = []
    for i in range(12):
        r = 34 if i % 2 == 0 else 15
        a = math.pi * i / 6
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(255, 176, 40))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 240, 180))


def panel_desert(draw, x, y, w, h):
    """Sinaloa at dusk: sun, mesas, cactus, road."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 148, 72))
    draw.ellipse([x + w - 66, y + 12, x + w - 18, y + 60], fill=(255, 222, 130))
    draw.polygon([(x, y + h), (x + 40, y + int(h * 0.45)),
                  (x + 110, y + h)], fill=(150, 74, 44))
    draw.polygon([(x + 80, y + h), (x + 150, y + int(h * 0.55)),
                  (x + w, y + h)], fill=(120, 56, 36))
    draw.rectangle([x, y + int(h * 0.78), x + w, y + h], fill=(196, 120, 62))
    # cactus
    cx, cy = x + 26, y + int(h * 0.62)
    draw.rounded_rectangle([cx, cy, cx + 12, cy + 46], radius=6, fill=(46, 110, 52))
    draw.rounded_rectangle([cx - 14, cy + 14, cx - 2, cy + 30], radius=5,
                           fill=(46, 110, 52))
    draw.rounded_rectangle([cx + 14, cy + 8, cx + 26, cy + 24], radius=5,
                           fill=(46, 110, 52))
    # road
    draw.polygon([(x + w - 70, y + h), (x + w - 30, y + int(h * 0.78)),
                  (x + w - 8, y + int(h * 0.78)), (x + w - 34, y + h)],
                 fill=(60, 52, 48))


def panel_chart(draw, x, y, w, h):
    """Falling market chart on graph paper."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gx in range(x + 14, x + w, 18):
        draw.line([(gx, y), (gx, y + h)], fill=(228, 228, 228), width=1)
    for gy in range(y + 14, y + h, 18):
        draw.line([(x, gy), (x + w, gy)], fill=(228, 228, 228), width=1)
    pts = [(x + 8, y + 22), (x + 28, y + 30), (x + 48, y + 26),
           (x + 68, y + 48), (x + 88, y + 44), (x + 108, y + 72),
           (x + 128, y + 96), (x + 150, y + h - 12)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 14, ey - 2), (ex - 2, ey - 14)], fill=RED)


def panel_city(draw, x, y, w, h):
    """City under a blue-and-yellow sky, smoke rising."""
    draw.rectangle([x, y, x + w, y + int(h * 0.5)], fill=(58, 110, 180))
    draw.rectangle([x, y + int(h * 0.5), x + w, y + h], fill=(240, 200, 60))
    # buildings
    for bx, bw, bh in ((x + 8, 34, 58), (x + 48, 26, 78), (x + 80, 40, 48),
                       (x + 126, 30, 66)):
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(52, 52, 58))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 6, 11):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 214, 120))
    # smoke puffs
    for sx, sy, sr in ((x + 60, y + 26, 12), (x + 78, y + 14, 16),
                       (x + 100, y + 30, 10)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 122))
    # small burst
    cx, cy = x + 150, y + 22
    draw.polygon([(cx, cy - 14), (cx + 5, cy - 5), (cx + 14, cy - 2),
                  (cx + 5, cy + 4), (cx + 8, cy + 13), (cx, cy + 6),
                  (cx - 8, cy + 13), (cx - 5, cy + 4), (cx - 14, cy - 2),
                  (cx - 5, cy - 5)], fill=(255, 176, 40))


def panel_climate(draw, x, y, w, h):
    """A warming globe with a leaf."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 236, 214))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 200))
    draw.ellipse([cx - r + 12, cy - r + 8, cx - r + 46, cy - r + 34],
                 fill=(80, 170, 90))
    draw.ellipse([cx + 2, cy + 6, cx + 42, cy + 40], fill=(80, 170, 90))
    draw.ellipse([cx - r + 22, cy + r - 34, cx - r + 52, cy + r - 8],
                 fill=(80, 170, 90))
    draw.arc([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], 300, 60,
             fill=(201, 141, 32), width=4)
    # leaf
    lx, ly = x + w - 34, y + h - 30
    draw.ellipse([lx - 16, ly - 8, lx + 16, ly + 8], fill=(46, 125, 50))
    draw.line([(lx - 16, ly), (lx + 16, ly)], fill=(30, 90, 36), width=2)


def panel_mosquito(draw, x, y, w, h):
    """A Wolbachia mosquito under a shield."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 240, 226))
    cx, cy = x + w // 2, y + h // 2
    # wings
    draw.ellipse([cx - 58, cy - 30, cx - 6, cy - 2], fill=(255, 255, 255),
                 outline=(150, 170, 150))
    draw.ellipse([cx + 6, cy - 30, cx + 58, cy - 2], fill=(255, 255, 255),
                 outline=(150, 170, 150))
    # legs
    for dx in (-26, 0, 26):
        draw.line([(cx + dx, cy + 8), (cx + dx - 14, cy + 34)], fill=(60, 60, 60),
                  width=3)
        draw.line([(cx + dx, cy + 8), (cx + dx + 14, cy + 34)], fill=(60, 60, 60),
                  width=3)
    # body and head
    draw.ellipse([cx - 10, cy - 12, cx + 10, cy + 26], fill=(52, 52, 52))
    draw.ellipse([cx - 9, cy - 24, cx + 9, cy - 8], fill=(52, 52, 52))
    draw.line([(cx - 6, cy - 20), (cx - 18, cy - 34)], fill=(52, 52, 52), width=2)
    draw.line([(cx + 6, cy - 20), (cx + 18, cy - 34)], fill=(52, 52, 52), width=2)
    # green plus badges
    for sx, sy in ((x + 18, y + 18), (x + w - 18, y + 18)):
        draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(46, 125, 50))
        draw.text((sx - 4, sy - 7), "+", font=sans_b(13), fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = serif_b(62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    rule(d, MARGIN, 108, W - MARGIN, 3)
    dateline = "SATURDAY 21 NOVEMBER 2026"
    df = sans_b(26)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, 120), dateline, font=df, fill=RED)
    sub = "Six stories from one Saturday \u2014 the Gulf, Mexico, markets, Ukraine, climate and health"
    sf = sans(16)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 152), sub, font=sf, fill=GREY)
    rule(d, MARGIN, 182, W - MARGIN, 2)

    # ---- lead story: Middle East
    ly = 196
    panel_gulf(d, MARGIN, ly, 400, 200)
    tx = MARGIN + 420
    twd = W - MARGIN - tx
    d.text((tx, ly), "MIDDLE EAST  \u00b7  LEAD", font=sans_b(16), fill=RED)
    y = draw_wrapped(d, tx, ly + 26,
                     "Gulf war flares again as Bahrain intercepts Iranian attacks",
                     serif_b(30), twd, spacing=2)
    y = draw_wrapped(d, tx, y + 6,
                     "Bahrain said its air defences stopped Iranian aerial attacks on "
                     "Saturday evening, as tanker strikes in the Strait of Hormuz "
                     "hit their highest level since the war began. The US and Israel "
                     "are reported to be weighing new strikes within days.",
                     sans(18), twd, spacing=3)
    d.text((tx, y + 6), "Sources: Gulf News \u00b7 Dawn \u00b7 Al Jazeera \u00b7 Reuters",
           font=sans(14), fill=GREY)
    rule(d, MARGIN, 420, W - MARGIN, 2)

    # ---- 2x2 grid
    grid = [
        ("MEXICO", "FBI most-wanted cartel boss seized in Sinaloa raid",
         "Mexican forces captured Fausto Isidro Meza Flores, "
         "\u201cEl Chapo Isidro\u201d, in Guasave on Friday night; 11 people died "
         "in the cartel backlash.",
         "Sources: Reuters \u00b7 AP", panel_desert),
        ("MARKETS", "AI sell-off sinks world markets",
         "The S&P 500 fell 3.7% and the Nasdaq 5.3% on Friday. Nvidia fell "
         "about 14% after Reuters reported the SEC is examining its accounting.",
         "Source: Reuters", panel_chart),
        ("UKRAINE", "Missiles hit Zelenskyy\u2019s hometown, land in Poland",
         "Russian missiles struck Kryvyi Rih on Friday night, killing two "
         "and wounding 60. Two missiles and a drone also came down in Poland.",
         "Sources: AP \u00b7 Al Jazeera", panel_city),
        ("CLIMATE", "COP31 climate talks run past deadline in Antalya",
         "The UN climate summit in Turkey overran its Friday deadline as "
         "negotiators argued over a draft text that drops fossil-fuel language.",
         "Sources: One Turn \u00b7 WW6RAG", panel_climate),
    ]
    gx0, gy0 = MARGIN, 436
    cw, ch = (W - 2 * MARGIN - 24) // 2, 186
    for i, (kick, head, body, src, painter) in enumerate(grid):
        cx = gx0 + (i % 2) * (cw + 24)
        cy = gy0 + (i // 2) * (ch + 14)
        painter(d, cx, cy, 160, 128)
        tx2 = cx + 172
        tw2 = cx + cw - tx2
        d.text((tx2, cy), kick, font=sans_b(14), fill=RED)
        y2 = draw_wrapped(d, tx2, cy + 22, head, serif_b(19), tw2, spacing=1)
        y2 = draw_wrapped(d, tx2, y2 + 4, body, sans(14), tw2, spacing=2)
        d.text((tx2, y2 + 4), src, font=sans(12), fill=GREY)
        if i % 2 == 0:
            d.line([(cx + cw + 12, cy), (cx + cw + 12, cy + ch - 8)],
                   fill=(200, 194, 180), width=1)
    rule(d, MARGIN, 836, W - MARGIN, 2)

    # ---- bottom strip: science
    by = 850
    panel_mosquito(d, MARGIN, by, 188, 104)
    tx3 = MARGIN + 204
    tw3 = W - MARGIN - tx3
    d.text((tx3, by), "SCIENCE  \u00b7  HEALTH", font=sans_b(14), fill=RED)
    y3 = draw_wrapped(d, tx3, by + 22,
                      "Mosquitoes that beat dengue: infections down 69%",
                      serif_b(22), tw3, spacing=1)
    y3 = draw_wrapped(d, tx3, y3 + 4,
                      "A four-year study of more than 5,700 children in Belo Horizonte, "
                      "Brazil, found Wolbachia-carrying mosquitoes cut dengue and "
                      "chikungunya infections by about 69%.",
                      sans(15), tw3, spacing=2)
    d.text((tx3, y3 + 4), "Source: Associated Press", font=sans(12),
           fill=GREY)

    # ---- footer
    rule(d, MARGIN, 968, W - MARGIN, 1)
    foot = "Every story above was reported on Saturday 21 November 2026  \u00b7  Drawn entirely with code \u2014 no photographs"
    ff = sans(13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 976), foot, font=ff, fill=GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else "."
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
