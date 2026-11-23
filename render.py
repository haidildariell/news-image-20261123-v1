#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news broadsheet (1024x1024 PNG).

Fresh code written for news-image-20261123 v1. stdlib + Pillow at build time only;
the shipped entry (main.py) is a stdlib-only copy stub.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (247, 242, 231)
PAPER = (252, 248, 238)
INK = (26, 26, 26)
RED = (163, 22, 33)
TEAL = (15, 95, 92)
GOLD = (176, 132, 52)
GREY = (105, 100, 90)
RULE = (60, 55, 45)
LIGHT = (233, 226, 210)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, y, text, fnt, fill=INK, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.15)


def rule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# tag: CONFIRMED = officially confirmed; REPORTED = reported, not independently
# verified; CLAIM = one side's claim. region feeds the region bar counts.
LEADS = [
    dict(n=1, region="AMERICAS", tag="CONFIRMED", src="AP / Reuters",
         scene="capitol",
         head="DEMOCRATS\u2019 BIGGEST HOUSE MAJORITY SINCE 1992",
         body="At least 258 seats \u2014 a 44-seat gain \u2014 as Hubbard beats Foxx in North Carolina. Four races still uncalled."),
    dict(n=2, region="AMERICAS", tag="CONFIRMED", src="AP",
         scene="heli",
         head="\u2018CHAPO ISIDRO\u2019 SEIZED IN SINALOA",
         body="FBI Top 10 fugitive Meza-Flores captured in Guasave; 11 killed as gunmen hit back across the state."),
    dict(n=3, region="EUROPE", tag="CONFIRMED", src="Reuters",
         scene="stadium",
         head="LIVERPOOL ROUT 10-MAN UNITED 4\u20130",
         body="Pochettino\u2019s first game as United boss ends in humiliation at Anfield. Yoro sent off after 8 minutes."),
]

SMALL = [
    dict(n=4, region="WORLD", tag="CONFIRMED", src="NPR / UN", scene="robot",
         head="NO DEAL ON KILLER ROBOTS",
         body="UN talks end with two more years of talks, not binding rules; accord due 2028."),
    dict(n=5, region="MIDDLE EAST", tag="CONFIRMED", src="Reuters", scene="flame",
         head="EISENKOT: ARSON IS \u2018JEWISH TERRORISM\u2019",
         body="Overnight arson hits West Bank villages; Netanyahu rival blames Ben-Gvir."),
    dict(n=6, region="AFRICA", tag="REPORTED", src="AFP", scene="huts",
         head="24 CIVILIANS KILLED IN S. SUDAN",
         body="SPLA-IO blamed for raid on Bol Bol Boma camp in Warrap; toll rose to 24."),
    dict(n=7, region="MIDDLE EAST", tag="REPORTED", src="UKMTO", scene="tanker",
         head="TANKER IN GULF OF OMAN INCIDENT",
         body="UKMTO reports a tanker in an incident with military forces near Chabahar."),
    dict(n=8, region="AFRICA", tag="CONFIRMED", src="Reuters / WHO", scene="hospital",
         head="FIGHTING TRAPS EBOLA TEAMS IN CONGO",
         body="WHO: clashes near an Ituri hospital force staff to shelter for over 24 hours."),
    dict(n=9, region="AMERICAS", tag="CONFIRMED", src="Reuters", scene="chip",
         head="US SEEKS NVIDIA ANSWERS ON CHINA CHIPS",
         body="Bessent: \u201cWe need to know who was in charge of compliance\u201d after Huang quit."),
    dict(n=10, region="EUROPE", tag="CLAIM", src="AP", scene="mic",
         head="RAPPER \u2018TWICE TARGETED BY RUSSIA\u2019",
         body="Poland says Kyivstoner was targeted in August; Denmark expels an official."),
    dict(n=11, region="ASIA-PACIFIC", tag="CONFIRMED", src="Reuters", scene="flags",
         head="MYANMAR CALLS ASEAN RULING \u2018UNFAIR\u2019",
         body="Army-backed government protests exclusion from summits after the Manila decision."),
    dict(n=12, region="EUROPE", tag="CONFIRMED", src="Reuters", scene="crowd",
         head="THOUSANDS MARCH IN LISBON",
         body="CGTP rally against living costs, low wages and housing; inflation 3.8%."),
    dict(n=13, region="ASIA-PACIFIC", tag="CONFIRMED", src="MEA", scene="handshake",
         head="NEPAL PM MEETS MODI IN DELHI",
         body="Balendra Shah holds talks today on energy, trade and a $2bn package."),
    dict(n=14, region="ASIA-PACIFIC", tag="CONFIRMED", src="Korea JoongAng Daily", scene="exam",
         head="KOREA MINISTER QUITS OVER AI EXAM CHAOS",
         body="Choi Kyo-jin resigns after CSAT anti-cheating chaos; 111 cases caught."),
    dict(n=15, region="AMERICAS", tag="CONFIRMED", src="Reuters", scene="plane",
         head="DELTA GLITCH GROUNDS ATLANTA FLIGHTS",
         body="Weight-and-balance outage forces manual loading; ~1,000 flights delayed."),
]

