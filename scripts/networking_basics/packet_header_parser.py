#!/usr/bin/env python3
"""
Packet Header Parser
=====================
Parses raw hexadecimal bytes of common network packet headers and breaks
them down field by field with human-readable explanations.

Supported headers: Ethernet II, IPv4, TCP, UDP, ICMP.

Concepts demonstrated:
  * Byte-level structure of L2–L4 headers
  * Bit fields, flags, and checksums
  * Protocol number → name mapping
  * Big-endian (network byte order) interpretation

Usage:
    python packet_header_parser.py                        # run demo
    python packet_header_parser.py --ipv4 4500003C1C46...
    python packet_header_parser.py --icmp 08004D5600010001
"""

import argparse
import struct
import sys

ETHERTYPES = {
    0x0800: "IPv4",
    0x0806: "ARP",
    0x86DD: "IPv6",
    0x8100: "802.1Q VLAN",
    0x88CC: "LLDP",
}

IP_PROTOCOLS = {
    1: "ICMP", 2: "IGMP", 6: "TCP", 17: "UDP",
    41: "IPv6 encap", 47: "GRE", 50: "ESP", 51: "AH", 89: "OSPF",
}

TCP_FLAG_NAMES = ["FIN", "SYN", "RST", "PSH", "ACK", "URG", "ECE", "CWR"]

ICMP_TYPES = {
    0: "Echo Reply", 3: "Destination Unreachable", 4: "Source Quench",
    5: "Redirect", 8: "Echo Request", 11: "Time Exceeded",
    13: "Timestamp Request", 14: "Timestamp Reply",
}


def hex_to_bytes(hex_str: str) -> bytes:
    clean = hex_str.replace(" ", "").replace(":", "").replace("-", "")
    return bytes.fromhex(clean)


def fmt_mac(b: bytes) -> str:
    return ":".join(f"{x:02X}" for x in b)


def field(name: str, value: str, extra: str = "") -> None:
    ex = f"  ({extra})" if extra else ""
    print(f"    {name:<22s}: {value}{ex}")


def hdr(title: str) -> None:
    print(f"\n  ── {title} {'─' * (54 - len(title))}")


def parse_ethernet(data: bytes) -> int:
    """Parse and display Ethernet II header. Returns EtherType."""
    hdr("Ethernet II Header (14 bytes)")
    dst, src = data[0:6], data[6:12]
    etype = struct.unpack("!H", data[12:14])[0]
    field("Destination MAC", fmt_mac(dst),
          "broadcast" if dst == b"\xff" * 6 else "")
    field("Source MAC", fmt_mac(src))
    field("EtherType", f"0x{etype:04X}", ETHERTYPES.get(etype, "unknown"))
    return etype


def parse_ipv4(data: bytes) -> dict:
    """Parse IPv4 header. Returns dict with protocol and header length."""
    hdr("IPv4 Header")
    ver_ihl = data[0]
    version = (ver_ihl >> 4) & 0xF
    ihl = ver_ihl & 0xF
    hdr_len = ihl * 4
    dscp_ecn = data[1]
    total_len = struct.unpack("!H", data[2:4])[0]
    ident = struct.unpack("!H", data[4:6])[0]
    flags_frag = struct.unpack("!H", data[6:8])[0]
    flags = (flags_frag >> 13) & 0x7
    frag_off = flags_frag & 0x1FFF
    ttl = data[8]
    proto = data[9]
    checksum = struct.unpack("!H", data[10:12])[0]
    src = ".".join(str(b) for b in data[12:16])
    dst = ".".join(str(b) for b in data[16:20])

    df = "DF " if flags & 0x2 else ""
    mf = "MF " if flags & 0x1 else ""
    flag_str = (df + mf).strip() or "none"

    field("Version", str(version))
    field("IHL", f"{ihl} ({hdr_len} bytes)")
    field("DSCP / ECN", f"0x{dscp_ecn:02X}")
    field("Total length", f"{total_len} bytes")
    field("Identification", f"0x{ident:04X} ({ident})")
    field("Flags", flag_str)
    field("Fragment offset", str(frag_off))
    field("TTL", str(ttl))
    field("Protocol", str(proto), IP_PROTOCOLS.get(proto, "unknown"))
    field("Header checksum", f"0x{checksum:04X}")
    field("Source IP", src)
    field("Destination IP", dst)

    if hdr_len > 20:
        field("Options", f"{data[20:hdr_len].hex()} ({hdr_len - 20} bytes)")
    return {"protocol": proto, "header_length": hdr_len}


