#!/usr/bin/env python3
"""
SMTP Protocol Conversation Simulator
======================================
Walks through a complete SMTP email-sending session without opening any
real network connections. Every protocol command and server reply is printed
with a plain-language explanation so you can see exactly how mail transfer
works under the hood.

Steps simulated:
  1. TCP connection to port 25 / 587
  2. Server greeting (220)
  3. EHLO — client identifies itself and requests extensions
  4. STARTTLS negotiation (optional)
  5. AUTH LOGIN (optional, with base64 credentials)
  6. MAIL FROM — envelope sender
  7. RCPT TO — envelope recipient(s)
  8. DATA — message headers + body, terminated by <CRLF>.<CRLF>
  9. QUIT — graceful disconnect

SMTP response code families:
  2xx — Success       3xx — Intermediate (send more data)
  4xx — Temporary failure   5xx — Permanent failure

Concepts demonstrated:
  * SMTP command / response dialogue
  * Envelope vs header addresses
  * EHLO extension advertisement
  * STARTTLS upgrade to encrypted channel
  * Base64-encoded AUTH credentials
  * Multi-line DATA termination with lone dot

Usage:
    python smtp_client_demo.py                           # run built-in demo
    python smtp_client_demo.py --sender a@x.com --recipient b@y.com
    python smtp_client_demo.py --show-codes              # list response codes
"""

import argparse
import base64
import time

SMTP_CODES = {
    211: "System status or help reply",
    214: "Help message",
    220: "Service ready — server greeting",
    221: "Service closing transmission channel",
    235: "Authentication successful",
    250: "Requested action completed (OK)",
    251: "User not local; will forward",
    334: "Server challenge (send credentials)",
    354: "Start mail input; end with <CRLF>.<CRLF>",
    421: "Service not available, closing channel",
    450: "Mailbox unavailable (temporary)",
    451: "Local error in processing",
    452: "Insufficient storage",
    500: "Syntax error, command unrecognised",
    501: "Syntax error in parameters",
    502: "Command not implemented",
    503: "Bad sequence of commands",
    504: "Parameter not implemented",
    550: "Mailbox unavailable (permanent)",
    553: "Mailbox name not allowed",
    554: "Transaction failed",
}

EXTENSIONS = [
    "SIZE 35882577",
    "8BITMIME",
    "STARTTLS",
    "AUTH LOGIN PLAIN",
    "ENHANCEDSTATUSCODES",
    "PIPELINING",
    "CHUNKING",
]


def _step(direction, text, explanation, pause=0.05):
    """Print one line of the SMTP dialogue."""
    arrow = "C →" if direction == "C" else "S ←"
    print(f"  {arrow}  {text}")
    if explanation:
        print(f"       ⤷ {explanation}")


