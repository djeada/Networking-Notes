#!/usr/bin/env python3
"""Packet Sniffer Demo — Educational Networking Script

Since actual packet sniffing requires root / raw-socket privileges, this
script instead **constructs** sample Ethernet, IPv4 and TCP headers as
raw byte arrays, then **parses** them field by field — exactly the way a
real sniffer (tcpdump, Wireshark) would.

For every header field the script prints:
  • byte offset and length
  • raw hex value
  • decoded / human-readable value
  • a short explanation of the field's purpose

This is an excellent study aid for understanding packet anatomy at the
byte level.

Usage:
    python packet_sniffer_demo.py
"""

from __future__ import annotations

import struct
import textwrap

# ── Helpers ──────────────────────────────────────────────────────────────

def hex_dump(data: bytes, width: int = 16) -> str:
    """Return a classic hex-dump string."""
    lines = []
    for offset in range(0, len(data), width):
        chunk = data[offset : offset + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"  {offset:04x}  {hex_part:<{width * 3}}  {ascii_part}")
    return "\n".join(lines)


def ip_str(packed: bytes) -> str:
    """Convert 4 raw bytes to dotted-decimal IP string."""
    return ".".join(str(b) for b in packed)


def mac_str(packed: bytes) -> str:
    """Convert 6 raw bytes to colon-separated MAC string."""
    return ":".join(f"{b:02x}" for b in packed)


# ── Packet builders ─────────────────────────────────────────────────────

def build_ethernet_frame(
    dst_mac: str = "de:ad:be:ef:ca:fe",
    src_mac: str = "02:42:ac:11:00:02",
    ether_type: int = 0x0800,  # IPv4
) -> bytes:
    """Build a 14-byte Ethernet II header."""
    dst = bytes(int(x, 16) for x in dst_mac.split(":"))
    src = bytes(int(x, 16) for x in src_mac.split(":"))
    return dst + src + struct.pack("!H", ether_type)


def build_ipv4_header(
    src_ip: str = "192.168.1.100",
    dst_ip: str = "93.184.216.34",
    protocol: int = 6,  # TCP
    payload_len: int = 20,
) -> bytes:
    """Build a minimal 20-byte IPv4 header (no options)."""
    version_ihl = (4 << 4) | 5    # version=4, IHL=5 (20 bytes)
    dscp_ecn = 0
    total_length = 20 + payload_len
    identification = 0x1234
    flags_fragment = 0x4000        # Don't Fragment
    ttl = 64
    # Checksum set to 0 for simplicity (would be computed in real code)
    checksum = 0
    src = bytes(int(x) for x in src_ip.split("."))
    dst = bytes(int(x) for x in dst_ip.split("."))

    return struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl, dscp_ecn, total_length,
        identification, flags_fragment,
        ttl, protocol, checksum,
        src, dst,
    )


def build_tcp_header(
    src_port: int = 49152,
    dst_port: int = 80,
    seq: int = 1000,
    ack: int = 0,
    flags: int = 0x02,  # SYN
) -> bytes:
    """Build a minimal 20-byte TCP header (no options)."""
    data_offset = 5 << 4  # 5 × 4 = 20 bytes, upper nibble
    window = 65535
    checksum = 0
    urgent = 0
    return struct.pack(
        "!HHIIBBHHH",
        src_port, dst_port,
        seq, ack,
        data_offset, flags,
        window, checksum, urgent,
    )


# ── Parsers ──────────────────────────────────────────────────────────────

ETHER_TYPES = {0x0800: "IPv4", 0x0806: "ARP", 0x86DD: "IPv6"}
IP_PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP", 47: "GRE", 50: "ESP"}
TCP_FLAG_NAMES = ["FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR"]


def parse_ethernet(data: bytes) -> int:
    """Parse and explain a 14-byte Ethernet II header. Returns offset."""
    print("┌─────────────────────────────────────────────────────────┐")
    print("│              ETHERNET II  HEADER  (14 bytes)            │")
    print("└─────────────────────────────────────────────────────────┘\n")
    print(hex_dump(data[:14]))
    print()

    dst = data[0:6]
    src = data[6:12]
    etype = struct.unpack("!H", data[12:14])[0]

    fields = [
        ("Destination MAC", "0-5",   mac_str(dst), "Layer-2 destination address"),
        ("Source MAC",      "6-11",  mac_str(src), "Layer-2 source address"),
        ("EtherType",      "12-13", f"0x{etype:04x} ({ETHER_TYPES.get(etype, '?')})",
         "Identifies the upper-layer protocol"),
    ]
    for name, off, val, desc in fields:
        print(f"  [{off:>5}]  {name:<20}  {val:<28}  {desc}")
    print()
    return 14


