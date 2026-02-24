#!/usr/bin/env python3
"""VPN Tunnel Simulator — Educational Networking Script

Demonstrates the concept of VPN tunnelling / packet encapsulation:

  1. An **original (inner) packet** is created with its own IP header,
     protocol header, and payload.
  2. The VPN "encrypts" the original packet (simulated with XOR) and
     wraps it inside a **new outer IP packet** with VPN-specific headers.
  3. At the remote end the outer headers are stripped and the inner
     packet is "decrypted" and recovered.

The script prints a side-by-side comparison of the original vs. the
tunnelled packet so students can see exactly what encapsulation adds.

Usage:
    python vpn_tunnel_simulator.py
"""

from __future__ import annotations

import dataclasses
import textwrap

# ── Simulated packet structures ─────────────────────────────────────────

@dataclasses.dataclass
class IPHeader:
    """Simplified IP header (v4)."""
    version: int = 4
    ttl: int = 64
    protocol: str = "TCP"     # human-readable for educational clarity
    src_ip: str = "0.0.0.0"
    dst_ip: str = "0.0.0.0"

    def display(self, indent: str = "") -> str:
        return (
            f"{indent}┌─ IP Header ──────────────────────┐\n"
            f"{indent}│  Version : {self.version:<23} │\n"
            f"{indent}│  TTL     : {self.ttl:<23} │\n"
            f"{indent}│  Protocol: {self.protocol:<23} │\n"
            f"{indent}│  Src IP  : {self.src_ip:<23} │\n"
            f"{indent}│  Dst IP  : {self.dst_ip:<23} │\n"
            f"{indent}└──────────────────────────────────┘"
        )


@dataclasses.dataclass
class TCPHeader:
    """Simplified TCP header."""
    src_port: int = 0
    dst_port: int = 0
    seq: int = 1000
    flags: str = "SYN"

    def display(self, indent: str = "") -> str:
        return (
            f"{indent}┌─ TCP Header ─────────────────────┐\n"
            f"{indent}│  Src Port: {self.src_port:<23} │\n"
            f"{indent}│  Dst Port: {self.dst_port:<23} │\n"
            f"{indent}│  Seq     : {self.seq:<23} │\n"
            f"{indent}│  Flags   : {self.flags:<23} │\n"
            f"{indent}└──────────────────────────────────┘"
        )


@dataclasses.dataclass
class VPNHeader:
    """Simulated VPN header (like GRE, IPsec ESP, or WireGuard)."""
    vpn_type: str = "IPsec-ESP"
    spi: str = "0xDEADBEEF"    # Security Parameter Index
    seq_num: int = 1
    encryption: str = "AES-256-GCM"

    def display(self, indent: str = "") -> str:
        return (
            f"{indent}┌─ VPN Header ─────────────────────┐\n"
            f"{indent}│  Type    : {self.vpn_type:<23} │\n"
            f"{indent}│  SPI     : {self.spi:<23} │\n"
            f"{indent}│  Seq #   : {self.seq_num:<23} │\n"
            f"{indent}│  Cipher  : {self.encryption:<23} │\n"
            f"{indent}└──────────────────────────────────┘"
        )


@dataclasses.dataclass
class Packet:
    """A simulated network packet with an IP header, optional transport
    header, and a payload."""
    ip: IPHeader
    transport: TCPHeader | None = None
    payload: str = ""

    def display(self, indent: str = "") -> str:
        parts = [self.ip.display(indent)]
        if self.transport:
            parts.append(self.transport.display(indent))
        if self.payload:
            wrapped = textwrap.fill(self.payload, width=32)
            parts.append(
                f"{indent}┌─ Payload ────────────────────────┐\n"
                + "\n".join(f"{indent}│  {line:<33}│" for line in wrapped.splitlines())
                + f"\n{indent}└──────────────────────────────────┘"
            )
        return "\n".join(parts)


# ── VPN operations ───────────────────────────────────────────────────────

def xor_encrypt(data: str, key: int = 0xAA) -> bytes:
    """Toy XOR 'encryption' for demonstration only."""
    return bytes(b ^ key for b in data.encode())


def xor_decrypt(data: bytes, key: int = 0xAA) -> str:
    """Reverse the toy XOR encryption."""
    return bytes(b ^ key for b in data).decode()


