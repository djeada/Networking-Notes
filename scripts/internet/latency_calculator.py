#!/usr/bin/env python3
"""
Network Latency Calculator
===========================
Calculates and explains the four key components of end-to-end network delay:

  Total Delay = Propagation + Transmission + Queuing + Processing

Each component models a different physical or operational constraint:

  * Propagation delay  – time for a signal to travel through a medium.
        Formula: distance / propagation_speed
        Speed of light in vacuum ≈ 3 × 10⁸ m/s; in fiber ≈ 2 × 10⁸ m/s.

  * Transmission delay  – time to push all bits of a packet onto the link.
        Formula: packet_size / bandwidth

  * Queuing delay      – time a packet waits in router buffers.
        Modeled here with an M/D/1 queue approximation.

  * Processing delay   – time a router takes to examine headers and forward.
        Typically microseconds on modern hardware.

The script also computes Round-Trip Time (RTT = 2 × one-way delay) and
shows how each component contributes to the total.

Concepts demonstrated:
  * The four sources of network delay
  * Speed-of-light constraints in different media
  * Bandwidth-delay product
  * M/D/1 queuing model for average queue wait

Usage:
    python latency_calculator.py                        # built-in demo scenarios
    python latency_calculator.py --distance 5000 --medium fiber \\
        --bandwidth 10e9 --packet-size 1500 --utilization 0.6
"""

import argparse
import textwrap

# Propagation speeds (m/s) for common media
MEDIA_SPEEDS = {
    "fiber":     2.0e8,   # ~2/3 speed of light
    "copper":    2.3e8,   # ~77% speed of light
    "wireless":  3.0e8,   # ~speed of light (free space)
    "satellite": 3.0e8,   # free-space radio
}

PROCESSING_DELAY_S = 50e-6  # 50 µs typical router processing


def propagation_delay(distance_km, medium="fiber"):
    """Return propagation delay in seconds."""
    speed = MEDIA_SPEEDS[medium]
    return (distance_km * 1000) / speed


def transmission_delay(packet_bytes, bandwidth_bps):
    """Return transmission delay in seconds."""
    return (packet_bytes * 8) / bandwidth_bps


def queuing_delay_md1(utilization):
    """Approximate average queuing delay factor using M/D/1 model.

    Average queue wait = (ρ / (1 − ρ)) × (service_time / 2)
    We return the multiplicative factor ρ / (2 × (1 − ρ)) so the caller
    can multiply by the transmission (service) time.
    """
    if utilization >= 1.0:
        return float("inf")
    if utilization <= 0:
        return 0.0
    return utilization / (2.0 * (1.0 - utilization))


def calculate(distance_km, medium, bandwidth_bps, packet_bytes, utilization):
    """Calculate all delay components and return a results dict."""
    prop = propagation_delay(distance_km, medium)
    trans = transmission_delay(packet_bytes, bandwidth_bps)
    q_factor = queuing_delay_md1(utilization)
    queue = q_factor * trans
    proc = PROCESSING_DELAY_S
    total = prop + trans + queue + proc
    rtt = 2 * total
    bdp = bandwidth_bps * rtt
    return {
        "propagation_s": prop,
        "transmission_s": trans,
        "queuing_s": queue,
        "processing_s": proc,
        "total_one_way_s": total,
        "rtt_s": rtt,
        "bandwidth_delay_product_bits": bdp,
    }


def fmt(seconds):
    """Format a time value to a human-friendly string."""
    if seconds >= 1:
        return f"{seconds:.4f} s"
    if seconds >= 1e-3:
        return f"{seconds * 1e3:.4f} ms"
    return f"{seconds * 1e6:.2f} µs"


def print_scenario(label, distance_km, medium, bandwidth_bps, packet_bytes,
                   utilization):
    """Pretty-print one scenario with educational annotations."""
    r = calculate(distance_km, medium, bandwidth_bps, packet_bytes,
                  utilization)
    bw_label = f"{bandwidth_bps / 1e9:.1f} Gbps" if bandwidth_bps >= 1e9 \
        else f"{bandwidth_bps / 1e6:.1f} Mbps"

    print(f"\n{'=' * 60}")
    print(f"  Scenario: {label}")
    print(f"{'=' * 60}")
    print(f"  Distance        : {distance_km:,.0f} km")
    print(f"  Medium          : {medium}  "
          f"(speed ≈ {MEDIA_SPEEDS[medium]:.2e} m/s)")
    print(f"  Bandwidth       : {bw_label}")
    print(f"  Packet size     : {packet_bytes} bytes")
    print(f"  Link utilization: {utilization * 100:.0f}%")
    print(f"{'-' * 60}")
    print(f"  Propagation  delay : {fmt(r['propagation_s']):>14}")
    print(f"  Transmission delay : {fmt(r['transmission_s']):>14}")
    print(f"  Queuing      delay : {fmt(r['queuing_s']):>14}")
    print(f"  Processing   delay : {fmt(r['processing_s']):>14}")
    print(f"{'-' * 60}")
    print(f"  ➜ One-way delay    : {fmt(r['total_one_way_s']):>14}")
    print(f"  ➜ Round-trip time  : {fmt(r['rtt_s']):>14}")
    print(f"  Bandwidth-delay product: "
          f"{r['bandwidth_delay_product_bits'] / 8:,.0f} bytes")
    print()


def demo():
    """Run built-in educational demo scenarios."""
    print("Network Latency Calculator – Demo Scenarios")
    print("Each scenario shows how the four delay components combine.\n")

    scenarios = [
        ("Transcontinental fiber (NYC → LA)",
         4000, "fiber", 10e9, 1500, 0.3),
        ("Submarine cable (London → Tokyo)",
         9500, "fiber", 100e9, 1500, 0.5),
        ("Geostationary satellite link",
         35786, "satellite", 50e6, 1500, 0.4),
        ("Local LAN (same building)",
         0.1, "copper", 1e9, 1500, 0.1),
        ("Campus Wi-Fi hop",
         0.05, "wireless", 300e6, 1500, 0.6),
    ]
    for label, dist, med, bw, pkt, util in scenarios:
        print_scenario(label, dist, med, bw, pkt, util)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate network latency components.")
    parser.add_argument("--distance", type=float,
                        help="Link distance in km")
    parser.add_argument("--medium", choices=MEDIA_SPEEDS.keys(),
                        default="fiber", help="Transmission medium")
    parser.add_argument("--bandwidth", type=float, default=1e9,
                        help="Link bandwidth in bps (default 1 Gbps)")
    parser.add_argument("--packet-size", type=int, default=1500,
                        help="Packet size in bytes (default 1500)")
    parser.add_argument("--utilization", type=float, default=0.5,
                        help="Link utilization 0-1 (default 0.5)")
    args = parser.parse_args()

    if args.distance is None:
        demo()
    else:
        print_scenario("Custom scenario", args.distance, args.medium,
                       args.bandwidth, args.packet_size, args.utilization)


if __name__ == "__main__":
    main()
