#!/usr/bin/env python3
"""
IPv4 Subnet Calculator
======================
Given an IP address with a CIDR prefix length **or** a dotted-decimal subnet
mask, this script calculates and displays:

* Network address
* Broadcast address
* First and last usable host addresses
* Number of usable hosts
* Wildcard mask
* Binary representations of address, mask, network, and broadcast

The output is intentionally verbose and educational — it shows the bitwise
math behind every result so you can see *why* subnetting works the way it
does.

Usage:
    python subnet_calculator.py                         # run built-in demo
    python subnet_calculator.py 192.168.1.100/24
    python subnet_calculator.py 10.0.0.50 255.255.240.0
"""

import argparse
import ipaddress
import sys


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def ip_to_binary(ip_str: str) -> str:
    """Convert a dotted-decimal IPv4 address to a 32-bit binary string."""
    return "".join(format(int(o), "08b") for o in ip_str.split("."))


def binary_to_ip(bits: str) -> str:
    """Convert a 32-bit binary string back to dotted-decimal."""
    return ".".join(str(int(bits[i : i + 8], 2)) for i in range(0, 32, 8))


def dotted_binary(bits: str) -> str:
    """Insert dots between each octet of a 32-bit binary string."""
    return ".".join(bits[i : i + 8] for i in range(0, 32, 8))


def mask_from_prefix(prefix_len: int) -> str:
    """Return the dotted-decimal subnet mask for a given prefix length."""
    bits = "1" * prefix_len + "0" * (32 - prefix_len)
    return binary_to_ip(bits)


def wildcard_from_mask(mask_str: str) -> str:
    """Return the wildcard mask (bitwise NOT of the subnet mask)."""
    octets = mask_str.split(".")
    return ".".join(str(255 - int(o)) for o in octets)


# ---------------------------------------------------------------------------
# Core calculation
# ---------------------------------------------------------------------------

def calculate_subnet(ip_str: str, mask_str: str) -> dict:
    """Calculate all subnet details for *ip_str* with subnet mask *mask_str*.

    Both arguments must be dotted-decimal strings.  Returns a dict with
    every useful field.
    """
    ip_bits = ip_to_binary(ip_str)
    mask_bits = ip_to_binary(mask_str)
    prefix_len = mask_bits.count("1")

    # Network address: IP AND mask
    net_bits = "".join(
        str(int(a) & int(m)) for a, m in zip(ip_bits, mask_bits)
    )
    # Broadcast address: network OR (NOT mask)
    inv_mask_bits = "".join("1" if b == "0" else "0" for b in mask_bits)
    bcast_bits = "".join(
        str(int(n) | int(w)) for n, w in zip(net_bits, inv_mask_bits)
    )

    network_addr = binary_to_ip(net_bits)
    broadcast_addr = binary_to_ip(bcast_bits)

    total_hosts = 2 ** (32 - prefix_len)
    # Usable hosts: total minus network and broadcast (at least 0)
    usable_hosts = max(total_hosts - 2, 0)

    # First and last usable host
    net_int = int(net_bits, 2)
    bcast_int = int(bcast_bits, 2)
    if usable_hosts > 0:
        first_host = binary_to_ip(format(net_int + 1, "032b"))
        last_host = binary_to_ip(format(bcast_int - 1, "032b"))
    else:
        first_host = "N/A"
        last_host = "N/A"

    return {
        "ip": ip_str,
        "mask": mask_str,
        "prefix_len": prefix_len,
        "wildcard": wildcard_from_mask(mask_str),
        "network": network_addr,
        "broadcast": broadcast_addr,
        "first_host": first_host,
        "last_host": last_host,
        "total_addresses": total_hosts,
        "usable_hosts": usable_hosts,
        # Binary representations for educational display
        "ip_bin": dotted_binary(ip_bits),
        "mask_bin": dotted_binary(mask_bits),
        "network_bin": dotted_binary(net_bits),
        "broadcast_bin": dotted_binary(bcast_bits),
    }


# ---------------------------------------------------------------------------
# Pretty-print
# ---------------------------------------------------------------------------

