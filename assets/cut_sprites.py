"""Cut sprites from the asset sheet: remove white bg + baked gray shadows, save RGBA PNGs.
Usage: python3 assets/cut_sprites.py assets/asset-sheet.webp assets/sprites
"""
import sys, numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
sheet = np.asarray(Image.open(SRC).convert('RGB')).astype(np.int16)

# name: (x0, y0, x1, y1, sat_tol, bri_tol)   sheet pixel coords
# sat_tol/bri_tol: pixels with (max-min) < sat_tol and min > bri_tol, connected to the border, are background.
SPRITES = {
    'hull':        (198, 579, 458, 652, 22, 150),
    'paddle':      (302, 508, 468, 538, 22, 150),
    'body':        (340, 314, 400, 377, 30, 60),
    'arm':         (340, 262, 402, 292, 22, 150),
    'lotus1':      (1074, 25, 1153, 113, 22, 150),
    'lotus2':      (1158, 30, 1236, 115, 22, 150),
    'lotus3':      (1077, 115, 1143, 188, 22, 150),
    'lotus4':      (1158, 122, 1230, 198, 22, 150),
    'lotus5':      (1079, 192, 1135, 255, 22, 150),
    'lotus6':      (1161, 197, 1220, 260, 22, 150),
    'lotus7':      (1081, 262, 1126, 308, 22, 150),
    'lotus8':      (1161, 265, 1205, 310, 22, 150),
    'cargo_o':     (1245, 35, 1308, 138, 22, 150),
    'cargo_w':     (1245, 137, 1305, 228, 10, 232),
    'cargo_g':     (1244, 225, 1308, 321, 22, 150),
    'pad1':        (1077, 322, 1120, 365, 22, 150),
    'pad2':        (1127, 326, 1169, 370, 22, 150),
    'pad3':        (1171, 317, 1244, 391, 22, 150),
    'pad4':        (1082, 382, 1120, 420, 22, 150),
    'pad5':        (1130, 375, 1170, 415, 22, 150),
    'pad6':        (1180, 391, 1244, 455, 22, 150),
    'pad7':        (1086, 431, 1116, 461, 22, 150),
    'pad8':        (1136, 419, 1175, 458, 22, 150),
}

def shift(m, dy, dx):
    o = np.zeros_like(m)
    H, W = m.shape
    o[max(dy,0):H+min(dy,0), max(dx,0):W+min(dx,0)] = m[max(-dy,0):H+min(-dy,0), max(-dx,0):W+min(-dx,0)]
    return o

def bg_mask(px, sat_tol, bri_tol):
    mx, mn = px.max(2), px.min(2)
    cand = ((mx - mn) < sat_tol) & (mn > bri_tol)
    bg = np.zeros_like(cand)
    bg[0, :] = cand[0, :]; bg[-1, :] = cand[-1, :]; bg[:, 0] = cand[:, 0]; bg[:, -1] = cand[:, -1]
    while True:
        grown = (bg | shift(bg,1,0) | shift(bg,-1,0) | shift(bg,0,1) | shift(bg,0,-1)) & cand
        if (grown == bg).all(): return bg
        bg = grown

for name, (x0, y0, x1, y1, st, bt) in SPRITES.items():
    px = sheet[y0:y1, x0:x1]
    fg = ~bg_mask(px, st, bt)
    fg = fg & shift(fg,1,0) & shift(fg,-1,0) & shift(fg,0,1) & shift(fg,0,-1)   # erode 1px: kill white fringe
    a = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    rgba = Image.fromarray(px.astype(np.uint8)).convert('RGBA'); rgba.putalpha(a)
    rgba = rgba.crop(rgba.getbbox())
    rgba.save(f'{OUT}/{name}.png')
    print(name, rgba.size)
