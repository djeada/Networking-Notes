"""
tcp_server.py - Simple TCP Server

Demonstrates how a TCP server works:
  1. Creates a TCP socket and binds it to an address and port.
  2. Listens for incoming connection requests.
  3. Accepts connections one at a time (sequential / iterative server).
  4. Receives data from the client, processes it, and sends a response.
  5. Closes the client connection and waits for the next one.

Key concepts:
  - SO_REUSEADDR allows the server to rebind to a port that is still in the
    TIME_WAIT state after a previous run, avoiding "Address already in use".
  - listen(backlog) sets the maximum number of queued connections.
  - accept() blocks until a client connects, then returns a *new* socket
    dedicated to that client conversation.

Usage:
    python tcp_server.py [-b BIND_ADDRESS] [-p PORT]
"""

import argparse
import socket
import sys


def run_tcp_server(bind_address, port):
    """Start a TCP server that handles clients sequentially.

    Args:
        bind_address: The IP address to bind to ('' or '0.0.0.0' for all interfaces).
        port: The port number to listen on.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # Allow immediate reuse of the address after the server restarts.
        # Without this, the OS may keep the port in TIME_WAIT for up to 2×MSL.
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_sock.bind((bind_address, port))

        # backlog=5 means the OS will queue up to 5 pending connections
        server_sock.listen(5)
        print(f"[*] TCP server listening on {bind_address or '0.0.0.0'}:{port}")
        print("[*] Press Ctrl+C to stop the server.\n")

        try:
            while True:
                # accept() blocks until a client connects
                client_sock, client_addr = server_sock.accept()
                with client_sock:
                    print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")
                    handle_client(client_sock, client_addr)
        except KeyboardInterrupt:
            print("\n[*] Server shutting down.")


def handle_client(client_sock, client_addr):
    """Receive data from a single client and send a response.

    This simple handler reads one message, echoes it back with a prefix,
    and then closes the connection.

    Args:
        client_sock: The connected client socket.
        client_addr: Tuple of (ip, port) identifying the client.
    """
    try:
        data = client_sock.recv(4096)
        if not data:
            print(f"[*] {client_addr} disconnected without sending data.")
            return

        message = data.decode("utf-8", errors="replace")
        print(f"[*] Received from {client_addr}: {message!r}")

        # Build and send a response
        response = f"Echo: {message}"
        client_sock.sendall(response.encode("utf-8"))
        print(f"[*] Sent response to {client_addr}")
    except ConnectionResetError:
        print(f"[-] Connection reset by {client_addr}")
    except OSError as exc:
        print(f"[-] Error handling {client_addr}: {exc}")
    finally:
        print(f"[*] Closing connection to {client_addr}\n")


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple TCP server")
    parser.add_argument(
        "-b", "--bind",
        default="127.0.0.1",
        help="Address to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=9999,
        help="Port to listen on (default: 9999)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    run_tcp_server(args.bind, args.port)
