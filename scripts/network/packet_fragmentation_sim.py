#!/usr/bin/env python3
"""
IPv4 Packet Fragmentation Simulator
=====================================
Simulates how an IPv4 router splits an oversized datagram into fragments
that fit within a link's Maximum Transmission Unit (MTU), and then
reassembles the fragments at the destination.

Key IPv4 header fields involved:
  * Identification  – 16-bit value shared by all fragments of one datagram.
  * Fragment Offset – measured in 8-byte units; tells the receiver where
                      this fragment's payload belongs in the original data.
  * More Fragments (MF) flag – set on every fragment except the last.
  * Total Length    – includes the IP header + this fragment's payload.

The payload of each fragment (except possibly the last) must be a multiple
of 8 bytes so that Fragment Offset arithmetic stays integral.

Concepts demonstrated:
  * Why fragmentation exists (MTU mismatch)
  * Fragment offset calculation in 8-byte units
  * MF (More Fragments) flag usage
  * Reassembly by sorting on offset and concatenating payloads
  * Why "Don't Fragment" (DF) exists to avoid fragmentation

Usage:
    python packet_fragmentation_sim.py                           # demo
    python packet_fragmentation_sim.py --size 4000 --mtu 1500    # custom
    python packet_fragmentation_sim.py --size 10000 --mtu 576    # tiny MTU
"""

import argparse
import textwrap

IP_HEADER_LEN = 20  # bytes (no options)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class IPv4Packet:
    """Simplified IPv4 datagram."""

    def __init__(self, src: str, dst: str, payload_size: int,
                 identification: int = 1, offset: int = 0, mf: bool = False,
                 payload_tag: str = ""):
        self.src = src
        self.dst = dst
        self.identification = identification
        self.offset = offset          # in bytes (stored in header as /8)
        self.mf = mf
        self.payload_size = payload_size
        self.total_length = IP_HEADER_LEN + payload_size
        self.payload_tag = payload_tag  # descriptive label for display

    def __repr__(self):
        mf_str = "1" if self.mf else "0"
        return (f"[ID={self.identification:#06x}  Offset={self.offset:>5d} "
                f"({self.offset // 8:>4d}×8)  MF={mf_str}  "
                f"PayloadLen={self.payload_size:>5d}  "
                f"TotalLen={self.total_length:>5d}]")


# ---------------------------------------------------------------------------
# Fragmentation logic
# ---------------------------------------------------------------------------

