"""
udp_server.py - Simple UDP Server

Demonstrates how a UDP server works:
  1. Creates a UDP socket and binds it to an address and port.
  2. Waits for incoming datagrams (no listen/accept — UDP is connectionless).
  3. Processes each datagram independently and optionally sends a response.

Key differences from a TCP server:
  - No listen() or accept() calls — there are no connections to manage.
  - Each recvfrom() returns the sender's address so we know where to reply.
  - The server can handle "multiple clients" naturally because every datagram
    is independent; there is no per-client state or connection object.
  - Datagrams may arrive out of order or not at all — the application must
    handle these cases if reliability is needed.

Usage:
    python udp_server.py [-b BIND_ADDRESS] [-p PORT]
"""

import argparse
import socket
import sys


def run_udp_server(bind_address, port):
    """Start a UDP server that receives datagrams and sends responses.

    Args:
        bind_address: The IP address to bind to.
        port: The port number to bind to.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((bind_address, port))
        print(f"[*] UDP server listening on {bind_address or '0.0.0.0'}:{port}")
        print("[*] Press Ctrl+C to stop the server.\n")

        try:
            while True:
                # recvfrom() blocks until a datagram arrives.
                # Returns (bytes, (sender_ip, sender_port)).
                data, client_addr = sock.recvfrom(4096)
                message = data.decode("utf-8", errors="replace")
                print(f"[+] Received from {client_addr[0]}:{client_addr[1]}: {message!r}")

                # Send a response back to the client
                response = f"Echo: {message}"
                sock.sendto(response.encode("utf-8"), client_addr)
                print(f"[*] Sent response to {client_addr[0]}:{client_addr[1]}\n")
        except KeyboardInterrupt:
            print("\n[*] Server shutting down.")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple UDP server")
    parser.add_argument(
        "-b", "--bind",
        default="127.0.0.1",
        help="Address to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=9998,
        help="Port to listen on (default: 9998)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    run_udp_server(args.bind, args.port)
