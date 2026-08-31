const CACHE = 'temperatura-v88';
const ASSETS = ['./manifest.json', './icon-192.png', './icon-512.png'];

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
    e.respondWith(
      fetch(new Request(e.request, { cache: 'no-cache' }))
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});