def parse_tcp(data: bytes) -> None:
    """Parse TCP header (minimum 20 bytes)."""
    hdr("TCP Header")
    src_port = struct.unpack("!H", data[0:2])[0]
    dst_port = struct.unpack("!H", data[2:4])[0]
    seq = struct.unpack("!I", data[4:8])[0]
    ack = struct.unpack("!I", data[8:12])[0]
    offset_flags = struct.unpack("!H", data[12:14])[0]
    data_offset = (offset_flags >> 12) & 0xF
    hdr_len = data_offset * 4
    flags_raw = offset_flags & 0xFF
    window = struct.unpack("!H", data[14:16])[0]
    checksum = struct.unpack("!H", data[16:18])[0]
    urgent = struct.unpack("!H", data[18:20])[0]

    active = [TCP_FLAG_NAMES[i] for i in range(8) if flags_raw & (1 << i)]
    flag_str = " | ".join(reversed(active)) if active else "none"

    field("Source port", str(src_port))
    field("Destination port", str(dst_port))
    field("Sequence number", f"{seq} (0x{seq:08X})")
    field("Ack number", f"{ack} (0x{ack:08X})")
    field("Data offset", f"{data_offset} ({hdr_len} bytes)")
    field("Flags", f"0x{flags_raw:02X}  [{flag_str}]")
    field("Window size", str(window))
    field("Checksum", f"0x{checksum:04X}")
    field("Urgent pointer", str(urgent))

    if hdr_len > 20 and len(data) >= hdr_len:
        field("Options", f"{data[20:hdr_len].hex()} ({hdr_len - 20} bytes)")


def parse_udp(data: bytes) -> None:
    """Parse UDP header (8 bytes)."""
    hdr("UDP Header (8 bytes)")
    field("Source port", str(struct.unpack("!H", data[0:2])[0]))
    field("Destination port", str(struct.unpack("!H", data[2:4])[0]))
    field("Length", f"{struct.unpack('!H', data[4:6])[0]} bytes")
    field("Checksum", f"0x{struct.unpack('!H', data[6:8])[0]:04X}")


def parse_icmp(data: bytes) -> None:
    """Parse ICMP header (8 bytes minimum)."""
    hdr("ICMP Header")
    icmp_type, code = data[0], data[1]
    checksum = struct.unpack("!H", data[2:4])[0]
    rest = struct.unpack("!I", data[4:8])[0]
    field("Type", str(icmp_type), ICMP_TYPES.get(icmp_type, "unknown"))
    field("Code", str(code))
    field("Checksum", f"0x{checksum:04X}")
    if icmp_type in (0, 8):
        field("Identifier", f"0x{(rest >> 16) & 0xFFFF:04X}")
        field("Sequence number", str(rest & 0xFFFF))
    else:
        field("Rest of header", f"0x{rest:08X}")


def demo() -> None:
    """Run demonstrations with sample packets."""
    print("=" * 62)
    print("  Packet Header Parser — Demo Mode")
    print("=" * 62)

    # Sample 1: Ethernet + IPv4 + TCP SYN (192.168.0.1:49152 → 192.168.0.200:80)
    print("\n  ════ Sample 1: Ethernet → IPv4 → TCP SYN ════")
    raw = hex_to_bytes(
        "FFFFFFFFFFFF001122334455" "0800"
        "4500002C1C4640004006B1E6C0A80001C0A800C8"
        "C000005000000001000000005002FFFF12340000"
    )
    etype = parse_ethernet(raw)
    info = parse_ipv4(raw[14:])
    parse_tcp(raw[14 + info["header_length"]:])

    # Sample 2: IPv4 + UDP DNS query (10.0.0.1 → 8.8.8.8:53)
    print("\n\n  ════ Sample 2: IPv4 → UDP (DNS query) ════")
    raw = hex_to_bytes(
        "45000036ABCD000080110000" "0A00000108080808"
        "C35000350022" "0000"
    )
    info = parse_ipv4(raw)
    parse_udp(raw[info["header_length"]:])

    # Sample 3: IPv4 + ICMP Echo Request (192.168.1.1 → 192.168.1.2)
    print("\n\n  ════ Sample 3: IPv4 → ICMP Echo Request (ping) ════")
    raw = hex_to_bytes(
        "450000541234400040010000C0A80101C0A80102"
        "08004D5600010001"
    )
    info = parse_ipv4(raw)
    parse_icmp(raw[info["header_length"]:])

    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse raw hex packet headers field by field")
    parser.add_argument("--ethernet", metavar="HEX", help="Parse Ethernet II frame")
    parser.add_argument("--ipv4", metavar="HEX", help="Parse IPv4 header")
    parser.add_argument("--tcp", metavar="HEX", help="Parse TCP header")
    parser.add_argument("--udp", metavar="HEX", help="Parse UDP header")
    parser.add_argument("--icmp", metavar="HEX", help="Parse ICMP header")
    args = parser.parse_args()

    if not any([args.ethernet, args.ipv4, args.tcp, args.udp, args.icmp]):
        demo()
        return

    try:
        if args.ethernet:
            raw = hex_to_bytes(args.ethernet)
            parse_ethernet(raw)
        if args.ipv4:
            raw = hex_to_bytes(args.ipv4)
            parse_ipv4(raw)
        if args.tcp:
            raw = hex_to_bytes(args.tcp)
            parse_tcp(raw)
        if args.udp:
            raw = hex_to_bytes(args.udp)
            parse_udp(raw)
        if args.icmp:
            raw = hex_to_bytes(args.icmp)
            parse_icmp(raw)
    except (ValueError, struct.error) as e:
        print(f"  [!] Parse error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
