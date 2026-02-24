#!/usr/bin/env python3
"""
CRC-32 Calculator for Ethernet FCS
====================================
Implements the CRC-32 algorithm used in the Ethernet Frame Check Sequence
(FCS) field.  For small inputs the script prints the polynomial long-division
step by step so you can see exactly how CRC works; for larger inputs it uses
the standard table-driven algorithm.

How CRC works (simplified):
    1. Treat the message as a long binary polynomial M(x).
    2. Multiply M(x) by x^32 (append 32 zero bits).
    3. Divide by the generator polynomial G(x) using XOR-based division.
    4. The remainder is the 32-bit CRC that is appended to the frame.
    5. The receiver repeats the division on the frame + CRC; if the
       remainder is zero the frame is error-free.

Ethernet uses the CRC-32 polynomial:
    G(x) = x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10
          + x^8  + x^7  + x^5  + x^4  + x^2  + x + 1
    Hex: 0x04C11DB7  (bit-reversed: 0xEDB88320)

Concepts demonstrated:
    * Binary polynomial long division (XOR division)
    * CRC-32 computation with bit-reflection and pre/post inversion
    * Lookup-table optimisation (256-entry table)
    * Verifying data integrity at the data link layer

Usage:
    python crc_calculator.py                        # built-in demo
    python crc_calculator.py --text "Hello"         # CRC of a string
    python crc_calculator.py --hex 48656C6C6F       # CRC of hex bytes
    python crc_calculator.py --step "Hi"            # step-by-step division
"""

import argparse
import binascii
import textwrap

CRC32_POLY = 0xEDB88320  # bit-reversed representation


# ── lookup table (built once) ────────────────────────────────────────────────

def _build_table() -> list:
    """Build the 256-entry CRC-32 lookup table."""
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ CRC32_POLY
            else:
                crc >>= 1
        table.append(crc)
    return table


CRC_TABLE = _build_table()


# ── table-driven CRC-32 ─────────────────────────────────────────────────────

def crc32(data: bytes, verbose: bool = False) -> int:
    """Compute CRC-32 using the table-driven algorithm."""
    crc = 0xFFFFFFFF
    for i, byte in enumerate(data):
        index = (crc ^ byte) & 0xFF
        crc = (crc >> 8) ^ CRC_TABLE[index]
        if verbose and len(data) <= 16:
            print(f"    byte {i:3d}: 0x{byte:02X}  "
                  f"table[0x{index:02X}]=0x{CRC_TABLE[index]:08X}  "
                  f"crc=0x{crc:08X}")
    result = crc ^ 0xFFFFFFFF
    return result & 0xFFFFFFFF


# ── step-by-step XOR division (educational, small inputs only) ───────────

POLY_BITS = 0x104C11DB7  # 33-bit generator (includes leading 1)
POLY_WIDTH = 33


def step_by_step_division(data: bytes) -> int:
    """Show CRC-32 polynomial division one XOR at a time.

    This mirrors the *unreflected* CRC-32 so the bit-shifting is
    easier to follow.  The final value matches the standard CRC-32
    only for the reflected variant; here we focus on the educational
    XOR-division process.
    """
    bits = "".join(f"{b:08b}" for b in data) + "0" * 32
    dividend = int(bits, 2)
    total_bits = len(bits)

    print(f"\n  Message bits ({len(bits) - 32} data + 32 zeros):")
    _print_bits(bits)
    print(f"\n  Generator polynomial (33 bits): {POLY_BITS:033b}")
    print(f"  Performing XOR long division …\n")

    step = 0
    for i in range(total_bits - 32):
        if dividend & (1 << (total_bits - 1 - i)):
            step += 1
            shifted_poly = POLY_BITS << (total_bits - POLY_WIDTH - i)
            dividend ^= shifted_poly
            if step <= 12:
                remainder_bits = f"{dividend:0{total_bits}b}"
                print(f"    Step {step:3d}  XOR at bit {i:3d} → "
                      f"…{remainder_bits[max(0,i-4):i+36]}…")

    if step > 12:
        print(f"    … ({step - 12} more steps omitted for brevity) …")

    remainder = dividend & 0xFFFFFFFF
    print(f"\n  Remainder (unreflected CRC-32): 0x{remainder:08X}")
    print(f"  Remainder in binary           : {remainder:032b}")
    return remainder


