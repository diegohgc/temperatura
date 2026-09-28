const CACHE = 'temperatura-v181';
const ASSETS = ['./manifest.json', './icon-192.png', './icon-512.png', './nube-textura.png', './nube2-textura.png', './sol-textura.png', './luna-textura.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('open-meteo.com') || e.request.url.includes('bigdatacloud.net') || e.request.url.includes('nominatim.openstreetmap.org') ||
      e.request.url.includes('openweathermap.org') || e.request.url.includes('rainviewer.com') ||
      e.request.url.includes('tile.openstreetmap.org') || e.request.url.includes('unpkg.com') ||
      e.request.url.includes('cdnjs.cloudflare.com') || e.request.url.includes('tomorrow.io')) return;

  if (e.request.mode === 'navigate' || e.request.url.endsWith('index.html')) {
    // Red primero, cache como respaldo solo si falla/no hay conexion. Antes
    // era stale-while-revalidate (servia la copia guardada al instante y
    // dejaba la version fresca para la SIGUIENTE apertura) -- eso hacia que
    // cualquier usuario que no borrara cache/datos fuera siempre "una
    // apertura por detras" de cada cambio publicado. Como la app ya
    // necesita conexion para los datos del tiempo, casi nunca hay usuarios
    // realmente offline, asi que priorizar red no penaliza la velocidad de
    // apertura en la practica y todos ven las novedades al instante.
    e.respondWith(
      caches.open(CACHE).then(async (cache) => {
        try {
          const resp = await fetch(new Request(e.request, { cache: 'no-cache' }));
          if (resp && resp.ok) cache.put('./index.html', resp.clone());
          return resp;
        } catch (err) {
          const cached = await cache.match('./index.html');
          if (cached) return cached;
          throw err;
        }
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});
