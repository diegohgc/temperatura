from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 500

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# Fondo degradado azul (igual que la app)
for y in range(H):
    t = y / H
    r = int(30 + t * (15))
    g = int(60 + t * (40))
    b = int(120 + t * (60))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- Montaña (izquierda) ---
mx = 200
my = H - 80
picos = [
    (mx - 160, my),
    (mx - 40, my - 180),
    (mx + 20, my - 120),
    (mx + 110, my - 220),
    (mx + 200, my),
]
draw.polygon(picos, fill=(255, 255, 255, 180))
# sombra/detalle montaña
draw.polygon([
    (mx + 110, my - 220),
    (mx + 160, my - 120),
    (mx + 200, my),
    (mx + 110, my - 220),
], fill=(200, 220, 255))

# --- Termómetro (centro-izquierda) ---
tx = 420
ty = 100
t_alto = 260
t_ancho = 28
radio_bulbo = 36

# Tubo exterior
draw.rounded_rectangle(
    [tx - t_ancho//2, ty, tx + t_ancho//2, ty + t_alto],
    radius=t_ancho//2,
    fill=(255, 255, 255)
)
# Bulbo
draw.ellipse(
    [tx - radio_bulbo, ty + t_alto - radio_bulbo,
     tx + radio_bulbo, ty + t_alto + radio_bulbo],
    fill=(255, 80, 80)
)
# Relleno mercurio
mercurio_h = int(t_alto * 0.62)
draw.rounded_rectangle(
    [tx - t_ancho//2 + 5, ty + t_alto - mercurio_h,
     tx + t_ancho//2 - 5, ty + t_alto],
    radius=5,
    fill=(255, 80, 80)
)
# Marcas del termómetro
for i in range(5):
    my_mark = ty + 30 + i * 46
    draw.line([(tx + t_ancho//2 + 2, my_mark), (tx + t_ancho//2 + 14, my_mark)],
              fill=(255, 255, 255), width=3)

# --- Texto derecha ---
try:
    font_grande = ImageFont.truetype("arial.ttf", 80)
    font_medio = ImageFont.truetype("arial.ttf", 36)
    font_small = ImageFont.truetype("arial.ttf", 26)
except:
    font_grande = ImageFont.load_default()
    font_medio = font_grande
    font_small = font_grande

tx_x = 500
draw.text((tx_x, 130), "QuickTemp", font=font_grande, fill=(255, 255, 255))
draw.text((tx_x + 4, 240), "Temperatura · Altitud · Marea", font=font_medio, fill=(180, 210, 255))
draw.text((tx_x + 4, 305), "Simple. Rápido. Siempre contigo.", font=font_small, fill=(140, 180, 230))

img.save("feature_graphic.png")
print("Banner guardado: feature_graphic.png (1024x500)")
