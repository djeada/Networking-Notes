#!/usr/bin/env python3
"""Network Chat Application — Educational Networking Script

A simple TCP-based chat system with **server** and **client** modes.

Server:
  • Listens on a configurable host/port.
  • Accepts multiple simultaneous connections using threads.
  • Broadcasts every message to all connected clients.
  • Demonstrates: socket binding, listening, accepting, threading.

Client:
  • Connects to the server and lets the user send messages from stdin.
  • A background thread listens for broadcasts from the server.
  • Demonstrates: socket connecting, send/recv, concurrent I/O.

Usage:
    # Terminal 1 — start the server
    python network_chat_app.py server --port 9000

    # Terminal 2 — connect a client
    python network_chat_app.py client --port 9000

    # Terminal 3 — connect another client
    python network_chat_app.py client --port 9000 --nick Bob

Protocol (kept deliberately simple for educational purposes):
    • Messages are UTF-8 text terminated by a newline ('\\n').
    • No length prefix — we use makefile() for line-oriented I/O.
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading

# ── Server ───────────────────────────────────────────────────────────────

class ChatServer:
    """Multi-client TCP chat server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9000) -> None:
        self.host = host
        self.port = port
        # Map of socket → nickname
        self.clients: dict[socket.socket, str] = {}
        self.lock = threading.Lock()

    def broadcast(self, message: str, sender: socket.socket | None = None) -> None:
        """Send *message* to every connected client except *sender*."""
        with self.lock:
            for client_sock in list(self.clients):
                if client_sock is sender:
                    continue
                try:
                    client_sock.sendall((message + "\n").encode())
                except OSError:
                    self._remove_client(client_sock)

    def _remove_client(self, sock: socket.socket) -> None:
        nick = self.clients.pop(sock, "?")
        try:
            sock.close()
        except OSError:
            pass
        return nick

    def _handle_client(self, sock: socket.socket, addr: tuple) -> None:
        """Handle one client connection in its own thread."""
        # First line the client sends is their nickname
        try:
            rfile = sock.makefile("r", encoding="utf-8", errors="replace")
            nick = rfile.readline().strip() or f"anon-{addr[1]}"
        except OSError:
            sock.close()
            return

        with self.lock:
            self.clients[sock] = nick

        print(f"  [+] {nick} connected from {addr[0]}:{addr[1]}")
        self.broadcast(f"*** {nick} has joined the chat ***")

        try:
            for line in rfile:
                msg = line.strip()
                if not msg:
                    continue
                print(f"  <{nick}> {msg}")
                self.broadcast(f"<{nick}> {msg}", sender=sock)
        except OSError:
            pass
        finally:
            with self.lock:
                left_nick = self._remove_client(sock)
            print(f"  [-] {left_nick} disconnected")
            self.broadcast(f"*** {left_nick} has left the chat ***")

    def run(self) -> None:
        """Start listening and accept connections forever."""
        # Create a TCP socket
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow quick restart after Ctrl-C
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen(5)

        print("=" * 50)
        print(f"  Chat Server listening on {self.host}:{self.port}")
        print("  Press Ctrl-C to stop.")
        print("=" * 50)

        try:
            while True:
                client_sock, addr = server_sock.accept()
                t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr),
                    daemon=True,
                )
                t.start()
        except KeyboardInterrupt:
            print("\n  Server shutting down.")
        finally:
            server_sock.close()


# ── Client ───────────────────────────────────────────────────────────────

class ChatClient:
    """Simple TCP chat client with a background receive thread."""

    def __init__(self, host: str, port: int, nick: str) -> None:
        self.host = host
        self.port = port
        self.nick = nick
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def _receive_loop(self) -> None:
        """Background thread: print messages received from server."""
        rfile = self.sock.makefile("r", encoding="utf-8", errors="replace")
        try:
            for line in rfile:
                if not self.running:
                    break
                print(f"\r{line.strip()}\n> ", end="", flush=True)
        except OSError:
            pass
        finally:
            self.running = False

    def run(self) -> None:
        """Connect to server and enter the send loop."""
        try:
            self.sock.connect((self.host, self.port))
        except OSError as exc:
            print(f"  ✖ Could not connect to {self.host}:{self.port} — {exc}")
            return

        # Send nickname as the first message
        self.sock.sendall((self.nick + "\n").encode())

        print("=" * 50)
        print(f"  Connected to {self.host}:{self.port} as '{self.nick}'")
        print("  Type messages and press Enter.  Ctrl-C to quit.")
        print("=" * 50)

        recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        recv_thread.start()

        try:
            while self.running:
                msg = input("> ")
                if not msg:
                    continue
                self.sock.sendall((msg + "\n").encode())
        except (KeyboardInterrupt, EOFError):
            print("\n  Disconnecting …")
        finally:
            self.running = False
            self.sock.close()


# ── CLI ──────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple TCP chat application (server + client).",
    )
    sub = parser.add_subparsers(dest="mode")

    srv = sub.add_parser("server", help="Run the chat server")
    srv.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    srv.add_argument("--port", type=int, default=9000, help="Listen port (default: 9000)")

    cli = sub.add_parser("client", help="Run a chat client")
    cli.add_argument("--host", default="127.0.0.1", help="Server address (default: 127.0.0.1)")
    cli.add_argument("--port", type=int, default=9000, help="Server port (default: 9000)")
    cli.add_argument("--nick", default="User", help="Your nickname (default: User)")

    return parser


def print_usage_demo() -> None:
    """Print educational info when invoked without arguments."""
    print("=" * 60)
    print(" Network Chat App — Educational Demo")
    print("=" * 60)
    print("""
  This is a simple TCP-based chat application that demonstrates:

    • Socket programming (bind, listen, accept, connect)
    • Multi-threaded server design
    • Broadcasting messages to multiple clients
    • Line-oriented text protocol over TCP

  How to use:
    1. Start the server:
         python network_chat_app.py server --port 9000

    2. In another terminal, start a client:
         python network_chat_app.py client --port 9000 --nick Alice

    3. Open more terminals for more clients:
         python network_chat_app.py client --port 9000 --nick Bob

    4. Type messages in any client — they appear in all others.

  Under the hood:
    • The server creates a TCP socket and calls listen().
    • For each new connection, accept() returns a new socket
      which is handled in a dedicated thread.
    • The client sends its nickname first, then user messages.
    • The server broadcasts each message to all OTHER clients.
    • Messages are UTF-8 text delimited by newlines (\\n).
""")


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.mode is None:
        print_usage_demo()
        sys.exit(0)

    if args.mode == "server":
        ChatServer(host=args.host, port=args.port).run()
    elif args.mode == "client":
        ChatClient(host=args.host, port=args.port, nick=args.nick).run()
