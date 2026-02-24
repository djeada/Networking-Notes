#!/usr/bin/env python3
"""
IPv4 Address Class Identifier
===============================
Identifies the *classful* network class (A–E) of an IPv4 address and
displays educational information including:

* The class and its first-octet range
* Default (classful) subnet mask
* Network and host portions of the address
* The total number of networks and hosts per network for that class
* A reference table of all five classes

**Note:** Classful addressing is largely historical — modern networks use
CIDR (Classless Inter-Domain Routing). This tool is intended as a learning
aid for understanding legacy classful concepts.

Usage:
    python ip_class_identifier.py                   # run built-in demo
    python ip_class_identifier.py 10.0.0.1
    python ip_class_identifier.py 192.168.1.1 224.0.0.5
"""

import argparse
import ipaddress
import sys

# ---------------------------------------------------------------------------
# Class definitions (classful addressing rules)
# ---------------------------------------------------------------------------
#   Class  | First-octet range | Default mask     | Leading bits
#   -------+-------------------+------------------+-------------
#     A    |   1 – 126         | 255.0.0.0   /8   | 0
#     B    | 128 – 191         | 255.255.0.0 /16  | 10
#     C    | 192 – 223         | 255.255.255.0 /24| 110
#     D    | 224 – 239         | (multicast)       | 1110
#     E    | 240 – 255         | (experimental)    | 1111

CLASS_INFO = {
    "A": {
        "range": "1.0.0.0 – 126.255.255.255",
        "first_octet": (1, 126),
        "default_mask": "255.0.0.0",
        "prefix_len": 8,
        "leading_bits": "0",
        "num_networks": 126,         # 2^7 - 2
        "hosts_per_network": 16777214,  # 2^24 - 2
        "purpose": "Large networks (few networks, many hosts)",
    },
    "B": {
        "range": "128.0.0.0 – 191.255.255.255",
        "first_octet": (128, 191),
        "default_mask": "255.255.0.0",
        "prefix_len": 16,
        "leading_bits": "10",
        "num_networks": 16384,       # 2^14
        "hosts_per_network": 65534,  # 2^16 - 2
        "purpose": "Medium networks",
    },
    "C": {
        "range": "192.0.0.0 – 223.255.255.255",
        "first_octet": (192, 223),
        "default_mask": "255.255.255.0",
        "prefix_len": 24,
        "leading_bits": "110",
        "num_networks": 2097152,     # 2^21
        "hosts_per_network": 254,    # 2^8 - 2
        "purpose": "Small networks (many networks, few hosts)",
    },
    "D": {
        "range": "224.0.0.0 – 239.255.255.255",
        "first_octet": (224, 239),
        "default_mask": "N/A (multicast)",
        "prefix_len": None,
        "leading_bits": "1110",
        "num_networks": "N/A",
        "hosts_per_network": "N/A",
        "purpose": "Multicast — not used for normal unicast traffic",
    },
    "E": {
        "range": "240.0.0.0 – 255.255.255.255",
        "first_octet": (240, 255),
        "default_mask": "N/A (experimental)",
        "prefix_len": None,
        "leading_bits": "1111",
        "num_networks": "N/A",
        "hosts_per_network": "N/A",
        "purpose": "Experimental / reserved — not used on the public Internet",
    },
}


def identify_class(ip_str: str) -> dict:
    """Determine the classful network class of an IPv4 address.

    Returns a dict with the class letter and associated metadata.
    """
    addr = ipaddress.IPv4Address(ip_str)
    first_octet = int(str(addr).split(".")[0])

    # Special case: 127.x.x.x is technically Class A space but reserved
    if first_octet == 127:
        cls = "A"
        special = "loopback (127.0.0.0/8)"
    elif first_octet == 0:
        cls = "A"
        special = "reserved (0.0.0.0/8 — 'this' network)"
    else:
        special = None
        for letter, meta in CLASS_INFO.items():
            lo, hi = meta["first_octet"]
            if lo <= first_octet <= hi:
                cls = letter
                break

    meta = CLASS_INFO[cls]

    # Determine network / host portions based on classful mask
    octets = str(addr).split(".")
    if cls == "A":
        network_portion = octets[0]
        host_portion = ".".join(octets[1:])
    elif cls == "B":
        network_portion = ".".join(octets[:2])
        host_portion = ".".join(octets[2:])
    elif cls == "C":
        network_portion = ".".join(octets[:3])
        host_portion = octets[3]
    else:
        network_portion = "N/A"
        host_portion = "N/A"

    first_octet_bin = format(first_octet, "08b")

    return {
        "ip": ip_str,
        "first_octet": first_octet,
        "first_octet_bin": first_octet_bin,
        "class": cls,
        "special": special,
        "network_portion": network_portion,
        "host_portion": host_portion,
        **meta,
    }


def print_class_info(info: dict) -> None:
    """Print a detailed educational report for one IP address."""
    w = 26
    print("=" * 58)
    print(f"  IP Address : {info['ip']}")
    print("=" * 58)
    print(f"{'First Octet':<{w}}: {info['first_octet']} (binary: {info['first_octet_bin']})")
    print(f"{'Class':<{w}}: {info['class']}")
    if info["special"]:
        print(f"{'Special Note':<{w}}: {info['special']}")
    print(f"{'First-Octet Range':<{w}}: {info['range']}")
    print(f"{'Default Subnet Mask':<{w}}: {info['default_mask']}")
    print(f"{'Leading Bits':<{w}}: {info['leading_bits']}")
    print(f"{'Purpose':<{w}}: {info['purpose']}")
    if info["class"] in ("A", "B", "C"):
        print(f"{'Network Portion':<{w}}: {info['network_portion']}")
        print(f"{'Host Portion':<{w}}: {info['host_portion']}")
        print(f"{'# of Networks':<{w}}: {info['num_networks']:,}")
        print(f"{'Hosts per Network':<{w}}: {info['hosts_per_network']:,}")
    print()


def print_reference_table() -> None:
    """Print a compact reference table of all IP classes."""
    print("=" * 72)
    print("  Classful IPv4 Address Reference Table")
    print("=" * 72)
    hdr = f"  {'Class':<6} {'Range':<32} {'Mask':<20} {'Leading'}"
    print(hdr)
    print("  " + "-" * 68)
    for letter, meta in CLASS_INFO.items():
        print(
            f"  {letter:<6} {meta['range']:<32} "
            f"{meta['default_mask']:<20} {meta['leading_bits']}"
        )
    print()


# ---------------------------------------------------------------------------
# Demo addresses
# ---------------------------------------------------------------------------
DEMO_ADDRESSES = [
    "10.0.0.1",
    "127.0.0.1",
    "172.16.5.10",
    "192.168.1.100",
    "224.0.0.5",
    "240.0.0.1",
]


def main():
    parser = argparse.ArgumentParser(
        description="Identify the classful network class of IPv4 addresses."
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="IPv4 addresses to classify. If omitted, runs a built-in demo.",
    )
    args = parser.parse_args()

    addresses = args.addresses if args.addresses else DEMO_ADDRESSES

    if not args.addresses:
        print("=" * 58)
        print("  IPv4 Class Identifier — Demo Mode")
        print("=" * 58)

    # Always show the reference table first
    print()
    print_reference_table()

    for addr in addresses:
        try:
            info = identify_class(addr)
            print_class_info(info)
        except ValueError as exc:
            print(f"\n  ✗ Invalid address '{addr}': {exc}\n")


if __name__ == "__main__":
    main()
