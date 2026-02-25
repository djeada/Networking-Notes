#!/usr/bin/env python3
"""
Proxy Server Simulator (Forward & Reverse)
============================================
Simulates forward-proxy and reverse-proxy behaviour without opening any real
network connections.  Shows how proxies intercept HTTP requests, rewrite
headers, cache responses, and route traffic.

Concepts demonstrated:
* Forward proxy — sits in front of clients; the client explicitly sends
  requests to the proxy, which fetches the resource on the client's behalf.
  Typical use: corporate web filter, anonymiser, caching proxy (Squid).
  Key header: X-Forwarded-For (original client IP).
* Reverse proxy — sits in front of servers; the client believes it is
  talking to the origin, but the proxy dispatches to one of many backends.
  Typical use: load balancing, TLS termination, CDN edge (Nginx, Cloudflare).
  Key header: Via (proxy hop identifier).
* Response caching — the proxy stores responses keyed by URL and serves
  subsequent identical requests from cache, reducing backend load.

Usage:
    python proxy_server_demo.py              # runs built-in demo
    python proxy_server_demo.py --no-cache   # disable caching behaviour
"""

import argparse
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class HttpRequest:
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    client_ip: str = "0.0.0.0"

    def summary(self):
        return f"{self.method} {self.url} (from {self.client_ip})"


@dataclass
class HttpResponse:
    status: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    cache_control: str = "max-age=60"

    def summary(self):
        return f"HTTP {self.status} ({len(self.body)} bytes)"


class SimpleCache:
    def __init__(self, max_size: int = 64):
        self._store: OrderedDict[str, HttpResponse] = OrderedDict()
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[HttpResponse]:
        if key in self._store:
            self.hits += 1
            self._store.move_to_end(key)
            return self._store[key]
        self.misses += 1
        return None

    def put(self, key: str, resp: HttpResponse):
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = resp
        if len(self._store) > self.max_size:
            self._store.popitem(last=False)

    def stats(self) -> str:
        total = self.hits + self.misses
        ratio = (self.hits / total * 100) if total else 0
        return f"hits={self.hits}, misses={self.misses}, ratio={ratio:.0f}%"


class OriginServer:
    """Simulated web server that returns canned responses."""

    PAGES = {
        "/": ("200 OK", "<html><body>Welcome!</body></html>"),
        "/about": ("200 OK", "<html><body>About Us</body></html>"),
        "/api/data": ("200 OK", '{"results": [1,2,3]}'),
        "/secret": ("403 Forbidden", "Access Denied"),
    }

    def __init__(self, name: str):
        self.name = name
        self.requests_served = 0

    def handle(self, req: HttpRequest) -> HttpResponse:
        self.requests_served += 1
        from urllib.parse import urlparse
        path = urlparse(req.url).path
        status_text, body = self.PAGES.get(path, ("404 Not Found", "Not Found"))
        code = int(status_text.split()[0])
        return HttpResponse(
            status=code,
            headers={"Server": self.name, "Content-Length": str(len(body))},
            body=body,
        )


class ForwardProxy:
    def __init__(self, name: str, use_cache: bool = True):
        self.name = name
        self.cache = SimpleCache() if use_cache else None

    def handle(self, req: HttpRequest, origin: OriginServer) -> HttpResponse:
        print(f"  [{self.name}] ← Client request: {req.summary()}")

        # Rewrite headers
        req.headers["X-Forwarded-For"] = req.client_ip
        req.headers["Via"] = f"1.1 {self.name}"
        print(f"    Added X-Forwarded-For: {req.client_ip}")
        print(f"    Added Via: 1.1 {self.name}")

        # Check cache
        if self.cache:
            cached = self.cache.get(req.url)
            if cached:
                print(f"    ⚡ Cache HIT for {req.url}")
                cached.headers["X-Cache"] = "HIT"
                return cached
            print(f"    ✗ Cache MISS for {req.url}")

        # Forward to origin
        print(f"    → Forwarding to origin server ({origin.name})...")
        resp = origin.handle(req)
        resp.headers["Via"] = f"1.1 {self.name}"

        if self.cache and resp.status == 200:
            self.cache.put(req.url, resp)
            resp.headers["X-Cache"] = "MISS"
            print(f"    Stored response in cache")

        print(f"    ← Origin responded: {resp.summary()}")
        return resp


