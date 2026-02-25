#!/usr/bin/env python3
"""
Binary / Decimal / Hex IP Converter
=====================================
Converts IP addresses between binary, decimal, and hexadecimal
representations with step-by-step educational output.

Each IPv4 octet is an 8-bit value (0–255).  This script shows how the
positional value of each bit (128, 64, 32, 16, 8, 4, 2, 1) contributes
to the decimal result, making it a handy study aid for subnetting and
network exams.

IPv6 addresses use eight 16-bit groups written in hexadecimal.  The tool
demonstrates expansion, compression (::), and binary breakdown.

Concepts demonstrated:
  * Positional (base-2) number system
  * IPv4 dotted-decimal ↔ binary ↔ hex conversion
  * IPv6 colon-hex ↔ binary conversion
  * Bit-weight tables for quick mental math

Usage:
    python binary_ip_converter.py                         # run demo
    python binary_ip_converter.py --ip 192.168.1.1
    python binary_ip_converter.py --binary 11000000.10101000.00000001.00000001
    python binary_ip_converter.py --ip ::1 --ipv6
"""

import argparse
import sys

BIT_WEIGHTS = [128, 64, 32, 16, 8, 4, 2, 1]


def decimal_to_binary_verbose(octet: int) -> str:
    """Convert one decimal octet to binary with explanation."""
    bits = []
    remainder = octet
    parts = []
    for w in BIT_WEIGHTS:
        if remainder >= w:
            bits.append("1")
            parts.append(str(w))
            remainder -= w
        else:
            bits.append("0")
    binary = "".join(bits)
    expr = " + ".join(parts) if parts else "0"
    print(f"    {octet:>3d}  =  {binary}  ({expr})")
    return binary


def ipv4_to_binary(ip: str) -> str:
    """Convert dotted-decimal IPv4 to dotted-binary with verbose output."""
    octets = ip.strip().split(".")
    if len(octets) != 4:
        print(f"  [!] Expected 4 octets, got {len(octets)}")
        return ""
    print("\n  Step-by-step decimal → binary:")
    print(f"    {'Dec':>5s}     {'Binary':8s}   Bit weights used")
    print(f"    {'---':>5s}     {'--------':8s}   ----------------")
    bins = []
    for o in octets:
        val = int(o)
        if not 0 <= val <= 255:
            print(f"  [!] Octet {val} out of range 0-255")
            return ""
        bins.append(decimal_to_binary_verbose(val))
    result = ".".join(bins)
    return result


def binary_to_ipv4(bip: str) -> str:
    """Convert dotted-binary IPv4 to decimal."""
    parts = bip.strip().split(".")
    if len(parts) != 4 or any(len(p) != 8 for p in parts):
        print("  [!] Expected 4 groups of 8 bits separated by dots")
        return ""
    decimals = []
    print("\n  Step-by-step binary → decimal:")
    print(f"    {'Binary':8s}     {'Weights used':<30s}  = Dec")
    print(f"    {'--------':8s}     {'------------':<30s}  -----")
    for p in parts:
        total = 0
        used = []
        for i, bit in enumerate(p):
            if bit == "1":
                total += BIT_WEIGHTS[i]
                used.append(str(BIT_WEIGHTS[i]))
        expr = " + ".join(used) if used else "0"
        print(f"    {p}     {expr:<30s}  = {total}")
        decimals.append(str(total))
    return ".".join(decimals)


def ipv4_to_hex(ip: str) -> str:
    octets = ip.strip().split(".")
    hex_parts = [f"{int(o):02X}" for o in octets]
    return ".".join(hex_parts)


def expand_ipv6(addr: str) -> str:
    """Expand a compressed IPv6 address to full 8-group form."""
    if "::" in addr:
        left, right = addr.split("::", 1)
        left_groups = left.split(":") if left else []
        right_groups = right.split(":") if right else []
        missing = 8 - len(left_groups) - len(right_groups)
        groups = left_groups + ["0000"] * missing + right_groups
    else:
        groups = addr.split(":")
    return ":".join(g.zfill(4) for g in groups)


def ipv6_to_binary(addr: str) -> str:
    """Convert IPv6 address to binary representation."""
    full = expand_ipv6(addr)
    groups = full.split(":")
    print(f"\n  Expanded IPv6: {full}")
    print("\n  Group-by-group hex → binary:")
    bins = []
    for g in groups:
        val = int(g, 16)
        b = format(val, "016b")
        print(f"    0x{g} = {b}")
        bins.append(b)
    return ":".join(bins)


def show_conversion(ip: str, is_ipv6: bool = False) -> None:
    """Show all representations of an IP address."""
    print(f"\n  Input: {ip}")
    if is_ipv6:
        full = expand_ipv6(ip)
        print(f"  Full form : {full}")
        binary = ipv6_to_binary(ip)
        print(f"\n  Binary    : {binary}")
    else:
        binary = ipv4_to_binary(ip)
        if not binary:
            return
        hex_repr = ipv4_to_hex(ip)
        as_int = sum(int(o) << (8 * (3 - i)) for i, o in enumerate(ip.split(".")))
        print(f"\n  Decimal : {ip}")
        print(f"  Binary  : {binary}")
        print(f"  Hex     : {hex_repr}")
        print(f"  Integer : {as_int}")


def show_binary_to_decimal(bip: str) -> None:
    print(f"\n  Input (binary): {bip}")
    dec = binary_to_ipv4(bip)
    if dec:
        print(f"\n  Decimal : {dec}")
        print(f"  Hex     : {ipv4_to_hex(dec)}")


def demo() -> None:
    print("=" * 62)
    print("  Binary / Decimal / Hex IP Converter — Demo Mode")
    print("=" * 62)

    print("\n" + "-" * 62)
    print("  [1] Bit-weight reference table for one octet (8 bits)")
    print("-" * 62)
    print(f"    Position:  {'  '.join(f'b{i}' for i in range(7, -1, -1))}")
    print(f"    Weight  :  {' '.join(f'{w:>3d}' for w in BIT_WEIGHTS)}")
    print(f"    Example :    1   1   0   0   0   0   0   0  = 128+64 = 192")

    print("\n" + "-" * 62)
    print("  [2] Converting decimal IPs to binary & hex")
    print("-" * 62)
    for ip in ["192.168.1.1", "10.0.0.255", "255.255.255.0"]:
        show_conversion(ip)
        print()

    print("-" * 62)
    print("  [3] Converting binary IP back to decimal")
    print("-" * 62)
    show_binary_to_decimal("11000000.10101000.00000001.00000001")

    print("\n" + "-" * 62)
    print("  [4] IPv6 conversion")
    print("-" * 62)
    for v6 in ["::1", "2001:db8::ff00:42:8329"]:
        show_conversion(v6, is_ipv6=True)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert IPs between binary, decimal, and hex")
    parser.add_argument("--ip", help="Decimal IP address to convert")
    parser.add_argument("--binary", help="Dotted-binary IPv4 to convert back")
    parser.add_argument("--ipv6", action="store_true", help="Treat --ip as IPv6")
    args = parser.parse_args()

    if not args.ip and not args.binary:
        demo()
        return

    if args.binary:
        show_binary_to_decimal(args.binary)
    elif args.ip:
        show_conversion(args.ip, is_ipv6=args.ipv6)


if __name__ == "__main__":
    main()
