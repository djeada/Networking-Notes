#!/usr/bin/env python3
"""
Intrusion Detection System — Rule Matcher
===========================================
Simulates a signature-based Network IDS (like Snort or Suricata).  A set of
detection rules are defined in a simplified Snort-like syntax and then
evaluated against simulated network events.  When a rule matches, an alert
is generated with severity and description.

Concepts demonstrated:
* Signature-based detection: each rule is a pattern (protocol, IPs, ports,
  payload content) that characterizes known malicious traffic.
* Rule anatomy: action, protocol, src/dst addresses, src/dst ports, options
  (msg, content, sid, priority).
* Matching logic: a packet must satisfy ALL fields in the rule to trigger.
* Limitations: signature-based IDS cannot detect zero-day attacks or
  encrypted traffic without decryption.

Usage:
    python ids_rule_matcher.py                       # runs built-in demo
    python ids_rule_matcher.py --verbose             # extra match details
    python ids_rule_matcher.py --rule-file rules.txt # load custom rules
"""

import argparse
import re
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class IDSRule:
    sid: int
    action: str          # alert, log, drop
    protocol: str        # tcp, udp, icmp, any
    src_ip: str          # CIDR or "any"
    src_port: str        # port number, range, or "any"
    dst_ip: str
    dst_port: str
    msg: str = ""
    content: List[str] = field(default_factory=list)
    priority: int = 3

    def __str__(self):
        return (f'[SID:{self.sid}] {self.action} {self.protocol} '
                f'{self.src_ip}:{self.src_port} -> {self.dst_ip}:{self.dst_port} '
                f'(msg:"{self.msg}"; priority:{self.priority})')


@dataclass
class Packet:
    protocol: str
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    payload: str = ""
    timestamp: str = ""

    def __str__(self):
        return (f'{self.timestamp} {self.protocol.upper()} '
                f'{self.src_ip}:{self.src_port} -> {self.dst_ip}:{self.dst_port} '
                f'len={len(self.payload)}')


def ip_matches(rule_ip: str, packet_ip: str) -> bool:
    if rule_ip == "any":
        return True
    if "/" in rule_ip:
        from ipaddress import ip_address, ip_network
        return ip_address(packet_ip) in ip_network(rule_ip, strict=False)
    return rule_ip == packet_ip


def port_matches(rule_port: str, packet_port: int) -> bool:
    if rule_port == "any":
        return True
    if ":" in rule_port:
        lo, hi = rule_port.split(":")
        return int(lo) <= packet_port <= int(hi)
    return int(rule_port) == packet_port


def match_rule(rule: IDSRule, pkt: Packet, verbose: bool = False) -> bool:
    checks = []

    proto_ok = rule.protocol == "any" or rule.protocol == pkt.protocol
    checks.append(("protocol", proto_ok))

    src_ip_ok = ip_matches(rule.src_ip, pkt.src_ip)
    checks.append(("src_ip", src_ip_ok))

    src_port_ok = port_matches(rule.src_port, pkt.src_port)
    checks.append(("src_port", src_port_ok))

    dst_ip_ok = ip_matches(rule.dst_ip, pkt.dst_ip)
    checks.append(("dst_ip", dst_ip_ok))

    dst_port_ok = port_matches(rule.dst_port, pkt.dst_port)
    checks.append(("dst_port", dst_port_ok))

    content_ok = all(c.lower() in pkt.payload.lower() for c in rule.content)
    checks.append(("content", content_ok))

    matched = all(ok for _, ok in checks)
    if verbose:
        detail = ", ".join(f"{name}={'✓' if ok else '✗'}" for name, ok in checks)
        status = "MATCH" if matched else "no match"
        print(f"      SID {rule.sid}: {detail} → {status}")
    return matched


PRIORITY_LABELS = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}


