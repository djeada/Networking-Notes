#!/usr/bin/env python3
"""
CIDR to Hosts Converter
========================
Given one or more CIDR blocks (e.g. ``192.168.1.0/24``), this script uses
Python's ``ipaddress`` module to display:

* Network and broadcast addresses
* Total number of addresses in the block
* Number of usable host addresses
* The full list of usable host addresses (capped for large blocks)

This is an educational tool — the output explains how the host count is
derived from the prefix length.

Usage:
    python cidr_to_hosts.py                        # run built-in demo
    python cidr_to_hosts.py 192.168.1.0/24
    python cidr_to_hosts.py 10.0.0.0/16 172.16.0.0/28
"""

import argparse
import ipaddress
import sys

# When a network has more hosts than this, we only print the first and last
# few to avoid flooding the terminal.
HOST_DISPLAY_LIMIT = 20


def analyse_cidr(cidr_str: str) -> dict:
    """Parse a CIDR string and return a dict with host information.

    Supports both IPv4 and IPv6 CIDR notation.
    """
    network = ipaddress.ip_network(cidr_str, strict=False)

    # .hosts() returns an iterator of usable host addresses
    # (excludes network and broadcast for IPv4; excludes subnet-router
    #  anycast address for IPv6 with prefixlen < 127)
    hosts = list(network.hosts())

    info = {
        "cidr": str(network),
        "version": network.version,
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address) if network.version == 4 else "N/A (IPv6)",
        "prefix_length": network.prefixlen,
        "netmask": str(network.netmask),
        "total_addresses": network.num_addresses,
        "usable_hosts_count": len(hosts),
        "hosts": hosts,
    }
    return info


def print_analysis(info: dict) -> None:
    """Pretty-print the CIDR analysis."""
    w = 24
    print("=" * 60)
    print(f"  CIDR Block: {info['cidr']}")
    print("=" * 60)
    print(f"{'IP Version':<{w}}: IPv{info['version']}")
    print(f"{'Network Address':<{w}}: {info['network_address']}")
    print(f"{'Broadcast Address':<{w}}: {info['broadcast_address']}")
    print(f"{'Prefix Length':<{w}}: /{info['prefix_length']}")
    print(f"{'Subnet Mask':<{w}}: {info['netmask']}")
    print(f"{'Total Addresses':<{w}}: {info['total_addresses']}")
    print(f"{'Usable Host Addresses':<{w}}: {info['usable_hosts_count']}")

    # Educational note on how usable hosts are calculated
    host_bits = (128 if info["version"] == 6 else 32) - info["prefix_length"]
    print()
    print(f"  How the count is derived:")
    print(f"    Host bits        = {32 if info['version'] == 4 else 128} - {info['prefix_length']} = {host_bits}")
    print(f"    Total addresses  = 2^{host_bits} = {2 ** host_bits}")
    if info["version"] == 4:
        print(f"    Usable hosts     = 2^{host_bits} - 2 = {max(2 ** host_bits - 2, 0)}")
        print(f"    (subtract 1 for network address, 1 for broadcast)")

    hosts = info["hosts"]
    print()

    if len(hosts) == 0:
        print("  No usable host addresses in this network.")
    elif len(hosts) <= HOST_DISPLAY_LIMIT:
        print(f"  Usable host addresses ({len(hosts)}):")
        for h in hosts:
            print(f"    {h}")
    else:
        half = HOST_DISPLAY_LIMIT // 2
        print(f"  Usable host addresses (showing first {half} and last {half} of {len(hosts)}):")
        for h in hosts[:half]:
            print(f"    {h}")
        print(f"    ... ({len(hosts) - HOST_DISPLAY_LIMIT} more addresses) ...")
        for h in hosts[-half:]:
            print(f"    {h}")
    print()


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
DEMO_CIDRS = [
    "192.168.1.0/24",
    "10.0.0.0/30",
    "172.16.0.0/28",
    "192.168.100.0/26",
]


def main():
    parser = argparse.ArgumentParser(
        description="Convert CIDR notation to detailed host information."
    )
    parser.add_argument(
        "cidrs",
        nargs="*",
        help="CIDR blocks to analyse (e.g. 192.168.1.0/24). "
        "If omitted, runs a built-in demo.",
    )
    args = parser.parse_args()

    cidrs = args.cidrs if args.cidrs else DEMO_CIDRS

    if not args.cidrs:
        print("=" * 60)
        print("  CIDR to Hosts — Demo Mode")
        print("=" * 60)

    for cidr in cidrs:
        try:
            info = analyse_cidr(cidr)
            print_analysis(info)
        except ValueError as exc:
            print(f"\n  ✗ Invalid CIDR '{cidr}': {exc}\n")


if __name__ == "__main__":
    main()
