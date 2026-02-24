#!/usr/bin/env python3
"""Simple Firewall Simulator — Educational Networking Script

Simulates a stateless packet-filtering firewall.  Key concepts:

  • **Rules** are evaluated top-to-bottom; the first match wins.
  • Each rule specifies an *action* (ALLOW / DENY) and match criteria
    (source IP, destination IP, destination port, protocol).
  • A **default policy** applies when no rule matches (typically DENY).
  • Wildcards ("*") in a rule field match anything.

The simulator processes a list of simulated packets and prints a
colour-coded verdict for each one, explaining *which* rule matched.

Usage:
    python simple_firewall_simulator.py          # run the built-in demo
"""

from __future__ import annotations

import dataclasses
import ipaddress
import textwrap
from typing import List

# ── Data structures ──────────────────────────────────────────────────────

@dataclasses.dataclass
class FirewallRule:
    """A single packet-filter rule."""
    action: str          # "ALLOW" or "DENY"
    protocol: str        # "TCP", "UDP", "ICMP", or "*"
    src_ip: str          # CIDR like "10.0.0.0/8", single IP, or "*"
    dst_ip: str          # same as src_ip
    dst_port: str        # port number, range "80-443", or "*"
    description: str = ""

    def matches(self, packet: "Packet") -> bool:
        """Return True if this rule matches *packet*."""
        if self.protocol != "*" and self.protocol.upper() != packet.protocol.upper():
            return False
        if not self._ip_matches(self.src_ip, packet.src_ip):
            return False
        if not self._ip_matches(self.dst_ip, packet.dst_ip):
            return False
        if not self._port_matches(self.dst_port, packet.dst_port):
            return False
        return True

    # -- helpers --

    @staticmethod
    def _ip_matches(rule_ip: str, packet_ip: str) -> bool:
        if rule_ip == "*":
            return True
        try:
            network = ipaddress.ip_network(rule_ip, strict=False)
            return ipaddress.ip_address(packet_ip) in network
        except ValueError:
            return rule_ip == packet_ip

    @staticmethod
    def _port_matches(rule_port: str, packet_port: int) -> bool:
        if rule_port == "*":
            return True
        if "-" in str(rule_port):
            lo, hi = rule_port.split("-")
            return int(lo) <= packet_port <= int(hi)
        return int(rule_port) == packet_port


@dataclasses.dataclass
class Packet:
    """A simulated network packet."""
    protocol: str
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    description: str = ""


class Firewall:
    """A simple ordered rule-set firewall with a default policy."""

    def __init__(self, default_policy: str = "DENY") -> None:
        self.rules: List[FirewallRule] = []
        self.default_policy = default_policy.upper()

    def add_rule(self, rule: FirewallRule) -> None:
        self.rules.append(rule)

    def evaluate(self, packet: Packet) -> tuple[str, str]:
        """Return (action, reason) for the given packet."""
        for idx, rule in enumerate(self.rules, start=1):
            if rule.matches(packet):
                reason = f"Rule #{idx}: {rule.action} — {rule.description or 'no description'}"
                return rule.action.upper(), reason
        return self.default_policy, f"Default policy: {self.default_policy}"

    def print_rules(self) -> None:
        print("── Firewall Rule Set ──")
        print(f"  Default policy: {self.default_policy}\n")
        header = f"  {'#':<4} {'Action':<7} {'Proto':<6} {'Src IP':<18} {'Dst IP':<18} {'DPort':<10} Description"
        print(header)
        print("  " + "─" * (len(header) - 2))
        for i, r in enumerate(self.rules, 1):
            print(
                f"  {i:<4} {r.action:<7} {r.protocol:<6} {r.src_ip:<18} "
                f"{r.dst_ip:<18} {r.dst_port:<10} {r.description}"
            )
        print()


# ── Demo ─────────────────────────────────────────────────────────────────

