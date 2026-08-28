"""
胡思辞典 PWA 图标生成器：方形全出血深色底 + 渐变线 logo（开书+光柱+光点）
输出 180 / 192 / 512 三尺寸 PNG（180 给 iOS 主屏幕，192/512 给 PWA/安卓）
四角不透明（#0f1115），iOS 自动加圆角后边缘干净。
"""
from PIL import Image, ImageDraw
import math

# 归一化坐标（基于 1000 单位）→ 任意尺寸
def N(x): return x / 1000.0

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_gradient_line(draw, x1, y1, x2, y2, width, c_start, c_end, steps=140):
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0: return
    for i in range(steps):
        t = i / (steps - 1)
        c = lerp_color(c_start, c_end, t)
        cx = x1 + dx * t
        cy = y1 + dy * t
        draw.ellipse((cx - width/2, cy - width/2, cx + width/2, cy + width/2), fill=c)

def make_icon(size, out_path):
    S = size
    img = Image.new("RGB", (S, S), (15, 17, 21))   # #0f1115 全出血（不透明方形）
    draw = ImageDraw.Draw(img, "RGBA")

    G1 = (255, 185, 138)   # #FFB98A
    G2 = (255, 138, 91)    # #FF8A5B
    G3 = (230, 114, 143)   # #E6728F

    # 线宽随尺寸缩放（512 基准约 20 单位）
    lw = S * 0.022

    def px(x, y): return x * S / 1000.0, y * S / 1000.0

    # 主线：V 形开书（左页 + 右页）+ 中央光柱
    x1, y1 = px(230, 800); xc, yc = px(500, 540); x2, y2 = px(770, 800); xt, yt = px(500, 250)
    draw_gradient_line(draw, x1, y1, xc, yc, lw, G1, G2)   # 左页
    draw_gradient_line(draw, xc, yc, x2, y2, lw, G2, G3)   # 右页
    draw_gradient_line(draw, xc, yc, xt, yt, lw, G2, G3)   # 光柱

    # 顶部光点（带光晕）
    gx, gy = px(500, 208)
    gr = S * 0.028
    for radius, alpha in [(gr*3.2, 0.10), (gr*2.3, 0.16), (gr*1.6, 0.24), (gr, 0.34)]:
        draw.ellipse((gx-radius, gy-radius, gx+radius, gy+radius),
                     fill=(255, 138, 91, int(alpha*255)))
    for i, alpha in enumerate([1.0, 0.82]):
        r = gr - i * gr * 0.15
        draw.ellipse((gx-r, gy-r, gx+r, gy+r),
                     fill=(255, int(138+30*i), int(91+30*i), int(255*alpha)))

    img.save(out_path, "PNG", optimize=True)
    print("生成", out_path, size, "x", size)

os_guard = None
import os
os.makedirs(os.path.dirname("/Users/g/WorkBuddy/2026-07-31-21-21-04/husi-cidian/redesign/icon-180.png") or ".", exist_ok=True)
make_icon(180, "/Users/g/WorkBuddy/2026-07-31-21-21-04/husi-cidian/redesign/icon-180.png")
make_icon(192, "/Users/g/WorkBuddy/2026-07-31-21-21-04/husi-cidian/redesign/icon-192.png")
make_icon(512, "/Users/g/WorkBuddy/2026-07-31-21-21-04/husi-cidian/redesign/icon-512.png")
