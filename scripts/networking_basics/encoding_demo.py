#!/usr/bin/env python3
"""
Network Data Encoding Demo
============================
Demonstrates common encoding schemes used in network protocols:
Base64 (email/MIME, HTTP auth), URL-encoding (HTTP query strings),
hexadecimal (packet dumps), and ASCII/UTF-8 (everything).

Each encoding is shown step-by-step so you can see exactly how the
original bytes are transformed, which helps when reading RFCs,
debugging HTTP headers, or inspecting packet captures.

Concepts demonstrated:
  * Base64 encoding and the 6-bit group ↔ character mapping
  * Percent-encoding (URL encoding) per RFC 3986
  * Hexadecimal representation of raw bytes
  * ASCII vs UTF-8 multibyte encoding

Usage:
    python encoding_demo.py                        # run built-in demo
    python encoding_demo.py --encode "Hello World"
    python encoding_demo.py --decode-base64 SGVsbG8gV29ybGQ=
    python encoding_demo.py --decode-url "Hello%20World"
"""

import argparse
import base64
import binascii
import sys
import urllib.parse

B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def section(title: str) -> None:
    print(f"\n{'─' * 62}")
    print(f"  {title}")
    print(f"{'─' * 62}")


def show_ascii(text: str) -> None:
    """Show ASCII code points for each character."""
    section("ASCII / UTF-8 Representation")
    raw = text.encode("utf-8")
    print(f"  Input string : {text}")
    print(f"  Byte length  : {len(raw)} bytes")
    print()
    print(f"    {'Char':<6s} {'Dec':>5s} {'Hex':>5s} {'Binary':>10s}  Note")
    print(f"    {'----':<6s} {'---':>5s} {'---':>5s} {'------':>10s}  ----")
    for b in raw:
        ch = chr(b) if 32 <= b < 127 else "·"
        note = ""
        if b < 32:
            note = "control character"
        elif b == 32:
            note = "space"
        elif b > 127:
            note = "UTF-8 continuation / multibyte"
        print(f"    {ch:<6s} {b:>5d} 0x{b:02X}  {b:>08b}  {note}")


def show_hex_encoding(text: str) -> None:
    """Show hex encoding of bytes."""
    section("Hexadecimal Encoding")
    raw = text.encode("utf-8")
    hex_str = binascii.hexlify(raw).decode()
    print(f"  Input  : {text}")
    print(f"  Bytes  : {list(raw)}")
    print(f"  Hex    : {hex_str}")
    print()
    print("  Byte-by-byte:")
    for i, b in enumerate(raw):
        ch = chr(b) if 32 <= b < 127 else "·"
        print(f"    byte {i:>2d}: '{ch}' -> 0x{b:02X} (decimal {b})")
    print(f"\n  Packed hex string: {hex_str}")
    print(f"  With spaces     : {' '.join(f'{b:02X}' for b in raw)}")


def show_base64(text: str) -> None:
    """Show Base64 encoding with 6-bit group breakdown."""
    section("Base64 Encoding (RFC 4648)")
    raw = text.encode("utf-8")
    encoded = base64.b64encode(raw).decode()
    print(f"  Input  : {text}")
    print(f"  Base64 : {encoded}")
    print()

    # Show the bit-level process
    bit_string = "".join(f"{b:08b}" for b in raw)
    # Pad to multiple of 6
    padded = bit_string + "0" * ((6 - len(bit_string) % 6) % 6)
    groups = [padded[i:i+6] for i in range(0, len(padded), 6)]

    print("  Step 1 — Convert input bytes to a bit stream:")
    for i, b in enumerate(raw):
        ch = chr(b) if 32 <= b < 127 else "·"
        print(f"    '{ch}' (0x{b:02X}) -> {b:08b}")

    print(f"\n  Bit stream: {bit_string}")
    if len(bit_string) % 6:
        print(f"  Padded to 6-bit boundary: {padded}")

    print("\n  Step 2 — Split into 6-bit groups and map to Base64 alphabet:")
    print(f"    {'Group':<8s} {'Index':>5s}  Char")
    print(f"    {'-----':<8s} {'-----':>5s}  ----")
    for g in groups:
        idx = int(g, 2)
        if idx < len(B64_ALPHABET):
            ch = B64_ALPHABET[idx]
        else:
            ch = "?"
        print(f"    {g}   {idx:>5d}  '{ch}'")

    pad_count = (3 - len(raw) % 3) % 3
    if pad_count:
        print(f"\n  Step 3 — Append {'=' * pad_count} padding ({pad_count} byte(s) short of 3-byte group)")
    print(f"\n  Result: {encoded}")
    print(f"  Decoded back: {base64.b64decode(encoded).decode('utf-8', errors='replace')}")


def show_url_encoding(text: str) -> None:
    """Show URL / percent-encoding."""
    section("URL (Percent) Encoding — RFC 3986")
    encoded = urllib.parse.quote(text, safe="")
    safe_encoded = urllib.parse.quote(text)

    print(f"  Input            : {text}")
    print(f"  Fully encoded    : {encoded}")
    print(f"  With safe='/'    : {safe_encoded}")
    print()
    print("  Character-by-character (full encoding):")
    print(f"    {'Char':<6s} {'Encoded':<8s}  Reason")
    print(f"    {'----':<6s} {'-------':<8s}  ------")
    unreserved = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~")
    for ch in text:
        enc = urllib.parse.quote(ch, safe="")
        if ch in unreserved:
            reason = "unreserved — no encoding needed"
        elif ch == " ":
            reason = "space → %20 (or + in query strings)"
        else:
            reason = "reserved / special — must encode"
        print(f"    {ch!r:<6s} {enc:<8s}  {reason}")

    print(f"\n  query_string style (space → +):")
    print(f"    {urllib.parse.quote_plus(text)}")


def full_encode(text: str) -> None:
    """Run all encoding demonstrations on the given text."""
    print(f"\n{'=' * 62}")
    print(f"  Encoding all representations of: {text!r}")
    print(f"{'=' * 62}")
    show_ascii(text)
    show_hex_encoding(text)
    show_base64(text)
    show_url_encoding(text)


def demo() -> None:
    print("=" * 62)
    print("  Network Data Encoding Demo")
    print("=" * 62)
    print("  Encoding is how raw data is represented for transmission.")
    print("  Different protocols require different encoding schemes.")

    for sample in ["Hello, World!", "user:p@ss/w0rd", "café ☕"]:
        full_encode(sample)

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate network data encoding schemes")
    parser.add_argument("--encode", metavar="TEXT", help="Encode text in all formats")
    parser.add_argument("--decode-base64", metavar="B64", help="Decode a Base64 string")
    parser.add_argument("--decode-url", metavar="URL", help="Decode a URL-encoded string")
    args = parser.parse_args()

    if not any([args.encode, args.decode_base64, args.decode_url]):
        demo()
        return

    if args.encode:
        full_encode(args.encode)

    if args.decode_base64:
        try:
            decoded = base64.b64decode(args.decode_base64).decode("utf-8", errors="replace")
            print(f"  Base64 input : {args.decode_base64}")
            print(f"  Decoded      : {decoded}")
        except Exception as e:
            print(f"  [!] Decode error: {e}")

    if args.decode_url:
        decoded = urllib.parse.unquote(args.decode_url)
        print(f"  URL input : {args.decode_url}")
        print(f"  Decoded   : {decoded}")


if __name__ == "__main__":
    main()
