"""
tcp_client.py - Simple TCP Client

Demonstrates how a TCP client works:
  1. Creates a TCP socket (SOCK_STREAM).
  2. Connects to a remote server using the TCP 3-way handshake.
  3. Sends data reliably over the established connection.
  4. Receives the server's response.
  5. Closes the connection gracefully.

TCP (Transmission Control Protocol) is a connection-oriented protocol that
provides reliable, ordered, and error-checked delivery of data between
applications. It operates at the Transport Layer (Layer 4) of the OSI model.

Usage:
    python tcp_client.py [-s HOST] [-p PORT] [-m MESSAGE]
"""

import argparse
import socket
import sys


def create_tcp_client(host, port, message):
    """Connect to a TCP server, send a message, and print the response.

    Args:
        host: The server hostname or IP address to connect to.
        port: The server port number.
        message: The string message to send to the server.
    """
    # AF_INET  = IPv4 address family
    # SOCK_STREAM = TCP (reliable, connection-oriented byte stream)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Set a timeout so we don't hang forever if the server is unreachable
        sock.settimeout(10.0)

        print(f"[*] Connecting to {host}:{port} ...")
        try:
            # connect() initiates the TCP 3-way handshake (SYN → SYN-ACK → ACK)
            sock.connect((host, port))
            print(f"[+] Connected to {host}:{port}")
        except socket.timeout:
            print(f"[-] Connection to {host}:{port} timed out.")
            return
        except ConnectionRefusedError:
            print(f"[-] Connection refused by {host}:{port}. Is the server running?")
            return
        except OSError as exc:
            print(f"[-] Could not connect to {host}:{port}: {exc}")
            return

        # Encode the string to bytes before sending — TCP works with raw bytes
        data = message.encode("utf-8")
        print(f"[*] Sending: {message!r}")
        sock.sendall(data)  # sendall() ensures the entire buffer is transmitted

        try:
            # Receive up to 4096 bytes from the server
            response = sock.recv(4096)
            if response:
                print(f"[+] Received: {response.decode('utf-8', errors='replace')!r}")
            else:
                print("[*] Server closed the connection without sending data.")
        except socket.timeout:
            print("[-] Timed out waiting for a response from the server.")

    # Exiting the 'with' block automatically closes the socket, which
    # triggers the TCP connection teardown (FIN → ACK → FIN → ACK).
    print("[*] Connection closed.")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple TCP client")
    parser.add_argument(
        "-s", "--host",
        default="127.0.0.1",
        help="Server hostname or IP (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=9999,
        help="Server port (default: 9999)",
    )
    parser.add_argument(
        "-m", "--message",
        default="Hello, TCP Server!",
        help="Message to send (default: 'Hello, TCP Server!')",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    create_tcp_client(args.host, args.port, args.message)
