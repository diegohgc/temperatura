const CACHE = 'temperatura-v132';
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
    // Stale-while-revalidate: sirve la copia guardada al instante (apertura
    // rápida) y en paralelo pide la version fresca en segundo plano para
    // la próxima apertura. Los datos del tiempo nunca pasan por aqui (se
    // excluyen arriba), así que esto nunca deja una temperatura anticuada,
    // solo puede dejar el código/diseño "una apertura por detrás" justo
    // despues de publicar un cambio.
    e.respondWith(
      caches.open(CACHE).then(async (cache) => {
        const cached = await cache.match('./index.html');
        const actualizado = fetch(new Request(e.request, { cache: 'no-cache' }))
          .then((resp) => {
            if (resp && resp.ok) cache.put('./index.html', resp.clone());
            return resp;
          })
          .catch(() => cached);
        return cached || actualizado;
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});
