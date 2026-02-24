#!/usr/bin/env python3
"""
TCP State Machine Simulator
=============================
Walks through the 11 states of a TCP connection as defined in RFC 793,
printing each transition with the triggering event, the action taken,
and an ASCII state-diagram highlight.

TCP States modelled:
  CLOSED → LISTEN → SYN_RECEIVED → ESTABLISHED →
  FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED   (active close)
  ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED    (passive close)
  Plus: SYN_SENT, CLOSING

Each transition is driven by an *event* (e.g. "active OPEN", "rcv SYN")
and produces an *action* (e.g. "snd SYN", "snd ACK").

Concepts demonstrated:
  * Full TCP state diagram (RFC 793 Figure 6)
  * Three-way handshake and four-way teardown
  * Simultaneous open and simultaneous close paths
  * TIME_WAIT purpose (2 × MSL delay)

Usage:
    python tcp_state_machine.py                   # full lifecycle demo
    python tcp_state_machine.py --scenario client  # client-side only
    python tcp_state_machine.py --scenario server  # server-side only
    python tcp_state_machine.py --scenario simclose # simultaneous close
"""

import argparse
import textwrap

# ── Transition table ──────────────────────────────────────────────────
# Maps (current_state, event) → (next_state, action_description)

TRANSITIONS = {
    # Connection establishment
    ("CLOSED",       "passive OPEN"):  ("LISTEN",       "create TCB, wait for SYN"),
    ("CLOSED",       "active OPEN"):   ("SYN_SENT",     "snd SYN, seq=x"),
    ("LISTEN",       "rcv SYN"):       ("SYN_RECEIVED", "snd SYN,ACK  seq=y ack=x+1"),
    ("SYN_SENT",     "rcv SYN,ACK"):   ("ESTABLISHED",  "snd ACK  ack=y+1"),
    ("SYN_SENT",     "rcv SYN"):       ("SYN_RECEIVED", "snd SYN,ACK (simultaneous open)"),
    ("SYN_RECEIVED", "rcv ACK"):       ("ESTABLISHED",  "connection established"),
    # Data transfer (stays in ESTABLISHED)
    ("ESTABLISHED",  "snd DATA"):      ("ESTABLISHED",  "transmit segment(s)"),
    ("ESTABLISHED",  "rcv DATA"):      ("ESTABLISHED",  "deliver to application, snd ACK"),
    # Active close (initiator)
    ("ESTABLISHED",  "CLOSE"):         ("FIN_WAIT_1",   "snd FIN"),
    ("FIN_WAIT_1",   "rcv ACK"):       ("FIN_WAIT_2",   "FIN acknowledged"),
    ("FIN_WAIT_1",   "rcv FIN"):       ("CLOSING",      "snd ACK (simultaneous close)"),
    ("FIN_WAIT_2",   "rcv FIN"):       ("TIME_WAIT",    "snd ACK, start 2×MSL timer"),
    ("CLOSING",      "rcv ACK"):       ("TIME_WAIT",    "start 2×MSL timer"),
    ("TIME_WAIT",    "timeout 2MSL"):  ("CLOSED",       "delete TCB"),
    # Passive close (responder)
    ("ESTABLISHED",  "rcv FIN"):       ("CLOSE_WAIT",   "snd ACK"),
    ("CLOSE_WAIT",   "CLOSE"):         ("LAST_ACK",     "snd FIN"),
    ("LAST_ACK",     "rcv ACK"):       ("CLOSED",       "delete TCB"),
    # Edge: FIN_WAIT_1 can go straight to TIME_WAIT
    ("FIN_WAIT_1",   "rcv FIN,ACK"):   ("TIME_WAIT",    "snd ACK, start 2×MSL timer"),
}

ALL_STATES = [
    "CLOSED", "LISTEN", "SYN_SENT", "SYN_RECEIVED", "ESTABLISHED",
    "FIN_WAIT_1", "FIN_WAIT_2", "CLOSING", "TIME_WAIT",
    "CLOSE_WAIT", "LAST_ACK",
]

# ── Simulator class ───────────────────────────────────────────────────

