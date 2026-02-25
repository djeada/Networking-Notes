#!/usr/bin/env python3
"""
IP Geolocation Lookup (Educational)
=====================================
Demonstrates how IP geolocation works **without calling any external API**.

Real-world geolocation services map IP addresses to locations using databases
built from:
  1. Regional Internet Registry (RIR) allocation records – ARIN, RIPE, APNIC,
     LACNIC, and AFRINIC publish which IP blocks they delegate.
  2. Local Internet Registry / ISP registration data.
  3. Active and passive measurement (traceroute, latency triangulation, BGP).
  4. User-submitted corrections and commercial datasets.

This script contains a small **sample database** of well-known IP ranges that
mirrors the hierarchical allocation model:

    IANA → RIR → LIR / ISP → End-user organisation

For each lookup it walks you through the decision process a geolocation engine
would follow, and it explains the confidence level of the result.

Concepts demonstrated:
  * CIDR prefix matching and longest-prefix-match
  * Hierarchical IP address allocation (RIR → ISP → end user)
  * Why geolocation accuracy varies (country vs. city level)
  * IPv4 address structure and integer conversion

Usage:
    python ip_geolocation_lookup.py                   # demo with sample IPs
    python ip_geolocation_lookup.py 8.8.8.8 1.1.1.1  # look up specific IPs
"""

import argparse
import struct
import socket
import textwrap

# --------------------------------------------------------------------------- #
# Mini geolocation database                                                   #
# Each entry: (CIDR, RIR, Country, Region/City, Org, Confidence%)            #
# Entries are ordered from most-specific to least-specific where needed.      #
# --------------------------------------------------------------------------- #
_DB = [
    # Google Public DNS
    ("8.8.8.0/24",     "ARIN",   "US", "California, USA",   "Google LLC",               95),
    ("8.8.4.0/24",     "ARIN",   "US", "California, USA",   "Google LLC",               95),
    # Cloudflare
    ("1.1.1.0/24",     "APNIC",  "AU", "Global Anycast",    "Cloudflare / APNIC Labs",  70),
    ("1.0.0.0/24",     "APNIC",  "AU", "Global Anycast",    "Cloudflare / APNIC Labs",  70),
    # Amazon AWS US-East
    ("3.80.0.0/12",    "ARIN",   "US", "Virginia, USA",     "Amazon AWS (us-east-1)",   85),
    # Microsoft Azure
    ("20.33.0.0/16",   "ARIN",   "US", "Washington, USA",   "Microsoft Azure",          80),
    # Akamai
    ("23.0.0.0/12",    "ARIN",   "US", "Global CDN",        "Akamai Technologies",      60),
    # RIPE – European blocks
    ("2.0.0.0/8",      "RIPE",   "EU", "Europe (various)",  "RIPE NCC allocation",      40),
    # APNIC – Asia-Pacific
    ("1.0.0.0/8",      "APNIC",  "AP", "Asia-Pacific",      "APNIC allocation",         30),
    # LACNIC – Latin America
    ("177.0.0.0/8",    "LACNIC", "BR", "Brazil (various)",  "LACNIC allocation",        35),
    # AFRINIC
    ("41.0.0.0/8",     "AFRINIC","ZA", "Africa (various)",  "AFRINIC allocation",       30),
    # Private ranges – RFC 1918
    ("10.0.0.0/8",     "IANA",   "--", "Private network",   "RFC 1918 – private use",    0),
    ("172.16.0.0/12",  "IANA",   "--", "Private network",   "RFC 1918 – private use",    0),
    ("192.168.0.0/16", "IANA",   "--", "Private network",   "RFC 1918 – private use",    0),
    # Loopback
    ("127.0.0.0/8",    "IANA",   "--", "Loopback",          "RFC 1122 – loopback",       0),
]


def _ip_to_int(ip_str):
    """Convert dotted-quad IPv4 string to a 32-bit integer."""
    return struct.unpack("!I", socket.inet_aton(ip_str))[0]


