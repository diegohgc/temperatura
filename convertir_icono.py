from PIL import Image

SIZE = 512
bg_color = (13, 27, 60, 255)  # azul oscuro del icono

original = Image.open("icono_original.png").convert("RGBA")
original = original.resize((SIZE, SIZE), Image.LANCZOS)

fondo = Image.new("RGBA", (SIZE, SIZE), bg_color)
fondo.paste(original, (0, 0), original)

resultado = fondo.convert("RGB")
resultado.save("icono_play_store.png", "PNG")
print("icono_play_store.png generado (512x512 fondo solido)")
