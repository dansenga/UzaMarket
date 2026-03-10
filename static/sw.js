// UzaMarket Service Worker — PWA Offline Support
const CACHE_NAME = 'uzamarket-v1';
const STATIC_CACHE = 'uzamarket-static-v1';
const DYNAMIC_CACHE = 'uzamarket-dynamic-v1';

// Ressources statiques essentielles à mettre en cache
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/img/favicon.svg',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  'https://unpkg.com/htmx.org@1.9.10',
];

// Installation — mise en cache des ressources statiques
self.addEventListener('install', (event) => {
  console.log('[SW] Installation...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Mise en cache des ressources statiques');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
      .catch((err) => {
        console.log('[SW] Erreur de cache:', err);
        return self.skipWaiting();
      })
  );
});

// Activation — nettoyage des anciens caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activation...');
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== DYNAMIC_CACHE)
          .map((key) => {
            console.log('[SW] Suppression ancien cache:', key);
            return caches.delete(key);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch — stratégie Network First avec fallback cache
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Ignorer les requêtes non-GET
  if (request.method !== 'GET') return;

  // Ignorer les requêtes admin et API
  if (request.url.includes('/admin/') || request.url.includes('/api/')) return;

  // Stratégie pour les ressources statiques (Cache First)
  if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Stratégie pour les pages HTML (Network First)
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Autres ressources (Network First)
  event.respondWith(networkFirst(request));
});

// Vérifier si c'est une ressource statique
function isStaticAsset(url) {
  return url.includes('/static/') ||
         url.includes('cdn.jsdelivr.net') ||
         url.includes('cdnjs.cloudflare.com') ||
         url.includes('unpkg.com') ||
         url.includes('fonts.googleapis.com') ||
         url.includes('fonts.gstatic.com');
}

// Stratégie Cache First (statiques)
async function cacheFirst(request) {
  try {
    const cached = await caches.match(request);
    if (cached) return cached;

    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response('Offline', { status: 503 });
  }
}

// Stratégie Network First (pages dynamiques)
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request);
    if (cached) return cached;

    // Fallback page hors ligne
    if (request.headers.get('Accept')?.includes('text/html')) {
      return offlineFallback();
    }
    return new Response('Offline', { status: 503 });
  }
}

// Page de fallback hors ligne
function offlineFallback() {
  const html = `
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UzaMarket — Hors ligne</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(180deg, #6366F1 0%, #4338CA 100%);
      color: #fff;
      text-align: center;
      padding: 2rem;
    }
    .offline-container { max-width: 420px; }
    .offline-icon {
      width: 80px; height: 80px;
      background: rgba(255,255,255,0.15);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1.5rem;
      font-size: 2.5rem;
    }
    h1 { font-size: 1.8rem; margin-bottom: 0.75rem; font-weight: 800; }
    p { opacity: 0.85; line-height: 1.6; margin-bottom: 1.5rem; }
    .retry-btn {
      display: inline-block;
      padding: 0.75rem 2rem;
      background: #F59E0B;
      color: #1a1a2e;
      border: none;
      border-radius: 12px;
      font-weight: 700;
      font-size: 1rem;
      cursor: pointer;
      text-decoration: none;
      transition: transform 0.2s;
    }
    .retry-btn:hover { transform: scale(1.05); }
  </style>
</head>
<body>
  <div class="offline-container">
    <div class="offline-icon">📡</div>
    <h1>Vous êtes hors ligne</h1>
    <p>Vérifiez votre connexion internet et réessayez. UzaMarket sera de retour dès que vous serez connecté.</p>
    <button class="retry-btn" onclick="window.location.reload()">Réessayer</button>
  </div>
</body>
</html>`;
  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8' }
  });
}