ALSO = [
    (16, "AMERICAS", "CONFIRMED", "PEOPLE", "Miley Cyrus weds Maxx Morando in Palm Springs"),
    (17, "AMERICAS", "CONFIRMED", "ESPN", "Broncos great Tom Jackson dies at 75"),
    (18, "EUROPE", "CONFIRMED", "AP", "Denmark expels Russian defence attach\u00e9"),
    (19, "MIDDLE EAST", "CLAIM", "Iranian media", "Two supertankers ablaze after \u2018mine strikes\u2019"),
    (20, "MIDDLE EAST", "CLAIM", "IRGC", "Iran says it downed a US MQ-9 drone"),
    (21, "AMERICAS", "CONFIRMED", "House committee", "879,868 AI chips cleared for China firms"),
    (22, "ASIA-PACIFIC", "CONFIRMED", "KJD", "Lee vows to close AI-cheating loopholes"),
    (23, "EUROPE", "CONFIRMED", "The Times", "Hull stun Brighton 2\u20130"),
    (24, "AMERICAS", "CONFIRMED", "AP", "GOP holds at least 173 House seats"),
    (25, "MIDDLE EAST", "CONFIRMED", "UN", "410 settler attacks since September"),
    (26, "AFRICA", "REPORTED", "WHO", "Ebola cases 11,613; deaths 5,678"),
    (27, "ASIA-PACIFIC", "REPORTED", "MEA", "Nepal\u2013India eye Janakpur\u2013Ayodhya train"),
    (28, "ASIA-PACIFIC", "CONFIRMED", "KJD", "Seoul offers $75,000 for cheating tips"),
    (29, "EUROPE", "CONFIRMED", "Eurostat", "Portugal wages 37% below EU average"),
    (30, "ASIA-PACIFIC", "REPORTED", "Reuters", "Min Aung Hlaing weighs ASEAN future"),
    (31, "WORLD", "CONFIRMED", "UN", "Guterres\u2019 2026 robot-weapons deadline passes"),
    (32, "AMERICAS", "CONFIRMED", "FBI", "$5m FBI reward stood on Chapo Isidro"),
    (33, "EUROPE", "CONFIRMED", "Opta", "United 19th, one win in 11 games"),
    (34, "AMERICAS", "CONFIRMED", "Delta", "Delta blames glitch for 70% of delays"),
    (35, "MIDDLE EAST", "CONFIRMED", "Reuters", "Eisenkot blames Ben-Gvir, Smotrich"),
    (36, "ASIA-PACIFIC", "CONFIRMED", "MEA", "Shah leads 34-strong delegation"),
    (37, "AMERICAS", "CONFIRMED", "PEOPLE", "Miley\u2019s wedding: Wayne Coyne officiates, 140 guests"),
]

STATS = [
    ("258", "DEM HOUSE SEATS"),
    ("4\u20130", "LIVERPOOL v MAN UTD"),
    ("24", "KILLED IN S. SUDAN"),
    ("11", "KILLED IN SINALOA"),
    ("879,868", "AI CHIPS CLEARED"),
    ("111", "CSAT CHEATING CASES"),
]

TIMELINE = [
    ("17:48Z", "Bessent: Nvidia answers sought"),
    ("18:44Z", "Eisenkot condemns arson"),
    ("19:07Z", "UKMTO: tanker incident"),
    ("19:16Z", "Delta delays Atlanta flights"),
    ("22:31Z", "UN robot talks end, no deal"),
    ("23:24Z", "S. Sudan toll rises to 24"),
]

# pin positions (lon, lat) for the 15 illustrated stories; nudged where the
# real places cluster so the numbered pins do not overlap on the small map
PINS = {
    1: (-77.0, 38.9), 2: (-107.4, 25.6), 3: (-8.0, 56.0),
    4: (0.0, 46.0), 5: (36.0, 31.0), 6: (24.0, 9.0),
    7: (60.6, 25.3), 8: (32.0, 0.0), 9: (-122.0, 37.4),
    10: (18.0, 59.0), 11: (96.1, 19.8), 12: (-12.0, 35.0),
    13: (77.2, 28.6), 14: (126.98, 37.57), 15: (-84.43, 33.64),
}

# ---------------------------------------------------------------- scenes
# Each scene draws a small flat illustration inside box (x, y, w, h).
# Coordinates are relative fractions of the box so the same scene works at
# lead size and at small-story size.

