#!/usr/bin/env python3
"""
IP Address Validator and Classifier
====================================
Validates and classifies IPv4 and IPv6 addresses using Python's built-in
``ipaddress`` module.  Reports whether an address is private, public,
loopback, multicast, link-local, reserved, or unspecified, and prints
detailed metadata about the address.

Usage:
    python ip_address_validator.py                  # run built-in demo
    python ip_address_validator.py 192.168.1.1      # validate one address
    python ip_address_validator.py 10.0.0.1 ::1 8.8.8.8  # validate several
"""

import argparse
import ipaddress
import sys


def validate_ip(address_str: str) -> dict:
    """Validate an IP address string and return a dict of properties.

    Parameters
    ----------
    address_str : str
        A string that may represent an IPv4 or IPv6 address.

    Returns
    -------
    dict
        Keys include 'valid', 'version', 'is_private', etc.
        If the address is invalid, only 'valid' and 'error' are present.
    """
    result = {"input": address_str}

    try:
        addr = ipaddress.ip_address(address_str)
    except ValueError as exc:
        result["valid"] = False
        result["error"] = str(exc)
        return result

    result["valid"] = True
    result["version"] = addr.version  # 4 or 6
    result["compressed"] = str(addr)

    # Exploded form is useful for IPv6 (shows all groups in full)
    if addr.version == 6:
        result["exploded"] = addr.exploded

    # Classification flags provided by the ipaddress module
    result["is_private"] = addr.is_private
    result["is_global"] = addr.is_global
    result["is_loopback"] = addr.is_loopback
    result["is_multicast"] = addr.is_multicast
    result["is_link_local"] = addr.is_link_local
    result["is_reserved"] = addr.is_reserved
    result["is_unspecified"] = addr.is_unspecified

    # Binary / integer representation (educational)
    result["integer"] = int(addr)
    if addr.version == 4:
        result["binary"] = format(int(addr), "032b")
        # Dotted-binary (e.g. "11000000.10101000.00000001.00000001")
        octets = result["binary"]
        result["binary_dotted"] = ".".join(
            octets[i : i + 8] for i in range(0, 32, 8)
        )
    else:
        result["binary"] = format(int(addr), "0128b")

    return result


def format_report(info: dict) -> str:
    """Return a human-readable report string for a validated address."""
    lines = [f"Address : {info['input']}"]

    if not info["valid"]:
        lines.append(f"  ✗ INVALID — {info['error']}")
        return "\n".join(lines)

    lines.append(f"  Version          : IPv{info['version']}")
    lines.append(f"  Compressed       : {info['compressed']}")
    if "exploded" in info:
        lines.append(f"  Exploded         : {info['exploded']}")
    lines.append(f"  Integer          : {info['integer']}")
    if "binary_dotted" in info:
        lines.append(f"  Binary (dotted)  : {info['binary_dotted']}")
    lines.append(f"  Private          : {info['is_private']}")
    lines.append(f"  Global (public)  : {info['is_global']}")
    lines.append(f"  Loopback         : {info['is_loopback']}")
    lines.append(f"  Multicast        : {info['is_multicast']}")
    lines.append(f"  Link-local       : {info['is_link_local']}")
    lines.append(f"  Reserved         : {info['is_reserved']}")
    lines.append(f"  Unspecified      : {info['is_unspecified']}")

    # Friendly one-line classification
    tags = []
    if info["is_loopback"]:
        tags.append("loopback")
    if info["is_private"]:
        tags.append("private")
    if info["is_global"]:
        tags.append("global/public")
    if info["is_multicast"]:
        tags.append("multicast")
    if info["is_link_local"]:
        tags.append("link-local")
    if info["is_reserved"]:
        tags.append("reserved")
    if info["is_unspecified"]:
        tags.append("unspecified")
    lines.append(f"  Classification   : {', '.join(tags) if tags else 'none'}")

    return "\n".join(lines)


# -- Demo addresses used when no arguments are supplied --------------------
DEMO_ADDRESSES = [
    "192.168.1.1",
    "10.0.0.1",
    "8.8.8.8",
    "127.0.0.1",
    "224.0.0.1",
    "169.254.1.1",
    "0.0.0.0",
    "255.255.255.255",
    "::1",
    "fe80::1",
    "2001:db8::1",
    "not_an_ip",
    "999.999.999.999",
]


def main():
    parser = argparse.ArgumentParser(
        description="Validate and classify IPv4/IPv6 addresses."
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="One or more IP addresses to validate. "
        "If omitted a built-in demo set is used.",
    )
    args = parser.parse_args()

    addresses = args.addresses if args.addresses else DEMO_ADDRESSES

    if not args.addresses:
        print("=" * 60)
        print("  IP Address Validator — Demo Mode")
        print("=" * 60)

    for addr in addresses:
        info = validate_ip(addr)
        print()
        print(format_report(info))

    print()


if __name__ == "__main__":
    main()