def default_rules() -> List[IDSRule]:
    return [
        IDSRule(1001, "alert", "tcp", "any", "any", "any", "80",
                msg="HTTP GET flood attempt",
                content=["GET / HTTP"], priority=2),
        IDSRule(1002, "alert", "tcp", "any", "any", "any", "22",
                msg="SSH brute-force attempt",
                content=["SSH-"], priority=1),
        IDSRule(1003, "alert", "tcp", "any", "any", "any", "any",
                msg="SQL injection probe",
                content=["' OR '1'='1"], priority=1),
        IDSRule(1004, "alert", "icmp", "any", "any", "any", "any",
                msg="ICMP ping sweep",
                content=[], priority=3),
        IDSRule(1005, "alert", "udp", "any", "any", "any", "53",
                msg="DNS zone transfer attempt",
                content=["AXFR"], priority=1),
        IDSRule(1006, "alert", "tcp", "any", "any", "10.0.0.0/8", "3306",
                msg="External access to MySQL",
                content=[], priority=2),
        IDSRule(1007, "alert", "tcp", "any", "any", "any", "443",
                msg="Suspicious TLS payload keyword",
                content=["<script>"], priority=2),
    ]


def sample_traffic() -> List[Packet]:
    return [
        Packet("tcp", "192.168.1.50", 49812, "10.0.1.10", 80,
               "GET / HTTP/1.1\r\nHost: example.com", "12:00:01"),
        Packet("tcp", "203.0.113.5", 55321, "10.0.1.20", 22,
               "SSH-2.0-OpenSSH_8.9", "12:00:02"),
        Packet("tcp", "198.51.100.7", 50100, "10.0.1.10", 80,
               "GET /login?user=admin' OR '1'='1--", "12:00:03"),
        Packet("icmp", "172.16.0.1", 0, "10.0.1.255", 0,
               "", "12:00:04"),
        Packet("udp", "198.51.100.9", 12345, "10.0.1.5", 53,
               "AXFR example.com", "12:00:05"),
        Packet("tcp", "10.0.2.15", 60100, "10.0.1.30", 443,
               "TLS data normal traffic", "12:00:06"),
        Packet("tcp", "192.168.1.100", 61234, "10.0.1.40", 3306,
               "SELECT * FROM users;", "12:00:07"),
        Packet("tcp", "203.0.113.11", 44000, "10.0.1.10", 443,
               "POST /api <script>alert('xss')</script>", "12:00:08"),
        Packet("udp", "10.0.2.20", 5000, "10.0.1.5", 123,
               "NTP sync", "12:00:09"),
        Packet("tcp", "192.168.1.50", 49820, "10.0.1.10", 80,
               "POST /upload HTTP/1.1\r\nContent-Type: multipart", "12:00:10"),
    ]


def demo(verbose: bool):
    print("=" * 65)
    print("  Intrusion Detection System — Rule Matcher")
    print("=" * 65)

    rules = default_rules()
    print(f"\n  Loaded {len(rules)} detection rules:")
    for r in rules:
        print(f"    {r}")

    packets = sample_traffic()
    print(f"\n  Processing {len(packets)} packets...\n")

    alerts = []
    for pkt in packets:
        print(f"  ► Packet: {pkt}")
        matched_any = False
        for rule in rules:
            if match_rule(rule, pkt, verbose=verbose):
                sev = PRIORITY_LABELS.get(rule.priority, "???")
                alert_msg = f'    🚨 ALERT [{sev}] SID:{rule.sid} — {rule.msg}'
                print(alert_msg)
                alerts.append((pkt, rule))
                matched_any = True
        if not matched_any:
            print("    ✓ No rules matched — traffic appears benign.")
        print()

    # Summary
    print(f"{'═' * 65}")
    print(f"  Detection Summary")
    print(f"{'═' * 65}")
    print(f"  Packets analysed : {len(packets)}")
    print(f"  Alerts generated : {len(alerts)}")
    by_sev = {1: 0, 2: 0, 3: 0}
    for _, r in alerts:
        by_sev[r.priority] = by_sev.get(r.priority, 0) + 1
    for p in sorted(by_sev):
        print(f"    {PRIORITY_LABELS[p]:<8}: {by_sev[p]}")
    print(f"\n  Note: Signature-based IDS can only detect KNOWN attack")
    print(f"  patterns. Zero-day exploits and encrypted payloads require")
    print(f"  anomaly-based detection or TLS inspection.")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple IDS rule matcher simulator")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-field match details for every rule check")
    parser.add_argument("--rule-file", type=str, default=None,
                        help="Path to a file with custom rules (not implemented in demo)")
    args = parser.parse_args()
    demo(verbose=args.verbose)
