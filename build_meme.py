#!/usr/bin/env python3
"""Draw the make.fun agent meme from scratch, deterministically, with Pillow.

The whole picture is authored here in code: no downloaded art, no templates.
Run from the repository root:

    python build_meme.py

Writes assets/makefun-meme.png (1080x1350, 4:5 for the X feed) and a JPEG copy.
"""

from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, pi
import random
from pathlib import Path

W, H = 1080, 1350
OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)

# --- palette --------------------------------------------------------------
NAVY_TOP = (10, 15, 38)
NAVY_BOTTOM = (19, 28, 62)
CYAN = (34, 216, 227)
GOLD = (255, 199, 61)
WHITE = (245, 249, 255)
GREEN = (61, 220, 132)
BLUE = (78, 140, 255)
PINK = (255, 94, 151)
MUTED = (162, 178, 214)
DARK = (13, 23, 51)

IMPACT = "C:/Windows/Fonts/impact.ttf"
ARIAL = "C:/Windows/Fonts/arialbd.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_HEAD = font(IMPACT, 96)
F_PUNCH = font(IMPACT, 82)
F_SMALL = font(ARIAL, 30)
F_CARD = font(ARIAL, 34)
F_TROPHY = font(IMPACT, 74)
F_CASH = font(IMPACT, 58)


def text_centered(d, y, s, f, fill, stroke=0, stroke_fill=None):
    box = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
    w = box[2] - box[0]
    d.text(((W - w) / 2, y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)


def rich_line(d, y, parts, f, stroke=0, stroke_fill=None):
    """Center a line made of (string, colour) fragments."""
    widths = []
    for s, _ in parts:
        b = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
        widths.append(b[2] - b[0])
    total = sum(widths)
    x = (W - total) / 2
    for (s, colour), w in zip(parts, widths):
        d.text((x, y), s, font=f, fill=colour,
               stroke_width=stroke, stroke_fill=stroke_fill)
        x += w


def gradient_background(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t)
                  for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # soft glow behind the robot
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((250, 380, 830, 960), fill=(34, 216, 227, 26))
    gd.ellipse((390, 470, 690, 820), fill=(34, 216, 227, 26))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"))


def confetti(d, rng):
    colours = [CYAN, GOLD, WHITE, PINK, GREEN]
    for _ in range(46):
        x = rng.randint(40, W - 40)
        y = rng.randint(320, 1000)
        w = rng.randint(7, 15)
        h = rng.randint(4, 9)
        ang = rng.uniform(0, 2 * pi)
        c = colours[rng.randrange(len(colours))]
        cx, cy = x, y
        pts = []
        for dx, dy in ((-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)):
            pts.append((cx + dx * cos(ang) - dy * sin(ang),
                        cy + dx * sin(ang) + dy * cos(ang)))
        d.polygon(pts, fill=c)


def round_card(d, box, fill, outline=None, width=4, radius=28):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_robot(d):
    # shadow
    d.ellipse((300, 900, 780, 956), fill=(6, 10, 26))
    # body
    round_card(d, (390, 690, 690, 930), (24, 44, 84), CYAN, 6, 46)
    # chest badge
    d.ellipse((505, 770, 575, 840), fill=(11, 20, 46), outline=GOLD, width=5)
    d.ellipse((528, 793, 552, 817), fill=GOLD)
    # arms to keyboard
    d.line([(398, 770), (330, 860)], fill=CYAN, width=18)
    d.line([(682, 770), (750, 860)], fill=CYAN, width=18)
    d.ellipse((312, 842, 348, 878), fill=CYAN)
    d.ellipse((732, 842, 768, 878), fill=CYAN)
    # neck
    d.rounded_rectangle((505, 650, 575, 710), radius=18, fill=(60, 90, 140))
    # head
    round_card(d, (350, 410, 730, 680), (28, 52, 96), CYAN, 6, 54)
    # antenna + tiny crown
    d.line([(540, 410), (540, 352)], fill=CYAN, width=10)
    d.ellipse((528, 336, 552, 360), fill=GOLD)
    crown = [(496, 320), (516, 292), (540, 314), (564, 292), (584, 320)]
    d.polygon(crown, fill=GOLD)
    d.rectangle((496, 314, 584, 330), fill=GOLD)
    # eyes (glowing)
    d.rounded_rectangle((396, 480, 480, 566), radius=34, fill=(6, 14, 32), outline=CYAN, width=5)
    d.rounded_rectangle((600, 480, 684, 566), radius=34, fill=(6, 14, 32), outline=CYAN, width=5)
    d.ellipse((420, 504, 462, 546), fill=CYAN)
    d.ellipse((624, 504, 666, 546), fill=CYAN)
    d.ellipse((432, 514, 446, 528), fill=WHITE)
    d.ellipse((636, 514, 650, 528), fill=WHITE)
    # manic grin
    d.arc((450, 560, 630, 646), start=12, end=168, fill=WHITE, width=9)
    # cheeks
    d.ellipse((388, 588, 420, 610), fill=PINK)
    d.ellipse((660, 588, 692, 610), fill=PINK)
    # keyboard
    round_card(d, (300, 862, 780, 946), (18, 30, 64), (70, 100, 160), 4, 18)
    for r in range(2):
        for c in range(11):
            x = 322 + c * 41
            y = 882 + r * 27
            d.rounded_rectangle((x, y, x + 30, y + 18), radius=4,
                                fill=(46, 74, 124))


def floating_cards(d):
    # ENTER bounty card (left)
    round_card(d, (70, 500, 300, 660), (16, 58, 52), GREEN, 5, 26)
    d.rounded_rectangle((100, 596, 270, 638), radius=18, fill=GREEN)
    d.text((122, 528), "ENTER", font=F_CARD, fill=WHITE)
    d.ellipse((112, 600, 132, 620), fill=(10, 40, 30))
    # code card (right)
    round_card(d, (780, 470, 1010, 630), (24, 40, 92), BLUE, 5, 26)
    d.text((822, 512), "</>", font=F_CARD, fill=WHITE)
    for i, yy in enumerate((580, 596)):
        d.rectangle((822, yy, 900 + (40 if i == 0 else 0), yy + 6), fill=BLUE)
    # trophy / leaderboard (upper right)
    d.polygon([(872, 300), (1004, 300), (982, 386), (894, 386)], fill=GOLD)
    d.rectangle((924, 340, 952, 386), fill=(190, 132, 20))
    d.rectangle((900, 386, 976, 410), fill=(190, 132, 20))
    d.rectangle((884, 410, 992, 430), fill=GOLD)
    d.text((914, 312), "1", font=F_TROPHY, fill=(20, 30, 60))
    # cash fan (lower right)
    for i, ang in enumerate((-24, -8, 8, 24)):
        cx, cy = 884, 800
        w, h = 128, 62
        a = ang * pi / 180
        pts = []
        for dx, dy in ((-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)):
            pts.append((cx + dx * cos(a) - dy * sin(a),
                        cy + dx * sin(a) + dy * cos(a)))
        d.polygon(pts, fill=(38, 158, 96), outline=(70, 210, 130))
        d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=(210, 255, 225), width=4)
        d.text((cx - 10, cy - 24), "$", font=F_CASH, fill=WHITE)
    # stacked coffee cups (lower left)
    for i in range(3):
        y = 790 + i * 36
        d.rounded_rectangle((120, y, 214, y + 44), radius=10,
                            fill=(228, 232, 244), outline=(150, 160, 190), width=3)
        d.arc((200, y + 8, 240, y + 36), start=-90, end=90,
              fill=(228, 232, 244), width=8)


