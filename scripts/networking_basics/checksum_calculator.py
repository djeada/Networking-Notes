"""
Internet Checksum Calculator
==============================
Demonstrates how the Internet checksum algorithm works, as specified in
RFC 1071.  This checksum is used in IPv4, TCP, UDP, and ICMP headers to
detect data corruption.

Algorithm overview:
    1. Divide the data into 16-bit words.
    2. If the data has an odd number of bytes, pad with a zero byte.
    3. Sum all 16-bit words using one's-complement addition.
    4. Take the one's complement of the final sum — that is the checksum.

Verification:
    Summing the data *including* the checksum should yield 0xFFFF (all ones
    in 16 bits), confirming that the data has not been altered.

Usage examples:
    python checksum_calculator.py --data "Hello"
    python checksum_calculator.py --hex "4500 0034 1234 4000 4006 0000 C0A80001 C0A800C8"
    python checksum_calculator.py --verify "4500 0034 1234 4000 4006 B1E6 C0A80001 C0A800C8"
"""

import argparse


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def ones_complement_add(a: int, b: int) -> int:
    """Add two 16-bit values with one's-complement carry wraparound."""
    total = a + b
    # Fold any carry bits back into the lower 16 bits
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return total


def compute_checksum(data: bytes, verbose: bool = False) -> int:
    """
    Compute the Internet checksum (RFC 1071) over *data*.

    Parameters
    ----------
    data : bytes
        The raw bytes to checksum.
    verbose : bool
        If True, print step-by-step binary/hex details.

    Returns
    -------
    int
        The 16-bit checksum value.
    """
    if len(data) % 2 != 0:
        data += b"\x00"  # pad to even length

    if verbose:
        print("\nStep-by-step checksum calculation")
        print("=" * 62)
        print(f"{'Word':>4}  {'Hex':>6}  {'Binary':>18}  {'Running Sum':>6}  "
              f"{'Sum Binary':>18}")
        print("-" * 62)

    running_sum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        running_sum = ones_complement_add(running_sum, word)

        if verbose:
            idx = i // 2
            print(f"  {idx:>2}   0x{word:04X}  {word:016b}  "
                  f"0x{running_sum:04X}  {running_sum:016b}")

    checksum = ~running_sum & 0xFFFF  # one's complement

    if verbose:
        print("-" * 62)
        print(f"  Final sum    : 0x{running_sum:04X}  ({running_sum:016b})")
        print(f"  ~sum (chksum): 0x{checksum:04X}  ({checksum:016b})")
        print("=" * 62)

    return checksum


def verify_checksum(data: bytes, verbose: bool = False) -> bool:
    """
    Verify a block of data that already contains a checksum.

    The data (including the checksum field) is summed.  If the result
    is 0xFFFF, the data is intact.
    """
    if len(data) % 2 != 0:
        data += b"\x00"

    running_sum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        running_sum = ones_complement_add(running_sum, word)

    ok = running_sum == 0xFFFF
    if verbose:
        print(f"\n  Verification sum: 0x{running_sum:04X} "
              f"({'PASS ✓' if ok else 'FAIL ✗'})\n")
    return ok


# ---------------------------------------------------------------------------
# Helpers for CLI input parsing
# ---------------------------------------------------------------------------

def hex_string_to_bytes(hex_str: str) -> bytes:
    """Convert a whitespace-separated hex string to bytes."""
    cleaned = hex_str.replace(" ", "").replace("\n", "")
    if len(cleaned) % 2 != 0:
        cleaned = "0" + cleaned  # prepend nibble so we have full bytes
    return bytes.fromhex(cleaned)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute or verify an Internet checksum (RFC 1071).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d", "--data", type=str, metavar="TEXT",
        help="Compute checksum of a text string (UTF-8 encoded)",
    )
    group.add_argument(
        "-x", "--hex", type=str, metavar="HEX",
        help="Compute checksum of hex bytes (e.g. '4500 0034 …')",
    )
    group.add_argument(
        "-v", "--verify", type=str, metavar="HEX",
        help="Verify a hex block that already contains a checksum",
    )
    return parser


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.data:
        raw = args.data.encode("utf-8")
        print(f"\nInput text : {args.data!r}")
        print(f"Bytes (hex): {raw.hex(' ')}")
        chk = compute_checksum(raw, verbose=True)
        print(f"\n  Checksum: 0x{chk:04X}\n")

    elif args.hex:
        raw = hex_string_to_bytes(args.hex)
        print(f"\nInput hex: {raw.hex(' ')}")
        chk = compute_checksum(raw, verbose=True)
        print(f"\n  Checksum: 0x{chk:04X}\n")

    elif args.verify:
        raw = hex_string_to_bytes(args.verify)
        print(f"\nVerifying hex block: {raw.hex(' ')}")
        verify_checksum(raw, verbose=True)

    else:
        # No arguments — run a comprehensive demo
        print("=" * 62)
        print("  Internet Checksum Calculator — Demo")
        print("=" * 62)

        # Demo 1: Simple text
        text = "Hello"
        raw = text.encode("utf-8")
        print(f"\n[Demo 1] Text: {text!r}  →  bytes: {raw.hex(' ')}")
        chk = compute_checksum(raw, verbose=True)
        print(f"  Checksum: 0x{chk:04X}")

        # Verify by appending checksum (pad data to even length first)
        padded = raw if len(raw) % 2 == 0 else raw + b"\x00"
        with_chk = padded + chk.to_bytes(2, "big")
        print(f"\n  Appending checksum → {with_chk.hex(' ')}")
        verify_checksum(with_chk, verbose=True)

        # Demo 2: Simulated IPv4 header (checksum field zeroed)
        # Version/IHL=0x4500, TotalLen=0x0034, ID=0x1234, Flags/Frag=0x4000,
        # TTL/Proto=0x4006, Checksum=0x0000 (to be calculated),
        # SrcIP=192.168.0.1, DstIP=192.168.0.200
        print("-" * 62)
        ip_header_hex = "4500 0034 1234 4000 4006 0000 C0A80001 C0A800C8"
        ip_bytes = hex_string_to_bytes(ip_header_hex)
        print(f"[Demo 2] IPv4 header (checksum field = 0000):")
        print(f"  {ip_bytes.hex(' ')}")
        ip_chk = compute_checksum(ip_bytes, verbose=True)
        print(f"  Calculated IP header checksum: 0x{ip_chk:04X}")

        # Insert checksum at bytes 10-11 and verify
        ip_with_chk = bytearray(ip_bytes)
        ip_with_chk[10] = (ip_chk >> 8) & 0xFF
        ip_with_chk[11] = ip_chk & 0xFF
        print(f"\n  Header with checksum inserted: {bytes(ip_with_chk).hex(' ')}")
        verify_checksum(bytes(ip_with_chk), verbose=True)

        print("Tip: run with --help to see all options.\n")
