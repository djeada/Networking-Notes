#!/usr/bin/env python3
"""
DNS Cache Simulator with TTL-Based Expiry
===========================================
Simulates how a recursive DNS resolver's cache works.  Queries pass through
a hierarchical chain (stub → recursive resolver cache → root → TLD →
authoritative nameserver) and responses are cached according to their TTL.
Subsequent queries for the same name are served from cache until the TTL
expires.

Concepts demonstrated:
* Hierarchical resolution: root nameservers → TLD nameservers →
  authoritative nameservers, each returning referrals or final answers.
* TTL (Time To Live): every DNS record carries a TTL in seconds; the
  resolver caches the answer and decrements the TTL over time.
* Cache hit vs. miss: a cache hit avoids the full resolution chain and
  returns the answer in microseconds instead of milliseconds.
* Cache eviction: when the TTL reaches zero the entry is purged and the
  next query triggers a fresh resolution.

Usage:
    python dns_cache_simulator.py                    # runs built-in demo
    python dns_cache_simulator.py --queries 20       # more random queries
    python dns_cache_simulator.py --time-step 30     # 30 s between queries
"""

import argparse
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class DNSRecord:
    name: str
    rtype: str      # A, AAAA, CNAME, NS
    value: str
    ttl: int         # seconds

    def __str__(self):
        return f"{self.name:30s} {self.ttl:>5}s  IN  {self.rtype:5s}  {self.value}"


@dataclass
class CacheEntry:
    record: DNSRecord
    remaining_ttl: int

    def __str__(self):
        return f"{self.record.name:30s}  TTL={self.remaining_ttl:>4}s  {self.record.rtype}  {self.record.value}"


class AuthoritativeZone:
    """Simulated authoritative nameserver for a zone."""

    def __init__(self, zone: str, records: List[DNSRecord]):
        self.zone = zone
        self.records = {(r.name, r.rtype): r for r in records}
        self.queries_received = 0

    def query(self, name: str, rtype: str) -> Optional[DNSRecord]:
        self.queries_received += 1
        return self.records.get((name, rtype))


# Pre-built zone data
ZONES: Dict[str, AuthoritativeZone] = {}

def _build_zones():
    global ZONES
    ZONES["root"] = AuthoritativeZone(".", [
        DNSRecord("com.", "NS", "tld-ns.com.", 172800),
        DNSRecord("org.", "NS", "tld-ns.org.", 172800),
    ])
    ZONES["com."] = AuthoritativeZone("com.", [
        DNSRecord("example.com.", "NS", "ns1.example.com.", 86400),
    ])
    ZONES["org."] = AuthoritativeZone("org.", [
        DNSRecord("openai.org.", "NS", "ns1.openai.org.", 86400),
    ])
    ZONES["example.com."] = AuthoritativeZone("example.com.", [
        DNSRecord("example.com.", "A", "93.184.216.34", 60),
        DNSRecord("www.example.com.", "CNAME", "example.com.", 120),
        DNSRecord("mail.example.com.", "A", "93.184.216.50", 30),
        DNSRecord("api.example.com.", "A", "93.184.216.99", 45),
    ])
    ZONES["openai.org."] = AuthoritativeZone("openai.org.", [
        DNSRecord("openai.org.", "A", "13.107.238.51", 90),
        DNSRecord("docs.openai.org.", "A", "13.107.238.52", 40),
    ])


class DNSResolverCache:
    def __init__(self):
        self.cache: Dict[Tuple[str, str], CacheEntry] = {}
        self.total_hits = 0
        self.total_misses = 0

    def lookup(self, name: str, rtype: str) -> Optional[CacheEntry]:
        key = (name, rtype)
        entry = self.cache.get(key)
        if entry and entry.remaining_ttl > 0:
            self.total_hits += 1
            return entry
        if entry:
            del self.cache[key]  # expired
        self.total_misses += 1
        return None

    def store(self, record: DNSRecord):
        key = (record.name, record.rtype)
        self.cache[key] = CacheEntry(record, record.ttl)

    def advance_time(self, seconds: int):
        expired = []
        for key, entry in self.cache.items():
            entry.remaining_ttl -= seconds
            if entry.remaining_ttl <= 0:
                expired.append(key)
        for key in expired:
            del self.cache[key]
        return expired

    def dump(self):
        if not self.cache:
            print("    (cache is empty)")
            return
        for entry in self.cache.values():
            print(f"    {entry}")