def _sky(d, x, y, w, h, top, bot):
    for i in range(int(h)):
        t = i / max(1, int(h) - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def scene_capitol(d, x, y, w, h):
    _sky(d, x, y, w, h, (168, 200, 220), (232, 236, 228))
    d.rectangle([x + w * .30, y + h * .62, x + w * .70, y + h * .80], fill=(240, 234, 220))
    for i in range(5):
        cx = x + w * (.34 + i * .08)
        d.rectangle([cx, y + h * .64, cx + w * .03, y + h * .80], fill=(205, 195, 175))
    d.rectangle([x + w * .28, y + h * .58, x + w * .72, y + h * .63], fill=(225, 218, 205))
    d.polygon([(x + w * .40, y + h * .58), (x + w * .60, y + h * .58),
               (x + w * .50, y + h * .34)], fill=(248, 244, 234))
    d.ellipse([x + w * .43, y + h * .22, x + w * .57, y + h * .44], fill=(250, 246, 236))
    d.line([(x + w * .50, y + h * .22), (x + w * .50, y + h * .10)], fill=(90, 85, 75), width=2)
    d.polygon([(x + w * .50, y + h * .10), (x + w * .60, y + h * .15),
               (x + w * .50, y + h * .20)], fill=(180, 40, 50))
    d.rectangle([x, y + h * .80, x + w, y + h], fill=(90, 120, 90))
    d.rectangle([x + w * .05, y + h * .88, x + w * .95, y + h * .92], fill=(240, 240, 240))


def scene_heli(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 170, 120), (240, 210, 160))
    d.polygon([(x, y + h), (x + w * .30, y + h * .35), (x + w * .55, y + h),
               (x + w * .75, y + h * .45), (x + w, y + h)], fill=(90, 110, 70))
    d.polygon([(x + w * .55, y + h), (x + w * .75, y + h * .45), (x + w, y + h)],
              fill=(70, 90, 55))
    d.ellipse([x + w * .42, y + h * .18, x + w * .62, y + h * .38], fill=(40, 40, 40))
    d.rectangle([x + w * .60, y + h * .26, x + w * .86, y + h * .34], fill=(40, 40, 40))
    d.line([(x + w * .30, y + h * .22), (x + w * .74, y + h * .22)], fill=(30, 30, 30), width=3)
    d.line([(x + w * .50, y + h * .38), (x + w * .50, y + h * .52)], fill=(30, 30, 30), width=3)
    d.line([(x + w * .44, y + h * .52), (x + w * .56, y + h * .52)], fill=(30, 30, 30), width=3)


def scene_stadium(d, x, y, w, h):
    _sky(d, x, y, w, h, (120, 160, 200), (200, 220, 235))
    d.rectangle([x, y + h * .45, x + w, y + h], fill=(40, 130, 60))
    d.rectangle([x, y + h * .45, x + w, y + h * .55], fill=(52, 148, 72))
    d.ellipse([x + w * .30, y + h * .55, x + w * .70, y + h * .95], fill=(240, 240, 240))
    d.ellipse([x + w * .40, y + h * .65, x + w * .60, y + h * .85], fill=(250, 250, 250))
    d.polygon([(x + w * .44, y + h * .70), (x + w * .50, y + h * .66),
               (x + w * .56, y + h * .70), (x + w * .54, y + h * .78),
               (x + w * .46, y + h * .78)], fill=(30, 30, 30))
    d.rectangle([x + w * .06, y + h * .18, x + w * .94, y + h * .45], fill=(210, 214, 218))
    for i in range(14):
        cx = x + w * (.08 + i * .062)
        d.ellipse([cx, y + h * .24, cx + w * .035, y + h * .30], fill=(180, 40, 50) if i % 3 == 0 else (60, 70, 90))
        d.ellipse([cx, y + h * .34, cx + w * .035, y + h * .40], fill=(40, 90, 160) if i % 3 == 1 else (200, 170, 60))


def scene_robot(d, x, y, w, h):
    _sky(d, x, y, w, h, (210, 215, 205), (240, 238, 225))
    d.rectangle([x + w * .32, y + h * .18, x + w * .68, y + h * .62], fill=(120, 125, 130))
    d.rectangle([x + w * .36, y + h * .24, x + w * .46, y + h * .34], fill=(60, 200, 190))
    d.rectangle([x + w * .54, y + h * .24, x + w * .64, y + h * .34], fill=(60, 200, 190))
    d.rectangle([x + w * .40, y + h * .44, x + w * .60, y + h * .50], fill=(60, 60, 60))
    d.line([(x + w * .42, y + h * .18), (x + w * .42, y + h * .08)], fill=(90, 90, 90), width=3)
    d.ellipse([x + w * .39, y + h * .04, x + w * .45, y + h * .10], fill=(200, 60, 60))
    d.line([(x + w * .58, y + h * .18), (x + w * .58, y + h * .08)], fill=(90, 90, 90), width=3)
    d.ellipse([x + w * .55, y + h * .04, x + w * .61, y + h * .10], fill=(200, 60, 60))
    d.rectangle([x + w * .38, y + h * .62, x + w * .62, y + h * .92], fill=(100, 105, 110))
    d.ellipse([x + w * .10, y + h * .70, x + w * .26, y + h * .86], fill=(250, 250, 250))
    d.ellipse([x + w * .74, y + h * .70, x + w * .90, y + h * .86], fill=(250, 250, 250))


