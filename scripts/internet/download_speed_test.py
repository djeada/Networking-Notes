#!/usr/bin/env python3
"""Simple Download Speed Estimation Tool — Educational Networking Script

Demonstrates how download-speed tests work conceptually:
  1. Generate (or download) a block of data.
  2. Measure the wall-clock time for the transfer.
  3. Compute throughput in multiple units.

Two modes of operation:
  • **local** (default) — generates synthetic random data in memory and
    measures the throughput of the generation + copy pipeline.  This is
    useful for understanding the *math* behind speed tests without
    requiring network access.
  • **network** — attempts to download a small payload from a public URL
    using only ``urllib`` (standard library).  If the download succeeds
    the measured time is used to estimate real throughput.

Educational notes printed along the way explain what a production speed
test (like Ookla or fast.com) does differently.

Usage:
    python download_speed_test.py            # local synthetic test
    python download_speed_test.py --network  # attempt a real download
"""

import io
import os
import time
import urllib.request
import urllib.error

# ── Helpers ──────────────────────────────────────────────────────────────

def format_speed(bits_per_second: float) -> str:
    """Return speed in the most readable unit."""
    if bits_per_second >= 1_000_000_000:
        return f"{bits_per_second / 1_000_000_000:.2f} Gbps"
    if bits_per_second >= 1_000_000:
        return f"{bits_per_second / 1_000_000:.2f} Mbps"
    if bits_per_second >= 1_000:
        return f"{bits_per_second / 1_000:.2f} Kbps"
    return f"{bits_per_second:.2f} bps"


def format_bytes(n: int) -> str:
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f} GB"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.2f} KB"
    return f"{n} bytes"


def print_results(total_bytes: int, elapsed: float, label: str) -> None:
    """Print detailed speed results with the math shown."""
    bits = total_bytes * 8
    bps = bits / elapsed if elapsed > 0 else 0

    print(f"\n── {label} Results ──")
    print(f"  Data transferred : {format_bytes(total_bytes)}")
    print(f"  Elapsed time     : {elapsed:.4f} seconds")
    print()
    print("  Math:")
    print(f"    {total_bytes:,} bytes × 8 = {bits:,} bits")
    print(f"    {bits:,} bits ÷ {elapsed:.4f} s = {bps:,.0f} bps")
    print()
    print(f"  Speed: {format_speed(bps)}")
    print(f"         {bps:,.0f} bps")
    print(f"         {bps / 8:,.0f} bytes/s  ({format_bytes(int(bps / 8))}/s)")


# ── Test modes ───────────────────────────────────────────────────────────

def local_speed_test(size_mb: int = 64) -> None:
    """Synthetic local test — measures throughput of in-memory data copy.

    This does NOT measure your network speed.  It shows the *concept*
    of a speed test: transfer data, time it, compute throughput.
    """
    print("=" * 60)
    print(" Local Synthetic Speed Test")
    print("=" * 60)
    print()
    print("  ℹ  This generates random data in memory and measures")
    print("     how fast Python can copy it.  It illustrates the math")
    print("     behind a real speed test, not actual network speed.")
    print()

    total_bytes = size_mb * 1_000_000
    chunk_size = 1_000_000  # 1 MB chunks
    sink = io.BytesIO()

    print(f"  Generating {size_mb} MB of random data in {chunk_size // 1_000_000} MB chunks …")
    start = time.perf_counter()
    remaining = total_bytes
    while remaining > 0:
        block = os.urandom(min(chunk_size, remaining))
        sink.write(block)
        remaining -= len(block)
    elapsed = time.perf_counter() - start

    print_results(total_bytes, elapsed, "Local Synthetic Test")

    print()
    print("  📝 Educational note:")
    print("     Real speed tests (Ookla, fast.com) download large files")
    print("     from geographically distributed servers and use multiple")
    print("     TCP connections to saturate your link.  They also measure")
    print("     upload speed and latency (ping).")


def network_speed_test() -> None:
    """Attempt to download a payload from the network and measure speed."""
    print("=" * 60)
    print(" Network Download Speed Test")
    print("=" * 60)
    print()

    # We use a small, publicly available file for the test.
    url = "http://speedtest.tele2.net/1MB.zip"
    print(f"  Target URL: {url}")
    print("  Downloading …")
    print()

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkingNotes/1.0"})
        start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        elapsed = time.perf_counter() - start

        print_results(len(data), elapsed, "Network Download Test")

        print()
        print("  📝 Educational note:")
        print("     This single-stream HTTP download underestimates your")
        print("     true bandwidth.  Production tests open many parallel")
        print("     connections and use larger payloads to fill the pipe.")

    except (urllib.error.URLError, OSError) as exc:
        print(f"  ⚠  Network test failed: {exc}")
        print("     Falling back to local synthetic test.\n")
        local_speed_test()


# ── Entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple download speed estimation tool.")
    parser.add_argument(
        "--network", action="store_true",
        help="Attempt a real HTTP download instead of a local synthetic test.",
    )
    parser.add_argument(
        "--size", type=int, default=64,
        help="Size in MB for the local synthetic test (default: 64).",
    )
    args = parser.parse_args()

    if args.network:
        network_speed_test()
    else:
        local_speed_test(size_mb=args.size)