def encapsulate(
    original: Packet,
    tunnel_src: str,
    tunnel_dst: str,
) -> tuple[IPHeader, VPNHeader, bytes]:
    """Simulate VPN encapsulation.

    Returns the outer IP header, the VPN header, and the 'encrypted'
    inner packet (as raw bytes).
    """
    # Serialise the inner packet to a string then 'encrypt'
    inner_repr = (
        f"{original.ip.src_ip}|{original.ip.dst_ip}|"
        f"{original.ip.protocol}|{original.ip.ttl}|"
    )
    if original.transport:
        inner_repr += f"{original.transport.src_port}|{original.transport.dst_port}|"
    inner_repr += original.payload

    encrypted = xor_encrypt(inner_repr)

    outer_ip = IPHeader(
        version=4,
        ttl=64,
        protocol="ESP",        # Encapsulating Security Payload
        src_ip=tunnel_src,
        dst_ip=tunnel_dst,
    )
    vpn_hdr = VPNHeader()

    return outer_ip, vpn_hdr, encrypted


def decapsulate(
    outer_ip: IPHeader,
    vpn_hdr: VPNHeader,
    encrypted: bytes,
) -> Packet:
    """Simulate VPN decapsulation — strip outer headers and decrypt."""
    decrypted = xor_decrypt(encrypted)
    parts = decrypted.split("|")
    ip = IPHeader(
        src_ip=parts[0],
        dst_ip=parts[1],
        protocol=parts[2],
        ttl=int(parts[3]),
    )
    transport = None
    payload_idx = 4
    if len(parts) > 5:
        transport = TCPHeader(src_port=int(parts[4]), dst_port=int(parts[5]))
        payload_idx = 6
    payload = "|".join(parts[payload_idx:])
    return Packet(ip=ip, transport=transport, payload=payload)


# ── Demo ─────────────────────────────────────────────────────────────────

def run_demo() -> None:
    print("=" * 70)
    print(" VPN Tunnel Simulator — Demo")
    print("=" * 70)
    print(textwrap.dedent("""\
        This demo shows how a VPN encapsulates an original packet inside
        a new outer packet for secure transport across an untrusted network.

        Scenario:
          • Alice (10.0.1.5) sends an HTTP request to Server (172.16.0.10).
          • The packet travels through a VPN tunnel between two gateways:
              VPN Gateway A  (203.0.113.1)  ←→  VPN Gateway B  (198.51.100.1)
          • On the public Internet, only the OUTER addresses are visible.
    """))

    # ── Step 1: Original packet ──
    original = Packet(
        ip=IPHeader(protocol="TCP", ttl=64, src_ip="10.0.1.5", dst_ip="172.16.0.10"),
        transport=TCPHeader(src_port=49152, dst_port=80, flags="PSH ACK"),
        payload="GET /index.html HTTP/1.1",
    )

    print("── Step 1: Original Packet (before VPN) ──\n")
    print(original.display(indent="    "))

    # ── Step 2: Encapsulate ──
    outer_ip, vpn_hdr, encrypted = encapsulate(
        original,
        tunnel_src="203.0.113.1",
        tunnel_dst="198.51.100.1",
    )

    print("\n\n── Step 2: Tunnelled Packet (on the public Internet) ──\n")
    print(outer_ip.display(indent="    "))
    print(vpn_hdr.display(indent="    "))
    enc_hex = encrypted[:24].hex()
    print(f"    ┌─ Encrypted Inner Packet ────────┐")
    print(f"    │  {enc_hex}… │")
    print(f"    │  ({len(encrypted)} bytes, XOR demo)       │")
    print(f"    └──────────────────────────────────┘")

    print("\n  📝 Notice:")
    print("     • The OUTER IP header shows gateway-to-gateway addresses.")
    print("     • The original source/destination IPs are hidden inside")
    print("       the encrypted payload — invisible to eavesdroppers.")

    # ── Step 3: Decapsulate ──
    recovered = decapsulate(outer_ip, vpn_hdr, encrypted)

    print("\n\n── Step 3: Decapsulated Packet (at the remote gateway) ──\n")
    print(recovered.display(indent="    "))

    print("\n  ✅ The original packet has been recovered intact.\n")

    # ── Size comparison ──
    orig_size = 20 + 20 + len(original.payload)   # IP + TCP + payload
    tunnel_size = 20 + 16 + len(encrypted)         # outer IP + VPN hdr + encrypted
    overhead = tunnel_size - orig_size

    print("── Overhead Comparison ──\n")
    print(f"    Original packet size  : ~{orig_size} bytes  (IP + TCP + payload)")
    print(f"    Tunnelled packet size : ~{tunnel_size} bytes  (outer IP + VPN hdr + encrypted)")
    print(f"    Overhead              : ~{overhead} bytes  ({overhead / orig_size * 100:.1f}%)")
    print()
    print("  📝 In practice, VPN overhead includes:")
    print("     • Outer IP header (20 bytes)")
    print("     • VPN protocol header (ESP/GRE/WireGuard — varies)")
    print("     • Encryption padding and authentication tag")
    print("     • Possible UDP encapsulation (for NAT traversal)")


if __name__ == "__main__":
    run_demo()