def scene_flame(d, x, y, w, h):
    _sky(d, x, y, w, h, (30, 25, 35), (80, 40, 30))
    d.rectangle([x + w * .15, y + h * .55, x + w * .45, y + h * .88], fill=(90, 70, 50))
    d.polygon([(x + w * .12, y + h * .55), (x + w * .30, y + h * .35),
               (x + w * .48, y + h * .55)], fill=(70, 55, 40))
    d.polygon([(x + w * .55, y + h * .60), (x + w * .72, y + h * .42),
               (x + w * .88, y + h * .60)], fill=(80, 62, 45))
    d.rectangle([x + w * .55, y + h * .60, x + w * .88, y + h * .88], fill=(95, 75, 55))
    d.polygon([(x + w * .28, y + h * .55), (x + w * .36, y + h * .30),
               (x + w * .42, y + h * .55)], fill=(240, 120, 20))
    d.polygon([(x + w * .60, y + h * .60), (x + w * .68, y + h * .36),
               (x + w * .76, y + h * .60)], fill=(250, 160, 30))
    d.ellipse([x + w * .30, y + h * .62, x + w * .42, y + h * .78], fill=(255, 200, 60))
    d.ellipse([x + w * .62, y + h * .66, x + w * .72, y + h * .80], fill=(255, 200, 60))


def scene_huts(d, x, y, w, h):
    _sky(d, x, y, w, h, (220, 180, 110), (245, 220, 160))
    d.ellipse([x + w * .70, y + h * .08, x + w * .92, y + h * .30], fill=(250, 220, 120))
    d.rectangle([x, y + h * .70, x + w, y + h], fill=(170, 130, 80))
    for cx, cw in ((.12, .22), (.42, .26), (.72, .20)):
        d.polygon([(x + w * cx, y + h * .72), (x + w * (cx + cw / 2), y + h * .42),
                   (x + w * (cx + cw), y + h * .72)], fill=(120, 85, 50))
        d.rectangle([x + w * (cx + .02), y + h * .72, x + w * (cx + cw - .02), y + h * .92],
                    fill=(150, 110, 65))
    d.rectangle([x + w * .48, y + h * .78, x + w * .52, y + h * .92], fill=(60, 40, 25))


def scene_tanker(d, x, y, w, h):
    _sky(d, x, y, w, h, (150, 185, 210), (215, 230, 240))
    d.rectangle([x, y + h * .62, x + w, y + h], fill=(35, 90, 130))
    d.rectangle([x, y + h * .62, x + w, y + h * .68], fill=(70, 130, 170))
    d.rectangle([x + w * .12, y + h * .42, x + w * .88, y + h * .64], fill=(140, 40, 35))
    d.rectangle([x + w * .55, y + h * .28, x + w * .72, y + h * .42], fill=(240, 240, 235))
    d.rectangle([x + w * .58, y + h * .18, x + w * .62, y + h * .28], fill=(60, 60, 60))
    d.polygon([(x + w * .20, y + h * .42), (x + w * .30, y + h * .14),
               (x + w * .38, y + h * .42)], fill=(120, 120, 115))
    d.ellipse([x + w * .24, y + h * .06, x + w * .34, y + h * .16], fill=(90, 90, 90))
    d.rectangle([x + w * .05, y + h * .74, x + w * .30, y + h * .78], fill=(255, 255, 255))
    d.rectangle([x + w * .60, y + h * .82, x + w * .90, y + h * .86], fill=(255, 255, 255))