class ReverseProxy:
    def __init__(self, name: str, backends: List[OriginServer], use_cache: bool = True):
        self.name = name
        self.backends = backends
        self.cache = SimpleCache() if use_cache else None
        self._rr = -1

    def _pick_backend(self) -> OriginServer:
        self._rr = (self._rr + 1) % len(self.backends)
        return self.backends[self._rr]

    def handle(self, req: HttpRequest) -> HttpResponse:
        print(f"  [{self.name}] ← Client request: {req.summary()}")
        print(f"    Client sees {self.name} as the origin server.")
        if self.cache:
            cached = self.cache.get(req.url)
            if cached:
                print(f"    ⚡ Cache HIT — serving directly")
                cached.headers["X-Cache"] = "HIT"
                return cached
            print(f"    ✗ Cache MISS")
        backend = self._pick_backend()
        print(f"    → Dispatching to backend: {backend.name}")
        req.headers["X-Forwarded-For"] = req.client_ip
        req.headers["X-Real-IP"] = req.client_ip
        req.headers["Host"] = backend.name
        resp = backend.handle(req)
        resp.headers["Via"] = f"1.1 {self.name}"
        resp.headers["Server"] = self.name
        if self.cache and resp.status == 200:
            self.cache.put(req.url, resp)
            resp.headers["X-Cache"] = "MISS"
            print(f"    Stored in edge cache")

        print(f"    ← Backend responded: {resp.summary()} (masked as {self.name})")
        return resp


def demo(use_cache: bool):
    print("=" * 65)
    print("  Proxy Server Simulator — Forward & Reverse")
    print("=" * 65)

    origin = OriginServer("origin.example.com")

    # ── Forward Proxy Demo ──
    print("\n  === FORWARD PROXY ===")
    print("  Client ──► Proxy ──► Origin Server")
    print("  The client knows about the proxy and sends requests to it.\n")

    fwd = ForwardProxy("squid-proxy.corp.local", use_cache=use_cache)
    requests_fwd = [
        HttpRequest("GET", "http://example.com/", client_ip="192.168.1.42"),
        HttpRequest("GET", "http://example.com/about", client_ip="192.168.1.42"),
        HttpRequest("GET", "http://example.com/", client_ip="192.168.1.99"),  # cache hit
        HttpRequest("GET", "http://example.com/secret", client_ip="192.168.1.42"),
    ]

    for i, req in enumerate(requests_fwd, 1):
        print(f"\n{'─' * 60}")
        print(f"  Forward Proxy — Request #{i}")
        resp = fwd.handle(req, origin)
        print(f"  Response headers: { {k:v for k,v in resp.headers.items()} }")

    if fwd.cache:
        print(f"\n  Forward proxy cache: {fwd.cache.stats()}")

    # ── Reverse Proxy Demo ──
    print("\n  === REVERSE PROXY ===")
    print("  Client ──► Reverse Proxy ──► Backend Pool")
    print("  The client thinks the proxy IS the server.\n")

    backends = [OriginServer("backend-1"), OriginServer("backend-2")]
    rev = ReverseProxy("cdn-edge.example.net", backends, use_cache=use_cache)
    requests_rev = [
        HttpRequest("GET", "https://cdn-edge.example.net/", client_ip="203.0.113.5"),
        HttpRequest("GET", "https://cdn-edge.example.net/api/data", client_ip="198.51.100.7"),
        HttpRequest("GET", "https://cdn-edge.example.net/", client_ip="203.0.113.12"),  # cache hit
        HttpRequest("GET", "https://cdn-edge.example.net/missing", client_ip="203.0.113.5"),
    ]

    for i, req in enumerate(requests_rev, 1):
        print(f"\n{'─' * 60}")
        print(f"  Reverse Proxy — Request #{i}")
        resp = rev.handle(req)
        print(f"  Response headers: { {k:v for k,v in resp.headers.items()} }")

    if rev.cache:
        print(f"\n  Reverse proxy cache: {rev.cache.stats()}")

    print(f"\n  Backend load: " + ", ".join(
        f"{b.name}={b.requests_served} reqs" for b in backends))
    print(f"\n{'═' * 65}")
    print("  • Forward proxy: hides client identity from server")
    print("  • Reverse proxy: hides backend topology from client")
    print("  Both can cache, filter, and modify HTTP traffic in transit.")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forward & reverse proxy simulator")
    parser.add_argument("--no-cache", action="store_true",
                        help="Disable proxy caching to see every request hit the backend")
    args = parser.parse_args()
    demo(use_cache=not args.no_cache)
