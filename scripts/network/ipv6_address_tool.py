#!/usr/bin/env python3
"""
IPv6 Address Tool
==================
A comprehensive IPv6 address utility that performs expansion, compression,
type identification, and prefix analysis — all using only the standard
library.

IPv6 addresses are 128-bit identifiers written as eight groups of four hex
digits separated by colons (e.g. 2001:0db8:0000:0000:0000:0000:0000:0001).
Several shorthand rules make them more readable:

  1. Leading zeros in each group may be omitted  → 2001:db8:0:0:0:0:0:1
  2. One consecutive run of all-zero groups may be replaced by "::"
     → 2001:db8::1

This tool reverses and applies those rules, and classifies addresses into
well-known types defined by RFCs.

Concepts demonstrated:
  * IPv6 address representation and notation
  * Address scopes: link-local, global unicast, multicast, loopback, ULA
  * Prefix / interface-identifier split
  * Solicited-node multicast address derivation

Usage:
    python ipv6_address_tool.py                          # built-in demo
    python ipv6_address_tool.py -a 2001:db8::1           # analyse one address
    python ipv6_address_tool.py -a fe80::1 ff02::1 ::1   # analyse several
"""

import argparse
import textwrap


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def expand_ipv6(addr: str) -> str:
    """Expand an abbreviated IPv6 address to its full 8-group form."""
    if "::" in addr:
        left, right = addr.split("::", 1)
        left_groups = left.split(":") if left else []
        right_groups = right.split(":") if right else []
        missing = 8 - len(left_groups) - len(right_groups)
        groups = left_groups + ["0"] * missing + right_groups
    else:
        groups = addr.split(":")
    return ":".join(g.zfill(4) for g in groups)


def compress_ipv6(addr: str) -> str:
    """Compress a full IPv6 address to its shortest valid representation."""
    groups = expand_ipv6(addr).split(":")
    # Strip leading zeros from each group
    stripped = [g.lstrip("0") or "0" for g in groups]

    # Find the longest run of consecutive "0" groups
    best_start, best_len = -1, 0
    cur_start, cur_len = -1, 0
    for i, g in enumerate(stripped):
        if g == "0":
            if cur_len == 0:
                cur_start = i
            cur_len += 1
        else:
            if cur_len > best_len:
                best_start, best_len = cur_start, cur_len
            cur_len = 0
    if cur_len > best_len:
        best_start, best_len = cur_start, cur_len

    if best_len >= 2:
        before = ":".join(stripped[:best_start])
        after = ":".join(stripped[best_start + best_len:])
        compressed = before + "::" + after
    else:
        compressed = ":".join(stripped)

    return compressed


def ipv6_to_int(addr: str) -> int:
    """Convert expanded IPv6 string to 128-bit integer."""
    expanded = expand_ipv6(addr)
    return int(expanded.replace(":", ""), 16)


def int_to_ipv6(n: int) -> str:
    """Convert 128-bit integer to full expanded IPv6."""
    h = format(n, "032x")
    return ":".join(h[i:i + 4] for i in range(0, 32, 4))


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

_TYPES = [
    ("::1/128",             "Loopback"),
    ("::/128",              "Unspecified"),
    ("::ffff:0:0/96",       "IPv4-Mapped"),
    ("fe80::/10",           "Link-Local Unicast"),
    ("fc00::/7",            "Unique Local Address (ULA)"),
    ("ff00::/8",            "Multicast"),
    ("2000::/3",            "Global Unicast"),
    ("::/0",                "Reserved / Unknown"),
]


def _prefix_match(addr_int: int, prefix_str: str) -> bool:
    net_str, plen_str = prefix_str.split("/")
    plen = int(plen_str)
    net_int = ipv6_to_int(net_str)
    mask = ((1 << 128) - 1) ^ ((1 << (128 - plen)) - 1)
    return (addr_int & mask) == (net_int & mask)


def classify_ipv6(addr: str) -> str:
    addr_int = ipv6_to_int(addr)
    for prefix, label in _TYPES:
        if _prefix_match(addr_int, prefix):
            return label
    return "Unknown"


def solicited_node_multicast(addr: str) -> str:
    """Derive the solicited-node multicast address (used by NDP)."""
    low24 = ipv6_to_int(addr) & 0xFFFFFF
    sol = ipv6_to_int("ff02::1:ff00:0") | low24
    return compress_ipv6(int_to_ipv6(sol))


# ---------------------------------------------------------------------------
# Analysis printer
# ---------------------------------------------------------------------------

def analyse(addr: str):
    expanded = expand_ipv6(addr)
    compressed = compress_ipv6(addr)
    addr_int = ipv6_to_int(addr)
    addr_type = classify_ipv6(addr)
    sol_node = solicited_node_multicast(addr)

    groups = expanded.split(":")
    prefix_hex = ":".join(groups[:4])
    iid_hex = ":".join(groups[4:])

    print(f"  Input            : {addr}")
    print(f"  Expanded         : {expanded}")
    print(f"  Compressed       : {compressed}")
    print(f"  Integer value    : {addr_int}")
    print(f"  Binary (first 16): {format(addr_int >> 112, '016b')} …")
    print(f"  Address type     : {addr_type}")
    print(f"  Network prefix   : {prefix_hex}  (/64 assumed)")
    print(f"  Interface ID     : {iid_hex}")
    print(f"  Solicited-node   : {sol_node}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    print(textwrap.dedent("""\
        ╭──────────────────────────────────────────────────╮
        │           IPv6 Address Tool — Demo Mode          │
        ╰──────────────────────────────────────────────────╯
    """))

    samples = [
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "2001:db8::1",
        "fe80::1",
        "::1",
        "::",
        "ff02::1",
        "fc00::abcd:1234",
        "::ffff:c0a8:0101",  # IPv4-mapped address for 192.168.1.1
        "2607:f8b0:4004:0800:0000:0000:0000:200e",
    ]

    for addr in samples:
        print(f"\n{'─' * 56}")
        print(f"  Analysing: {addr}")
        print(f"{'─' * 56}")
        analyse(addr)

    # Demonstrate compression vs expansion round-trip
    print(f"\n{'═' * 56}")
    print("  Round-trip verification (expand → compress → expand):")
    print(f"{'═' * 56}")
    for addr in samples[:4]:
        exp = expand_ipv6(addr)
        comp = compress_ipv6(exp)
        re_exp = expand_ipv6(comp)
        ok = "✓" if exp == re_exp else "✗"
        print(f"  {ok}  {addr:42s} → {comp:20s} → {re_exp}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="IPv6 address analyser and converter.")
    parser.add_argument("-a", "--address", nargs="*",
                        help="IPv6 address(es) to analyse. Omit for demo.")
    args = parser.parse_args()

    if not args.address:
        run_demo()
        return

    for addr in args.address:
        print(f"\n{'─' * 56}")
        print(f"  Analysing: {addr}")
        print(f"{'─' * 56}")
        analyse(addr)


if __name__ == "__main__":
    main()
