#!/usr/bin/env python3
"""
Routing Table Simulator
========================
Simulates IP routing table lookups using longest-prefix-match (LPM), the
fundamental algorithm routers use to forward packets.

A routing table contains entries with:
  - Destination network (e.g. 10.0.0.0)
  - Subnet mask / prefix length (e.g. /8)
  - Next-hop gateway IP
  - Outgoing interface name
  - Metric (cost; lower is preferred when multiple routes match equally)

When a packet arrives, the router converts the destination IP to an integer,
ANDs it with each route's mask, and checks for a match.  Among all matching
routes the one with the *longest* prefix (most specific mask) wins.  Ties are
broken by the lowest metric.

Concepts demonstrated:
  * CIDR notation and subnet masks
  * Longest-prefix-match forwarding
  * Default route (0.0.0.0/0) as a catch-all
  * Metric-based tie-breaking

Usage:
    python routing_table_simulator.py                       # built-in demo
    python routing_table_simulator.py -d 192.168.1.100      # look up one IP
    python routing_table_simulator.py -d 10.5.5.5 8.8.8.8   # look up several
"""

import argparse
import struct
import textwrap


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def ip_to_int(ip: str) -> int:
    """Convert dotted-quad IPv4 string to a 32-bit integer."""
    parts = [int(p) for p in ip.strip().split(".")]
    return struct.unpack("!I", bytes(parts))[0]


def int_to_ip(n: int) -> str:
    """Convert a 32-bit integer back to dotted-quad."""
    return ".".join(str(b) for b in struct.pack("!I", n))


def prefix_to_mask(prefix_len: int) -> int:
    """Return the integer mask for a given prefix length (0-32)."""
    if prefix_len == 0:
        return 0
    return (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF


def parse_cidr(cidr: str):
    """Parse '10.0.0.0/8' into (network_int, prefix_len)."""
    network_str, prefix_str = cidr.split("/")
    return ip_to_int(network_str), int(prefix_str)


# ---------------------------------------------------------------------------
# Routing table
# ---------------------------------------------------------------------------

class Route:
    """One entry in the routing table."""

    def __init__(self, cidr: str, next_hop: str, interface: str, metric: int = 0):
        self.cidr = cidr
        self.network, self.prefix_len = parse_cidr(cidr)
        self.mask = prefix_to_mask(self.prefix_len)
        self.next_hop = next_hop
        self.interface = interface
        self.metric = metric

    def matches(self, dest_int: int) -> bool:
        return (dest_int & self.mask) == self.network

    def __repr__(self):
        return (f"Route({self.cidr:18s} -> next-hop {self.next_hop:15s} "
                f"via {self.interface:6s}  metric {self.metric})")


class RoutingTable:
    """A simple IPv4 routing table with longest-prefix-match lookup."""

    def __init__(self):
        self.routes: list = []

    def add_route(self, cidr, next_hop, interface, metric=0):
        route = Route(cidr, next_hop, interface, metric)
        self.routes.append(route)

    def lookup(self, dest_ip: str, verbose: bool = True) -> Route:
        dest_int = ip_to_int(dest_ip)
        matches = [r for r in self.routes if r.matches(dest_int)]
        if not matches:
            if verbose:
                print(f"  [!] No route found for {dest_ip} — packet dropped.")
            return None

        # Sort by longest prefix first, then lowest metric
        matches.sort(key=lambda r: (-r.prefix_len, r.metric))

        if verbose:
            print(f"  Matching routes for {dest_ip}:")
            for m in matches:
                print(f"    • {m.cidr:18s}  (prefix /{m.prefix_len}, metric {m.metric})")
            print(f"  ✓ Best match: {matches[0].cidr} "
                  f"→ forward to {matches[0].next_hop} via {matches[0].interface}")
        return matches[0]

    def display(self):
        print("\n╔══════════════════════════════════════════════════════════════════╗")
        print("║                        ROUTING TABLE                           ║")
        print("╠══════════════════╤═══════════════╤════════╤═════════════════════╣")
        print("║ Destination      │ Next Hop      │ Iface  │ Metric              ║")
        print("╟──────────────────┼───────────────┼────────┼─────────────────────╢")
        for r in self.routes:
            print(f"║ {r.cidr:16s} │ {r.next_hop:13s} │ {r.interface:6s} │ {r.metric:<19d} ║")
        print("╚══════════════════╧═══════════════╧════════╧═════════════════════╝\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def build_demo_table() -> RoutingTable:
    """Create a realistic sample routing table."""
    rt = RoutingTable()
    rt.add_route("0.0.0.0/0",       "203.0.113.1",  "eth0", metric=100)
    rt.add_route("10.0.0.0/8",      "10.0.0.1",     "eth1", metric=10)
    rt.add_route("10.1.0.0/16",     "10.1.0.1",     "eth1", metric=10)
    rt.add_route("10.1.1.0/24",     "10.1.1.1",     "eth2", metric=5)
    rt.add_route("192.168.0.0/16",  "192.168.0.1",  "eth3", metric=10)
    rt.add_route("192.168.1.0/24",  "192.168.1.1",  "eth3", metric=5)
    rt.add_route("172.16.0.0/12",   "172.16.0.1",   "eth4", metric=20)
    return rt


def run_demo():
    print(textwrap.dedent("""\
        ╭─────────────────────────────────────────────────────╮
        │         Routing Table Simulator — Demo Mode         │
        ╰─────────────────────────────────────────────────────╯
    """))
    print("Building a sample routing table …\n")
    rt = build_demo_table()
    rt.display()

    test_ips = [
        "10.1.1.50",       # matches /8, /16, and /24 → /24 wins
        "10.1.2.99",       # matches /8 and /16 → /16 wins
        "10.5.0.1",        # matches only /8
        "192.168.1.42",    # matches /16 and /24 → /24 wins
        "192.168.50.1",    # matches /16 only
        "172.16.5.10",     # matches /12
        "8.8.8.8",         # matches only default route
        "255.255.255.255", # broadcast — only default route
    ]

    for ip in test_ips:
        print(f"\n── Routing lookup for {ip} ──")
        rt.lookup(ip)


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Simulate IPv4 routing table lookups with longest-prefix match.")
    parser.add_argument(
        "-d", "--dest", nargs="*",
        help="Destination IP(s) to look up.  Omit to run the built-in demo.")
    args = parser.parse_args()

    if not args.dest:
        run_demo()
        return

    rt = build_demo_table()
    rt.display()
    for ip in args.dest:
        print(f"\n── Routing lookup for {ip} ──")
        rt.lookup(ip)


if __name__ == "__main__":
    main()
