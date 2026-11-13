// Turbo – Offline-Cache. Netz zuerst (Updates kommen sofort an), sonst aus dem Cache.
const CACHE = 'turbo-v2';
const DATEIEN = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'];

self.addEventListener('install', (e) => {
  // Einzeln cachen: eine fehlende Datei darf die Installation nicht verhindern
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.all(DATEIEN.map((d) => c.add(d).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((namen) => Promise.all(namen.filter((n) => n !== CACHE).map((n) => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const anfrage = e.request;
  if (anfrage.method !== 'GET' || new URL(anfrage.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(anfrage)
      .then((antwort) => {
        if (antwort.ok) {
          const kopie = antwort.clone();
          caches.open(CACHE).then((c) => c.put(anfrage, kopie));
        }
        return antwort;
      })
      .catch(() =>
        caches.match(anfrage, { ignoreSearch: true }).then((treffer) => treffer || caches.match('index.html'))
      )
  );
});
