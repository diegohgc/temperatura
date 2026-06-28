# Temperatura — App web (PWA)

App de una sola página que muestra la temperatura actual en la ubicación del usuario,
usando geolocalización del navegador y la API gratuita Open-Meteo (sin API key).

## Arquitectura
- Todo el código está en `index.html` (HTML + CSS + JS, sin build).
- PWA: `manifest.json` + `sw.js` (service worker) + iconos. Instalable desde el navegador.
- Datos del tiempo: Open-Meteo (`api.open-meteo.com` + `geocoding-api.open-meteo.com`), sin clave de API.
- No usa localStorage ni backend propio; cada carga consulta la ubicación y el tiempo en directo.

## Marea (Stormglass)
- Estado de marea (subiendo/bajando) y hora del próximo cambio vía Stormglass API
  (`api.stormglass.io/v2/tide/extremes/point`).
- Auth con header `Authorization`. La API key está hardcodeada en `index.html`
  (`STORMGLASS_KEY`) porque es una app 100% cliente sin backend — visible en el código
  fuente para quien lo inspeccione. Riesgo aceptado por el usuario.
- Free tier: 10 llamadas/día — vigilar el consumo.
- Si falla la llamada o se agota la cuota, la app sigue funcionando sin mostrar la marea
  (no rompe el resto de la funcionalidad).
- Se probó también Marea API (`api.marea.ooo`) como alternativa, pero se ha vuelto a
  Stormglass a petición del usuario. La key de Marea API queda sin usar por si se retoma
  en el futuro: `715aa404-0c8b-41df-8710-d4a6782757dc`.

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