def scene_hospital(d, x, y, w, h):
    _sky(d, x, y, w, h, (190, 220, 215), (240, 244, 238))
    d.rectangle([x + w * .18, y + h * .30, x + w * .82, y + h * .88], fill=(250, 250, 248))
    d.rectangle([x + w * .18, y + h * .30, x + w * .82, y + h * .42], fill=(15, 95, 92))
    d.rectangle([x + w * .44, y + h * .52, x + w * .56, y + h * .76], fill=(200, 40, 40))
    d.rectangle([x + w * .38, y + h * .58, x + w * .62, y + h * .70], fill=(200, 40, 40))
    d.rectangle([x + w * .24, y + h * .82, x + w * .30, y + h * .88], fill=(60, 60, 60))
    d.rectangle([x + w * .70, y + h * .82, x + w * .76, y + h * .88], fill=(60, 60, 60))
    d.polygon([(x + w * .05, y + h * .88), (x + w * .12, y + h * .66),
               (x + w * .19, y + h * .88)], fill=(120, 150, 140))
    d.polygon([(x + w * .81, y + h * .88), (x + w * .88, y + h * .66),
               (x + w * .95, y + h * .88)], fill=(120, 150, 140))


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(35, 45, 60))
    d.rectangle([x + w * .28, y + h * .22, x + w * .72, y + h * .78], fill=(20, 25, 35))
    d.rectangle([x + w * .28, y + h * .22, x + w * .72, y + h * .78], outline=(200, 170, 60), width=3)
    d.rectangle([x + w * .40, y + h * .36, x + w * .60, y + h * .64], fill=(200, 170, 60))
    for i in range(5):
        px = x + w * (.32 + i * .09)
        d.rectangle([px, y + h * .08, px + w * .03, y + h * .22], fill=(200, 170, 60))
        d.rectangle([px, y + h * .78, px + w * .03, y + h * .92], fill=(200, 170, 60))
        py = y + h * (.26 + i * .11)
        d.rectangle([x + w * .08, py, x + w * .28, py + h * .03], fill=(200, 170, 60))
        d.rectangle([x + w * .72, py, x + w * .92, py + h * .03], fill=(200, 170, 60))
    d.ellipse([x + w * .78, y + h * .08, x + w * .92, y + h * .22], fill=(60, 200, 190))


def scene_mic(d, x, y, w, h):
    _sky(d, x, y, w, h, (40, 35, 60), (90, 70, 110))
    d.polygon([(x + w * .20, y), (x + w * .38, y), (x + w * .50, y + h * .55),
               (x + w * .30, y + h * .55)], fill=(240, 220, 130))
    d.polygon([(x + w * .62, y), (x + w * .80, y), (x + w * .70, y + h * .55),
               (x + w * .50, y + h * .55)], fill=(220, 200, 110))
    d.ellipse([x + w * .40, y + h * .14, x + w * .60, y + h * .38], fill=(50, 50, 55))
    d.rectangle([x + w * .44, y + h * .30, x + w * .56, y + h * .34], fill=(180, 180, 180))
    d.rectangle([x + w * .46, y + h * .38, x + w * .54, y + h * .62], fill=(70, 70, 75))
    d.rectangle([x + w * .38, y + h * .62, x + w * .62, y + h * .68], fill=(70, 70, 75))
    d.rectangle([x + w * .30, y + h * .80, x + w * .70, y + h * .86], fill=(150, 40, 45))
    d.rectangle([x + w * .30, y + h * .88, x + w * .70, y + h * .94], fill=(40, 60, 120))


def scene_flags(d, x, y, w, h):
    _sky(d, x, y, w, h, (170, 200, 220), (235, 238, 230))
    cols = [(200, 40, 40), (40, 90, 160), (240, 200, 40), (40, 140, 70), (160, 60, 140)]
    for i, c in enumerate(cols):
        fx = x + w * (.06 + i * .19)
        d.line([(fx + w * .02, y + h * .12), (fx + w * .02, y + h * .90)], fill=(90, 85, 75), width=3)
        d.polygon([(fx + w * .02, y + h * .12), (fx + w * .16, y + h * .20),
                   (fx + w * .02, y + h * .30)], fill=c)
    d.rectangle([x, y + h * .90, x + w, y + h], fill=(120, 140, 110))


def scene_crowd(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 205, 215), (238, 236, 228))
    d.rectangle([x, y + h * .72, x + w, y + h], fill=(140, 135, 125))
    heads = [(0.12, 0.52, (200, 60, 60)), (0.28, 0.46, (40, 90, 160)),
             (0.44, 0.54, (240, 180, 40)), (0.60, 0.44, (40, 140, 70)),
             (0.76, 0.52, (160, 60, 140)), (0.90, 0.48, (200, 100, 40))]
    for fx, fy, c in heads:
        d.ellipse([x + w * (fx - .05), y + h * (fy - .05), x + w * (fx + .05), y + h * (fy + .05)],
                  fill=(230, 190, 150))
        d.rectangle([x + w * (fx - .07), y + h * (fy + .05), x + w * (fx + .07), y + h * .74], fill=c)
    d.rectangle([x + w * .30, y + h * .16, x + w * .70, y + h * .34], fill=(250, 248, 240))
    d.rectangle([x + w * .30, y + h * .16, x + w * .70, y + h * .34], outline=(163, 22, 33), width=2)
    d.line([(x + w * .36, y + h * .34), (x + w * .36, y + h * .50)], fill=(90, 85, 75), width=2)
    d.line([(x + w * .64, y + h * .34), (x + w * .64, y + h * .50)], fill=(90, 85, 75), width=2)


