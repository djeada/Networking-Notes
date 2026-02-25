#!/usr/bin/env python3
"""
MAC Address Tool
=================
Generates, validates, and analyzes MAC (Media Access Control) addresses.

A MAC address is a 48-bit hardware identifier assigned to network interface
cards. It is split into two halves: the first 24 bits form the OUI
(Organizationally Unique Identifier) assigned by IEEE, and the last 24 bits
are assigned by the manufacturer.

Key bit flags in the first octet:
  - Bit 0 (least significant): 0 = unicast, 1 = multicast
  - Bit 1: 0 = universally administered (UAA), 1 = locally administered (LAA)

Concepts demonstrated:
  * MAC address structure and notation formats (colon, hyphen, dot)
  * OUI (Organizationally Unique Identifier) lookup
  * Unicast vs multicast and universal vs local addressing
  * Random MAC generation with proper flag settings

Usage:
    python mac_address_tool.py                        # run built-in demo
    python mac_address_tool.py --validate 00:1A:2B:3C:4D:5E
    python mac_address_tool.py --generate 5
    python mac_address_tool.py --analyze AA:BB:CC:DD:EE:FF
"""

import argparse
import random
import re
import sys

# Small sample OUI database (first 3 octets -> vendor)
OUI_DB = {
    "00:00:0C": "Cisco Systems",
    "00:1A:2B": "Ayecom Technology",
    "00:50:56": "VMware",
    "08:00:27": "Oracle VirtualBox",
    "DC:A6:32": "Raspberry Pi",
    "00:1B:44": "SanDisk",
    "3C:5A:B4": "Google",
    "F8:FF:C2": "Apple",
    "00:15:5D": "Microsoft Hyper-V",
    "00:0C:29": "VMware",
    "AC:DE:48": "Private (LAA)",
    "00:1C:42": "Parallels",
    "00:25:90": "Super Micro Computer",
    "B8:27:EB": "Raspberry Pi Foundation",
}

COLON_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
HYPHEN_RE = re.compile(r"^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$")
DOT_RE = re.compile(r"^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$")


def normalize(mac: str) -> str:
    """Return MAC in colon-separated uppercase form, or empty string if invalid."""
    mac = mac.strip()
    if COLON_RE.match(mac):
        return mac.upper()
    if HYPHEN_RE.match(mac):
        return mac.replace("-", ":").upper()
    if DOT_RE.match(mac):
        raw = mac.replace(".", "")
        return ":".join(raw[i:i+2] for i in range(0, 12, 2)).upper()
    return ""


def validate(mac: str) -> bool:
    """Check whether *mac* is in any accepted notation."""
    return normalize(mac) != ""


def detect_notation(mac: str) -> str:
    mac = mac.strip()
    if COLON_RE.match(mac):
        return "colon (IEEE 802)"
    if HYPHEN_RE.match(mac):
        return "hyphen (Windows)"
    if DOT_RE.match(mac):
        return "dot (Cisco)"
    return "unknown / invalid"


def analyze(mac: str) -> None:
    """Print a detailed breakdown of a MAC address."""
    norm = normalize(mac)
    if not norm:
        print(f"  [!] '{mac}' is not a valid MAC address.")
        return

    octets = norm.split(":")
    first_byte = int(octets[0], 16)
    is_multicast = bool(first_byte & 0x01)
    is_local = bool(first_byte & 0x02)
    oui = ":".join(octets[:3])
    vendor = OUI_DB.get(oui, "Unknown / not in sample DB")
    binary_repr = " ".join(format(int(o, 16), "08b") for o in octets)

    print(f"  Original input : {mac}")
    print(f"  Notation       : {detect_notation(mac)}")
    print(f"  Normalized     : {norm}")
    print(f"  Binary         : {binary_repr}")
    print(f"  OUI            : {oui}  ->  {vendor}")
    print(f"  NIC specific   : {':'.join(octets[3:])}")
    print(f"  Type           : {'Multicast' if is_multicast else 'Unicast'}")
    print(f"  Administration : {'Locally administered (LAA)' if is_local else 'Universally administered (UAA)'}")
    flag_bits = format(first_byte, "08b")
    print(f"  First octet bits: {flag_bits}")
    print(f"    bit 0 (I/G)  : {flag_bits[7]}  ({'group/multicast' if is_multicast else 'individual/unicast'})")
    print(f"    bit 1 (U/L)  : {flag_bits[6]}  ({'locally administered' if is_local else 'universally administered'})")


def generate(count: int = 1, local: bool = False) -> list:
    """Generate *count* random MAC addresses."""
    results = []
    for _ in range(count):
        octets = [random.randint(0x00, 0xFF) for _ in range(6)]
        # Ensure unicast
        octets[0] &= 0xFE
        if local:
            octets[0] |= 0x02  # set LAA bit
        else:
            octets[0] &= 0xFD  # clear LAA bit
        mac = ":".join(f"{b:02X}" for b in octets)
        results.append(mac)
    return results


def demo() -> None:
    """Run an interactive demonstration."""
    print("=" * 60)
    print("  MAC Address Tool — Demo Mode")
    print("=" * 60)

    print("\n[1] Generating 3 random universally-administered MACs:")
    for mac in generate(3, local=False):
        print(f"    {mac}")

    print("\n[2] Generating 2 locally-administered MACs:")
    for mac in generate(2, local=True):
        print(f"    {mac}")

    samples = ["00:1A:2B:3C:4D:5E", "01-00-5E-00-00-01", "0050.5600.0001",
               "DC:A6:32:AA:BB:CC", "ZZZZ"]
    print("\n[3] Analyzing sample addresses:")
    for s in samples:
        print(f"\n  --- {s} ---")
        analyze(s)

    print("\n[4] Format detection:")
    for s in ["AA:BB:CC:DD:EE:FF", "AA-BB-CC-DD-EE-FF", "AABB.CCDD.EEFF"]:
        print(f"    {s:20s} -> {detect_notation(s)}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="MAC address generator, validator, and analyzer")
    parser.add_argument("--validate", metavar="MAC", help="Validate a MAC address")
    parser.add_argument("--analyze", metavar="MAC", help="Analyze a MAC address in detail")
    parser.add_argument("--generate", metavar="N", type=int, help="Generate N random MAC addresses")
    parser.add_argument("--local", action="store_true", help="Set locally-administered bit when generating")
    args = parser.parse_args()

    if not any([args.validate, args.analyze, args.generate]):
        demo()
        return

    if args.validate:
        ok = validate(args.validate)
        print(f"{'✓ Valid' if ok else '✗ Invalid'}: {args.validate}")
        sys.exit(0 if ok else 1)

    if args.analyze:
        analyze(args.analyze)

    if args.generate:
        for mac in generate(args.generate, local=args.local):
            print(mac)


if __name__ == "__main__":
    main()
