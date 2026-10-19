#!/usr/bin/env python3
"""
CIDR to Hosts Converter
========================
Given one or more CIDR blocks (e.g. ``192.168.1.0/24``), this script uses
Python's ``ipaddress`` module to display:

* Network and broadcast addresses
* Total number of addresses in the block
* Number of usable host addresses
* A bounded sample of usable host addresses, without enumerating the block

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

    Supports both IPv4 and IPv6 CIDR notation. ``hosts`` contains at most
    HOST_DISPLAY_LIMIT addresses; ``usable_hosts_count`` is the exact count.
    Host selection follows ipaddress.hosts(), including /31, /32, /127,
    and /128. These counts do not include provider-specific reservations.
    """
    network = ipaddress.ip_network(cidr_str, strict=False)

    # Calculate offsets directly: even an IPv6 /64 must use bounded memory
    # and time. Using address arithmetic also preserves the IP version.
    if network.version == 4:
        first = 1 if network.prefixlen < 31 else 0
        last = network.num_addresses - (2 if network.prefixlen < 31 else 1)
    else:
        first = 1 if network.prefixlen < 127 else 0
        last = network.num_addresses - 1
    host_count = last - first + 1
    if host_count <= HOST_DISPLAY_LIMIT:
        offsets = range(first, last + 1)
    else:
        half = HOST_DISPLAY_LIMIT // 2
        offsets = list(range(first, first + half)) + list(range(last - half + 1, last + 1))
    hosts = [network.network_address + offset for offset in offsets]

    if network.version == 6:
        broadcast = "N/A (IPv6 has no broadcast)"
    elif network.prefixlen >= 31:
        broadcast = "N/A (/31 point-to-point or /32 host route)"
    else:
        broadcast = str(network.broadcast_address)

    info = {
        "cidr": str(network),
        "version": network.version,
        "network_address": str(network.network_address),
        "broadcast_address": broadcast,
        "prefix_length": network.prefixlen,
        "netmask": str(network.netmask),
        "total_addresses": network.num_addresses,
        "usable_hosts_count": host_count,
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
    count = info["usable_hosts_count"]
    if info["version"] == 4 and info["prefix_length"] < 31:
        print(f"    Usable hosts     = 2^{host_bits} - 2 = {count}")
        print(f"    (subtract 1 for network address, 1 for broadcast)")
    elif info["version"] == 4:
        print(f"    Usable hosts     = {count} (no network/broadcast subtraction)")
        print("    (/31: both point-to-point endpoints; /32: one host address)")
    elif info["prefix_length"] < 127:
        print(f"    Usable hosts     = 2^{host_bits} - 1 = {count}")
        print("    (ipaddress.hosts() excludes the subnet-router anycast address)")
    else:
        print(f"    Usable hosts     = {count} (all addresses for /127 and /128)")

    hosts = info["hosts"]
    print()

    if count <= HOST_DISPLAY_LIMIT:
        print(f"  Usable host addresses ({count}):")
        for h in hosts:
            print(f"    {h}")
    else:
        half = HOST_DISPLAY_LIMIT // 2
        print(f"  Usable host addresses (showing first {half} and last {half} of {count}):")
        for h in hosts[:half]:
            print(f"    {h}")
        print(f"    ... ({count - len(hosts)} more addresses) ...")
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

    failed = False
    for cidr in cidrs:
        try:
            info = analyse_cidr(cidr)
            print_analysis(info)
        except ValueError as exc:
            print(f"\n  ✗ Invalid CIDR '{cidr}': {exc}\n", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
