#!/usr/bin/env python3
"""
Traceroute Visualizer
======================
Takes traceroute-style data (simulated or user-supplied) and produces an
ASCII diagram of the network path, highlighting each hop's round-trip time
and flagging potential bottlenecks.

How traceroute works (conceptual overview):
  1. Send a probe packet with TTL = 1.  The first router decrements TTL
     to 0 and replies with ICMP Time Exceeded, revealing its IP.
  2. Increment TTL and repeat.  Each router along the path is discovered.
  3. When the probe reaches the destination, it replies with ICMP Echo
     Reply (or Port Unreachable for UDP probes).

This script does NOT send real packets.  Instead it:
  * Generates realistic simulated traceroute data, OR
  * Accepts hop data via --hops on the command line.

It then renders:
  * A numbered hop table with RTT statistics
  * An ASCII network-path diagram
  * A bottleneck analysis (hops where RTT jumps significantly)

Concepts demonstrated:
  * How TTL-based route discovery works
  * Interpreting RTT variations along a path
  * Identifying congested or distant hops
  * ASCII data visualisation techniques

Usage:
    python traceroute_visualizer.py                          # demo routes
    python traceroute_visualizer.py --destination 8.8.8.8    # simulated route
    python traceroute_visualizer.py --hops '192.168.1.1:1.2' \\
        '10.0.0.1:5.4' '72.14.236.1:15.3' '8.8.8.8:20.1'
"""

import argparse
import random
import textwrap

# --------------------------------------------------------------------------- #
# Simulated route templates                                                   #
# --------------------------------------------------------------------------- #
_TEMPLATES = {
    "8.8.8.8": [
        ("192.168.1.1",    "Home router",        0.8,  1.5),
        ("10.0.0.1",       "ISP aggregation",    3.0,  6.0),
        ("72.14.204.136",  "ISP backbone",       8.0, 14.0),
        ("108.170.248.65", "Google edge",        12.0, 18.0),
        ("142.251.49.24",  "Google core",        14.0, 22.0),
        ("8.8.8.8",        "Google Public DNS",  18.0, 26.0),
    ],
    "1.1.1.1": [
        ("192.168.1.1",    "Home router",        0.5,  1.2),
        ("10.10.0.1",      "ISP PE router",      2.0,  4.5),
        ("198.51.100.1",   "IXP peering",        6.0, 10.0),
        ("162.158.0.1",    "Cloudflare edge",    7.0, 12.0),
        ("1.1.1.1",        "Cloudflare DNS",     8.0, 14.0),
    ],
    "default": [
        ("192.168.1.1",    "Home router",        0.5,  1.5),
        ("10.0.0.1",       "ISP access",         3.0,  7.0),
        ("203.0.113.1",    "Regional backbone",  10.0, 20.0),
        ("198.51.100.10",  "Tier-1 transit",     25.0, 45.0),
        ("203.0.113.200",  "Remote ISP",         50.0, 80.0),
        ("93.184.216.34",  "Destination host",   55.0, 90.0),
    ],
}


def _simulate_route(destination):
    """Generate simulated hops for *destination*."""
    template = _TEMPLATES.get(destination, _TEMPLATES["default"])
    hops = []
    for ip, label, rtt_lo, rtt_hi in template:
        rtt1 = round(random.uniform(rtt_lo, rtt_hi), 2)
        rtt2 = round(random.uniform(rtt_lo, rtt_hi), 2)
        rtt3 = round(random.uniform(rtt_lo, rtt_hi), 2)
        hops.append({"ip": ip, "label": label,
                     "rtts": [rtt1, rtt2, rtt3]})
    return hops


def _parse_hop_arg(hop_str):
    """Parse 'ip:rtt' or 'ip:rtt1,rtt2,rtt3' into a hop dict."""
    ip, rtt_part = hop_str.split(":", 1)
    rtts = [float(r) for r in rtt_part.split(",")]
    if len(rtts) == 1:
        rtts = rtts * 3
    return {"ip": ip.strip(), "label": "", "rtts": rtts[:3]}


# --------------------------------------------------------------------------- #
# Visualisation helpers                                                       #
# --------------------------------------------------------------------------- #

def _bar(value, max_val, width=30):
    """Return an ASCII bar proportional to *value*."""
    if max_val == 0:
        return ""
    filled = int(round(value / max_val * width))
    return "█" * filled + "░" * (width - filled)