def simulate_session(sender, recipient, server_host="mail.example.com",
                     client_host="client.example.com", subject="Hello!",
                     body="This is a test message.", use_tls=True,
                     use_auth=True):
    """Run a full simulated SMTP session and explain each step."""
    print(f"\n{'='*60}")
    print(f"  Connecting to {server_host}:587 …")
    print(f"{'='*60}\n")

    _step("S", f"220 {server_host} ESMTP ready",
          "Server greeting — connection accepted on port 587.")

    _step("C", f"EHLO {client_host}",
          "Client says hello and requests Extended SMTP features.")

    lines = [f"250-{server_host} Hello {client_host}"]
    for ext in EXTENSIONS[:-1]:
        lines.append(f"250-{ext}")
    lines.append(f"250 {EXTENSIONS[-1]}")
    _step("S", "\n       ".join(lines),
          "Server lists supported extensions (SIZE, AUTH, STARTTLS …).")

    if use_tls:
        print(f"\n  --- TLS Negotiation ---")
        _step("C", "STARTTLS",
              "Client requests upgrade to encrypted channel.")
        _step("S", "220 2.0.0 Ready to start TLS",
              "Server agrees — TLS handshake begins.")
        print(f"       ⤷ [TLS 1.3 handshake completed — channel encrypted]\n")

        _step("C", f"EHLO {client_host}",
              "Client must re-identify after TLS upgrade.")
        _step("S", f"250 {server_host} Hello, now encrypted",
              "Server acknowledges over secure channel.")

    if use_auth:
        print(f"\n  --- Authentication ---")
        _step("C", "AUTH LOGIN",
              "Client chooses LOGIN authentication mechanism.")
        _step("S", f"334 {base64.b64encode(b'Username:').decode()}",
              "Server sends base64-encoded 'Username:' challenge.")
        encoded_user = base64.b64encode(sender.encode()).decode()
        _step("C", encoded_user,
              f"Client sends base64-encoded username ({sender}).")
        _step("S", f"334 {base64.b64encode(b'Password:').decode()}",
              "Server sends base64-encoded 'Password:' challenge.")
        _step("C", base64.b64encode(b"[password hidden]").decode(),
              "Client sends base64-encoded password.")
        _step("S", "235 2.7.0 Authentication successful",
              "Credentials accepted — client is authorised to send.")

    print(f"\n  --- Envelope ---")
    _step("C", f"MAIL FROM:<{sender}>",
          "Envelope sender — used for bounces, not necessarily the From header.")
    _step("S", "250 2.1.0 OK",
          "Server accepts the sender address.")

    _step("C", f"RCPT TO:<{recipient}>",
          "Envelope recipient — who actually receives the message.")
    _step("S", "250 2.1.5 OK",
          "Server accepts the recipient.")

    print(f"\n  --- Message Data ---")
    _step("C", "DATA",
          "Client is ready to transmit the message body.")
    _step("S", "354 Start mail input; end with <CRLF>.<CRLF>",
          "Server says: go ahead, I'll wait for a lone dot to finish.")

    msg_lines = [
        f"From: {sender}",
        f"To: {recipient}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "",
        body,
        ".",
    ]
    for line in msg_lines:
        tag = "C →" if line != "." else "C →"
        print(f"  C →  {line}")
    print(f"       ⤷ Lone dot on its own line signals end of DATA.")
    _step("S", "250 2.0.0 OK: queued as ABC123",
          "Server accepted and queued the message for delivery.")

    print(f"\n  --- Disconnect ---")
    _step("C", "QUIT",
          "Client requests graceful disconnect.")
    _step("S", "221 2.0.0 Bye",
          "Server closes the connection.")

    print(f"\n{'='*60}")
    print(f"  Session complete — message queued for {recipient}")
    print(f"{'='*60}\n")


def show_codes():
    """Print a reference table of SMTP response codes."""
    print("\n  SMTP Response Code Reference")
    print(f"  {'Code':<6} {'Meaning'}")
    print(f"  {'-'*6} {'-'*48}")
    for code, meaning in sorted(SMTP_CODES.items()):
        print(f"  {code:<6} {meaning}")
    print()


def demo():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          SMTP Protocol Conversation Simulator           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    show_codes()
    simulate_session(
        sender="alice@example.com",
        recipient="bob@example.org",
        subject="Meeting tomorrow",
        body="Hi Bob,\n\nAre we still on for 10 AM?\n\nBest,\nAlice",
    )


def main():
    parser = argparse.ArgumentParser(
        description="SMTP Protocol Conversation Simulator")
    parser.add_argument("--sender", default="",
                        help="Sender email address")
    parser.add_argument("--recipient", default="",
                        help="Recipient email address")
    parser.add_argument("--show-codes", action="store_true",
                        help="Print SMTP response code reference")
    args = parser.parse_args()

    if args.show_codes:
        show_codes()
    elif args.sender and args.recipient:
        simulate_session(sender=args.sender, recipient=args.recipient)
    else:
        demo()


if __name__ == "__main__":
    main()
