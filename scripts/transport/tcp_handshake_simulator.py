"""
tcp_handshake_simulator.py - TCP 3-Way Handshake & Teardown Simulator

Simulates and visualizes the TCP connection lifecycle:

  Connection establishment (3-way handshake):
      Client  ──  SYN (seq=x)           ──▶  Server
      Client  ◀──  SYN-ACK (seq=y, ack=x+1) ──  Server
      Client  ──  ACK (seq=x+1, ack=y+1) ──▶  Server

  Data transfer (simplified):
      Client  ──  PSH-ACK (seq, ack, payload) ──▶  Server
      Client  ◀──  ACK (seq, ack)                ──  Server

  Connection teardown (4-way):
      Client  ──  FIN-ACK (seq, ack)     ──▶  Server
      Client  ◀──  ACK (seq, ack)         ──  Server
      Client  ◀──  FIN-ACK (seq, ack)     ──  Server
      Client  ──  ACK (seq, ack)         ──▶  Server

This is a purely educational simulation — no actual network connections are
made.  It uses classes to model TCP segments and endpoints so you can see
how sequence/acknowledgment numbers evolve throughout a connection.

Usage:
    python tcp_handshake_simulator.py
"""

import random


# ---------------------------------------------------------------------------
# TCP flags represented as human-readable strings
# ---------------------------------------------------------------------------
class TCPFlags:
    """Named constants for common TCP flag combinations."""
    SYN = "SYN"
    SYN_ACK = "SYN-ACK"
    ACK = "ACK"
    PSH_ACK = "PSH-ACK"
    FIN_ACK = "FIN-ACK"


# ---------------------------------------------------------------------------
# TCP Segment
# ---------------------------------------------------------------------------
class TCPSegment:
    """Represents a single TCP segment with header fields.

    Attributes:
        src_port: Source port number.
        dst_port: Destination port number.
        seq_num: Sequence number.
        ack_num: Acknowledgment number.
        flags: String describing the TCP flags set (e.g., "SYN", "ACK").
        payload: Optional payload data (bytes or string).
    """

    def __init__(self, src_port, dst_port, seq_num, ack_num, flags, payload=""):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = flags
        self.payload = payload

    def __repr__(self):
        parts = [
            f"[{self.flags}]",
            f"seq={self.seq_num}",
            f"ack={self.ack_num}",
            f"src_port={self.src_port}",
            f"dst_port={self.dst_port}",
        ]
        if self.payload:
            parts.append(f"payload={self.payload!r}")
        return "  ".join(parts)


# ---------------------------------------------------------------------------
# TCP Endpoint (client or server)
# ---------------------------------------------------------------------------
class TCPEndpoint:
    """Models one side of a TCP connection.

    Tracks the endpoint's current sequence number and the next expected
    acknowledgment number from the peer.

    Attributes:
        name: Human-readable label (e.g., "Client" or "Server").
        port: Port number for this endpoint.
        seq_num: Current sequence number.
        ack_num: Next expected sequence number from the peer.
    """

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.seq_num = 0
        self.ack_num = 0

    def set_initial_seq(self, isn):
        """Set the Initial Sequence Number (ISN) chosen during the handshake."""
        self.seq_num = isn


# ---------------------------------------------------------------------------
# Simulation helpers
# ---------------------------------------------------------------------------
def _arrow(sender, receiver, segment):
    """Return a formatted string showing a segment traveling between endpoints."""
    direction = f"{sender.name:<8} ──▶ {receiver.name:<8}"
    return f"  {direction}  {segment}"


def simulate_handshake(client, server):
    """Simulate the TCP 3-way handshake.

    Steps:
        1. Client → Server: SYN with client's ISN.
        2. Server → Client: SYN-ACK with server's ISN, ack = client ISN + 1.
        3. Client → Server: ACK, ack = server ISN + 1.

    Returns:
        A list of (description, formatted_line) tuples for display.
    """
    events = []

    # --- Step 1: Client sends SYN ---
    client_isn = client.seq_num
    syn = TCPSegment(
        src_port=client.port,
        dst_port=server.port,
        seq_num=client_isn,
        ack_num=0,
        flags=TCPFlags.SYN,
    )
    events.append(("Step 1 – Client sends SYN", _arrow(client, server, syn)))
    # After sending SYN the client's seq advances by 1 (SYN consumes a seq #)
    client.seq_num = client_isn + 1

    # --- Step 2: Server sends SYN-ACK ---
    server_isn = server.seq_num
    server.ack_num = client.seq_num  # expects next byte from client
    syn_ack = TCPSegment(
        src_port=server.port,
        dst_port=client.port,
        seq_num=server_isn,
        ack_num=server.ack_num,
        flags=TCPFlags.SYN_ACK,
    )
    events.append(("Step 2 – Server sends SYN-ACK", _arrow(server, client, syn_ack)))
    server.seq_num = server_isn + 1

    # --- Step 3: Client sends ACK ---
    client.ack_num = server.seq_num
    ack = TCPSegment(
        src_port=client.port,
        dst_port=server.port,
        seq_num=client.seq_num,
        ack_num=client.ack_num,
        flags=TCPFlags.ACK,
    )
    events.append(("Step 3 – Client sends ACK", _arrow(client, server, ack)))
    # ACK alone does not consume a sequence number

    return events