def _print_bits(bits: str, width: int = 64) -> None:
    for i in range(0, len(bits), width):
        chunk = bits[i:i + width]
        print(f"    {chunk}")


# ── verification helper ──────────────────────────────────────────────────────

def verify_crc(data: bytes, expected_crc: int) -> bool:
    """Verify a CRC-32 value against data."""
    computed = crc32(data)
    return computed == expected_crc


# ── demo ─────────────────────────────────────────────────────────────────────

def demo() -> None:
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          CRC-32 Calculator – Demo Mode                  ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Demo 1 – simple CRC computation
    print("\n── Demo 1: CRC-32 of the string 'Hello' ──")
    data = b"Hello"
    result = crc32(data, verbose=True)
    stdlib = binascii.crc32(data) & 0xFFFFFFFF
    print(f"\n  Computed CRC-32 : 0x{result:08X}")
    print(f"  stdlib crc32    : 0x{stdlib:08X}")
    print(f"  Match           : {'✓' if result == stdlib else '✗'}")

    # Demo 2 – lookup table excerpt
    print("\n── Demo 2: CRC-32 lookup table (first 16 entries) ──")
    for i in range(16):
        print(f"    table[{i:3d}] = 0x{CRC_TABLE[i]:08X}", end="")
        print("" if (i % 4 == 3) else "  ", end="")
        if i % 4 == 3:
            print()

    # Demo 3 – step-by-step XOR division (tiny input)
    print("\n── Demo 3: Step-by-step XOR division for 'Hi' ──")
    step_by_step_division(b"Hi")

    # Demo 4 – integrity verification
    print("\n── Demo 4: Integrity verification ──")
    msg = b"Ethernet frame payload"
    good_crc = crc32(msg)
    print(f"  Message : {msg.decode()}")
    print(f"  CRC-32  : 0x{good_crc:08X}")
    print(f"  Verify OK             : {'✓' if verify_crc(msg, good_crc) else '✗'}")
    bad = bytearray(msg)
    bad[0] ^= 0x01
    print(f"  Verify after bit-flip : "
          f"{'✓' if verify_crc(bytes(bad), good_crc) else '✗ mismatch detected'}")

    # Demo 5 – CRC properties
    print("\n── Demo 5: CRC properties ──")
    print("  • CRC detects all single-bit errors.")
    print("  • CRC detects all burst errors ≤ 32 bits.")
    print("  • CRC detects most (99.99999995%) random errors of any length.")
    print("  • Ethernet appends the CRC as a 4-byte FCS at the end of every frame.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute and explore CRC-32 (Ethernet FCS).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s
              %(prog)s --text "Hello, world!"
              %(prog)s --hex DEADBEEF
              %(prog)s --step "Hi"
        """))
    parser.add_argument("--text", help="Compute CRC-32 of a text string")
    parser.add_argument("--hex", help="Compute CRC-32 of hex-encoded bytes")
    parser.add_argument("--step", metavar="TEXT",
                        help="Show step-by-step XOR division (short strings)")
    args = parser.parse_args()

    if args.text:
        data = args.text.encode()
        result = crc32(data, verbose=True)
        print(f"\n  CRC-32: 0x{result:08X}")
    elif args.hex:
        data = bytes.fromhex(args.hex)
        result = crc32(data, verbose=True)
        print(f"\n  CRC-32: 0x{result:08X}")
    elif args.step:
        step_by_step_division(args.step.encode())
        result = crc32(args.step.encode())
        print(f"  Standard CRC-32 (reflected): 0x{result:08X}")
    else:
        demo()


if __name__ == "__main__":
    main()
