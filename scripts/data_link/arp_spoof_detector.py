#!/usr/bin/env python3
"""
ARP Spoof Detection Simulator
===============================
Simulates an ARP cache and processes a stream of ARP packets, flagging
behaviour that is commonly associated with ARP spoofing / poisoning attacks.

ARP (Address Resolution Protocol) maps IPv4 addresses to MAC addresses on a
local network.  Because ARP has **no authentication**, an attacker can send
forged ARP replies to associate their own MAC with another host's IP – this is
called ARP spoofing (or ARP poisoning).  It enables man-in-the-middle attacks,
denial of service, and session hijacking.

Detection heuristics implemented:
    1. **MAC flapping** – IP-to-MAC mapping unexpectedly changes.
    2. **Gratuitous ARP flood** – too many unsolicited announcements.
    3. **Broadcast source** – ARP reply with broadcast source MAC.

Concepts demonstrated:
    * ARP request / reply lifecycle
    * ARP cache (table) management
    * Common ARP-based attacks and defences
    * Heuristic-based intrusion detection at the data link layer

Usage:
    python arp_spoof_detector.py                    # built-in demo scenario
    python arp_spoof_detector.py --file pkts.json   # process custom packets
"""

import argparse
import json
import textwrap
from collections import defaultdict
from typing import Dict, List

# ── data structures ──────────────────────────────────────────────────────────

BROADCAST_MAC = "FF:FF:FF:FF:FF:FF"


class ArpPacket:
    """Lightweight representation of an ARP packet."""
    def __init__(self, op: str, sender_mac: str, sender_ip: str,
                 target_mac: str, target_ip: str, timestamp: float = 0.0):
        self.op = op.upper()
        self.sender_mac = sender_mac.upper()
        self.sender_ip = sender_ip
        self.target_mac = target_mac.upper()
        self.target_ip = target_ip
        self.timestamp = timestamp

    def __repr__(self) -> str:
        arrow = "→" if self.op == "REQUEST" else "←"
        return (f"[{self.op:7s}] {self.sender_ip} ({self.sender_mac}) "
                f"{arrow} {self.target_ip} ({self.target_mac})")


class ArpTableEntry:
    """Single ARP cache entry."""
    def __init__(self, mac: str, first_seen: float, last_seen: float):
        self.mac, self.first_seen, self.last_seen = mac, first_seen, last_seen


class Alert:
    """Security alert raised by the detector."""
    ICONS = {"INFO": "ℹ", "WARNING": "⚠", "CRITICAL": "🚨"}
    def __init__(self, level: str, message: str, packet: ArpPacket):
        self.level, self.message, self.packet = level, message, packet
    def __str__(self) -> str:
        return (f"  {self.ICONS.get(self.level, '?')}  [{self.level}] "
                f"{self.message}\n       Packet: {self.packet}")


# ── detector engine ──────────────────────────────────────────────────────────

class ArpSpoofDetector:
    """Processes ARP packets and raises alerts for suspicious activity."""

    GRATUITOUS_WINDOW = 10.0   # seconds
    GRATUITOUS_THRESHOLD = 5   # max announcements per IP in window

    def __init__(self):
        self.table: Dict[str, ArpTableEntry] = {}        # IP → entry
        self.alerts: List[Alert] = []
        self.gratuitous_log: Dict[str, List[float]] = defaultdict(list)

    def process(self, pkt: ArpPacket) -> List[Alert]:
        """Process one ARP packet; return any new alerts."""
        new_alerts: List[Alert] = []

        # Check 1 – broadcast source MAC (always invalid)
        if pkt.sender_mac == BROADCAST_MAC:
            new_alerts.append(Alert(
                "CRITICAL",
                f"Broadcast source MAC in ARP {pkt.op} – always illegitimate.",
                pkt))

        # Check 2 – gratuitous ARP flood detection
        if self._is_gratuitous(pkt):
            self._record_gratuitous(pkt)
            count = len(self.gratuitous_log[pkt.sender_ip])
            if count >= self.GRATUITOUS_THRESHOLD:
                new_alerts.append(Alert(
                    "WARNING",
                    f"Gratuitous ARP flood: {count} announcements for "
                    f"{pkt.sender_ip} in {self.GRATUITOUS_WINDOW}s window.",
                    pkt))

        # Check 3 – MAC flapping / duplicate IP
        existing = self.table.get(pkt.sender_ip)
        if existing and existing.mac != pkt.sender_mac:
            new_alerts.append(Alert(
                "CRITICAL",
                f"MAC flap detected! {pkt.sender_ip} changed from "
                f"{existing.mac} → {pkt.sender_mac}.",
                pkt))

        # Update the ARP table
        if pkt.sender_ip in self.table:
            self.table[pkt.sender_ip].mac = pkt.sender_mac
            self.table[pkt.sender_ip].last_seen = pkt.timestamp
        else:
            self.table[pkt.sender_ip] = ArpTableEntry(
                pkt.sender_mac, pkt.timestamp, pkt.timestamp)

        self.alerts.extend(new_alerts)
        return new_alerts

    # ── helpers ──

    @staticmethod
    def _is_gratuitous(pkt: ArpPacket) -> bool:
        """A gratuitous ARP has sender_ip == target_ip."""
        return pkt.sender_ip == pkt.target_ip

    def _record_gratuitous(self, pkt: ArpPacket) -> None:
        cutoff = pkt.timestamp - self.GRATUITOUS_WINDOW
        log = self.gratuitous_log[pkt.sender_ip]
        self.gratuitous_log[pkt.sender_ip] = [
            t for t in log if t > cutoff
        ]
        self.gratuitous_log[pkt.sender_ip].append(pkt.timestamp)

    def print_table(self) -> None:
        """Pretty-print the current ARP table."""
        print(f"\n  {'IP Address':<18s} {'MAC Address':<20s} {'Last Seen':>10s}")
        print(f"  {'─'*18} {'─'*20} {'─'*10}")
        for ip in sorted(self.table):
            e = self.table[ip]
            print(f"  {ip:<18s} {e.mac:<20s} {e.last_seen:>10.1f}s")