def print_hop_table(hops):
    """Print a formatted table of hops with RTT statistics."""
    max_rtt = max(max(h["rtts"]) for h in hops) if hops else 1

    print(f"  {'Hop':>3}  {'IP Address':<18} {'Avg RTT':>9} "
          f"{'Min':>8} {'Max':>8}  RTT distribution")
    print(f"  {'─' * 3}  {'─' * 18} {'─' * 9} {'─' * 8} {'─' * 8}  {'─' * 30}")

    for i, h in enumerate(hops, 1):
        avg = sum(h["rtts"]) / len(h["rtts"])
        mn = min(h["rtts"])
        mx = max(h["rtts"])
        bar = _bar(avg, max_rtt)
        label = f"  ({h['label']})" if h.get("label") else ""
        print(f"  {i:>3}  {h['ip']:<18} {avg:>7.2f}ms "
              f"{mn:>6.2f}ms {mx:>6.2f}ms  {bar}{label}")


def print_ascii_path(hops):
    """Draw an ASCII network-path diagram."""
    print("\n  Network path:\n")
    print(f"    [ You ]")

    for i, h in enumerate(hops):
        avg = sum(h["rtts"]) / len(h["rtts"])
        pipe_len = max(1, int(avg / 5))  # scale: 5 ms per segment
        pipe = "─" * min(pipe_len, 12)
        marker = "►" if i < len(hops) - 1 else "■"
        label = h.get("label", "")
        tag = f"  {label}" if label else ""
        print(f"      │{pipe}{marker} [{h['ip']}]  {avg:.1f} ms{tag}")

    print(f"    [ Done ]\n")


def print_bottleneck_analysis(hops):
    """Flag hops where RTT increases sharply relative to the previous hop."""
    print("  Bottleneck analysis:")
    print("  (Hops where average RTT increases by >50% over previous hop)\n")

    found = False
    prev_avg = 0
    for i, h in enumerate(hops, 1):
        avg = sum(h["rtts"]) / len(h["rtts"])
        if prev_avg > 0:
            increase = avg - prev_avg
            pct = (increase / prev_avg) * 100
            if pct > 50 and increase > 2:
                found = True
                print(f"    ⚠  Hop {i} ({h['ip']}): "
                      f"+{increase:.1f} ms ({pct:.0f}% increase) "
                      f"– possible congestion or long-distance link")
        prev_avg = avg

    if not found:
        print("    ✓  No significant bottlenecks detected.")
    print()


def visualize(hops, title="Traceroute"):
    """Render full visualisation for a list of hops."""
    print(f"\n{'=' * 68}")
    print(f"  {title}")
    print(f"{'=' * 68}\n")
    print_hop_table(hops)
    print_ascii_path(hops)
    print_bottleneck_analysis(hops)


# --------------------------------------------------------------------------- #
# Demo and CLI                                                                #
# --------------------------------------------------------------------------- #

def demo():
    """Generate and visualise several simulated traceroutes."""
    print("Traceroute Visualizer – Demo Mode")
    print(textwrap.dedent("""\
        Traceroute discovers the path packets take through the Internet
        by sending probes with increasing TTL values.  Each router along
        the way reveals itself when it returns an ICMP Time Exceeded
        message.  This tool visualises that data.
    """))

    for dest in ("8.8.8.8", "1.1.1.1", "default"):
        label = dest if dest != "default" else "93.184.216.34 (example.com)"
        hops = _simulate_route(dest)
        visualize(hops, title=f"Traceroute to {label}")


def main():
    parser = argparse.ArgumentParser(
        description="Visualise traceroute data as ASCII diagrams.")
    parser.add_argument("--destination", "-d",
                        help="Destination IP to simulate a route for")
    parser.add_argument("--hops", nargs="+", metavar="IP:RTT",
                        help="Manual hop data as 'ip:rtt' or 'ip:r1,r2,r3'")
    args = parser.parse_args()

    if args.hops:
        hops = [_parse_hop_arg(h) for h in args.hops]
        visualize(hops, title="Traceroute (user-supplied data)")
    elif args.destination:
        hops = _simulate_route(args.destination)
        visualize(hops, title=f"Traceroute to {args.destination} (simulated)")
    else:
        demo()


if __name__ == "__main__":
    main()
