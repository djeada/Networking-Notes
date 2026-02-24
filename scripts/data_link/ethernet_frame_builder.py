#!/usr/bin/env python3
"""
Ethernet II Frame Builder & Parser
====================================
Builds and parses Ethernet II (DIX) frames, the most common frame format on
modern LANs.  The script walks through every field so you can see exactly how
bytes are laid out on the wire.

Frame structure (bytes):
    ┌──────────────┬──────────────┬───────────┬─────────────────┬──────────┐
    │ Dest MAC (6) │ Src MAC (6)  │ Type (2)  │ Payload (46-1500)│ FCS (4)  │
    └──────────────┴──────────────┴───────────┴─────────────────┴──────────┘

    * Destination MAC  – 6-byte hardware address of the intended receiver.
    * Source MAC       – 6-byte hardware address of the sender.
    * EtherType        – 2-byte field identifying the upper-layer protocol
                         (0x0800 = IPv4, 0x0806 = ARP, 0x86DD = IPv6, …).
    * Payload          – between 46 and 1500 bytes of upper-layer data.
                         Payloads shorter than 46 bytes are zero-padded.
    * FCS (CRC-32)     – 4-byte Frame Check Sequence for error detection.

Concepts demonstrated:
    * Ethernet II frame layout and field sizes
    * MAC address encoding / decoding
    * EtherType values and their meaning
    * Minimum payload padding (46 bytes)
    * CRC-32 Frame Check Sequence calculation

Usage:
    python ethernet_frame_builder.py                          # built-in demo
    python ethernet_frame_builder.py --dst AA:BB:CC:DD:EE:FF \\
        --src 11:22:33:44:55:66 --ethertype 0x0800 --payload "Hello"
    python ethernet_frame_builder.py --parse <hex string>     # parse raw hex
"""

import argparse
import binascii
import struct
import sys
import textwrap

# Well-known EtherType values
ETHERTYPES = {
    0x0800: "IPv4",
    0x0806: "ARP",
    0x8100: "802.1Q VLAN Tag",
    0x86DD: "IPv6",
    0x8847: "MPLS Unicast",
    0x88CC: "LLDP",
}

MIN_PAYLOAD = 46
MAX_PAYLOAD = 1500


def mac_to_bytes(mac_str: str) -> bytes:
    """Convert a colon-separated MAC string to 6 bytes."""
    parts = mac_str.split(":")
    if len(parts) != 6:
        raise ValueError(f"Invalid MAC address: {mac_str}")
    return bytes(int(p, 16) for p in parts)


def bytes_to_mac(data: bytes) -> str:
    """Convert 6 bytes to a colon-separated MAC string."""
    return ":".join(f"{b:02X}" for b in data)


def compute_fcs(frame_bytes: bytes) -> bytes:
    """Return the 4-byte CRC-32 FCS for *frame_bytes*."""
    crc = binascii.crc32(frame_bytes) & 0xFFFFFFFF
    return struct.pack("<I", crc)


def build_frame(dst_mac: str, src_mac: str, ethertype: int,
                payload: bytes, verbose: bool = True) -> bytes:
    """Build an Ethernet II frame and optionally print a breakdown."""
    dst = mac_to_bytes(dst_mac)
    src = mac_to_bytes(src_mac)
    etype = struct.pack("!H", ethertype)

    if len(payload) < MIN_PAYLOAD:
        pad_len = MIN_PAYLOAD - len(payload)
        if verbose:
            print(f"  ⚠  Payload is {len(payload)} bytes – padding with "
                  f"{pad_len} zero bytes to meet 46-byte minimum.")
        payload = payload + b"\x00" * pad_len
    elif len(payload) > MAX_PAYLOAD:
        raise ValueError(f"Payload too large ({len(payload)} > {MAX_PAYLOAD})")

    header = dst + src + etype
    fcs = compute_fcs(header + payload)
    frame = header + payload + fcs

    if verbose:
        etype_name = ETHERTYPES.get(ethertype, "Unknown")
        print(f"\n{'='*60}")
        print("  Ethernet II Frame Construction")
        print(f"{'='*60}")
        print(f"  Destination MAC : {bytes_to_mac(dst)}")
        print(f"  Source MAC      : {bytes_to_mac(src)}")
        print(f"  EtherType       : 0x{ethertype:04X} ({etype_name})")
        print(f"  Payload length  : {len(payload)} bytes")
        print(f"  FCS (CRC-32)    : {fcs.hex().upper()}")
        print(f"  Total frame size: {len(frame)} bytes")
        print(f"{'='*60}")
        print(f"  Raw hex:\n  {frame.hex().upper()}")

    return frame