def scene_handshake(d, x, y, w, h):
    _sky(d, x, y, w, h, (240, 200, 120), (250, 235, 200))
    d.rectangle([x + w * .08, y + h * .14, x + w * .46, y + h * .86], fill=(255, 140, 40))
    d.rectangle([x + w * .08, y + h * .14, x + w * .46, y + h * .38], fill=(255, 170, 60))
    d.rectangle([x + w * .08, y + h * .62, x + w * .46, y + h * .86], fill=(20, 120, 60))
    d.ellipse([x + w * .24, y + h * .44, x + w * .32, y + h * .52], fill=(20, 40, 120))
    d.rectangle([x + w * .54, y + h * .14, x + w * .92, y + h * .86], fill=(200, 20, 50))
    d.polygon([(x + w * .54, y + h * .14), (x + w * .92, y + h * .14),
               (x + w * .73, y + h * .50)], fill=(220, 40, 70))
    d.polygon([(x + w * .54, y + h * .86), (x + w * .92, y + h * .86),
               (x + w * .73, y + h * .50)], fill=(20, 40, 120))
    d.rectangle([x + w * .40, y + h * .42, x + w * .60, y + h * .62], fill=(250, 240, 220))
    d.ellipse([x + w * .42, y + h * .44, x + w * .58, y + h * .60], fill=(230, 190, 150))


def scene_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 110, 140))
    d.rectangle([x + w * .18, y + h * .10, x + w * .82, y + h * .90], fill=(250, 248, 240))
    for i in range(5):
        ly = y + h * (.24 + i * .12)
        d.line([(x + w * .26, ly), (x + w * .74, ly)], fill=(180, 175, 165), width=2)
    d.ellipse([x + w * .60, y + h * .55, x + w * .88, y + h * .83], outline=(40, 40, 40), width=4)
    d.line([(x + w * .86, y + h * .80), (x + w * .96, y + h * .92)], fill=(40, 40, 40), width=4)
    d.rectangle([x + w * .10, y + h * .78, x + w * .34, y + h * .84], fill=(240, 180, 40))
    d.polygon([(x + w * .34, y + h * .78), (x + w * .42, y + h * .81),
               (x + w * .34, y + h * .84)], fill=(60, 60, 60))


def scene_plane(d, x, y, w, h):
    _sky(d, x, y, w, h, (110, 170, 220), (205, 225, 240))
    for cx, cy, s in ((.18, .22, .16), (.55, .12, .12), (.80, .30, .14)):
        d.ellipse([x + w * cx, y + h * cy, x + w * (cx + s), y + h * (cy + s * .5)], fill=(255, 255, 255))
        d.ellipse([x + w * (cx + s * .5), y + h * (cy - s * .15), x + w * (cx + s * 1.2), y + h * (cy + s * .35)],
                  fill=(255, 255, 255))
    d.ellipse([x + w * .30, y + h * .42, x + w * .68, y + h * .58], fill=(240, 240, 238))
    d.polygon([(x + w * .66, y + h * .44), (x + w * .88, y + h * .36),
               (x + w * .88, y + h * .52), (x + w * .66, y + h * .54)], fill=(220, 220, 215))
    d.polygon([(x + w * .36, y + h * .58), (x + w * .44, y + h * .72),
               (x + w * .52, y + h * .58)], fill=(200, 200, 195))
    d.polygon([(x + w * .60, y + h * .58), (x + w * .66, y + h * .70),
               (x + w * .72, y + h * .58)], fill=(200, 200, 195))
    for i in range(5):
        d.ellipse([x + w * (.36 + i * .05), y + h * .47, x + w * (.38 + i * .05), y + h * .51],
                  fill=(40, 80, 140))
    d.rectangle([x + w * .10, y + h * .46, x + w * .14, y + h * .52], fill=(200, 40, 40))


SCENES = {
    "capitol": scene_capitol, "heli": scene_heli, "stadium": scene_stadium,
    "robot": scene_robot, "flame": scene_flame, "huts": scene_huts,
    "tanker": scene_tanker, "hospital": scene_hospital, "chip": scene_chip,
    "mic": scene_mic, "flags": scene_flags, "crowd": scene_crowd,
    "handshake": scene_handshake, "exam": scene_exam, "plane": scene_plane,
}


def draw_scene(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 218))
    SCENES[kind](d, x + 1, y + 1, w - 2, h - 2)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)

# ---------------------------------------------------------------- layout

MX = 28
CW = W - 2 * MX

