# Temperatura — App web (PWA)

App de una sola página que muestra la temperatura actual en la ubicación del usuario,
usando geolocalización del navegador y la API gratuita Open-Meteo (sin API key).

## Arquitectura
- Todo el código está en `index.html` (HTML + CSS + JS, sin build).
- PWA: `manifest.json` + `sw.js` (service worker) + iconos. Instalable desde el navegador.
- Datos del tiempo: Open-Meteo (`api.open-meteo.com` + `geocoding-api.open-meteo.com`), sin clave de API.
- No usa localStorage ni backend propio; cada carga consulta la ubicación y el tiempo en directo.

## Marea (Open-Meteo Marine API)
- Estado de marea (subiendo/bajando) y hora del próximo cambio vía la API marina de
  Open-Meteo (`marine-api.open-meteo.com/v1/marine`, variable `sea_level_height_msl`
  horaria). Gratis, sin API key.
- El estado y el próximo extremo se calculan en el cliente comparando la serie horaria
  de altura del nivel del mar (se busca el primer cambio de pendiente a partir de ahora).
  Precisión de ±1h al ser datos horarios (menos exacta que un proveedor dedicado de
  mareas, pero suficiente para el uso de la app).
- Sin límite de llamadas restrictivo (a diferencia de los proveedores anteriores).
- Si falla la llamada, la app sigue funcionando sin mostrar la marea (no rompe el resto
  de la funcionalidad).
- Proveedores probados anteriormente, descartados:
  - Stormglass (`api.stormglass.io`): free tier de solo 10 llamadas/día.
  - Marea API (`api.marea.ooo`): key sin usar por si se retoma en el futuro:
    `715aa404-0c8b-41df-8710-d4a6782757dc`.

## Altitud
- Se usa siempre la elevación del terreno en esas coordenadas vía Open-Meteo
  (`api.open-meteo.com/v1/elevation`, gratis sin key).
- Antes se usaba `coords.altitude` (GPS) cuando estaba disponible, pero se descartó:
  esa altitud es sobre el elipsoide WGS84, no sobre el geoide/nivel del mar real, y
  el navegador no permite corregir eso (depende del chip GPS/SO). La elevación de
  Open-Meteo sí está referida a nivel del mar, así que es más correcta aunque menos
  "en vivo" (terreno, no posición exacta dentro de un edificio, por ejemplo).

## Plan futuro
- De momento es solo PWA. Intención de empaquetarla más adelante como APK Android
  (WebView que cargue la PWA publicada), igual que se hizo con el proyecto de halterofilia
  (repo `diegohgc/tandas-2`).
- Iconos actuales son placeholder (copiados de otro proyecto) — sustituir por iconos propios.

## Flujo de trabajo
- `git add -A && git commit -m "..." && git push` para publicar cambios.
- Pendiente: decidir hosting (GitHub Pages u otro) para tener URL pública e instalar en el móvil.