def parse_frame(hex_str: str) -> None:
    """Parse raw hex into Ethernet II frame fields."""
    raw = bytes.fromhex(hex_str.replace(" ", "").replace(":", ""))
    if len(raw) < 64:
        print(f"  ⚠  Frame is only {len(raw)} bytes (minimum Ethernet "
              "frame is 64 bytes including FCS).")

    dst = raw[0:6]
    src = raw[6:12]
    etype = struct.unpack("!H", raw[12:14])[0]
    fcs_received = raw[-4:]
    payload = raw[14:-4]

    expected_fcs = compute_fcs(raw[:-4])
    fcs_ok = fcs_received == expected_fcs
    etype_name = ETHERTYPES.get(etype, "Unknown")

    print(f"\n{'='*60}")
    print("  Ethernet II Frame Parse Result")
    print(f"{'='*60}")
    print(f"  Destination MAC : {bytes_to_mac(dst)}")
    print(f"  Source MAC      : {bytes_to_mac(src)}")
    print(f"  EtherType       : 0x{etype:04X} ({etype_name})")
    print(f"  Payload length  : {len(payload)} bytes")
    print(f"  FCS received    : {fcs_received.hex().upper()}")
    print(f"  FCS expected    : {expected_fcs.hex().upper()}")
    print(f"  FCS valid       : {'✓ Yes' if fcs_ok else '✗ No – frame is CORRUPTED'}")
    print(f"{'='*60}")
    if len(payload) <= 64:
        print(f"  Payload hex : {payload.hex().upper()}")
        printable = "".join(chr(b) if 32 <= b < 127 else "." for b in payload)
        print(f"  Payload text: {printable}")


def demo() -> None:
    """Run several educational demonstrations."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        Ethernet II Frame Builder – Demo Mode            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n── Demo 1: IPv4 frame with short payload (auto-padded) ──")
    frame1 = build_frame("FF:FF:FF:FF:FF:FF", "DE:AD:BE:EF:00:01",
                         0x0800, b"Hello, Ethernet!")

    print("\n── Demo 2: ARP frame ──")
    arp_payload = b"\x00\x01" + b"\x08\x00" + b"\x06\x04" + b"\x00\x01"
    arp_payload += b"\xde\xad\xbe\xef\x00\x01" + b"\xc0\xa8\x01\x01"
    arp_payload += b"\x00" * 6 + b"\xc0\xa8\x01\x02"
    build_frame("FF:FF:FF:FF:FF:FF", "DE:AD:BE:EF:00:01", 0x0806, arp_payload)

    print("\n── Demo 3: Parse the IPv4 frame we just built ──")
    parse_frame(frame1.hex())

    print("\n── Demo 4: Detect a corrupted frame ──")
    corrupted = bytearray(frame1)
    corrupted[20] ^= 0xFF  # flip a byte in the payload
    parse_frame(corrupted.hex())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build or parse Ethernet II frames.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s
              %(prog)s --dst FF:FF:FF:FF:FF:FF --src AA:BB:CC:DD:EE:FF \\
                       --ethertype 0x0800 --payload "ping"
              %(prog)s --parse 00112233...
        """))
    parser.add_argument("--dst", help="Destination MAC (e.g. AA:BB:CC:DD:EE:FF)")
    parser.add_argument("--src", help="Source MAC")
    parser.add_argument("--ethertype", help="EtherType as hex (e.g. 0x0800)")
    parser.add_argument("--payload", help="Payload as a UTF-8 string")
    parser.add_argument("--parse", metavar="HEX", help="Parse a frame from hex")
    args = parser.parse_args()

    if args.parse:
        parse_frame(args.parse)
    elif args.dst and args.src and args.ethertype:
        etype = int(args.ethertype, 16)
        data = (args.payload or "").encode()
        build_frame(args.dst, args.src, etype, data)
    else:
        demo()


if __name__ == "__main__":
    main()
