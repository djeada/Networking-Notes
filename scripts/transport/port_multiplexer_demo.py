#!/usr/bin/env python3
"""
Transport-Layer Port Multiplexing / Demultiplexing Demo
========================================================
Demonstrates how the transport layer uses **4-tuples**
(src_ip, src_port, dst_ip, dst_port) to multiplex many
application flows over a single IP address.

When a host has several programs communicating over the network, the OS
must *demultiplex* incoming segments to the correct socket.  For TCP the
lookup key is the full 4-tuple; for UDP it is typically only the
destination IP and port.  This script simulates both behaviours.

Key concepts:
  * Multiplexing   — gathering data from multiple sockets, adding
                     transport headers, and passing to the network layer.
  * Demultiplexing — delivering incoming segments to the correct socket
                     using header fields.
  * 4-tuple identification (TCP) vs. 2-tuple (UDP)
  * Ephemeral (source) ports assigned by the OS
  * Well-known destination ports (80, 443, 53, …)

Usage:
    python port_multiplexer_demo.py                     # built-in demo
    python port_multiplexer_demo.py --connections 6     # custom count
    python port_multiplexer_demo.py --show-udp          # include UDP demo
"""

import argparse
import random
import collections

# ── Data structures ───────────────────────────────────────────────────

Connection = collections.namedtuple(
    "Connection", ["src_ip", "src_port", "dst_ip", "dst_port", "proto", "app"]
)

WELL_KNOWN_PORTS = {
    22:  "SSH",
    53:  "DNS",
    80:  "HTTP",
    443: "HTTPS",
    993: "IMAPS",
}

SAMPLE_APPS = [
    ("Web browser tab 1",  "93.184.216.34", 443),
    ("Web browser tab 2",  "93.184.216.34", 443),
    ("Web browser tab 3",  "151.101.1.69",  443),
    ("SSH session",         "192.0.2.10",    22),
    ("Mail client (IMAPS)", "74.125.24.108", 993),
    ("DNS resolver",        "8.8.8.8",       53),
    ("curl to API",         "104.26.10.78",  80),
    ("Another SSH",         "192.0.2.10",    22),
]

LOCAL_IP = "10.0.0.5"

# ── helpers ───────────────────────────────────────────────────────────

def allocate_ephemeral_port(used, rng):
    """Pick a random ephemeral port (49152-65535) not already in use."""
    while True:
        port = rng.randint(49152, 65535)
        if port not in used:
            used.add(port)
            return port


def port_service(port):
    return WELL_KNOWN_PORTS.get(port, "unknown")


def fmt_tuple(conn):
    return (f"({conn.src_ip}:{conn.src_port} → "
            f"{conn.dst_ip}:{conn.dst_port} [{conn.proto}])")

# ── simulation ────────────────────────────────────────────────────────

def create_connections(count, rng):
    """Build a list of Connection namedtuples with unique 4-tuples."""
    used_ports = set()
    conns = []
    for i in range(count):
        app_name, dst_ip, dst_port = SAMPLE_APPS[i % len(SAMPLE_APPS)]
        src_port = allocate_ephemeral_port(used_ports, rng)
        proto = "UDP" if dst_port == 53 else "TCP"
        conns.append(Connection(LOCAL_IP, src_port, dst_ip, dst_port, proto, app_name))
    return conns


def show_connection_table(conns):
    """Print a nicely formatted connection table."""
    hdr = (f"  {'#':>2}  {'Application':<22} {'Proto':<5} "
           f"{'Source':>21}  {'Destination':>21}")
    sep = "  " + "─" * 76
    print(sep)
    print(hdr)
    print(sep)
    for idx, c in enumerate(conns, 1):
        src = f"{c.src_ip}:{c.src_port}"
        dst = f"{c.dst_ip}:{c.dst_port}"
        print(f"  {idx:>2}  {c.app:<22} {c.proto:<5} {src:>21}  {dst:>21}")
    print(sep)


