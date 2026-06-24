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
- La API key está hardcodeada en `index.html` (`STORMGLASS_KEY`) porque es una app
  100% cliente sin backend — por tanto la key es visible en el código fuente para
  cualquiera que la inspeccione. Riesgo aceptado por el usuario dado el free tier
  limitado (10 llamadas/día).
- Si se agota la cuota diaria o falla la llamada, la app sigue funcionando sin mostrar
  la marea (no rompe el resto de la funcionalidad).

## Altitud
- Si el GPS del dispositivo devuelve altitud (`coords.altitude`, requiere
  `enableHighAccuracy: true`), se muestra esa.
- Si no, se usa la elevación del terreno en esas coordenadas vía Open-Meteo
  (`api.open-meteo.com/v1/elevation`, gratis sin key) como aproximación.

## Plan futuro
- De momento es solo PWA. Intención de empaquetarla más adelante como APK Android
  (WebView que cargue la PWA publicada), igual que se hizo con el proyecto de halterofilia
  (repo `diegohgc/tandas-2`).
- Iconos actuales son placeholder (copiados de otro proyecto) — sustituir por iconos propios.

## Flujo de trabajo
- `git add -A && git commit -m "..." && git push` para publicar cambios.
- Pendiente: decidir hosting (GitHub Pages u otro) para tener URL pública e instalar en el móvil.
