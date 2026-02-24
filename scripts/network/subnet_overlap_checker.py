#!/usr/bin/env python3
"""
Subnet Overlap Checker
=======================
Determines whether two or more IPv4 subnets overlap — a common mistake in
network planning that leads to ambiguous routing and connectivity issues.

Algorithm:
  1. Parse each CIDR block into a (network, broadcast) integer range.
  2. For every pair of subnets, check if one range intersects the other.
     Two ranges [a_lo, a_hi] and [b_lo, b_hi] overlap iff
         a_lo <= b_hi  AND  b_lo <= a_hi
  3. Report all overlapping pairs with their shared address range.

Concepts demonstrated:
  * CIDR notation ↔ address ranges
  * Network and broadcast address calculation
  * Pairwise overlap detection
  * Visual address-range bars for intuitive comparison

Usage:
    python subnet_overlap_checker.py                                 # demo
    python subnet_overlap_checker.py -s 10.0.0.0/24 10.0.0.128/25   # custom
    python subnet_overlap_checker.py -s 192.168.0.0/16 192.168.1.0/24 10.0.0.0/8
"""

import argparse
import struct
import textwrap
from itertools import combinations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ip_to_int(ip: str) -> int:
    parts = [int(p) for p in ip.strip().split(".")]
    return struct.unpack("!I", bytes(parts))[0]


def int_to_ip(n: int) -> str:
    return ".".join(str(b) for b in struct.pack("!I", n))


class Subnet:
    """Represents an IPv4 CIDR block."""

    def __init__(self, cidr: str):
        self.cidr = cidr.strip()
        net_str, prefix_str = self.cidr.split("/")
        self.prefix_len = int(prefix_str)
        if self.prefix_len == 0:
            mask = 0
        else:
            mask = (0xFFFFFFFF << (32 - self.prefix_len)) & 0xFFFFFFFF
        self.network = ip_to_int(net_str) & mask
        self.broadcast = self.network | (mask ^ 0xFFFFFFFF)
        self.host_count = self.broadcast - self.network + 1

    @property
    def network_ip(self):
        return int_to_ip(self.network)

    @property
    def broadcast_ip(self):
        return int_to_ip(self.broadcast)

    def overlaps(self, other: "Subnet") -> bool:
        return self.network <= other.broadcast and other.network <= self.broadcast

    def overlap_range(self, other: "Subnet"):
        if not self.overlaps(other):
            return None
        lo = max(self.network, other.network)
        hi = min(self.broadcast, other.broadcast)
        return lo, hi

    def __repr__(self):
        return (f"{self.cidr:18s}  range {self.network_ip:>15s} – "
                f"{self.broadcast_ip:<15s}  ({self.host_count} addrs)")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def display_subnets(subnets: list):
    print("\n  Subnets under analysis:")
    print(f"  {'─' * 72}")
    for i, s in enumerate(subnets, 1):
        print(f"    {i}. {s}")
    print(f"  {'─' * 72}\n")


def visualise(subnets: list):
    """Draw a simple ASCII range diagram."""
    if not subnets:
        return
    all_lo = min(s.network for s in subnets)
    all_hi = max(s.broadcast for s in subnets)
    span = all_hi - all_lo
    if span == 0:
        span = 1
    width = 60

    print("  Address-range visualisation:")
    print(f"  {int_to_ip(all_lo):<15s}{' ' * (width - 30)}{int_to_ip(all_hi):>15s}")
    print(f"  {'│' + '─' * width + '│'}")
    for i, s in enumerate(subnets):
        start = int((s.network - all_lo) / span * width)
        end = int((s.broadcast - all_lo) / span * width)
        bar_len = max(1, end - start + 1)
        line = " " * start + "█" * bar_len
        print(f"  │{line:<{width}}│  {s.cidr}")
    print(f"  {'│' + '─' * width + '│'}\n")


def check_overlaps(subnets: list):
    """Check every pair and report overlaps."""
    found = False
    for a, b in combinations(subnets, 2):
        r = a.overlap_range(b)
        if r:
            found = True
            lo, hi = r
            count = hi - lo + 1
            print(f"  ⚠  OVERLAP between {a.cidr} and {b.cidr}")
            print(f"     Shared range: {int_to_ip(lo)} – {int_to_ip(hi)}  "
                  f"({count} address{'es' if count != 1 else ''})")
            # Determine relationship
            if a.network <= b.network and a.broadcast >= b.broadcast:
                print(f"     → {b.cidr} is entirely contained within {a.cidr}\n")
            elif b.network <= a.network and b.broadcast >= a.broadcast:
                print(f"     → {a.cidr} is entirely contained within {b.cidr}\n")
            else:
                print(f"     → Partial overlap\n")

    if not found:
        print("  ✓ No overlaps detected — all subnets are disjoint.\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    print(textwrap.dedent("""\
        ╭──────────────────────────────────────────────────────╮
        │        Subnet Overlap Checker — Demo Mode            │
        ╰──────────────────────────────────────────────────────╯
    """))

    scenarios = [
        (
            "Scenario 1: overlapping private ranges",
            ["10.0.0.0/8", "10.1.0.0/16", "10.1.1.0/24"],
        ),
        (
            "Scenario 2: adjacent but non-overlapping",
            ["192.168.0.0/24", "192.168.1.0/24", "192.168.2.0/24"],
        ),
        (
            "Scenario 3: partial overlap",
            ["172.16.0.0/20", "172.16.8.0/21"],
        ),
        (
            "Scenario 4: completely disjoint",
            ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        ),
        (
            "Scenario 5: identical subnets",
            ["192.168.1.0/24", "192.168.1.0/24"],
        ),
    ]

    for title, cidrs in scenarios:
        print(f"\n  ╌╌╌ {title} ╌╌╌")
        subnets = [Subnet(c) for c in cidrs]
        display_subnets(subnets)
        visualise(subnets)
        check_overlaps(subnets)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Check whether IPv4 subnets overlap.")
    parser.add_argument("-s", "--subnets", nargs="*",
                        help="Two or more CIDR blocks (e.g. 10.0.0.0/24). "
                             "Omit to run demo.")
    args = parser.parse_args()

    if not args.subnets:
        run_demo()
        return

    if len(args.subnets) < 2:
        parser.error("Provide at least two subnets to compare.")

    subnets = [Subnet(c) for c in args.subnets]
    display_subnets(subnets)
    visualise(subnets)
    check_overlaps(subnets)


if __name__ == "__main__":
    main()