class TCPStateMachine:
    """Simulate one side of a TCP connection."""

    def __init__(self, role="peer"):
        self.state = "CLOSED"
        self.role = role
        self.history = []

    def handle(self, event):
        key = (self.state, event)
        if key not in TRANSITIONS:
            print(f"  ✗ No transition from {self.state} on event '{event}' — ignored.")
            return
        new_state, action = TRANSITIONS[key]
        self._print_transition(event, new_state, action)
        self.history.append((self.state, event, new_state))
        self.state = new_state

    def _print_transition(self, event, new_state, action):
        arrow = self._state_bar(self.state, new_state)
        print(arrow)
        print(f"  Event : {event}")
        print(f"  Action: {action}")
        print(f"  {self.state}  ──▶  {new_state}")
        print()

    @staticmethod
    def _state_bar(current, next_st):
        """One-line bar highlighting current → next among all states."""
        parts = []
        for s in ALL_STATES:
            if s == current:
                parts.append(f"[{s}]")
            elif s == next_st:
                parts.append(f"»{s}«")
            else:
                parts.append(f" {s} ")
        return "  " + " → ".join(parts)


def section(title):
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {title}")
    print(f"{'─' * width}\n")

# ── Scenario runners ──────────────────────────────────────────────────

def run_client():
    """Active-open client: SYN → ESTABLISHED → active CLOSE."""
    section("Client (active open / active close)")
    c = TCPStateMachine("client")
    for evt in ("active OPEN", "rcv SYN,ACK", "snd DATA", "rcv DATA",
                "CLOSE", "rcv ACK", "rcv FIN", "timeout 2MSL"):
        c.handle(evt)
    return c


def run_server():
    """Passive-open server: LISTEN → ESTABLISHED → passive CLOSE."""
    section("Server (passive open / passive close)")
    s = TCPStateMachine("server")
    for evt in ("passive OPEN", "rcv SYN", "rcv ACK", "rcv DATA", "snd DATA",
                "rcv FIN", "CLOSE", "rcv ACK"):
        s.handle(evt)
    return s


def run_simultaneous_close():
    """Both sides send FIN at the same time → CLOSING path."""
    section("Simultaneous Close (both peers)")
    peer = TCPStateMachine("peer")
    peer.state = "ESTABLISHED"
    print(f"  (starting in ESTABLISHED)\n")
    for evt in ("CLOSE", "rcv FIN", "rcv ACK", "timeout 2MSL"):
        peer.handle(evt)
    return peer


def print_summary(machines):
    """Print the history of every machine as a compact trace."""
    section("Transition Summary")
    for m in machines:
        print(f"  [{m.role}]")
        for old, evt, new in m.history:
            print(f"    {old:<15} ──({evt})──▶ {new}")
        print()


def print_state_reference():
    """Print a quick reference of all states and their meaning."""
    info = {
        "CLOSED":       "No connection exists.",
        "LISTEN":       "Waiting for a connection request (server).",
        "SYN_SENT":     "SYN sent, waiting for SYN,ACK (client).",
        "SYN_RECEIVED": "SYN received and SYN,ACK sent; awaiting ACK.",
        "ESTABLISHED":  "Connection open; data transfer in progress.",
        "FIN_WAIT_1":   "FIN sent, waiting for ACK of FIN.",
        "FIN_WAIT_2":   "FIN acknowledged; waiting for peer's FIN.",
        "CLOSING":      "Both sides sent FIN before receiving ACK.",
        "TIME_WAIT":    "Waiting 2×MSL before fully closing.",
        "CLOSE_WAIT":   "Peer sent FIN; waiting for local CLOSE.",
        "LAST_ACK":     "FIN sent after CLOSE_WAIT; awaiting ACK.",
    }
    section("TCP State Quick Reference")
    for st in ALL_STATES:
        print(f"  {st:<15}  {info[st]}")
    print()

# ── Entry point ───────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(description="Simulate the TCP state machine.")
    p.add_argument(
        "--scenario", choices=["client", "server", "simclose", "all"],
        default="all",
        help="Which scenario to run (default: all)")
    return p


def main():
    args = build_parser().parse_args()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║         TCP State Machine — Educational Demo            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    machines = []

    if args.scenario in ("all", "client"):
        machines.append(run_client())
    if args.scenario in ("all", "server"):
        machines.append(run_server())
    if args.scenario in ("all", "simclose"):
        machines.append(run_simultaneous_close())

    if machines:
        print_summary(machines)

    print_state_reference()


if __name__ == "__main__":
    main()