def _parse_cidr(cidr):
    """Return (network_int, prefix_len) for a CIDR string."""
    net_str, prefix = cidr.split("/")
    return _ip_to_int(net_str), int(prefix)


def _matches(ip_int, network_int, prefix_len):
    """Check if *ip_int* falls within the given network/prefix."""
    mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return (ip_int & mask) == (network_int & mask)


def lookup(ip_str):
    """Perform longest-prefix-match lookup.  Returns (entry, steps)."""
    ip_int = _ip_to_int(ip_str)
    best = None
    best_prefix = -1
    steps = []

    for cidr, rir, country, region, org, conf in _DB:
        net_int, prefix_len = _parse_cidr(cidr)
        if _matches(ip_int, net_int, prefix_len):
            steps.append((cidr, rir, org, prefix_len))
            if prefix_len > best_prefix:
                best = (cidr, rir, country, region, org, conf)
                best_prefix = prefix_len

    return best, steps


def explain_lookup(ip_str):
    """Print a verbose educational explanation of the lookup."""
    print(f"\n{'─' * 60}")
    print(f"  Looking up: {ip_str}")
    print(f"{'─' * 60}")

    try:
        _ip_to_int(ip_str)
    except (OSError, socket.error):
        print(f"  ✗ '{ip_str}' is not a valid IPv4 address.\n")
        return

    ip_int = _ip_to_int(ip_str)
    print(f"  Integer representation: {ip_int}  "
          f"(0x{ip_int:08X})")

    result, steps = lookup(ip_str)

    if not steps:
        print("  No matching entries found in sample database.")
        print("  A real geolocation service would query much larger datasets.\n")
        return

    print(f"\n  Matching prefixes (most general → most specific):")
    for cidr, rir, org, plen in sorted(steps, key=lambda s: s[3]):
        print(f"    /{plen:<3}  {cidr:<18}  RIR: {rir:<8}  {org}")

    cidr, rir, country, region, org, conf = result
    print(f"\n  ➜ Best match (longest prefix): {cidr}")
    print(f"    RIR          : {rir}")
    print(f"    Country      : {country}")
    print(f"    Region / City: {region}")
    print(f"    Organisation : {org}")
    print(f"    Confidence   : {conf}%")

    if conf == 0:
        print("    ⚠  This is a reserved / private range – not geolocatable.")
    elif conf < 50:
        print("    ⚠  Low confidence – only RIR-level allocation known.")
        print("       Real services use BGP and latency data to refine this.")
    elif conf < 80:
        print("    ℹ  Moderate confidence – ISP or cloud region identified.")
    else:
        print("    ✓  High confidence – well-known infrastructure block.")
    print()


def demo():
    """Look up a set of interesting sample IPs."""
    print("IP Geolocation Lookup – Educational Demo")
    print("=" * 60)
    print(textwrap.dedent("""\
        This tool uses a built-in sample database to demonstrate how
        geolocation engines resolve an IP to a geographic location.
        Real databases (e.g., MaxMind GeoIP2) contain millions of
        prefix entries; ours has a handful for illustration.
    """))

    sample_ips = [
        "8.8.8.8",        # Google DNS
        "1.1.1.1",        # Cloudflare
        "3.92.45.10",     # AWS us-east
        "192.168.1.1",    # Private
        "41.58.200.3",    # AFRINIC
        "177.100.50.25",  # LACNIC / Brazil
    ]
    for ip in sample_ips:
        explain_lookup(ip)


def main():
    parser = argparse.ArgumentParser(
        description="Educational IP geolocation lookup using a sample DB.")
    parser.add_argument("ips", nargs="*",
                        help="IPv4 addresses to look up (omit for demo)")
    args = parser.parse_args()

    if not args.ips:
        demo()
    else:
        for ip in args.ips:
            explain_lookup(ip)


if __name__ == "__main__":
    main()
