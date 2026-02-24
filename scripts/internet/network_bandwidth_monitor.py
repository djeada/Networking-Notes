#!/usr/bin/env python3
"""
Network Bandwidth Monitor
==========================
Monitors network interface statistics over time and calculates throughput.

On Linux the script reads /proc/net/dev, which exposes per-interface counters
maintained by the kernel:

    Inter-|   Receive                            |  Transmit
     face | bytes packets errs drop ...          | bytes packets errs drop ...

The monitor takes two snapshots separated by a configurable interval and
computes the delta to derive:
  * Throughput (Mbps) for RX and TX
  * Packet rate (packets/s)
  * Error and drop counts

If /proc/net/dev is unavailable (e.g., macOS, Windows, or containers with
restricted /proc), the script falls back to **simulated data** so you can
still see what the output looks like.

Concepts demonstrated:
  * Reading kernel-exported network counters
  * Calculating throughput from byte-counter deltas
  * Graceful platform fallback
  * Human-friendly formatting of network rates

Usage:
    python network_bandwidth_monitor.py                     # demo (3 samples, 1 s)
    python network_bandwidth_monitor.py -i eth0 -n 10 -t 2 # 10 samples, 2 s interval
    python network_bandwidth_monitor.py --list              # list available interfaces
"""

import argparse
import os
import random
import time

PROC_NET_DEV = "/proc/net/dev"

# Fields in /proc/net/dev (per side: receive or transmit)
_FIELDS = ("bytes", "packets", "errs", "drop", "fifo", "frame_or_colls",
           "compressed", "multicast_or_carrier")


def _parse_proc_net_dev():
    """Parse /proc/net/dev and return {iface: {rx_bytes, tx_bytes, ...}}."""
    result = {}
    with open(PROC_NET_DEV) as f:
        for line in f:
            if ":" not in line:
                continue
            iface, data = line.split(":", 1)
            iface = iface.strip()
            nums = list(map(int, data.split()))
            rx = {f"rx_{_FIELDS[i]}": nums[i] for i in range(8)}
            tx = {f"tx_{_FIELDS[i]}": nums[i + 8] for i in range(8)}
            result[iface] = {**rx, **tx}
    return result


def _simulated_snapshot(iface, base_state):
    """Generate a plausible simulated snapshot."""
    if base_state is None:
        return {
            "rx_bytes": random.randint(1_000_000, 500_000_000),
            "rx_packets": random.randint(1000, 200_000),
            "rx_errs": 0, "rx_drop": 0,
            "tx_bytes": random.randint(500_000, 100_000_000),
            "tx_packets": random.randint(500, 80_000),
            "tx_errs": 0, "tx_drop": 0,
        }
    delta_rx = random.randint(50_000, 12_000_000)
    delta_tx = random.randint(20_000, 5_000_000)
    return {
        "rx_bytes": base_state["rx_bytes"] + delta_rx,
        "rx_packets": base_state["rx_packets"] + random.randint(50, 8000),
        "rx_errs": base_state["rx_errs"] + (1 if random.random() < 0.02 else 0),
        "rx_drop": base_state["rx_drop"],
        "tx_bytes": base_state["tx_bytes"] + delta_tx,
        "tx_packets": base_state["tx_packets"] + random.randint(30, 4000),
        "tx_errs": base_state["tx_errs"],
        "tx_drop": base_state["tx_drop"],
    }


def _have_proc():
    return os.path.isfile(PROC_NET_DEV)


def list_interfaces():
    if _have_proc():
        stats = _parse_proc_net_dev()
        print("Available network interfaces:")
        for name in sorted(stats):
            print(f"  {name}")
    else:
        print("Cannot read /proc/net/dev – showing simulated interfaces.")
        for name in ("lo", "eth0", "wlan0"):
            print(f"  {name}  (simulated)")


