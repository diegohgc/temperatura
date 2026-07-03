# QuickTemp — App web (PWA) + Android

App de una sola página que muestra temperatura, altitud, marea y previsión meteorológica
según la ubicación GPS del usuario. Publicada en Google Play en prueba cerrada.

## Arquitectura
- Todo el código está en `index.html` (HTML + CSS + JS, sin build).
- PWA: `manifest.json` + `sw.js` (service worker v4) + iconos. Instalable desde el navegador.
- Datos del tiempo: Open-Meteo (`api.open-meteo.com` + `geocoding-api.open-meteo.com`), sin clave de API.
- Ciudad: BigDataCloud (`api.bigdatacloud.net/data/reverse-geocode-client`), sin key.
- No usa localStorage ni backend propio; cada carga consulta la ubicación y el tiempo en directo.
- URL pública: https://diegohgc.github.io/temperatura/
- Se publica con GitHub Pages: editar `index.html` + `git push` y se actualiza solo.

## Android (repo: temperatura-android)
- APK/AAB: WebView que carga `https://diegohgc.github.io/temperatura/`
- Package: `com.diegohg.quicktemp`
- Keystore: `temperatura-android/quicktemp.jks`, alias `quicktemp`, pass en `local.properties`
- Para compilar AAB firmado:
  `gradlew bundleRelease -PQUICKTEMP_STORE_PASS=Dindurra1 -PQUICKTEMP_KEY_PASS=Dindurra1`
- AAB generado en: `app/build/outputs/bundle/release/app-release.aab`
- AdMob App ID: `ca-app-pub-5015878857432448~7059763758`
- Widget de pantalla de inicio implementado (TemperaturaWidget.kt): temperatura, altitud y ciudad.
  Usa Open-Meteo + BigDataCloud. Click en el widget refresca los datos.
- Versión actual: versionCode=2, versionName=1.1

## Google Play
- App: QuickTemp (`com.diegohg.quicktemp`)
- Estado: **prueba cerrada activa** (desde ~3 julio 2026)
- Testers: >12 aceptados (requisito cumplido)
- Falta: ejecutar prueba 14 días → solicitar acceso a producción (~17 julio 2026)
- Cuenta desarrollador: DHaudiovisuales (hay typo, debería ser DHaudiovisuales sin la 'a' extra — en proceso de corrección)
- Grupo Telegram testers: @Android12TestersBot

## Funcionalidades implementadas
- Temperatura actual + sensación térmica, viento, humedad
- Previsión horaria (8h) y diaria (7 días) con iconos SVG
- Amanecer/anochecer
- Altitud del terreno (Open-Meteo elevation)
- Estado de marea + hora del próximo extremo (Open-Meteo Marine API)
- Buscador de ciudades (geocoding Open-Meteo)
- **Fondo de color dinámico** según temperatura: azul hielo (<0°) → azul (frío) → verde (templado) → naranja (cálido) → rojo (sofocante). Cambia gradualmente con transición suave.
- **Multiidioma**: detecta el idioma del navegador automáticamente. Soporta: es, en, de, fr, pt, it, zh.
- Widget Android en pantalla de inicio

## Marea (Open-Meteo Marine API)
- Variable `sea_level_height_msl` horaria. Gratis, sin API key.
- El estado y próximo extremo se calculan en el cliente comparando la serie horaria.
- Precisión ±1h. Solo se muestra si la ubicación es costera.
- Proveedores descartados: Stormglass (10 llamadas/día), Marea API.

## Altitud
- Elevación del terreno vía Open-Meteo (`/v1/elevation`), referida a nivel del mar.
- Se descartó `coords.altitude` del GPS (altitud sobre elipsoide WGS84, no nivel del mar).

## Gradle / compilación Android
- Memoria: `C:\Users\diego\.gradle\gradle.properties` tiene `-Xmx4096m` y las passwords
- Si falla por memoria, ese archivo global sobreescribe el del proyecto — revisarlo primero
- `android.enableR8.fullMode=false` en gradle.properties del proyecto (R8 desactivado)

## Flujo de trabajo
- Al empezar: `git pull`
- Cambios en la web (index.html): `git add -A && git commit -m "..." && git push` → se publica solo
- Cambios en Android: recompilar AAB y subir a Play Console manualmente
