#!/usr/bin/env python3
"""
Traceroute Simulator
=====================
Simulates the traceroute process to teach how TTL-based route discovery
works.  Real ``traceroute`` requires raw sockets and often root privileges;
this script instead uses a **simulated network topology** to demonstrate
the concept step by step.

How traceroute works (simplified):
1. Send a packet with TTL = 1.  The first router decrements TTL to 0,
   drops the packet, and sends back an ICMP "Time Exceeded" message.
2. Record that router's IP as hop 1.
3. Send a packet with TTL = 2.  The second router sends "Time Exceeded".
4. Repeat, incrementing TTL, until the destination replies (ICMP Echo Reply
   or port unreachable for UDP-based traceroute).

The simulated topology is fully configurable — feel free to edit the
``TOPOLOGIES`` dict to explore different network paths.

Usage:
    python traceroute_sim.py                    # run the built-in demo
    python traceroute_sim.py --topology wan     # use the 'wan' topology
"""

import argparse
import random
import time
import sys

# ---------------------------------------------------------------------------
# Simulated network topologies
# Each topology is a list of (router_ip, router_name, simulated_rtt_ms).
# The *last* entry is the destination host itself.
# ---------------------------------------------------------------------------
TOPOLOGIES = {
    "default": {
        "source": "192.168.1.100",
        "destination": "93.184.216.34",
        "destination_name": "example.com",
        "hops": [
            ("192.168.1.1", "Home Router (default gateway)", 1.2),
            ("10.0.0.1", "ISP Access Router", 8.5),
            ("10.10.10.1", "ISP Aggregation Router", 14.3),
            ("172.16.0.1", "ISP Core Router", 22.1),
            ("198.51.100.1", "Internet Exchange Point", 35.7),
            ("203.0.113.10", "CDN Edge Router", 42.4),
            ("93.184.216.34", "example.com (destination)", 48.9),
        ],
    },
    "wan": {
        "source": "10.1.1.50",
        "destination": "151.101.1.69",
        "destination_name": "reddit.com",
        "hops": [
            ("10.1.1.1", "Office Gateway", 0.8),
            ("10.255.0.1", "Corporate WAN Router", 5.2),
            ("172.20.0.1", "Regional ISP PE Router", 12.0),
            ("172.20.255.1", "ISP Backbone (City A)", 25.4),
            ("172.20.255.5", "ISP Backbone (City B)", 38.6),
            ("198.51.100.50", "Peering Point", 45.1),
            ("151.101.0.1", "Destination AS Edge", 50.3),
            ("151.101.1.69", "reddit.com (destination)", 52.7),
        ],
    },
    "local": {
        "source": "192.168.0.10",
        "destination": "192.168.0.50",
        "destination_name": "local-server",
        "hops": [
            ("192.168.0.1", "LAN Switch / Router", 0.4),
            ("192.168.0.50", "local-server (destination)", 0.9),
        ],
    },
}


# ---------------------------------------------------------------------------
# Simulation engine
# ---------------------------------------------------------------------------

def simulate_traceroute(topology_name: str = "default", verbose: bool = True) -> list[dict]:
    """Simulate a traceroute using the named topology.

    Returns a list of hop dicts with keys: hop, ip, name, rtt_ms, status.
    """
    topo = TOPOLOGIES[topology_name]
    source = topo["source"]
    destination = topo["destination"]
    dest_name = topo["destination_name"]
    hops = topo["hops"]
    max_hops = len(hops)

    if verbose:
        print("=" * 66)
        print(f"  Traceroute Simulation")
        print("=" * 66)
        print(f"  Source      : {source}")
        print(f"  Destination : {destination} ({dest_name})")
        print(f"  Max hops    : {max_hops}")
        print(f"  Topology    : '{topology_name}'")
        print("=" * 66)
        print()

    results = []

    for ttl in range(1, max_hops + 1):
        hop_ip, hop_name, base_rtt = hops[ttl - 1]
        is_destination = (hop_ip == destination)

        # Simulate three probes per hop (like real traceroute)
        rtts = []
        for _ in range(3):
            jitter = random.uniform(-0.5, 0.5)
            rtts.append(round(max(0.1, base_rtt + jitter), 2))

        if is_destination:
            status = "Reply (destination reached)"
            icmp_type = "Echo Reply / Port Unreachable"
        else:
            status = "Time Exceeded"
            icmp_type = "ICMP Type 11 — Time Exceeded"

        hop_result = {
            "hop": ttl,
            "ip": hop_ip,
            "name": hop_name,
            "rtts": rtts,
            "status": status,
        }
        results.append(hop_result)

        if verbose:
            rtt_str = "  ".join(f"{r:6.2f} ms" for r in rtts)
            print(f"  TTL={ttl:<3d}  {hop_ip:<20s}  {rtt_str}")
            print(f"           {hop_name}")
            print(f"           ICMP: {icmp_type}")
            if not is_destination:
                print(f"           → Router decrements TTL to 0, sends Time Exceeded")
            else:
                print(f"           ✓ Destination reached!")
            print()

            # Small delay to make the simulation feel more realistic
            time.sleep(0.15)

        if is_destination:
            break

    if verbose:
        print("=" * 66)
        print(f"  Trace complete — {len(results)} hops to {dest_name}")
        print("=" * 66)
        print()
        _print_educational_notes()

    return results


def _print_educational_notes() -> None:
    """Print educational notes about how traceroute works."""
    print("-" * 66)
    print("  How Traceroute Works (summary)")
    print("-" * 66)
    print("""
  1. The source sends a probe packet with TTL (Time To Live) = 1.
  2. The first router receives the packet, decrements TTL to 0, and
     MUST discard it.  It sends back an ICMP "Time Exceeded" message.
  3. The source records the router's IP and the round-trip time (RTT).
  4. The source sends another probe with TTL = 2.  Now the first router
     passes it on (TTL becomes 1), but the SECOND router hits TTL = 0
     and replies with Time Exceeded.
  5. This continues with TTL = 3, 4, 5, ... until the probe reaches
     the destination, which replies normally (ICMP Echo Reply for
     ICMP-based traceroute, or Port Unreachable for UDP-based).
  6. Three probes are typically sent per hop to measure RTT variance.

  Useful notes:
  • Some routers don't respond to TTL-expired packets (shown as * * *)
  • Asymmetric routing means the return path may differ from forward path
  • Firewalls may block ICMP, causing incomplete traces
  • On Windows, use `tracert`; on Linux/macOS, use `traceroute`
""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Simulate traceroute to demonstrate TTL-based route discovery."
    )
    parser.add_argument(
        "--topology", "-t",
        choices=list(TOPOLOGIES.keys()),
        default="default",
        help="Simulated network topology to use (default: 'default').",
    )
    parser.add_argument(
        "--list-topologies", "-l",
        action="store_true",
        help="List available topologies and exit.",
    )
    args = parser.parse_args()

    if args.list_topologies:
        print("Available topologies:")
        for name, topo in TOPOLOGIES.items():
            print(f"  {name:<12s}  {topo['source']} → {topo['destination']} "
                  f"({topo['destination_name']}, {len(topo['hops'])} hops)")
        return

    simulate_traceroute(topology_name=args.topology)


if __name__ == "__main__":
    main()