def resolve(cache: DNSResolverCache, name: str, rtype: str = "A",
            verbose: bool = True) -> Optional[DNSRecord]:
    """Full recursive resolution with caching."""
    if verbose:
        print(f"\n  ► Query: {name} {rtype}")
    cached = cache.lookup(name, rtype)
    if cached:
        if verbose:
            print(f"    ⚡ Cache HIT  →  {cached.record.value}  (TTL {cached.remaining_ttl}s remaining)")
        return cached.record
    if verbose:
        print(f"    ✗ Cache MISS — starting recursive resolution")
    parts = name.rstrip(".").split(".")
    tld = parts[-1] + "."
    domain = ".".join(parts[-2:]) + "." if len(parts) >= 2 else tld
    steps = [("root", "Root"), (tld, "TLD"), (domain, "Authoritative")]
    answer = None
    for zone_key, label in steps:
        zone = ZONES.get(zone_key)
        if not zone:
            continue
        if verbose:
            print(f"    → Querying {label} server ({zone_key})...")
        rec = zone.query(name, rtype)
        if rec:
            answer = rec
            if verbose:
                print(f"      ✓ Answer: {rec}")
            break
        # Check for NS referral
        ns_rec = zone.query(domain, "NS") if zone_key != domain else None
        if ns_rec and verbose:
            print(f"      ↳ Referral: {ns_rec.value}")

    if answer:
        cache.store(answer)
        if verbose:
            print(f"    Cached with TTL={answer.ttl}s")
        return answer

    if verbose:
        print(f"    ✗ NXDOMAIN — name not found")
    return None


def demo(num_extra_queries: int, time_step: int):
    print("=" * 65)
    print("  DNS Cache Simulator with TTL-Based Expiry")
    print("=" * 65)
    _build_zones()

    print("\n  Hierarchy: [Root .] → [TLD com./org.] → [Authoritative zone]")
    print("  Each answer is cached; TTL counts down with simulated time.\n")

    cache = DNSResolverCache()
    sim_time = 0

    scripted_queries = [
        ("example.com.", "A",  0),
        ("example.com.", "A",  0),   # immediate cache hit
        ("mail.example.com.", "A", 0),
        ("openai.org.", "A", 0),
        ("example.com.", "A", 35),   # 35 s later — still cached (TTL 60)
        ("mail.example.com.", "A", 0),  # 35 s total — TTL 30 expired
        ("api.example.com.", "A", 0),
        ("nonexistent.example.com.", "A", 0),
        ("example.com.", "A", 30),   # 65 s total — TTL 60 expired
    ]

    # Add random queries if requested
    names = ["example.com.", "www.example.com.", "mail.example.com.",
             "api.example.com.", "openai.org.", "docs.openai.org."]
    rng = random.Random(7)
    for _ in range(num_extra_queries):
        scripted_queries.append((rng.choice(names), "A", rng.choice([0, 10, 20, 40])))

    for name, rtype, dt in scripted_queries:
        if dt > 0:
            sim_time += dt
            print(f"\n  ⏱  Time advances by {dt}s  (now T={sim_time}s)")
            expired = cache.advance_time(dt)
            if expired:
                for k in expired:
                    print(f"    🗑  Expired from cache: {k[0]} {k[1]}")
            else:
                print(f"    (no cache entries expired)")

        resolve(cache, name, rtype, verbose=True)

    # Summary
    print(f"\n{'═' * 65}")
    print(f"  Cache state at T={sim_time}s:")
    cache.dump()

    print(f"\n  Resolver statistics:")
    print(f"    Cache hits  : {cache.total_hits}")
    print(f"    Cache misses: {cache.total_misses}")
    total = cache.total_hits + cache.total_misses
    if total:
        print(f"    Hit ratio   : {cache.total_hits/total*100:.0f}%")

    print(f"\n  Authoritative server query counts:")
    for zname, zone in ZONES.items():
        if zone.queries_received:
            print(f"    {zname:25s} → {zone.queries_received} queries")

    print(f"\n  Key takeaway: caching reduces upstream queries. Short TTLs")
    print(f"  cause more misses; long TTLs (NS records) are refreshed rarely.")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS cache simulator with TTL-based expiry")
    parser.add_argument("--queries", type=int, default=0,
                        help="Extra random queries to append after scripted demo")
    parser.add_argument("--time-step", type=int, default=30,
                        help="Time step in seconds between query batches (default: 30)")
    args = parser.parse_args()
    demo(args.queries, args.time_step)