def fragment_packet(packet: IPv4Packet, mtu: int) -> list:
    """Fragment *packet* so every piece fits within *mtu* bytes."""
    if packet.total_length <= mtu:
        return [packet]

    max_payload = mtu - IP_HEADER_LEN
    # Payload per fragment (except last) must be a multiple of 8
    max_payload = (max_payload // 8) * 8
    if max_payload == 0:
        raise ValueError(f"MTU {mtu} too small to carry any payload with "
                         f"{IP_HEADER_LEN}-byte header.")

    fragments = []
    remaining = packet.payload_size
    current_offset = packet.offset

    frag_num = 1
    while remaining > 0:
        chunk = min(max_payload, remaining)
        # Last fragment need not be multiple of 8
        is_last = (chunk == remaining) and not packet.mf
        if not is_last and chunk % 8 != 0:
            chunk = (chunk // 8) * 8

        frag = IPv4Packet(
            src=packet.src,
            dst=packet.dst,
            payload_size=chunk,
            identification=packet.identification,
            offset=current_offset,
            mf=not is_last,
            payload_tag=f"frag-{frag_num}",
        )
        fragments.append(frag)
        current_offset += chunk
        remaining -= chunk
        frag_num += 1

    return fragments


def reassemble(fragments: list) -> IPv4Packet:
    """Reassemble a list of fragments into the original packet."""
    ordered = sorted(fragments, key=lambda f: f.offset)
    total_payload = sum(f.payload_size for f in ordered)

    # Sanity checks
    expected_offset = ordered[0].offset
    for f in ordered:
        assert f.offset == expected_offset, (
            f"Gap detected: expected offset {expected_offset}, got {f.offset}")
        expected_offset += f.payload_size

    return IPv4Packet(
        src=ordered[0].src,
        dst=ordered[0].dst,
        payload_size=total_payload,
        identification=ordered[0].identification,
        offset=ordered[0].offset,
        mf=False,
        payload_tag="reassembled",
    )


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_packet(pkt: IPv4Packet, indent: str = "  "):
    print(f"{indent}{pkt}")


def print_fragment_diagram(fragments: list, original_size: int):
    """Show a simple ASCII bar chart of fragment layout."""
    bar_width = 60
    scale = bar_width / original_size if original_size else 1

    print("\n  Fragment layout (not to scale for very small fragments):")
    print(f"  {'─' * (bar_width + 2)}")
    for i, f in enumerate(fragments):
        start = int(f.offset * scale)
        length = max(1, int(f.payload_size * scale))
        bar = " " * start + "█" * length
        mf = "MF=1" if f.mf else "MF=0"
        print(f"  |{bar:<{bar_width}}| frag {i + 1} offset={f.offset} "
              f"len={f.payload_size} {mf}")
    print(f"  {'─' * (bar_width + 2)}")
    print(f"  0{' ' * (bar_width - len(str(original_size)))}"
          f"{original_size} bytes\n")


# ---------------------------------------------------------------------------
# Demo / CLI
# ---------------------------------------------------------------------------

def run_simulation(payload_size: int, mtu: int):
    print(f"\n{'═' * 62}")
    print(f"  Original datagram: payload={payload_size} bytes, "
          f"total={payload_size + IP_HEADER_LEN} bytes")
    print(f"  Link MTU: {mtu} bytes   (max payload per fragment: "
          f"{((mtu - IP_HEADER_LEN) // 8) * 8} bytes)")
    print(f"{'═' * 62}\n")

    original = IPv4Packet("192.0.2.1", "198.51.100.5", payload_size,
                          identification=0xABCD)
    print("  Original packet:")
    print_packet(original)

    fragments = fragment_packet(original, mtu)
    print(f"\n  → Fragmented into {len(fragments)} piece(s):\n")
    for i, f in enumerate(fragments, 1):
        print(f"    Fragment {i}: {f}")

    print_fragment_diagram(fragments, payload_size)

    # Reassemble
    rebuilt = reassemble(fragments)
    print("  Reassembled packet:")
    print_packet(rebuilt)
    match = rebuilt.payload_size == original.payload_size
    status = "✓ SUCCESS" if match else "✗ MISMATCH"
    print(f"\n  Reassembly check: original={original.payload_size}, "
          f"reassembled={rebuilt.payload_size}  {status}\n")


def run_demo():
    print(textwrap.dedent("""\
        ╭──────────────────────────────────────────────────────────╮
        │      IPv4 Packet Fragmentation Simulator — Demo Mode     │
        ╰──────────────────────────────────────────────────────────╯
    """))

    scenarios = [
        (3000, 1500, "Typical Internet MTU"),
        (5000, 1500, "Larger payload on standard MTU"),
        (1400, 1500, "No fragmentation needed"),
        (4000, 576,  "Legacy minimum MTU (RFC 791)"),
    ]

    for size, mtu, label in scenarios:
        print(f"\n  ╌╌╌ Scenario: {label} ╌╌╌")
        run_simulation(size, mtu)


def main():
    parser = argparse.ArgumentParser(
        description="Simulate IPv4 packet fragmentation and reassembly.")
    parser.add_argument("--size", type=int, default=0,
                        help="Payload size in bytes (default: run demo).")
    parser.add_argument("--mtu", type=int, default=1500,
                        help="Link MTU in bytes (default: 1500).")
    args = parser.parse_args()

    if args.size <= 0:
        run_demo()
    else:
        run_simulation(args.size, args.mtu)


if __name__ == "__main__":
    main()