def get_snapshot(iface, prev=None):
    """Return counter dict for *iface*."""
    if _have_proc():
        all_stats = _parse_proc_net_dev()
        if iface not in all_stats:
            raise SystemExit(f"Interface '{iface}' not found. "
                             f"Available: {', '.join(sorted(all_stats))}")
        return all_stats[iface]
    return _simulated_snapshot(iface, prev)


def fmt_rate(bits_per_sec):
    """Human-friendly bit-rate string."""
    if bits_per_sec >= 1e9:
        return f"{bits_per_sec / 1e9:.2f} Gbps"
    if bits_per_sec >= 1e6:
        return f"{bits_per_sec / 1e6:.2f} Mbps"
    if bits_per_sec >= 1e3:
        return f"{bits_per_sec / 1e3:.2f} Kbps"
    return f"{bits_per_sec:.0f} bps"


def fmt_bytes(n):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def print_header(iface, simulated):
    src = "(simulated)" if simulated else "(live from /proc/net/dev)"
    print(f"\n{'=' * 72}")
    print(f"  Monitoring interface: {iface}  {src}")
    print(f"{'=' * 72}")
    print(f"  {'Time':>8}  {'RX rate':>12}  {'TX rate':>12}  "
          f"{'RX pkts/s':>10}  {'TX pkts/s':>10}  {'Errs':>5}")
    print(f"  {'-' * 64}")


def monitor(iface, samples, interval):
    """Collect *samples* snapshots at *interval* seconds apart."""
    simulated = not _have_proc()
    print_header(iface, simulated)

    prev = get_snapshot(iface)
    for i in range(samples):
        time.sleep(interval)
        curr = get_snapshot(iface, prev)

        d_rx = curr["rx_bytes"] - prev["rx_bytes"]
        d_tx = curr["tx_bytes"] - prev["tx_bytes"]
        d_rx_pkt = curr["rx_packets"] - prev["rx_packets"]
        d_tx_pkt = curr["tx_packets"] - prev["tx_packets"]
        d_errs = ((curr["rx_errs"] - prev["rx_errs"])
                  + (curr["tx_errs"] - prev["tx_errs"]))

        rx_bps = (d_rx * 8) / interval
        tx_bps = (d_tx * 8) / interval
        rx_pps = d_rx_pkt / interval
        tx_pps = d_tx_pkt / interval

        ts = time.strftime("%H:%M:%S")
        print(f"  {ts:>8}  {fmt_rate(rx_bps):>12}  {fmt_rate(tx_bps):>12}  "
              f"{rx_pps:>10.0f}  {tx_pps:>10.0f}  {d_errs:>5}")

        prev = curr

    # Summary
    total = get_snapshot(iface, prev)
    print(f"\n  Cumulative totals for {iface}:")
    print(f"    RX: {fmt_bytes(total['rx_bytes']):>10}   "
          f"({total['rx_packets']} packets,  {total['rx_errs']} errors)")
    print(f"    TX: {fmt_bytes(total['tx_bytes']):>10}   "
          f"({total['tx_packets']} packets,  {total['tx_errs']} errors)")
    print()


def demo():
    """Run a short demo monitoring session."""
    print("Network Bandwidth Monitor – Demo Mode")
    print("Collecting 3 samples at 1-second intervals...\n")
    iface = "eth0"
    if _have_proc():
        stats = _parse_proc_net_dev()
        # pick the first non-lo interface, or lo
        iface = next((i for i in sorted(stats) if i != "lo"), "lo")
    monitor(iface, samples=3, interval=1)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor network interface throughput.")
    parser.add_argument("-i", "--interface", help="Interface name (e.g. eth0)")
    parser.add_argument("-n", "--samples", type=int, default=5,
                        help="Number of samples to collect (default 5)")
    parser.add_argument("-t", "--interval", type=float, default=1.0,
                        help="Seconds between samples (default 1)")
    parser.add_argument("--list", action="store_true",
                        help="List available interfaces and exit")
    args = parser.parse_args()

    if args.list:
        list_interfaces()
        return

    if args.interface is None:
        demo()
    else:
        monitor(args.interface, args.samples, args.interval)


if __name__ == "__main__":
    main()