def run_demo() -> None:
    print("=" * 70)
    print(" Simple Firewall Simulator — Demo")
    print("=" * 70)
    print()
    print(textwrap.dedent("""\
        This simulator shows how a stateless packet-filtering firewall works.
        Rules are checked top-to-bottom; the FIRST matching rule decides the
        packet's fate.  If no rule matches the default policy applies.
    """))

    # Build firewall
    fw = Firewall(default_policy="DENY")
    fw.add_rule(FirewallRule("ALLOW", "TCP",  "*",            "*", "80",     "Allow HTTP"))
    fw.add_rule(FirewallRule("ALLOW", "TCP",  "*",            "*", "443",    "Allow HTTPS"))
    fw.add_rule(FirewallRule("ALLOW", "TCP",  "10.0.0.0/8",  "*", "22",     "Allow SSH from internal"))
    fw.add_rule(FirewallRule("DENY",  "TCP",  "*",            "*", "22",     "Block SSH from external"))
    fw.add_rule(FirewallRule("ALLOW", "UDP",  "*",            "*", "53",     "Allow DNS"))
    fw.add_rule(FirewallRule("ALLOW", "ICMP", "10.0.0.0/8",  "*", "*",      "Allow ICMP from internal"))
    fw.add_rule(FirewallRule("DENY",  "TCP",  "*",            "*", "23",     "Block Telnet everywhere"))
    fw.add_rule(FirewallRule("ALLOW", "TCP",  "192.168.1.0/24", "*", "3306", "Allow MySQL from LAN"))

    fw.print_rules()

    # Simulated packets
    packets = [
        Packet("TCP",  "203.0.113.5",  "10.0.0.50", 49152, 80,   "External HTTP request"),
        Packet("TCP",  "203.0.113.5",  "10.0.0.50", 49153, 443,  "External HTTPS request"),
        Packet("TCP",  "10.0.1.20",    "10.0.0.50", 49154, 22,   "Internal SSH"),
        Packet("TCP",  "203.0.113.5",  "10.0.0.50", 49155, 22,   "External SSH attempt"),
        Packet("UDP",  "10.0.1.20",    "8.8.8.8",   49156, 53,   "DNS query"),
        Packet("ICMP", "10.0.1.20",    "10.0.0.1",  0,     0,    "Internal ping"),
        Packet("ICMP", "203.0.113.5",  "10.0.0.1",  0,     0,    "External ping"),
        Packet("TCP",  "203.0.113.5",  "10.0.0.50", 49157, 23,   "Telnet from outside"),
        Packet("TCP",  "192.168.1.10", "10.0.0.50", 49158, 3306, "MySQL from LAN"),
        Packet("TCP",  "172.16.0.5",   "10.0.0.50", 49159, 3306, "MySQL from other subnet"),
        Packet("TCP",  "10.0.1.20",    "10.0.0.50", 49160, 8080, "Internal request on port 8080"),
    ]

    print("── Processing Packets ──\n")
    allowed = 0
    denied = 0
    for pkt in packets:
        action, reason = fw.evaluate(pkt)
        symbol = "✅" if action == "ALLOW" else "❌"
        print(f"  {symbol} [{action:<5}] {pkt.protocol:<5} {pkt.src_ip:<16} → "
              f"{pkt.dst_ip:<16}:{pkt.dst_port:<5}  {pkt.description}")
        print(f"           Matched: {reason}")
        if action == "ALLOW":
            allowed += 1
        else:
            denied += 1

    print(f"\n── Summary: {allowed} allowed, {denied} denied out of {len(packets)} packets ──")

    print()
    print("  📝 Key takeaways:")
    print("     • Rule ORDER matters — SSH is allowed from 10.0.0.0/8 (rule 3)")
    print("       but denied for everyone else (rule 4).")
    print("     • A default DENY policy ensures anything not explicitly")
    print("       allowed is blocked (defence in depth).")
    print("     • Real firewalls also track connection STATE (stateful inspection).")


if __name__ == "__main__":
    run_demo()
