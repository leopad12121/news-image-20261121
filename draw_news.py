"""Draw a one-page newspaper front page for 21 November 2026.

Everything is deterministic: fixed text, fixed colours, fixed geometry,
no network, no randomness, no timestamps. Rendered with PIL only.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 44
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (251, 243, 228)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (85, 85, 85)
RULE = (17, 17, 17)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _split_words(text):
    return text.split()


def _wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in _split_words(text):
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


def _fit_lines(draw, text, font, max_width, max_lines):
    """Wrap text and trim to max_lines, adding an ellipsis if trimmed."""
    lines = _wrap(draw, text, font, max_width)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    last = kept[-1]
    while last and draw.textlength(last + "...", font=font) > max_width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    kept[-1] = last + "..."
    return kept


def _draw_lines(draw, lines, x, y, font, fill, spacing):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def _rule(draw, y, width=3):
    draw.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=RULE, width=width)


def _centred(draw, text, y, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((PAGE_W - w) / 2, y), text, font=font, fill=fill)


LEAD = {
    "kicker": "LEAD STORY - YEMEN AND SAUDI ARABIA",
    "headline": "Houthis claim new strikes on Saudi Arabia after Hodeidah hit",
    "body": (
        "The Saudi-led coalition struck the Red Sea port of Hodeidah to "
        "destroy Houthi capabilities. The Houthis say they then hit a power "
        "station and a port in southern Saudi Arabia and warned airlines to "
        "stay out of Saudi airspace."
    ),
}

STORIES = [
    {
        "kicker": "COPENHAGEN - ESPIONAGE",
        "headline": "Denmark expels Russian diplomat over alleged assassination plot",
        "body": (
            "Denmark says Russian intelligence planned to kill "
            "Ukrainian-American rapper Kyivstoner at a September concert "
            "near Copenhagen. Two men are charged with attempted murder."
        ),
    },
    {
        "kicker": "PARIS - UKRAINE TALKS",
        "headline": "EU leaders demand a full role in Ukraine talks",
        "body": (
            "European leaders would travel to Moscow for Ukraine talks if "
            "given a full role, France said, after President Putin invited "
            "them. President Zelensky warned that going to Moscow would be "
            "a mistake."
        ),
    },
    {
        "kicker": "WARSAW - NATO",
        "headline": "Poland calls Russian missile crash an intentional provocation",
        "body": (
            "A Russian cruise missile came down in eastern Poland during "
            "the overnight barrage of Ukraine, near European military "
            "exercises. NATO chief Mark Rutte called it clearly dangerous "
            "and visits Warsaw on Saturday."
        ),
    },
    {
        "kicker": "WASHINGTON - 2028",
        "headline": "Trump floats his chief of staff for president in 2028",
        "body": (
            "At a White House briefing President Trump jokingly asked his "
            "new chief of staff Stephen Miller, 'Do you wanna run for "
            "president?', praising him over Vice President Vance and "
            "Secretary Rubio."
        ),
    },
]

STRIP_ITEMS = [
    "US court jails Nikhil Gupta for 19 1/2 years",
    "Iraqi forces move into a pro-Iran militia stronghold",
    "Britain and the EU seal a reset deal",
    "Alcaraz reaches the ATP Finals last four",
]


def _story_lines(draw, story, width, head_size, body_size):
    head_font = _font(SERIF_BOLD, head_size)
    body_font = _font(SANS, body_size)
    head_lines = _fit_lines(draw, story["headline"], head_font, width, 3)
    body_lines = _fit_lines(draw, story["body"], body_font, width, 5)
    return head_lines, body_lines


def _story_height(draw, story, width, head_size, body_size):
    head_lines, body_lines = _story_lines(
        draw, story, width, head_size, body_size
    )
    return 22 + len(head_lines) * (head_size + 4) + 4 + len(body_lines) * (body_size + 4)


def _draw_story(draw, story, x, y, width, head_size, body_size):
    kicker_font = _font(SANS_BOLD, 16)
    head_font = _font(SERIF_BOLD, head_size)
    body_font = _font(SANS, body_size)
    head_lines, body_lines = _story_lines(
        draw, story, width, head_size, body_size
    )
    draw.text((x, y), story["kicker"], font=kicker_font, fill=RED)
    y += 22
    y = _draw_lines(draw, head_lines, x, y, head_font, INK, 4)
    y += 4
    y = _draw_lines(draw, body_lines, x, y, body_font, INK, 4)
    return y


def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    mast_font = _font(SERIF_BOLD, 62)
    _centred(draw, "THE WORLD IN ONE DAY", 22, mast_font, INK)
    _rule(draw, 100, 3)
    _rule(draw, 106, 1)

    # Dateline.
    date_font = _font(SANS_BOLD, 19)
    _centred(
        draw,
        "SATURDAY, 21 NOVEMBER 2026  -  THE DAY'S WORLD NEWS IN A SINGLE IMAGE",
        116,
        date_font,
        GREY,
    )
    _rule(draw, 146, 2)

    # Lead story, full width; the rule follows its measured height.
    y = 158
    y = _draw_story(draw, LEAD, MARGIN, y, CONTENT_W, 36, 19)
    _rule(draw, y + 12, 2)

    # Four stories in a two-by-two grid. The second row starts below
    # the taller of the two first-row stories, so no body can run into
    # the row beneath it.
    col_w = (CONTENT_W - 40) // 2
    col_x = [MARGIN, MARGIN + col_w + 40]
    row1_y = y + 26
    row1_h = max(
        _story_height(draw, STORIES[0], col_w, 26, 17),
        _story_height(draw, STORIES[1], col_w, 26, 17),
    )
    row2_y = row1_y + row1_h + 14
    row2_h = max(
        _story_height(draw, STORIES[2], col_w, 26, 17),
        _story_height(draw, STORIES[3], col_w, 26, 17),
    )
    for i, story in enumerate(STORIES):
        top = row1_y if i < 2 else row2_y
        _draw_story(draw, story, col_x[i % 2], top, col_w, 26, 17)
    strip_rule_y = row2_y + row2_h + 14
    _rule(draw, strip_rule_y, 2)

    # "Also in the news" strip, then a clear gap before the footer.
    strip_font = _font(SANS, 17)
    strip_head = _font(SANS_BOLD, 18)
    y = strip_rule_y + 12
    draw.text((MARGIN, y), "ALSO IN THE NEWS", font=strip_head, fill=RED)
    y += 28
    for item in STRIP_ITEMS:
        lines = _fit_lines(draw, "- " + item, strip_font, CONTENT_W, 1)
        y = _draw_lines(draw, lines, MARGIN, y, strip_font, INK, 2)
        y += 3

    # Footer, pinned near the bottom with the strip ending above it.
    _rule(draw, 968, 2)
    foot_font = _font(SANS, 15)
    _centred(
        draw,
        "Drawn entirely with Python and PIL - no photographs, no network. - 21 November 2026",
        978,
        foot_font,
        GREY,
    )
    return img


if __name__ == "__main__":
    render().save("entry.png")