def demux_demo_tcp(conns):
    """Show TCP demultiplexing: full 4-tuple match required."""
    tcp_conns = [c for c in conns if c.proto == "TCP"]
    if not tcp_conns:
        return

    print("\n  ── TCP Demultiplexing (4-tuple lookup) ──\n")
    print("  The OS keeps a table mapping each 4-tuple to a socket/FD.\n")

    # Build lookup table
    table = {}
    for c in tcp_conns:
        key = (c.src_ip, c.src_port, c.dst_ip, c.dst_port)
        table[key] = c.app

    # Simulate incoming segments (reverse the direction)
    print("  Incoming segments (from remote → local):")
    for c in tcp_conns:
        seg_tuple = (c.dst_ip, c.dst_port, c.src_ip, c.src_port)
        lookup = (c.src_ip, c.src_port, c.dst_ip, c.dst_port)
        matched = table.get(lookup, "NO MATCH")
        print(f"    segment {c.dst_ip}:{c.dst_port} → {c.src_ip}:{c.src_port}"
              f"  ⟶  socket: {matched}")

    # Highlight two connections to same dst but different src_port
    same_dst = collections.defaultdict(list)
    for c in tcp_conns:
        same_dst[(c.dst_ip, c.dst_port)].append(c)

    for key, group in same_dst.items():
        if len(group) > 1:
            print(f"\n  ★ {len(group)} connections share destination "
                  f"{key[0]}:{key[1]} ({port_service(key[1])})")
            print("    They are distinguished by their source ports:")
            for c in group:
                print(f"      src_port={c.src_port}  →  {c.app}")


def demux_demo_udp(conns):
    """Show UDP demultiplexing: only dst_ip + dst_port needed."""
    udp_conns = [c for c in conns if c.proto == "UDP"]
    if not udp_conns:
        print("\n  (No UDP connections in this demo — use --show-udp)\n")
        return

    print("\n  ── UDP Demultiplexing (2-tuple lookup) ──\n")
    print("  UDP sockets are identified by (local IP, local port) only.")
    print("  All segments to that port go to the SAME socket,")
    print("  regardless of the remote address.\n")

    seen = set()
    for c in udp_conns:
        local_key = (c.src_ip, c.src_port)
        if local_key in seen:
            continue
        seen.add(local_key)
        print(f"    Socket bound to {c.src_ip}:{c.src_port} "
              f"(app: {c.app})")
        print(f"      ← any remote can send to this port and reach the same socket.\n")


def multiplexing_visual(conns):
    """ASCII art showing multiple apps funnelling through one IP."""
    print("\n  ── Multiplexing: many apps, one IP ──\n")
    apps = [f"{c.app} (:{c.src_port})" for c in conns[:5]]
    width = max(len(a) for a in apps) + 4

    for a in apps:
        print(f"    {a:>{width}}  ─┐")
    print(f"    {'':>{width}}   ├──▶  [{LOCAL_IP}]  ──▶  Network")
    remaining = len(conns) - 5
    if remaining > 0:
        print(f"    {'... +' + str(remaining) + ' more':>{width}}  ─┘")
    else:
        last = apps[-1] if apps else ""
        print(f"    {'':>{width}}  ─┘")

    print(f"\n    Each outgoing segment carries (src_ip, src_port, dst_ip, dst_port)")
    print(f"    so the remote host and local OS can demultiplex correctly.\n")

# ── entry point ───────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        description="Demonstrate transport-layer port multiplexing/demux.")
    p.add_argument("--connections", type=int, default=0,
                   help="Number of connections to simulate (default: demo)")
    p.add_argument("--show-udp", action="store_true",
                   help="Include UDP demux explanation")
    p.add_argument("--seed", type=int, default=7,
                   help="Random seed for reproducibility")
    return p


def main():
    args = build_parser().parse_args()
    rng = random.Random(args.seed)

    count = args.connections if args.connections > 0 else 6

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║    Transport-Layer Port Multiplexing / Demux Demo           ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Ensure DNS connection present when --show-udp
    effective_count = max(count, 6) if args.show_udp else count
    conns = create_connections(effective_count, rng)

    print(f"\n  Local host: {LOCAL_IP}")
    print(f"  Active connections: {len(conns)}\n")

    show_connection_table(conns)

    multiplexing_visual(conns)

    demux_demo_tcp(conns)
    demux_demo_udp(conns)

    if not args.show_udp and not any(c.proto == "UDP" for c in conns):
        print("  Tip: run with --show-udp to see UDP demux behaviour.\n")

    print("✔  Demo complete.\n")


if __name__ == "__main__":
    main()