TAG_FILL = {"CONFIRMED": TEAL, "REPORTED": (150, 110, 20), "CLAIM": RED}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
     (-70, 45), (-80, 32), (-90, 21), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 10), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-75, -20), (-80, -5), (-80, 10)],
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (8, 57), (18, 56), (21, 60),
     (30, 70), (40, 68), (45, 60), (40, 52), (30, 46), (28, 41), (23, 36),
     (19, 42), (12, 44), (3, 43), (-2, 37), (-10, 36)],
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -26), (28, -33), (20, -35), (15, -27), (12, -18), (9, 4), (-8, 5),
     (-13, 9), (-17, 15)],
    [(40, 68), (55, 72), (70, 73), (90, 75), (110, 76), (130, 72), (160, 66),
     (178, 65), (170, 60), (158, 52), (142, 45), (140, 40), (130, 35), (127, 35),
     (120, 30), (110, 20), (105, 10), (100, 8), (95, 16), (90, 22), (80, 13),
     (77, 8), (72, 20), (66, 25), (60, 25), (57, 27), (50, 29), (48, 30),
     (44, 30), (40, 36), (36, 36), (40, 42), (40, 68)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (114, -22)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(208, 224, 232))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 150 * h) for lon, lat in poly]
        d.polygon(pts, fill=(228, 216, 188), outline=(120, 110, 90))
    for n, (lon, lat) in PINS.items():
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 150 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        tw = d.textlength(str(n), font=f)
        d.text((px - tw / 2, py - 5), str(n), font=f, fill=(255, 255, 255))


