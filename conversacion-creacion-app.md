# Creación de la app "Temperatura" — registro de conversación

Fecha: 2026-06-23

## Resumen

Se creó una PWA (web app instalable) llamada **Temperatura**, que muestra la temperatura
actual en la ubicación del usuario usando geolocalización del navegador y la API gratuita
**Open-Meteo** (sin necesidad de API key).

## Decisiones tomadas

- **Tipo de app**: PWA web (no nativa) de momento, con intención futura de empaquetarla
  como APK Android (igual que se hizo con el proyecto de halterofilia, repo `diegohgc/tandas-2`).
- **Ubicación del proyecto**: nueva carpeta independiente
  `C:\Users\diego\Desktop\TRABAJOS\proyectos claude\temperatura`, con su propio repo Git.
- **Nombre del proyecto**: `temperatura`.
- **Repo GitHub**: `https://github.com/diegohgc/temperatura.git` (público, vacío al crearlo).
- **Hosting**: GitHub Pages, branch `main`, carpeta raíz.
- **URL pública**: `https://diegohgc.github.io/temperatura/`

## Pasos realizados

1. Creación de la carpeta del proyecto e inicialización de git.
2. Creación de archivos:
   - `index.html`: página única con geolocalización, fetch a Open-Meteo (tiempo actual +
     geocoding inverso para el nombre de la ciudad), y botón de actualizar.
   - `manifest.json`: metadatos de PWA (nombre, iconos, colores).
   - `sw.js`: service worker para cache offline de los assets estáticos (no cachea las
     llamadas a la API del tiempo).
   - `icon-192.png` / `icon-512.png`: iconos placeholder, copiados temporalmente del
     proyecto de halterofilia — **pendiente sustituir por iconos propios**.
   - `CLAUDE.md`: contexto del proyecto para futuras sesiones de Claude Code.
3. Commit inicial y push al repo `diegohgc/temperatura` en GitHub.
4. Activación manual de GitHub Pages desde Settings → Pages (branch `main`, carpeta raíz).
5. Verificación: `https://diegohgc.github.io/temperatura/` responde 200 y funciona en
   navegador de escritorio.

## Cómo instalar en el móvil

- **Android (Chrome)**: abrir la URL → menú ⋮ → "Añadir a pantalla de inicio".
- **iPhone (Safari)**: abrir la URL → botón compartir → "Añadir a pantalla de inicio".
- Aceptar el permiso de ubicación cuando lo pida el navegador.

## Pendiente / próximos pasos

- Sustituir los iconos placeholder por iconos propios de la app.
- Si se quiere, empaquetar como APK Android (WebView apuntando a la URL de GitHub Pages),
  siguiendo el mismo patrón que `diegohgc/tandas-2`.
