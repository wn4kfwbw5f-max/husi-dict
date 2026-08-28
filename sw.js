/* 《胡思辞典》Service Worker —— 让网页可"安装到主屏幕"并离线打开应用壳。
   说明：
   - 应用壳（index.html 等静态文件）缓存到本地，离线也能打开。
   - 页面导航（HTML）走 network-first，保证重新部署后能拿到最新版。
   - /api/* 接口永远走网络（不缓存），因为释义需要实时 AI / D1。 */
const CACHE = "husicidian-search-v4";
const ASSETS = ["./", "./index.html", "./dict.js", "./manifest.webmanifest", "./icon.svg", "./icon-180.png", "./icon-192.png", "./icon-512.png", "./admin-dict.html"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((ks) =>
      Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // 接口：永远走网络，不缓存
  if (url.pathname.startsWith("/api/")) {
    e.respondWith(fetch(req).catch(() => new Response("{}", {
      status: 200,
      headers: { "Content-Type": "application/json" }
    })));
    return;
  }

  // 页面导航：network-first，失败回退缓存
  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req)
        .then((r) => {
          const cp = r.clone();
          caches.open(CACHE).then((c) => c.put("./index.html", cp));
          return r;
        })
        .catch(() => caches.match("./index.html"))
    );
    return;
  }

  // 其它静态资源：cache-first，回退网络并存一份
  e.respondWith(
    caches.match(req).then((r) =>
      r || fetch(req).then((resp) => {
        const cp = resp.clone();
        caches.open(CACHE).then((c) => c.put(req, cp));
        return resp;
      }).catch(() => caches.match("./index.html"))
    )
  );
});