def parse_ipv4(data: bytes, offset: int = 0) -> int:
    """Parse and explain a 20-byte IPv4 header. Returns new offset."""
    hdr = data[offset : offset + 20]
    print("┌─────────────────────────────────────────────────────────┐")
    print("│                IPv4  HEADER  (20 bytes)                 │")
    print("└─────────────────────────────────────────────────────────┘\n")
    print(hex_dump(hdr))
    print()

    ver_ihl = hdr[0]
    version = ver_ihl >> 4
    ihl = (ver_ihl & 0x0F) * 4
    dscp_ecn = hdr[1]
    total_len = struct.unpack("!H", hdr[2:4])[0]
    ident = struct.unpack("!H", hdr[4:6])[0]
    flags_frag = struct.unpack("!H", hdr[6:8])[0]
    flags = flags_frag >> 13
    frag_offset = flags_frag & 0x1FFF
    ttl = hdr[8]
    proto = hdr[9]
    checksum = struct.unpack("!H", hdr[10:12])[0]
    src = hdr[12:16]
    dst = hdr[16:20]

    flag_strs = []
    if flags & 0x2:
        flag_strs.append("DF")
    if flags & 0x1:
        flag_strs.append("MF")

    fields = [
        ("Version",       "0 hi",   str(version),                "IP version (4)"),
        ("IHL",           "0 lo",   f"{ihl} bytes",              "Header length in bytes"),
        ("DSCP / ECN",    "1",      f"0x{dscp_ecn:02x}",        "Differentiated services / congestion"),
        ("Total Length",  "2-3",    str(total_len),              "Entire packet length in bytes"),
        ("Identification","4-5",    f"0x{ident:04x}",           "Fragment identification"),
        ("Flags",         "6 hi",   " ".join(flag_strs) or "-", "DF=Don't Fragment, MF=More Fragments"),
        ("Frag Offset",   "6-7 lo", str(frag_offset),           "Offset of this fragment (×8 bytes)"),
        ("TTL",           "8",      str(ttl),                    "Time To Live — max hops remaining"),
        ("Protocol",      "9",      f"{proto} ({IP_PROTOCOLS.get(proto, '?')})",
         "Upper-layer protocol number"),
        ("Checksum",      "10-11",  f"0x{checksum:04x}",        "Header integrity check"),
        ("Source IP",     "12-15",  ip_str(src),                 "Sender's IP address"),
        ("Destination IP","16-19",  ip_str(dst),                 "Receiver's IP address"),
    ]
    for name, off, val, desc in fields:
        print(f"  [{off:>7}]  {name:<18}  {val:<28}  {desc}")
    print()
    return offset + ihl


def parse_tcp(data: bytes, offset: int = 0) -> int:
    """Parse and explain a 20-byte TCP header. Returns new offset."""
    hdr = data[offset : offset + 20]
    print("┌─────────────────────────────────────────────────────────┐")
    print("│                 TCP  HEADER  (20 bytes)                 │")
    print("└─────────────────────────────────────────────────────────┘\n")
    print(hex_dump(hdr))
    print()

    src_port = struct.unpack("!H", hdr[0:2])[0]
    dst_port = struct.unpack("!H", hdr[2:4])[0]
    seq = struct.unpack("!I", hdr[4:8])[0]
    ack = struct.unpack("!I", hdr[8:12])[0]
    data_off = (hdr[12] >> 4) * 4
    flags_byte = hdr[13]
    window = struct.unpack("!H", hdr[14:16])[0]
    checksum = struct.unpack("!H", hdr[16:18])[0]
    urgent = struct.unpack("!H", hdr[18:20])[0]

    active_flags = [TCP_FLAG_NAMES[i] for i in range(8) if flags_byte & (1 << i)]

    fields = [
        ("Source Port",   "0-1",    str(src_port),                    "Sender's port number"),
        ("Dest Port",     "2-3",    str(dst_port),                    "Receiver's port number"),
        ("Sequence #",    "4-7",    str(seq),                         "Byte-stream sequence number"),
        ("Ack #",         "8-11",   str(ack),                         "Next expected byte from peer"),
        ("Data Offset",   "12 hi",  f"{data_off} bytes",              "Header length"),
        ("Flags",         "13",     " ".join(active_flags) or "-",    "Control bits (SYN, ACK, FIN …)"),
        ("Window Size",   "14-15",  str(window),                      "Receive window (flow control)"),
        ("Checksum",      "16-17",  f"0x{checksum:04x}",             "Segment integrity check"),
        ("Urgent Ptr",    "18-19",  str(urgent),                      "Points to urgent data (if URG)"),
    ]
    for name, off, val, desc in fields:
        print(f"  [{off:>7}]  {name:<16}  {val:<28}  {desc}")
    print()
    return offset + data_off


# ── Demo ─────────────────────────────────────────────────────────────────

def run_demo() -> None:
    print("=" * 60)
    print(" Packet Sniffer Demo — Parsing Packet Bytes Field by Field")
    print("=" * 60)
    print(textwrap.dedent("""\
        This script constructs a sample Ethernet → IPv4 → TCP packet
        as raw bytes and then parses every header field, showing the
        byte offset, hex value, decoded value, and a short explanation.

        This is exactly what tools like Wireshark and tcpdump do when
        they capture packets off the wire.
    """))

    # Build a complete frame
    eth = build_ethernet_frame()
    ip = build_ipv4_header()
    tcp = build_tcp_header()
    payload = b"Hello, Network!"

    frame = eth + ip + tcp + payload

    print(f"  Total frame size: {len(frame)} bytes\n")
    print("── Full hex dump ──\n")
    print(hex_dump(frame))
    print("\n")

    # Parse each layer
    off = parse_ethernet(frame)
    off = parse_ipv4(frame, off)
    off = parse_tcp(frame, off)

    # Payload
    remaining = frame[off:]
    print("┌─────────────────────────────────────────────────────────┐")
    print("│                      PAYLOAD                            │")
    print("└─────────────────────────────────────────────────────────┘\n")
    print(hex_dump(remaining))
    print(f"\n  ASCII: {remaining.decode(errors='replace')!r}\n")

    print("  📝 Key points:")
    print("     • Each layer is stacked: Ethernet → IP → TCP → Payload.")
    print("     • A sniffer reads bytes sequentially, using header-length")
    print("       fields to know where one header ends and the next begins.")
    print("     • Understanding byte offsets is essential for writing")
    print("       protocol parsers and packet filters (BPF, eBPF).")


if __name__ == "__main__":
    run_demo()
