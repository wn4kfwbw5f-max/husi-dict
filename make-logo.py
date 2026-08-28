"""
胡思辞典 logo v2 —— 极简渐变线稿，1024x1024，无文字、无水印
设计：一条折线（V 形打开的书页）+ 中央一条向上光柱 + 顶部一个光点
渐变色与主站 hero 标题一致（橙 #FFB98A → 暖橙 #FF8A5B → 粉 #E6728F）
"""
from PIL import Image, ImageDraw
import math

W = H = 1024

# 1) 渲染"开书 + 光" 主线（线段两色渐变：起点橙 → 终点粉）
def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_gradient_line(draw, x1, y1, x2, y2, width, c_start, c_end, steps=120):
    """逐像素画线段，颜色从 c_start 渐变到 c_end（linecap=round 用端点大圆盖）"""
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0: return
    ux, uy = dx / length, dy / length  # 单位方向
    for i in range(steps):
        t = i / (steps - 1)
        c = lerp_color(c_start, c_end, t)
        # 在法线方向偏移（粗线宽用 line：把线拆成垂直短段）
        cx = x1 + dx * t
        cy = y1 + dy * t
        # 用 1px 圆点逐点涂（圆头/圆尾自然）
        draw.ellipse((cx - width/2, cy - width/2, cx + width/2, cy + width/2), fill=c)

# 2) 创建画布（深色圆角方，匹配主站背景）
img = Image.new("RGB", (W, H), (15, 17, 21))   # #0f1115
draw = ImageDraw.Draw(img, "RGBA")

# 圆角背景（用 mask 方式简化：直接画大圆角矩形）
def rounded_rect(d, x1, y1, x2, y2, r, fill):
    d.rounded_rectangle((x1, y1, x2, y2), radius=r, fill=fill)

rounded_rect(draw, 0, 0, W, H, 200, (15, 17, 21))  # 200px 圆角，更现代

# 3) 渐变色定义
G1 = (255, 185, 138)   # #FFB98A 浅橙
G2 = (255, 138, 91)    # #FF8A5B 主橙
G3 = (230, 114, 143)   # #E6728F 粉

LINE_W = 22  # 粗线视觉更高级（细线太弱）

# 4) 主线：V 形打开的书页（左 + 右）+ 中心向上光柱
# 中心点 (512, 540)，左下 (240, 800)，右下 (784, 800)
draw_gradient_line(draw, 240, 800, 512, 540, LINE_W, G1, G2, steps=160)  # 左书页
draw_gradient_line(draw, 512, 540, 784, 800, LINE_W, G2, G3, steps=160)  # 右书页
# 中央光柱：从中心点向上到 (512, 240)
draw_gradient_line(draw, 512, 540, 512, 240, LINE_W, G2, G3, steps=120)

# 5) 顶部光点（圆）
glow_cx, glow_cy, glow_r = 512, 200, 28
# 外圈淡淡光晕（多次小圆叠加）
for i, alpha in enumerate([(60, 0.10), (40, 0.16), (25, 0.24), (15, 0.34)]):
    r = glow_r + (4 - i) * 18
    color = (255, 138, 91, int(alpha[1] * 255))
    draw.ellipse((glow_cx - r, glow_cy - r, glow_cx + r, glow_cy + r), fill=color)
# 实心点
for i in range(2):
    a = (1.0 - i * 0.18)
    color = (255, int(138 + 30 * i), int(91 + 30 * i), int(255 * a))
    r = glow_r - i * 3
    draw.ellipse((glow_cx - r, glow_cy - r, glow_cx + r, glow_cy + r), fill=color)

img.save("logo-husi.png", "PNG", optimize=True)
print("已生成 logo-husi.png", W, "x", H)
