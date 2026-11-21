#!/usr/bin/env python3
"""Draw the front page for 21 November 2026 (news-image-20261121, round 1).

A 1024x1024 newspaper front page rendered entirely with Python + PIL.
Deterministic: fixed text, fixed colours, fixed geometry. No network,
no timestamps, no randomness -- running it twice yields a byte-identical
entry.png.

Round 1 note: built in the first hours of 21 November (UTC), so the five
lead stories are the day's news as reported in 21 November editions
(Dawn, Al Jazeera, The Manila Times). A round 2 rebuild from the full
day's news follows tomorrow.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
PAGE = 1024
MARGIN = 46
CONTENT = PAGE - 2 * MARGIN          # 932
GUTTER = 30
COLUMN = (CONTENT - GUTTER) // 2     # 451

PAPER = (248, 244, 235)
INK = (16, 16, 16)
GREY = (88, 84, 76)
RED = (158, 28, 28)
RULE = (58, 56, 50)
FAINT = (178, 172, 160)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONTS + name, size)


SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "SATURDAY, 21 NOVEMBER 2026  -  THE DAY'S WORLD NEWS IN A SINGLE IMAGE"

LEAD = {
    "kicker": "LEAD STORY - YEMEN AND SAUDI ARABIA",
    "headline": "Houthis claim new strikes on Saudi Arabia after Hodeidah hit",
    "body": (
        "The Saudi-led coalition said it struck the Red Sea port of Hodeidah "
        "to destroy Houthi capabilities. The Houthis say they then hit a "
        "power station and a port in southern Saudi Arabia, and warned "
        "airlines to stay out of Saudi airspace."
    ),
}

SECOND = {
    "kicker": "COPENHAGEN - ESPIONAGE",
    "headline": "Denmark expels Russian diplomat over alleged assassination plot",
    "body": (
        "Denmark says Russian intelligence planned to kill Ukrainian-American "
        "rapper Kyivstoner at a September concert near Copenhagen. Two men "
        "are charged with attempted murder; Russia denies the claim."
    ),
}

THIRD = {
    "kicker": "PARIS - UKRAINE TALKS",
    "headline": "EU leaders demand a full role in Ukraine talks",
    "body": (
        "European leaders would travel to Moscow for Ukraine talks if given "
        "a full role, France said, after President Putin invited them. "
        "President Zelensky warned that going to Moscow would be a mistake."
    ),
}

FOURTH = {
    "kicker": "WARSAW - NATO",
    "headline": "Poland calls Russian missile crash an intentional provocation",
    "body": (
        "A Russian cruise missile came down in eastern Poland during the "
        "overnight barrage of Ukraine, near European military exercises. "
        "NATO chief Mark Rutte called it clearly dangerous and visits "
        "Warsaw on Saturday."
    ),
}

FIFTH = {
    "kicker": "WASHINGTON - 2028",
    "headline": "Trump floats his chief of staff for president in 2028",
    "body": (
        "At a White House briefing President Trump jokingly asked his new "
        "chief of staff Stephen Miller, \"Do you wanna run for president?\" "
        "praising him over Vice President Vance and Secretary Rubio, who "
        "stood behind him."
    ),
}

ALSO_ITEMS = [
    "US court jails Nikhil Gupta for 19 1/2 years over a murder-for-hire plot.",
    "Iraqi forces move into a pro-Iran militia stronghold south of Baghdad.",
    "Britain and the EU seal a reset deal on food trade and youth mobility.",
    "Alcaraz beats Medvedev to reach the last four of the ATP Finals.",
]

FOOTER = "Drawn entirely with Python and PIL - no photographs, no network.  -  21 November 2026"


# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_rule(draw, y, thickness=2, x0=MARGIN, x1=PAGE - MARGIN):
    draw.rectangle([x0, y, x1, y + thickness - 1], fill=RULE)
    return y + thickness


def centred_x(draw, text, font):
    return (PAGE - draw.textlength(text, font=font)) / 2


def draw_story(draw, x, y, story, width, head_size=25, body_size=17):
    """One column story: red kicker, bold headline, serif body.

    Returns the y just below the body text.
    """
    kicker_font = load(SANS_BOLD, 16)
    head_font = load(SERIF_BOLD, head_size)
    body_font = load(SERIF, body_size)

    draw.text((x, y), story["kicker"], font=kicker_font, fill=RED)
    y += 23

    head_lines = wrap_text(draw, story["headline"], head_font, width)
    y = draw_lines(draw, x, y, head_lines, head_font, INK, head_size + 6)
    y += 4

    body_lines = wrap_text(draw, story["body"], body_font, width)
    y = draw_lines(draw, x, y, body_lines, body_font, INK, body_size + 5)
    return y


# ---------------------------------------------------------------- page
def build(out_path):
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)

    y = 24

    # Masthead
    mast_font = load(SERIF_BOLD, 58)
    draw.text((centred_x(draw, MASTHEAD, mast_font), y), MASTHEAD,
              font=mast_font, fill=INK)
    y += 68
    y = draw_rule(draw, y, thickness=3)
    y += 2
    y = draw_rule(draw, y, thickness=1)
    y += 9

    # Dateline
    date_font = load(SANS_BOLD, 17)
    draw.text((centred_x(draw, DATELINE, date_font), y), DATELINE,
              font=date_font, fill=GREY)
    y += 25
    y = draw_rule(draw, y)
    y += 12

    # Lead story, full width
    lead_kicker = load(SANS_BOLD, 17)
    draw.text((MARGIN, y), LEAD["kicker"], font=lead_kicker, fill=RED)
    y += 25

    lead_head = load(SERIF_BOLD, 38)
    head_lines = wrap_text(draw, LEAD["headline"], lead_head, CONTENT)
    y = draw_lines(draw, MARGIN, y, head_lines, lead_head, INK, 45)
    y += 5

    lead_body = load(SERIF, 19)
    body_lines = wrap_text(draw, LEAD["body"], lead_body, CONTENT)
    y = draw_lines(draw, MARGIN, y, body_lines, lead_body, INK, 25)
    y += 10
    y = draw_rule(draw, y)
    y += 10

    # Middle row: two columns
    left_end = draw_story(draw, MARGIN, y, SECOND, COLUMN)
    right_end = draw_story(draw, MARGIN + COLUMN + GUTTER, y,
                           THIRD, COLUMN)
    y = max(left_end, right_end) + 10
    y = draw_rule(draw, y)
    y += 10

    # Bottom row: two columns
    left_end = draw_story(draw, MARGIN, y, FOURTH, COLUMN)
    right_end = draw_story(draw, MARGIN + COLUMN + GUTTER, y,
                           FIFTH, COLUMN)
    y = max(left_end, right_end) + 10
    y = draw_rule(draw, y)
    y += 10

    # "Also in the news" strip
    strip_kicker = load(SANS_BOLD, 17)
    draw.text((MARGIN, y), "ALSO IN THE NEWS", font=strip_kicker, fill=RED)
    y += 25

    item_font = load(SERIF, 17)
    for item in ALSO_ITEMS:
        lines = wrap_text(draw, "- " + item, item_font, CONTENT)
        y = draw_lines(draw, MARGIN, y, lines, item_font, INK, 22)
        y += 2

    # Footer
    draw_rule(draw, PAGE - 36)
    foot_font = load(SANS, 14)
    draw.text((centred_x(draw, FOOTER, foot_font), PAGE - 27), FOOTER,
              font=foot_font, fill=GREY)

    image.save(out_path, format="PNG")
    print("wrote %s (1024x1024)" % out_path)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "entry.png"))
