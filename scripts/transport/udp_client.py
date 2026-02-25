"""
udp_client.py - Simple UDP Client

Demonstrates how a UDP client works:
  1. Creates a UDP socket (SOCK_DGRAM).
  2. Sends a datagram to the server — no connection is established first.
  3. Waits for a response with a configurable timeout.

UDP (User Datagram Protocol) is a connectionless protocol that offers:
  - No handshake — data is sent immediately.
  - No guaranteed delivery — datagrams may be lost in transit.
  - No ordering — datagrams may arrive out of order.
  - Low overhead — ideal for latency-sensitive applications (DNS, VoIP, gaming).

Because there is no connection, the client must use sendto() (specifying the
destination each time) and recvfrom() (which also returns the sender address).

Usage:
    python udp_client.py [-s HOST] [-p PORT] [-m MESSAGE] [-t TIMEOUT]
"""

import argparse
import socket
import sys


def create_udp_client(host, port, message, timeout):
    """Send a UDP datagram and wait for a response.

    Args:
        host: The server hostname or IP address.
        port: The server port number.
        message: The string message to send.
        timeout: Seconds to wait for a response before giving up.
    """
    # AF_INET    = IPv4
    # SOCK_DGRAM = UDP (connectionless datagrams)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Set a receive timeout so we don't block forever
        sock.settimeout(timeout)

        server_addr = (host, port)
        data = message.encode("utf-8")

        # sendto() delivers the datagram without establishing a connection.
        # Unlike TCP, there is no guarantee the server will receive it.
        print(f"[*] Sending to {host}:{port}: {message!r}")
        bytes_sent = sock.sendto(data, server_addr)
        print(f"[*] Sent {bytes_sent} bytes")

        try:
            # recvfrom() returns (data, (sender_ip, sender_port))
            response, sender = sock.recvfrom(4096)
            print(f"[+] Received from {sender[0]}:{sender[1]}: "
                  f"{response.decode('utf-8', errors='replace')!r}")
        except socket.timeout:
            print(f"[-] No response received within {timeout}s. "
                  "The datagram may have been lost (this is normal for UDP).")

    print("[*] Done.")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple UDP client")
    parser.add_argument(
        "-s", "--host",
        default="127.0.0.1",
        help="Server hostname or IP (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=9998,
        help="Server port (default: 9998)",
    )
    parser.add_argument(
        "-m", "--message",
        default="Hello, UDP Server!",
        help="Message to send (default: 'Hello, UDP Server!')",
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=5.0,
        help="Response timeout in seconds (default: 5.0)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    create_udp_client(args.host, args.port, args.message, args.timeout)