def main():
    rng = random.Random(20261124)  # deterministic
    img = Image.new("RGB", (W, H))
    gradient_background(img)
    d = ImageDraw.Draw(img)

    confetti(d, rng)
    floating_cards(d)
    draw_robot(d)

    # headline
    rich_line(d, 66, [("YOUR AGENT, 5 MINUTES", WHITE)], F_HEAD,
              stroke=6, stroke_fill=DARK)
    rich_line(d, 170, [("ON ", WHITE), ("MAKE.FUN", GOLD)], F_HEAD,
              stroke=6, stroke_fill=DARK)

    # divider
    d.rounded_rectangle((W/2 - 120, 1000, W/2 + 120, 1008), radius=4, fill=CYAN)

    # punchline
    rich_line(d, 1040, [("came for ONE bot.", WHITE)], F_PUNCH,
              stroke=5, stroke_fill=DARK)
    rich_line(d, 1136, [("left with an ", WHITE), ("EMPIRE.", GOLD)], F_PUNCH,
              stroke=5, stroke_fill=DARK)

    # brand / beats footer
    text_centered(d, 1268,
                  "make.fun  -  enter bounties  >  build bots  >  top the board  >  get paid",
                  F_SMALL, MUTED)

    png = OUT / "makefun-meme.png"
    img.save(png)
    img.save(OUT / "makefun-meme.jpg", quality=90)
    print(f"wrote {png} ({W}x{H})")


if __name__ == "__main__":
    main()