def tag_text(d, x, y, src, tag):
    f = font(SANS, 9)
    d.text((x, y), "\u2014 " + src + " \u00b7 ", font=f, fill=GREY)
    w0 = d.textlength("\u2014 " + src + " \u00b7 ", font=f)
    d.text((x + w0, y), tag, font=font(SANS_B, 9), fill=TAG_FILL[tag])


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=PAPER)
    d.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=1)

    # masthead
    y = 16
    rule(d, MX, W - MX, y, width=2)
    y += 6
    y = centre(d, y, "THE WORLD IN ONE DAY", font(SERIF_B, 48))
    y += 2
    f_date = font(SERIF_B, 32)
    dw = d.textlength("MONDAY 23 NOVEMBER 2026", font=f_date)
    cx = W // 2
    rule(d, MX, cx - dw / 2 - 14, y + 20, fill=RED, width=2)
    rule(d, cx + dw / 2 + 14, W - MX, y + 20, fill=RED, width=2)
    y = centre(d, y, "MONDAY 23 NOVEMBER 2026", f_date)
    y += 4
    f_deck = font(SERIF_I, 15)
    deck = ("Democrats\u2019 biggest House majority since 1992 \u00b7 "
            "\u2018Chapo Isidro\u2019 seized \u00b7 Liverpool rout United 4\u20130")
    y = centre(d, y, deck, f_deck, fill=RED)
    y += 6
    rule(d, MX, W - MX, y, width=1)
    rule(d, MX, W - MX, y + 3, width=2)

    # stat strip
    y += 10
    box_w, gap = 158, 4
    for i, (num, cap) in enumerate(STATS):
        bx = MX + i * (box_w + gap)
        d.rectangle([bx, y, bx + box_w, y + 44], fill=CREAM, outline=RULE, width=1)
        fn = font(SERIF_B, 25)
        nw = d.textlength(num, font=fn)
        d.text((bx + (box_w - nw) / 2, y + 2), num, font=fn, fill=RED)
        fc = font(SANS_B, 9)
        cw = d.textlength(cap, font=fc)
        d.text((bx + (box_w - cw) / 2, y + 31), cap, font=fc, fill=INK)
    y += 52

    # region bar
    counts = {}
    for s in LEADS + SMALL:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for n, r, t, src, _h in ALSO:
        counts[r] = counts.get(r, 0) + 1
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "AFRICA", "MIDDLE EAST", "WORLD"]
    parts = [f"{r} {counts.get(r, 0)}" for r in order]
    total = sum(counts.values())
    region_line = "  \u00b7  ".join(parts) + f"   \u2014   {total} STORIES"
    y = centre(d, y, region_line, font(SANS_B, 12))
    y += 4
    rule(d, MX, W - MX, y, width=1)

    # UTC timeline
    y += 6
    centre(d, y, "THE DAY IN UTC \u2014 SUNDAY EVENING INTO MONDAY",
           font(SANS_B, 10), fill=GREY)
    y += 16
    tw = CW // 6
    for i, (t, ev) in enumerate(TIMELINE):
        tx = MX + i * tw
        d.text((tx, y), t, font=font(SANS_B, 11), fill=RED)
        text_block(d, tx, y + 14, ev, font(SANS, 9), tw - 8, leading=11, max_lines=1)
    y += 28
    rule(d, MX, W - MX, y, width=1)

    # leads
    y += 6
    centre(d, y, "TOP STORIES", font(SANS_B, 11), fill=GREY)
    y += 16
    col_w, col_gap = 312, 16
    for i, s in enumerate(LEADS):
        lx = MX + i * (col_w + col_gap)
        draw_scene(d, s["scene"], lx, y, col_w, 72)
        hy = y + 78
        hy = text_block(d, lx, hy, f"{s['n']}. {s['head']}", font(SERIF_B, 17),
                        col_w, leading=20, max_lines=2)
        hy = text_block(d, lx, hy + 2, s["body"], font(SANS, 11), col_w,
                        leading=14, max_lines=2)
        tag_text(d, lx, hy + 3, s["src"], s["tag"])
    y += 168
    rule(d, MX, W - MX, y, width=1)

    # small stories: 3 cols x 4 rows
    y += 8
    row_h = 62
    for ri in range(4):
        for ci in range(3):
            s = SMALL[ri * 3 + ci]
            sx = MX + ci * (col_w + col_gap)
            sy = y + ri * row_h
            draw_scene(d, s["scene"], sx, sy, 92, 58)
            tx = sx + 100
            ty = text_block(d, tx, sy, f"{s['n']}. {s['head']}", font(SERIF_B, 12),
                            col_w - 100, leading=14, max_lines=2)
            ty = text_block(d, tx, ty, s["body"], font(SANS, 10), col_w - 100,
                            leading=11, max_lines=2)
            tag_text(d, tx, ty + 1, s["src"], s["tag"])
    y += 4 * row_h + 4
    rule(d, MX, W - MX, y, width=1)

    # map + date check
    y += 6
    centre(d, y, "WHERE IT HAPPENED \u2014 THE DAY\u2019S NEWS ON THE MAP",
           font(SANS_B, 11), fill=GREY)
    y += 16
    map_w, map_h = 640, 96
    draw_map(d, MX, y, map_w, map_h)
    bx = MX + map_w + 16
    bw = W - MX - bx
    d.rectangle([bx, y, bx + bw, y + map_h], fill=CREAM, outline=RED, width=2)
    tx = bx + 8
    ty = y + 5
    d.text((tx, ty), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    ty += 15
    ty = text_block(
        d, tx, ty,
        "NOT 23 NOVEMBER \u2014 LEFT OUT: COP31 ends with no deal (21 Nov) \u00b7 "
        "Russia\u2019s 186-drone raid on Kyiv region (22 Nov) \u00b7 Cikande factory fire "
        "toll (22 Nov) \u00b7 Verstappen wins in Las Vegas (22 Nov) \u00b7 Wembanyama "
        "scores 50 (22 Nov) \u00b7 India 720/9 declared in Wellington (22 Nov). "
        "Stories above were first reported overnight into Monday, Asia\u2013Pacific time.",
        font(SANS, 9), bw - 16, leading=11, max_lines=8)
    y += map_h + 6
    rule(d, MX, W - MX, y, width=1)

    # ALSO list, 2 columns x 11 rows
    y += 6
    centre(d, y, "ALSO ON MONDAY \u2014 22 MORE STORIES", font(SANS_B, 11), fill=GREY)
    y += 16
    half = (len(ALSO) + 1) // 2
    cols = [ALSO[:half], ALSO[half:]]
    f_also = font(SANS, 9)
    for ci, col in enumerate(cols):
        ax = MX + ci * (CW // 2 + 8)
        for ri, (n, _r, tag, src, head) in enumerate(col):
            ay = y + ri * 10
            d.text((ax, ay), f"{n}. {head}", font=f_also, fill=INK)
            tw2 = d.textlength(f"{n}. {head}", font=f_also)
            d.text((ax + tw2 + 4, ay), f"\u2014 {src} \u00b7 {tag}",
                   font=font(SANS, 8), fill=TAG_FILL[tag])
    y += half * 10 + 4
    rule(d, MX, W - MX, y, width=1)

    # footer
    y += 5
    centre(d, y, "SOURCES: Reuters \u00b7 AP \u00b7 CNN \u00b7 BBC \u00b7 UN News \u00b7 UKMTO \u00b7 WHO \u00b7 "
           "FBI \u00b7 MEA \u00b7 Korea JoongAng Daily \u00b7 PEOPLE \u00b7 ESPN \u00b7 Opta",
           font(SANS, 9), fill=GREY)
    y += 12
    centre(d, y, "CERTAINTY: CONFIRMED = officially confirmed  \u00b7  REPORTED = reported, "
           "not independently verified  \u00b7  CLAIM = one side\u2019s claim",
           font(SANS_B, 9), fill=GREY)
    return img


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        path = os.path.join(out, "entry.png")
    else:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(path, format="PNG", optimize=True)
    print(path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