# ── demo scenario ───────────────────────────────────────────────────────────

def demo() -> None:
    """Run an educational ARP spoofing scenario."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       ARP Spoof Detection Simulator – Demo Mode         ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\nScenario: small office LAN with 3 hosts and 1 attacker.\n")
    print("  Host A (workstation) : 192.168.1.10  /  AA:AA:AA:AA:AA:01")
    print("  Host B (server)      : 192.168.1.20  /  BB:BB:BB:BB:BB:02")
    print("  Gateway              : 192.168.1.1   /  CC:CC:CC:CC:CC:03")
    print("  Attacker             : 192.168.1.99  /  EE:EE:EE:EE:EE:99")

    P = ArpPacket
    packets = [
        # Normal traffic
        P("REQUEST", "AA:AA:AA:AA:AA:01", "192.168.1.10",
          BROADCAST_MAC, "192.168.1.1", 0.0),
        P("REPLY", "CC:CC:CC:CC:CC:03", "192.168.1.1",
          "AA:AA:AA:AA:AA:01", "192.168.1.10", 0.1),
        P("REQUEST", "BB:BB:BB:BB:BB:02", "192.168.1.20",
          BROADCAST_MAC, "192.168.1.10", 1.0),
        P("REPLY", "AA:AA:AA:AA:AA:01", "192.168.1.10",
          "BB:BB:BB:BB:BB:02", "192.168.1.20", 1.1),
        # Attacker announces itself (normal so far)
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.99",
          BROADCAST_MAC, "192.168.1.99", 5.0),
        # ATTACK – attacker claims to be the gateway
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "AA:AA:AA:AA:AA:01", "192.168.1.10", 10.0),
        # ATTACK – gratuitous ARP flood for gateway IP
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "EE:EE:EE:EE:EE:99", "192.168.1.1", 11.0),
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "EE:EE:EE:EE:EE:99", "192.168.1.1", 11.5),
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "EE:EE:EE:EE:EE:99", "192.168.1.1", 12.0),
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "EE:EE:EE:EE:EE:99", "192.168.1.1", 12.5),
        P("REPLY", "EE:EE:EE:EE:EE:99", "192.168.1.1",
          "EE:EE:EE:EE:EE:99", "192.168.1.1", 13.0),
        # Broadcast source MAC (always invalid)
        P("REPLY", BROADCAST_MAC, "192.168.1.50",
          "AA:AA:AA:AA:AA:01", "192.168.1.10", 20.0),
    ]

    detector = ArpSpoofDetector()

    for i, pkt in enumerate(packets, 1):
        print(f"\n─── Packet {i} (t={pkt.timestamp:.1f}s) ───")
        print(f"  {pkt}")
        alerts = detector.process(pkt)
        if alerts:
            for a in alerts:
                print(a)
        else:
            print("  ✓ No alerts.")

    print("\n" + "=" * 60)
    print("  Final ARP Table")
    print("=" * 60)
    detector.print_table()
    print(f"\n  Total alerts raised: {len(detector.alerts)}")

    print("\n── Takeaways ──")
    print("  • ARP has no authentication – any host can forge replies.")
    print("  • MAC flap and gratuitous ARP flood monitoring detects attacks.")
    print("  • Defences: DAI, static ARP entries, TLS/SSH to limit MITM.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate ARP spoof detection on a stream of ARP packets.")
    parser.add_argument("--file", metavar="PATH",
                        help="JSON file containing ARP packets to analyse")
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            packets = [ArpPacket(**e) for e in json.load(f)]
        detector = ArpSpoofDetector()
        for i, pkt in enumerate(packets, 1):
            print(f"\n─── Packet {i} (t={pkt.timestamp:.1f}s) ───")
            print(f"  {pkt}")
            for a in detector.process(pkt):
                print(a)
        detector.print_table()
        print(f"\n  Total alerts: {len(detector.alerts)}")
    else:
        demo()


if __name__ == "__main__":
    main()
