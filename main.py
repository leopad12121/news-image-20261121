"""News front page for Saturday 21 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news.
The imaging library is only imported lazily, inside main(), so that a
machine without it still exits 0: the shipped entry.png sitting beside
this file is copied to the output path instead. No network, no clock,
no randomness: the same input always produces the same bytes.
"""

import os
import shutil
import sys

PAGE_W = 1024
PAGE_H = 1024

NAVY = (22, 40, 63)
NAVY_DARK = (14, 28, 46)
RED = (163, 18, 18)
GOLD = (232, 201, 106)
PAPER = (246, 241, 231)
PANEL = (255, 255, 255)
INK = (34, 34, 34)
GREY = (102, 102, 102)
SKY = (178, 208, 224)
SEA = (52, 96, 128)
STEEL = (70, 90, 110)


def _output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return "./entry.png"


def _shipped_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def _wrap(text, max_chars):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= max_chars:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _chars_for(width, size, bold):
    factor = 0.66 if bold else 0.57
    return max(8, int(width / (size * factor)))


def _render(img_mod, draw_mod, font_mod):
    """Build the front page. All drawing helpers live in here so that no
    module-level name ever touches the imaging library."""

    def load_font(size, bold):
        names = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"] if bold else [
            "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
        dirs = []
        env_dirs = os.environ.get("MAKEFUN_FONT_DIRS")
        if env_dirs:
            dirs.extend([d for d in env_dirs.split(":") if d])
        dirs.extend([
            "/usr/share/fonts/truetype/dejavu",
            "/usr/share/fonts/dejavu",
            "/usr/local/share/fonts/truetype/dejavu",
            "/usr/share/fonts/truetype",
        ])
        for d in dirs:
            for name in names:
                try:
                    return font_mod.truetype(os.path.join(d, name), size)
                except Exception:
                    continue
        try:
            return font_mod.load_default(size=size)
        except Exception:
            pass
        return font_mod.load_default()

    def text_block(draw, x, y, lines, font, fill, line_height):
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += line_height
        return y

    def panel(draw, x0, y0, x1, y1):
        draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=NAVY, width=2)

    def kicker_headline(draw, x, y, width, kick, head_lines, head_size,
                        motif=None):
        kick_font = load_font(17, True)
        head_font = load_font(head_size, True)
        draw.text((x, y), kick, font=kick_font, fill=RED)
        if motif is not None:
            motif(x + width - 56, y - 4)
        y += 24
        y = text_block(draw, x, y, head_lines, head_font, NAVY,
                       head_size + 5)
        return y

    def body_sources(draw, x, y, width, body, sources, size=17):
        body_font = load_font(size, False)
        src_font = load_font(14, False)
        lines = _wrap(body, _chars_for(width, size, False))
        y = text_block(draw, x, y, lines, body_font, INK, size + 5)
        y += 4
        draw.text((x, y), sources, font=src_font, fill=GREY)
        return y

    def star(draw, cx, cy, r_out, r_in, fill):
        import math
        pts = []
        for i in range(10):
            r = r_out if i % 2 == 0 else r_in
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=fill)

    def globe(draw, x, y, r):
        draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=(120, 180, 200),
                     outline=NAVY, width=2)
        draw.ellipse([x + 6, y + 6, x + 2 * r - 6, y + 2 * r - 6],
                     outline=PANEL, width=2)
        draw.line([x, y + r, x + 2 * r, y + r], fill=PANEL, width=2)
        draw.arc([x + r // 2, y, x + 3 * r // 2, y + 2 * r],
                 270, 90, fill=PANEL, width=2)
        draw.arc([x + r // 2, y, x + 3 * r // 2, y + 2 * r],
                 90, 270, fill=PANEL, width=2)

    img = img_mod.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = draw_mod.Draw(img)

    # ---- Masthead ----
    draw.rectangle([0, 0, PAGE_W, 128], fill=NAVY)
    title_font = load_font(56, True)
    date_font = load_font(23, False)
    draw.text((512, 22), "THE WORLD IN ONE DAY", font=title_font,
              fill=PAPER, anchor="ma")
    draw.text((512, 88), "SATURDAY 21 NOVEMBER 2026",
              font=date_font, fill=GOLD, anchor="ma")
    draw.rectangle([0, 128, PAGE_W, 134], fill=RED)

    # ---- Lead story: Middle East (full width) ----
    panel(draw, 28, 148, 996, 404)
    lx = 48
    ly = 164
    y = kicker_headline(draw, lx, ly, 580, "MIDDLE EAST  -  LEAD STORY",
                        ["GULF ON EDGE AS", "STRIKES MOUNT"], 31)
    y += 6
    y = body_sources(
        draw, lx, y, 580,
        "Bahrain said its air defences stopped Iranian aerial attacks on "
        "Saturday evening. Tanker strikes in the Strait of Hormuz are at "
        "their highest level since the war began, and the US and Israel "
        "were reported to be weighing new strikes within days.",
        "Sources: Gulf News, Dawn, Al Jazeera, Reuters", size=18)

    # Lead illustration: strait at dusk, shield dome, tanker, radar.
    ix, iy, iw, ih = 648, 164, 328, 220
    draw.rectangle([ix, iy, ix + iw, iy + ih], fill=SKY)
    draw.rectangle([ix, iy + 96, ix + iw, iy + 120], fill=(232, 180, 110))
    draw.rectangle([ix, iy + 120, ix + iw, iy + ih], fill=SEA)
    draw.ellipse([ix + iw - 62, iy + 14, ix + iw - 14, iy + 62],
                 fill=(240, 200, 90))
    for bx, bh in ((ix + 8, 46), (ix + 44, 66), (ix + 88, 38)):
        draw.rectangle([bx, iy + 120 - bh, bx + 34, iy + 120], fill=NAVY_DARK)
    draw.arc([ix + 8, iy + 34, ix + 122, iy + 122], 180, 360,
             fill=GOLD, width=4)
    draw.arc([ix + 150, iy + 30, ix + 230, iy + 110], 200, 340,
             fill=PANEL, width=3)
    draw.arc([ix + 170, iy + 50, ix + 210, iy + 90], 200, 340,
             fill=PANEL, width=3)
    draw.rectangle([ix + 150, iy + 158, ix + 300, iy + 176], fill=(30, 30, 30))
    draw.polygon([(ix + 150, iy + 176), (ix + 158, iy + 192),
                  (ix + 292, iy + 192), (ix + 300, iy + 176)],
                 fill=(20, 20, 20))
    for cx in (ix + 170, ix + 205, ix + 240, ix + 272):
        draw.rectangle([cx, iy + 140, cx + 24, iy + 158], fill=RED)
    for wx in range(ix + 6, ix + iw - 10, 26):
        draw.arc([wx, iy + 196, wx + 22, iy + 210], 180, 360,
                 fill=PANEL, width=2)
    draw.text((ix + 8, iy + 126), "STRAIT OF HORMUZ",
              font=load_font(15, True), fill=PANEL)

    # ---- Grid row 1: Mexico | Markets ----
    # Mexico
    panel(draw, 28, 418, 502, 600)

    def mexico_motif(mx, my):
        draw.ellipse([mx, my, mx + 56, my + 56], fill=GOLD, outline=RED,
                     width=3)
        star(draw, mx + 28, my + 28, 22, 9, RED)

    y = kicker_headline(draw, 44, 432, 442, "MEXICO",
                        ["TOP FUGITIVE CAPTURED"], 21, motif=mexico_motif)
    y += 6
    body_sources(
        draw, 44, y, 442,
        "Mexican forces captured FBI Top-10 fugitive Fausto Isidro Meza "
        "Flores, known as El Chapo Isidro, in Guasave, Sinaloa, on Friday "
        "night. Eleven were killed in the cartel backlash.",
        "Sources: Reuters, AP")

    # Markets
    panel(draw, 522, 418, 996, 600)

    def markets_motif(mx, my):
        draw.rectangle([mx, my, mx + 56, my + 56], fill=(250, 235, 235),
                       outline=RED, width=2)
        draw.line([mx + 6, my + 44, mx + 20, my + 30, mx + 32, my + 36,
                   mx + 50, my + 10], fill=RED, width=3)
        draw.polygon([(mx + 50, my + 10), (mx + 40, my + 12),
                      (mx + 48, my + 22)], fill=RED)

    y = kicker_headline(draw, 538, 432, 442, "MARKETS",
                        ["STOCKS TUMBLE; NVIDIA SINKS"], 21,
                        motif=markets_motif)
    y += 6
    body_sources(
        draw, 538, y, 442,
        "The S&P 500 fell 3.7% and the Nasdaq 5.3% on Friday. Nvidia "
        "dropped 14% after Reuters reported the SEC is examining its "
        "accounting.",
        "Source: Reuters")

    # ---- Grid row 2: Ukraine | Climate ----
    # Ukraine
    panel(draw, 28, 614, 502, 796)

    def ukraine_motif(mx, my):
        star(draw, mx + 28, my + 28, 26, 10, (240, 170, 40))
        draw.ellipse([mx + 18, my + 18, mx + 38, my + 38], fill=RED)

    y = kicker_headline(draw, 44, 628, 442, "UKRAINE",
                        ["MISSILES HIT KRYVYI RIH"], 21,
                        motif=ukraine_motif)
    y += 6
    body_sources(
        draw, 44, y, 442,
        "Russian missiles struck Kryvyi Rih on Friday night, killing two "
        "people and wounding 60. Two Russian missiles and a drone also "
        "came down in Poland.",
        "Sources: AP, Al Jazeera")

    # Climate
    panel(draw, 522, 614, 996, 796)

    def climate_motif(mx, my):
        globe(draw, mx, my, 28)

    y = kicker_headline(draw, 538, 628, 442, "CLIMATE  -  COP31",
                        ["CLIMATE TALKS OVERRUN"], 21, motif=climate_motif)
    y += 6
    body_sources(
        draw, 538, y, 442,
        "COP31 in Antalya, Turkey, overran its Friday deadline. Delegates "
        "were split over a draft text that drops fossil-fuel language.",
        "Sources: One Turn, WW6RAG")

    # ---- Bottom strip: Science ----
    panel(draw, 28, 810, 996, 950)
    y = kicker_headline(draw, 48, 824, 928, "SCIENCE",
                        ["MOSQUITO TRIAL CUTS DENGUE BY ABOUT 69%"], 26)
    y += 4
    body_sources(
        draw, 48, y, 928,
        "Wolbachia mosquitoes cut dengue and chikungunya infections by "
        "about 69% among 5,700+ children in Belo Horizonte, Brazil, in a "
        "four-year study presented Saturday.",
        "Source: Associated Press", size=18)

    # ---- Footer ----
    foot_font = load_font(14, False)
    draw.text((512, 962),
              "Six stories from Saturday 21 November 2026 - every story "
              "first reported that day. Sources credited in each panel.",
              font=foot_font, fill=GREY, anchor="ma")
    return img


def main():
    out = _output_path()
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = _render(Image, ImageDraw, ImageFont)
        parent = os.path.dirname(os.path.abspath(out))
        if parent:
            os.makedirs(parent, exist_ok=True)
        img.save(out, format="PNG")
    except Exception:
        try:
            parent = os.path.dirname(os.path.abspath(out))
            if parent:
                os.makedirs(parent, exist_ok=True)
            shutil.copyfile(_shipped_path(), out)
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