def simulate_data_transfer(client, server, message):
    """Simulate a simple data exchange after the handshake.

    The client sends *message* to the server, and the server acknowledges it.

    Returns:
        A list of (description, formatted_line) tuples.
    """
    events = []
    payload_len = len(message.encode("utf-8"))

    # Client sends data
    psh = TCPSegment(
        src_port=client.port,
        dst_port=server.port,
        seq_num=client.seq_num,
        ack_num=client.ack_num,
        flags=TCPFlags.PSH_ACK,
        payload=message,
    )
    events.append((f"Client sends {payload_len} bytes of data",
                    _arrow(client, server, psh)))
    client.seq_num += payload_len

    # Server acknowledges
    server.ack_num = client.seq_num
    ack = TCPSegment(
        src_port=server.port,
        dst_port=client.port,
        seq_num=server.seq_num,
        ack_num=server.ack_num,
        flags=TCPFlags.ACK,
    )
    events.append(("Server acknowledges data", _arrow(server, client, ack)))

    return events


def simulate_teardown(client, server):
    """Simulate the TCP 4-way connection teardown.

    Steps:
        1. Client → Server: FIN-ACK
        2. Server → Client: ACK
        3. Server → Client: FIN-ACK
        4. Client → Server: ACK

    Returns:
        A list of (description, formatted_line) tuples.
    """
    events = []

    # --- Step 1: Client sends FIN ---
    fin1 = TCPSegment(
        src_port=client.port,
        dst_port=server.port,
        seq_num=client.seq_num,
        ack_num=client.ack_num,
        flags=TCPFlags.FIN_ACK,
    )
    events.append(("Step 1 – Client sends FIN-ACK", _arrow(client, server, fin1)))
    client.seq_num += 1  # FIN consumes a sequence number

    # --- Step 2: Server acknowledges client's FIN ---
    server.ack_num = client.seq_num
    ack1 = TCPSegment(
        src_port=server.port,
        dst_port=client.port,
        seq_num=server.seq_num,
        ack_num=server.ack_num,
        flags=TCPFlags.ACK,
    )
    events.append(("Step 2 – Server sends ACK", _arrow(server, client, ack1)))

    # --- Step 3: Server sends its own FIN ---
    fin2 = TCPSegment(
        src_port=server.port,
        dst_port=client.port,
        seq_num=server.seq_num,
        ack_num=server.ack_num,
        flags=TCPFlags.FIN_ACK,
    )
    events.append(("Step 3 – Server sends FIN-ACK", _arrow(server, client, fin2)))
    server.seq_num += 1

    # --- Step 4: Client acknowledges server's FIN ---
    client.ack_num = server.seq_num
    ack2 = TCPSegment(
        src_port=client.port,
        dst_port=server.port,
        seq_num=client.seq_num,
        ack_num=client.ack_num,
        flags=TCPFlags.ACK,
    )
    events.append(("Step 4 – Client sends ACK", _arrow(client, server, ack2)))

    return events


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------
def print_events(title, events):
    """Pretty-print a list of simulation events."""
    width = 72
    print("=" * width)
    print(f"  {title}")
    print("=" * width)
    for description, line in events:
        print(f"\n  >> {description}")
        print(f"     {line}")
    print()


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Choose random ISNs to mimic real TCP behavior
    client_isn = random.randint(1000, 9999)
    server_isn = random.randint(1000, 9999)

    client = TCPEndpoint("Client", port=54321)
    server = TCPEndpoint("Server", port=80)

    client.set_initial_seq(client_isn)
    server.set_initial_seq(server_isn)

    print(f"\n  Initial Sequence Numbers:")
    print(f"    Client ISN = {client_isn}")
    print(f"    Server ISN = {server_isn}\n")

    # 1. Connection establishment
    handshake_events = simulate_handshake(client, server)
    print_events("TCP 3-Way Handshake (Connection Establishment)", handshake_events)

    # 2. Data transfer
    data_events = simulate_data_transfer(client, server, "Hello!")
    print_events("Data Transfer", data_events)

    # 3. Connection teardown
    teardown_events = simulate_teardown(client, server)
    print_events("TCP 4-Way Teardown (Connection Termination)", teardown_events)

    print("=" * 72)
    print("  Simulation complete.")
    print("=" * 72)
