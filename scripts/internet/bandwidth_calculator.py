#!/usr/bin/env python3
"""Bandwidth Calculator — Educational Networking Tool

Calculates bandwidth-related metrics:
  • Given a file size and bandwidth, computes the transfer time.
  • Given bandwidth and time, computes the maximum transferable data.

Supports common units for both data size (bytes, KB, MB, GB) and
bandwidth (bps, Kbps, Mbps, Gbps).  Every calculation is printed
step-by-step so students can follow the math.

Usage examples:
    python bandwidth_calculator.py time  --size 700MB  --bandwidth 10Mbps
    python bandwidth_calculator.py data  --bandwidth 100Mbps --time 30
"""

import argparse
import re
import sys

# ── Unit conversion tables ──────────────────────────────────────────────
# Everything is normalised to *bits* for bandwidth and *bytes* for data.

BANDWIDTH_UNITS = {
    "bps":  1,
    "kbps": 1_000,
    "mbps": 1_000_000,
    "gbps": 1_000_000_000,
}

DATA_UNITS = {
    "b":  1,               # bytes
    "kb": 1_000,
    "mb": 1_000_000,
    "gb": 1_000_000_000,
}


def parse_bandwidth(text: str) -> float:
    """Parse a bandwidth string like '10Mbps' and return bits per second."""
    match = re.match(r"^([\d.]+)\s*(bps|kbps|mbps|gbps)$", text.strip(), re.IGNORECASE)
    if not match:
        raise ValueError(
            f"Invalid bandwidth format: '{text}'. "
            "Use a number followed by bps, Kbps, Mbps, or Gbps."
        )
    value = float(match.group(1))
    unit = match.group(2).lower()
    bits_per_second = value * BANDWIDTH_UNITS[unit]
    print(f"  Bandwidth : {value} {match.group(2)} = {bits_per_second:,.0f} bps")
    return bits_per_second


def parse_data_size(text: str) -> float:
    """Parse a data-size string like '700MB' and return the size in bytes."""
    match = re.match(r"^([\d.]+)\s*(b|kb|mb|gb|bytes?)$", text.strip(), re.IGNORECASE)
    if not match:
        raise ValueError(
            f"Invalid size format: '{text}'. "
            "Use a number followed by B, KB, MB, or GB."
        )
    value = float(match.group(1))
    raw_unit = match.group(2).lower().rstrip("ytes").rstrip("yte") or "b"
    # Normalise "bytes"/"byte" → "b"
    if raw_unit not in DATA_UNITS:
        raw_unit = "b"
    size_bytes = value * DATA_UNITS[raw_unit]
    print(f"  Data size : {value} {match.group(2).upper()} = {size_bytes:,.0f} bytes")
    return size_bytes


def format_time(seconds: float) -> str:
    """Return a human-friendly time string."""
    if seconds < 1:
        return f"{seconds * 1000:.2f} milliseconds"
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.2f} minutes ({seconds:.2f} s)"
    hours = minutes / 60
    return f"{hours:.2f} hours ({seconds:.2f} s)"


def format_data(size_bytes: float) -> str:
    """Return a human-friendly data-size string."""
    if size_bytes < 1_000:
        return f"{size_bytes:.2f} bytes"
    if size_bytes < 1_000_000:
        return f"{size_bytes / 1_000:.2f} KB"
    if size_bytes < 1_000_000_000:
        return f"{size_bytes / 1_000_000:.2f} MB"
    return f"{size_bytes / 1_000_000_000:.2f} GB"


# ── Calculation modes ───────────────────────────────────────────────────

def calc_transfer_time(size_str: str, bw_str: str) -> None:
    """Calculate how long it takes to transfer *size* at *bandwidth*."""
    print("\n── Calculating Transfer Time ──")
    size_bytes = parse_data_size(size_str)
    bps = parse_bandwidth(bw_str)

    size_bits = size_bytes * 8
    print(f"\n  Step 1 — Convert data to bits : {size_bytes:,.0f} bytes × 8 = {size_bits:,.0f} bits")

    seconds = size_bits / bps
    print(f"  Step 2 — Divide by bandwidth  : {size_bits:,.0f} bits ÷ {bps:,.0f} bps = {seconds:,.4f} s")

    print(f"\n  ⏱  Transfer time: {format_time(seconds)}\n")


def calc_max_data(bw_str: str, time_seconds: float) -> None:
    """Calculate the maximum data transferable in *time* at *bandwidth*."""
    print("\n── Calculating Maximum Transferable Data ──")
    bps = parse_bandwidth(bw_str)
    print(f"  Time      : {time_seconds} seconds")

    total_bits = bps * time_seconds
    print(f"\n  Step 1 — Total bits           : {bps:,.0f} bps × {time_seconds} s = {total_bits:,.0f} bits")

    total_bytes = total_bits / 8
    print(f"  Step 2 — Convert to bytes     : {total_bits:,.0f} bits ÷ 8 = {total_bytes:,.0f} bytes")

    print(f"\n  📦 Maximum data: {format_data(total_bytes)}\n")


# ── CLI ─────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bandwidth Calculator — compute transfer times or data limits.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s time --size 700MB --bandwidth 10Mbps\n"
            "  %(prog)s data --bandwidth 100Mbps --time 30\n"
        ),
    )
    sub = parser.add_subparsers(dest="mode", help="Calculation mode")

    # Sub-command: time
    p_time = sub.add_parser("time", help="Calculate transfer time for a given file size and bandwidth")
    p_time.add_argument("--size", required=True, help="File size, e.g. 700MB, 1.5GB, 4096KB")
    p_time.add_argument("--bandwidth", required=True, help="Link bandwidth, e.g. 10Mbps, 1Gbps")

    # Sub-command: data
    p_data = sub.add_parser("data", help="Calculate max data transferable in a given time")
    p_data.add_argument("--bandwidth", required=True, help="Link bandwidth, e.g. 100Mbps")
    p_data.add_argument("--time", required=True, type=float, help="Duration in seconds")

    return parser


def run_demo() -> None:
    """Run a quick built-in demo when no arguments are provided."""
    print("=" * 60)
    print(" Bandwidth Calculator — Demo Mode")
    print("=" * 60)

    calc_transfer_time("700MB", "10Mbps")
    calc_transfer_time("4.7GB", "100Mbps")
    calc_max_data("1Gbps", 10)
    calc_max_data("54Mbps", 60)


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.mode is None:
        run_demo()
        sys.exit(0)

    if args.mode == "time":
        calc_transfer_time(args.size, args.bandwidth)
    elif args.mode == "data":
        calc_max_data(args.bandwidth, args.time)
