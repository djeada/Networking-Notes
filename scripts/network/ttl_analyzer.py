#!/usr/bin/env python3
"""
TTL (Time To Live) Analyzer
=============================
Analyses observed TTL values to infer the sender's operating system and the
approximate number of network hops between sender and receiver.

Every IP datagram carries a TTL field (8-bit, max 255).  The sender sets an
initial value and each router along the path decrements it by 1.  When TTL
reaches 0 the packet is discarded, preventing infinite routing loops.

Different operating systems use characteristic initial TTL values:

    OS family          Typical initial TTL
    ──────────────────────────────────────
    Linux / Android         64
    Windows (modern)       128
    macOS / iOS             64
    Cisco IOS              255
    Solaris / AIX           255
    FreeBSD                 64

By observing the TTL when a packet *arrives*, we can estimate:
  initial_ttl  = next power-of-two-ish common value >= observed TTL
  hops         = initial_ttl − observed_ttl

This is a heuristic — firewalls and tunnels can alter TTL, and some hosts
choose non-standard values.

Concepts demonstrated:
  * TTL purpose (loop prevention) and decrement behaviour
  * OS fingerprinting via initial TTL
  * Hop-count estimation
  * How traceroute exploits TTL expiry

Usage:
    python ttl_analyzer.py                        # built-in demo
    python ttl_analyzer.py -t 117                 # analyse one TTL value
    python ttl_analyzer.py -t 52 120 243 64 1     # analyse several
"""

import argparse
import textwrap

# ---------------------------------------------------------------------------
# Known initial TTL → OS mapping
# ---------------------------------------------------------------------------

KNOWN_TTLS = [
    (32,  ["Windows 95/98"]),
    (64,  ["Linux", "macOS", "iOS", "Android", "FreeBSD"]),
    (128, ["Windows 10/11", "Windows Server", "Windows 7/8"]),
    (255, ["Cisco IOS", "Solaris", "AIX", "HP-UX"]),
]

# Sorted initial values for quick lookup
INITIAL_VALUES = sorted(t[0] for t in KNOWN_TTLS)


# ---------------------------------------------------------------------------
# Analysis logic
# ---------------------------------------------------------------------------

def guess_initial_ttl(observed: int) -> int:
    """Return the most likely initial TTL for an observed value."""
    for init in INITIAL_VALUES:
        if observed <= init:
            return init
    return 255


def analyse_ttl(observed: int) -> dict:
    """Analyse a single observed TTL value."""
    if observed < 1 or observed > 255:
        return {"error": f"Invalid TTL {observed}: must be 1-255"}

    initial = guess_initial_ttl(observed)
    hops = initial - observed

    os_list = []
    for init_val, systems in KNOWN_TTLS:
        if init_val == initial:
            os_list = systems
            break

    return {
        "observed": observed,
        "initial": initial,
        "hops": hops,
        "os_candidates": os_list,
    }


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_reference_table():
    print("  Common initial TTL values by OS:")
    print(f"  {'─' * 50}")
    print(f"  {'Initial TTL':>12s}   OS families")
    print(f"  {'─' * 50}")
    for init, systems in KNOWN_TTLS:
        print(f"  {init:>12d}   {', '.join(systems)}")
    print(f"  {'─' * 50}\n")


def print_analysis(info: dict):
    if "error" in info:
        print(f"  ✗ {info['error']}")
        return

    obs = info["observed"]
    init = info["initial"]
    hops = info["hops"]
    os_list = info["os_candidates"]

    print(f"  Observed TTL : {obs}")
    print(f"  Estimated initial TTL : {init}")
    print(f"  Estimated hops        : {hops}")
    print(f"  Likely OS             : {', '.join(os_list) if os_list else 'Unknown'}")

    # Confidence note
    if hops == 0:
        print("  Note: 0 hops means the packet likely originated on this host "
              "or a directly-connected device.")
    elif hops > 30:
        print(f"  Note: {hops} hops is unusually high. The initial TTL guess "
              "may be incorrect, or the packet traversed many networks.")

    # Visual hop bar
    bar_max = 30
    bar_len = min(hops, bar_max)
    bar = "─" * bar_len + "▶" if hops > 0 else "●"
    print(f"  Path visual : [{bar}]  ({hops} hop{'s' if hops != 1 else ''})")


def simulate_path(initial_ttl: int, hop_count: int, src: str, dst: str):
    """Simulate a packet traversing routers, showing TTL at each hop."""
    print(f"\n  Simulating {src} → {dst}  (initial TTL={initial_ttl}, "
          f"{hop_count} hops)\n")
    ttl = initial_ttl
    print(f"    [SRC {src}]  TTL={ttl}")
    for i in range(1, hop_count + 1):
        ttl -= 1
        if ttl <= 0:
            print(f"    Router {i:>2d}: TTL=0 → ✗ PACKET DROPPED (TTL expired)")
            return
        print(f"    Router {i:>2d}: TTL={ttl}")
    print(f"    [DST {dst}]  TTL={ttl}  ← packet delivered\n")
    return ttl


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    print(textwrap.dedent("""\
        ╭──────────────────────────────────────────────────────╮
        │           TTL Analyzer — Demo Mode                   │
        ╰──────────────────────────────────────────────────────╯
    """))

    print_reference_table()

    # Analyse a variety of observed TTL values
    sample_ttls = [64, 128, 255, 52, 117, 243, 1, 30, 60, 127]
    print("  Analysing sample TTL values:\n")
    for ttl in sample_ttls:
        print(f"  {'═' * 48}")
        print_analysis(analyse_ttl(ttl))
    print(f"  {'═' * 48}\n")

    # Path simulations
    print("  ╌╌╌ Path simulation examples ╌╌╌")
    simulate_path(64,  12, "192.168.1.10 (Linux)",   "93.184.216.34")
    simulate_path(128,  8, "10.0.0.5 (Windows)",     "8.8.8.8")
    simulate_path(255, 20, "172.16.0.1 (Cisco)",     "198.51.100.1")
    simulate_path(64,  70, "10.1.1.1 (Linux)",       "203.0.113.50")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyse TTL values to estimate sender OS and hop count.")
    parser.add_argument("-t", "--ttl", nargs="*", type=int,
                        help="Observed TTL value(s) to analyse. Omit for demo.")
    args = parser.parse_args()

    if not args.ttl:
        run_demo()
        return

    print_reference_table()
    for ttl in args.ttl:
        print(f"\n  {'═' * 48}")
        print_analysis(analyse_ttl(ttl))
    print()


if __name__ == "__main__":
    main()