def print_subnet_info(info: dict) -> None:
    """Print a detailed, educational summary of subnet calculations."""
    w = 24  # label width
    print("=" * 62)
    print("  Subnet Calculator Results")
    print("=" * 62)
    print(f"{'IP Address':<{w}}: {info['ip']}")
    print(f"{'Subnet Mask':<{w}}: {info['mask']} (/{info['prefix_len']})")
    print(f"{'Wildcard Mask':<{w}}: {info['wildcard']}")
    print("-" * 62)
    print(f"{'Network Address':<{w}}: {info['network']}")
    print(f"{'Broadcast Address':<{w}}: {info['broadcast']}")
    print(f"{'First Usable Host':<{w}}: {info['first_host']}")
    print(f"{'Last Usable Host':<{w}}: {info['last_host']}")
    print(f"{'Total Addresses':<{w}}: {info['total_addresses']}")
    print(f"{'Usable Hosts':<{w}}: {info['usable_hosts']}")
    print("-" * 62)
    print("  Binary Breakdown")
    print("-" * 62)
    print(f"{'IP Address (bin)':<{w}}: {info['ip_bin']}")
    print(f"{'Subnet Mask (bin)':<{w}}: {info['mask_bin']}")
    print(f"{'Network (bin)':<{w}}: {info['network_bin']}")
    print(f"{'Broadcast (bin)':<{w}}: {info['broadcast_bin']}")
    print("=" * 62)
    print()
    # Show the AND / OR logic
    print("  How it works:")
    print(f"    Network   = IP AND Mask")
    print(f"               {info['ip_bin']}")
    print(f"         AND   {info['mask_bin']}")
    print(f"             = {info['network_bin']}  →  {info['network']}")
    print()
    print(f"    Broadcast = Network OR Wildcard")
    wc_bits = dotted_binary(ip_to_binary(info["wildcard"]))
    print(f"               {info['network_bin']}")
    print(f"          OR   {wc_bits}")
    print(f"             = {info['broadcast_bin']}  →  {info['broadcast']}")
    print()


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_input(args: list[str]) -> tuple[str, str]:
    """Parse command-line tokens into (ip, mask) dotted-decimal strings.

    Accepts either:
        192.168.1.100/24
        192.168.1.100 255.255.255.0
    """
    if len(args) == 1 and "/" in args[0]:
        ip_part = args[0].split("/")[0]
        ipaddress.IPv4Address(ip_part)  # validate
        network = ipaddress.IPv4Network(args[0], strict=False)
        mask = str(network.netmask)
        return ip_part, mask
    if len(args) == 1 and "/" not in args[0]:
        # Bare IP — assume /32
        ipaddress.IPv4Address(args[0])  # validate
        return args[0], "255.255.255.255"
    if len(args) == 2:
        ipaddress.IPv4Address(args[0])  # validate IP
        ipaddress.IPv4Address(args[1])  # validate mask
        return args[0], args[1]
    raise ValueError(
        "Provide an address in CIDR notation (e.g. 192.168.1.0/24) "
        "or an IP and mask (e.g. 10.0.0.1 255.255.255.0)."
    )


def main():
    parser = argparse.ArgumentParser(
        description="IPv4 Subnet Calculator — educational edition."
    )
    parser.add_argument(
        "address",
        nargs="*",
        help="IP/CIDR or IP MASK (e.g. 192.168.1.0/24 or 10.0.0.1 255.255.240.0). "
        "If omitted, runs a built-in demo.",
    )
    args = parser.parse_args()

    if args.address:
        ip, mask = parse_input(args.address)
        info = calculate_subnet(ip, mask)
        print_subnet_info(info)
    else:
        # Built-in demo with several interesting subnets
        demos = [
            ("192.168.1.100", "255.255.255.0"),
            ("10.10.5.130", "255.255.240.0"),
            ("172.16.0.1", "255.255.255.252"),
            ("192.168.10.50", "255.255.255.128"),
        ]
        print("=" * 62)
        print("  Subnet Calculator — Demo Mode")
        print("=" * 62)
        for ip, mask in demos:
            info = calculate_subnet(ip, mask)
            print_subnet_info(info)


if __name__ == "__main__":
    main()
