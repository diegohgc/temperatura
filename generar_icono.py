from PIL import Image, ImageDraw, ImageFont
import math

SIZE = 512
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Fondo circular gradiente azul oscuro
for r in range(SIZE // 2, 0, -1):
    ratio = r / (SIZE // 2)
    R = int(10 + 30 * ratio)
    G = int(20 + 60 * ratio)
    B = int(50 + 100 * ratio)
    draw.ellipse(
        [SIZE // 2 - r, SIZE // 2 - r, SIZE // 2 + r, SIZE // 2 + r],
        fill=(R, G, B, 255)
    )

# --- MONTAÑA GRANDE (izquierda) ---
mtn_base_y = 420
mtn_left = 30
mtn_right = 210
mtn_peak_x = 105
mtn_peak_y = 200

# sombra
draw.polygon(
    [(mtn_left+5, mtn_base_y+5), (mtn_peak_x+5, mtn_peak_y+5), (mtn_right+5, mtn_base_y+5)],
    fill=(0, 0, 0, 70)
)
# montaña principal
draw.polygon(
    [(mtn_left, mtn_base_y), (mtn_peak_x, mtn_peak_y), (mtn_right, mtn_base_y)],
    fill=(55, 85, 135, 255)
)
# lado oscuro (sombra lateral)
draw.polygon(
    [(mtn_peak_x, mtn_peak_y), (mtn_right, mtn_base_y), (mtn_peak_x + 20, mtn_base_y)],
    fill=(35, 60, 105, 255)
)
# nieve en la cima
snow_pts = [
    (mtn_peak_x, mtn_peak_y),
    (mtn_peak_x - 38, mtn_peak_y + 55),
    (mtn_peak_x - 10, mtn_peak_y + 45),
    (mtn_peak_x + 15, mtn_peak_y + 58),
    (mtn_peak_x + 40, mtn_peak_y + 48),
]
draw.polygon(snow_pts, fill=(215, 232, 255, 230))

# --- OLA (derecha) con forma de ola curl ---
# Base del mar
sea_top = 340
sea_bottom = 430
sea_left = 290
sea_right = 490

# Fondo del mar
draw.rectangle([sea_left, sea_top + 30, sea_right, sea_bottom], fill=(30, 110, 180, 200))

# Ola principal con forma de tubo/curl
# Cuerpo de la ola: una curva que sube, se dobla y cae
wave_pts = []
# borde superior de la ola (de izquierda a derecha)
steps = 80
for i in range(steps + 1):
    t = i / steps
    x = sea_left + t * (sea_right - sea_left)
    # forma de ola: sube en el centro-izquierda, cae a la derecha
    y = sea_top + 30 - 70 * math.exp(-((t - 0.3) ** 2) / 0.03) + 40 * t
    wave_pts.append((x, y))

# borde inferior (línea recta abajo)
wave_pts.append((sea_right, sea_bottom))
wave_pts.append((sea_left, sea_bottom))
draw.polygon(wave_pts, fill=(35, 125, 200, 230))

# Cresta de la ola (parte que se dobla, más clara)
curl_pts = []
for i in range(steps + 1):
    t = i / steps
    x = sea_left + t * (sea_right - sea_left)
    y = sea_top + 30 - 70 * math.exp(-((t - 0.3) ** 2) / 0.03) + 40 * t
    curl_pts.append((x, y))

# interior del curl (más oscuro, efecto tubo)
inner_pts = []
for i in range(steps + 1):
    t = i / steps
    x = sea_left + t * (sea_right - sea_left)
    y = sea_top + 30 - 70 * math.exp(-((t - 0.3) ** 2) / 0.03) + 40 * t + 18
    inner_pts.append((x, y))

curl_shape = curl_pts[:int(steps * 0.55)] + list(reversed(inner_pts[:int(steps * 0.55)]))
draw.polygon(curl_shape, fill=(20, 80, 160, 180))

# Espuma / cresta blanca en el pico de la ola
foam_cx = sea_left + int(0.28 * (sea_right - sea_left))
foam_cy = sea_top + 30 - 68
for dx, dy, r, a in [
    (0, 0, 18, 200), (-18, 8, 12, 160), (18, 5, 13, 160),
    (-8, -10, 9, 140), (10, -8, 8, 140), (0, 12, 10, 130)
]:
    draw.ellipse(
        [foam_cx + dx - r, foam_cy + dy - r, foam_cx + dx + r, foam_cy + dy + r],
        fill=(220, 240, 255, a)
    )

# Líneas de agua debajo de la ola
for i, (ly, lw) in enumerate([(sea_top + 55, 80), (sea_top + 72, 60), (sea_top + 88, 70)]):
    lx = sea_left + 40 + i * 15
    draw.arc([lx, ly, lx + lw, ly + 14], start=180, end=0, fill=(100, 180, 240, 140), width=3)

# --- TERMÓMETRO (centro arriba) ---
tube_w = 40
tube_h = 160
tube_x = SIZE // 2 - tube_w // 2 + 40
tube_y = 80
tube_r = tube_w // 2

draw.rounded_rectangle(
    [tube_x + 4, tube_y + 4, tube_x + tube_w + 4, tube_y + tube_h + 4],
    radius=tube_r, fill=(0, 0, 0, 70)
)
draw.rounded_rectangle(
    [tube_x, tube_y, tube_x + tube_w, tube_y + tube_h],
    radius=tube_r, fill=(215, 232, 255, 255)
)
inner_margin = 8
draw.rounded_rectangle(
    [tube_x + inner_margin, tube_y + inner_margin,
     tube_x + tube_w - inner_margin, tube_y + tube_h - inner_margin // 2],
    radius=tube_r - inner_margin // 2,
    fill=(20, 40, 85, 255)
)
mercury_h = 100
mercury_x = tube_x + inner_margin + 2
mercury_y = tube_y + tube_h - inner_margin // 2 - mercury_h
mercury_w = tube_w - inner_margin * 2 - 4
draw.rounded_rectangle(
    [mercury_x, mercury_y, mercury_x + mercury_w, tube_y + tube_h - inner_margin // 2],
    radius=4, fill=(215, 55, 55, 255)
)
bulb_r = 30
bulb_cx = tube_x + tube_w // 2
bulb_cy = tube_y + tube_h + bulb_r - 8
draw.ellipse(
    [bulb_cx - bulb_r, bulb_cy - bulb_r, bulb_cx + bulb_r, bulb_cy + bulb_r],
    fill=(215, 55, 55, 255)
)
draw.ellipse(
    [bulb_cx - 10, bulb_cy - 14, bulb_cx + 2, bulb_cy - 4],
    fill=(255, 175, 175, 150)
)
for i in range(4):
    tick_y = tube_y + inner_margin + 16 + i * 24
    tick_x1 = tube_x + tube_w - inner_margin + 1
    draw.line([tick_x1, tick_y, tick_x1 + 10, tick_y], fill=(140, 195, 255, 200), width=2)

# --- TEXTO ---
try:
    font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
except:
    font_small = ImageFont.load_default()

text = "QuickTemp"
bbox = draw.textbbox((0, 0), text, font=font_small)
tw = bbox[2] - bbox[0]
tx = (SIZE - tw) // 2
ty = 450
draw.text((tx + 2, ty + 2), text, font=font_small, fill=(0, 0, 0, 100))
draw.text((tx, ty), text, font=font_small, fill=(175, 210, 255, 255))

img.save("icono_512.png", "PNG")
print("icono_512.png generado correctamente")
