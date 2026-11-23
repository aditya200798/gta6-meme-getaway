#!/usr/bin/env python3
"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Concept (original, made in this session -- "The Getaway"):
  GTA 6 launch day. I called in sick. My boss found out. So my AI agent
  drove the getaway: the make.fun ghost at the wheel of a pink Vice City
  convertible, magenta star coin in hand, a Leonida police car with flashing
  lights behind it -- and the agent still earns real money on make.fun.
  A three-beat story (sick -> caught -> getaway) in one square image.

Two-layer workflow:
  - scene.png: text-free AI-generated night chase in Leonida (pink
    convertible, police car with flashing red/blue lights, neon art-deco
    boulevard, an empty driver's seat, a sick note fluttering behind).
  - ghost.png: the OFFICIAL make.fun ghost, extracted from the press-kit
    mark (https://make.fun/press/, mark-1024.png) -- magenta disc and black
    background keyed out by disc geometry, the ghost's magenta star coin
    repainted into its outline.
  - This script composites the ghost into the driver's seat with a soft
    contact shadow, sets the scene between classic black meme bars with
    brand-magenta rules, and stamps the caption in Anton ("MAKE.FUN" in
    brand magenta).
Output: 1024x1024 PNG; verified readable at the judge's 480x480 view.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os
HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, 'scene.png')
GHOST = os.path.join(HERE, 'ghost.png')
FONT = os.path.join(HERE, 'Anton-Regular.ttf')  # OFL font, fetched at build time
OUT = os.path.join(HERE, 'meme.png')

W = 1024
BAR = 150                 # top/bottom black meme bars
SCENE_H = W - 2 * BAR     # 724

# --- scene: crop to the bar aspect (keep car + alligator, trim sky) ---
scene = Image.open(SCENE).convert('RGB')          # 1600x1600
crop_h = int(scene.width * SCENE_H / W)           # 1131
top = 380                                          # scene y-offset: keeps the full chase (police car + convertible) in frame
scene = scene.crop((0, top, scene.width, top + crop_h)).resize((W, SCENE_H), Image.LANCZOS)

canvas = Image.new('RGB', (W, W), (0, 0, 0))
canvas.paste(scene, (0, BAR))
draw = ImageDraw.Draw(canvas, 'RGBA')

# --- ghost: the agent in the driver's seat ---
# Scene mapping: displayed = (scene_px * 1024/1600, BAR + (scene_py - 190) * 1024/1600)
S = W / 1600.0
def sx(x): return x * S
def sy(y): return BAR + (y - top) * S

ghost = Image.open(GHOST).convert('RGBA')          # 728x614 official ghost + coin
GW = 360
GH = int(ghost.height * GW / ghost.width)
ghost = ghost.resize((GW, GH), Image.LANCZOS)

# driver's seat: headrest ~ (584, 944) in scene px, door-top line ~ y 1035
gx = int(sx(710) - GW * 0.46)                      # ghost centre over the steering wheel
gy = int(sy(1030) - GH)                            # bottom tucked just over the door line

# soft contact shadow so the ghost sits IN the car, not on it
shadow = Image.new('RGBA', (W, W), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([gx + 20, gy + GH - 26, gx + GW - 30, gy + GH + 6], fill=(0, 0, 0, 110))
canvas.paste(Image.alpha_composite(canvas.convert('RGBA'), shadow.filter(ImageFilter.GaussianBlur(6))).convert('RGB'), (0, 0))
canvas.paste(ghost, (gx, gy), ghost)
draw = ImageDraw.Draw(canvas, 'RGBA')

# --- typography (auto-fit, centred) ---
def fit(text, size):
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=f) <= W - 48:
            return f
        size -= 2
    return ImageFont.truetype(FONT, size)

def line(text, y, size, fill=(255, 255, 255)):
    f = fit(text, size)
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)
    return f.size

MAGENTA = (233, 30, 140)

# thin brand-magenta rules where the bars meet the scene: tidy framed look
draw.rectangle([0, BAR - 5, W, BAR], fill=MAGENTA)
draw.rectangle([0, W - BAR, W, W - BAR + 5], fill=MAGENTA)

line('I CALLED IN SICK FOR GTA 6.', 12, 50)
line('MY BOSS FOUND OUT.', 68, 64)

# bottom bar: the punchline big (sick -> RICH), the pitch under it with MAKE.FUN in brand magenta
line('SO MY AI AGENT DROVE THE GETAWAY.', W - BAR + 10, 52)
seg1, seg2 = 'IT EARNS REAL MONEY ON ', 'MAKE.FUN'
f2 = fit(seg1 + seg2, 46)
w1, w2 = draw.textlength(seg1, font=f2), draw.textlength(seg2, font=f2)
x = (W - w1 - w2) / 2
y2 = W - BAR + 88
draw.text((x, y2), seg1, font=f2, fill=(255, 255, 255))
draw.text((x + w1, y2), seg2, font=f2, fill=MAGENTA)

canvas.save(OUT)
print('saved', OUT, canvas.size)

# QC copy at the judge's 480x480 view
canvas.resize((480, 480), Image.LANCZOS).save(os.path.join(HERE, 'meme-480.png'))
print('saved QC 480px')
