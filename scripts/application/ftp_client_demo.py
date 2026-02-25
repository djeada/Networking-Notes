#!/usr/bin/env python3
"""
FTP Session Simulator
======================
Simulates a complete FTP control-channel conversation, showing every
command the client sends and every reply the server returns — without
opening any real network connections.

The simulator includes a virtual file system so commands like LIST, CWD,
PWD, RETR, and STOR produce realistic output. It also explains the
critical difference between active and passive data-transfer modes.

Concepts demonstrated:
  * Dual-channel architecture (control port 21, data port 20 / dynamic)
  * FTP commands: USER, PASS, PWD, CWD, LIST, RETR, STOR, PASV, PORT, QUIT
  * Active mode (PORT — server connects back) vs Passive (PASV — client connects)
  * ASCII vs binary transfer types and directory navigation

Usage:
    python ftp_client_demo.py                    # run built-in demo
    python ftp_client_demo.py --mode active      # demo in active mode
    python ftp_client_demo.py --show-codes       # list FTP response codes
"""

import argparse
import random

FTP_CODES = {
    150: "Opening data connection",
    200: "Command OK",
    215: "NAME system type",
    220: "Service ready for new user",
    221: "Service closing control connection",
    226: "Closing data connection; transfer complete",
    227: "Entering Passive Mode (h1,h2,h3,h4,p1,p2)",
    230: "User logged in, proceed",
    250: "Requested file action OK",
    257: '"PATHNAME" created / current directory',
    331: "Username OK, need password",
    425: "Can't open data connection",
    500: "Syntax error, unrecognised command",
    530: "Not logged in",
    550: "File not found / access denied",
}

# Virtual file system
VFS = {
    "/": ["docs/", "images/", "README.txt"],
    "/docs": ["manual.pdf", "changelog.txt"],
    "/images": ["logo.png", "banner.jpg"],
}

FILE_SIZES = {
    "README.txt": 1024,
    "manual.pdf": 245760,
    "changelog.txt": 4096,
    "logo.png": 51200,
    "banner.jpg": 102400,
}


def _cmd(direction, text, explanation=""):
    arrow = "C →" if direction == "C" else "S ←"
    print(f"  {arrow}  {text}")
    if explanation:
        print(f"       ⤷ {explanation}")


def simulate_session(mode="passive"):
    """Run a complete simulated FTP session."""
    server = "ftp.example.com"
    cwd = "/"
    passive = mode == "passive"

    print(f"\n{'='*60}")
    print(f"  Connecting to {server}:21 …")
    print(f"{'='*60}\n")

    _cmd("S", f"220 {server} FTP server ready",
         "Server greeting on control port 21.")

    # --- Authentication ---
    print(f"\n  --- Authentication ---")
    _cmd("C", "USER alice",
         "Client provides username.")
    _cmd("S", "331 Username OK, send password",
         "Server requests the password.")
    _cmd("C", "PASS ********",
         "Client sends password (hidden here).")
    _cmd("S", "230 User alice logged in",
         "Authentication successful.")

    # --- System info ---
    _cmd("C", "SYST",
         "Client queries the server OS type.")
    _cmd("S", "215 UNIX Type: L8",
         "Server identifies itself as UNIX with 8-bit bytes.")

    # --- Transfer type ---
    _cmd("C", "TYPE I",
         "Switch to binary (Image) transfer mode.")
    _cmd("S", "200 Type set to I",
         "Binary mode active — no newline conversion.")

    # --- PWD ---
    print(f"\n  --- Directory Navigation ---")
    _cmd("C", "PWD",
         "Print working directory.")
    _cmd("S", '257 "/" is current directory',
         f"Server confirms cwd = {cwd}")

    # --- Data channel + LIST ---
    print(f"\n  --- Directory Listing (data channel: {mode}) ---")
    _open_data_channel(passive, server)
    _cmd("C", "LIST",
         "Request directory listing over the data channel.")
    _cmd("S", "150 Opening data connection for LIST",
         "Server starts sending listing over the data channel.")
    print(f"\n       --- data channel ---")
    for entry in VFS.get(cwd, []):
        if entry.endswith("/"):
            print(f"       drwxr-xr-x  2 alice users  4096 Jun 01 10:00 {entry[:-1]}")
        else:
            size = FILE_SIZES.get(entry, 0)
            print(f"       -rw-r--r--  1 alice users {size:>6} Jun 01 09:30 {entry}")
    print(f"       --- end data ---\n")
    _cmd("S", "226 Transfer complete, closing data connection",
         "Listing finished; data channel closed.")

    # --- CWD ---
    cwd = "/docs"
    _cmd("C", "CWD docs",
         "Change into the docs/ subdirectory.")
    _cmd("S", "250 CWD command successful",
         f"Working directory is now {cwd}")

    # --- Data channel + LIST ---
    _open_data_channel(passive, server)
    _cmd("C", "LIST",
         "List the new directory.")
    _cmd("S", "150 Opening data connection for LIST", "")
    print(f"\n       --- data channel ---")
    for entry in VFS.get(cwd, []):
        size = FILE_SIZES.get(entry, 0)
        print(f"       -rw-r--r--  1 alice users {size:>6} May 28 14:00 {entry}")
    print(f"       --- end data ---\n")
    _cmd("S", "226 Transfer complete", "")

    # --- RETR (download) ---
    print(f"\n  --- File Download ---")
    fname = "manual.pdf"
    _cmd("C", f"SIZE {fname}",
         "Query file size before downloading.")
    _cmd("S", f"213 {FILE_SIZES[fname]}",
         f"File is {FILE_SIZES[fname]} bytes.")
    _open_data_channel(passive, server)
    _cmd("C", f"RETR {fname}",
         f"Download {fname} over the data channel.")
    _cmd("S", f"150 Opening BINARY data connection for {fname}",
         "Server begins sending file bytes.")
    print(f"       ⤷ [{FILE_SIZES[fname]} bytes transferred]")
    _cmd("S", "226 Transfer complete",
         "Download finished; data channel closed.")

    # --- STOR (upload) ---
    print(f"\n  --- File Upload ---")
    upload = "report.txt"
    upload_size = 2048
    _open_data_channel(passive, server)
    _cmd("C", f"STOR {upload}",
         f"Upload {upload} to the server.")
    _cmd("S", f"150 Opening BINARY data connection for {upload}",
         "Server ready to receive bytes.")
    print(f"       ⤷ [{upload_size} bytes transferred]")
    _cmd("S", "226 Transfer complete",
         "Upload finished; data channel closed.")

    # --- QUIT ---
    print(f"\n  --- Disconnect ---")
    _cmd("C", "QUIT",
         "Client requests graceful disconnect.")
    _cmd("S", "221 Goodbye",
         "Server closes the control connection.")

    print(f"\n{'='*60}")
    print(f"  Session complete — {mode.upper()} mode demonstration finished.")
    print(f"{'='*60}\n")


def _open_data_channel(passive, server):
    """Print the data-channel negotiation for passive or active mode."""
    if passive:
        p1, p2 = random.randint(128, 255), random.randint(0, 255)
        port = p1 * 256 + p2
        _cmd("C", "PASV",
             "Client requests passive mode (server opens a port).")
        _cmd("S", f"227 Entering Passive Mode (93,184,216,34,{p1},{p2})",
             f"Server listens on port {p1}*256+{p2} = {port}. Client connects to it.")
    else:
        p1, p2 = random.randint(128, 255), random.randint(0, 255)
        port = p1 * 256 + p2
        _cmd("C", f"PORT 192,168,1,100,{p1},{p2}",
             f"Client opens port {port} and tells the server to connect back.")
        _cmd("S", "200 PORT command successful",
             "Server will initiate the data connection to the client.")


def show_codes():
    """Print FTP response code reference."""
    print("\n  FTP Response Code Reference")
    print(f"  {'Code':<6} {'Meaning'}")
    print(f"  {'-'*6} {'-'*50}")
    for code, meaning in sorted(FTP_CODES.items()):
        print(f"  {code:<6} {meaning}")
    print()


def demo():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║               FTP Session Simulator                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\n  FTP uses TWO channels:")
    print("    • Control channel (port 21) — commands & replies")
    print("    • Data channel   (port 20 / dynamic) — file transfers & listings\n")
    show_codes()
    simulate_session(mode="passive")


def main():
    parser = argparse.ArgumentParser(description="FTP Session Simulator")
    parser.add_argument("--mode", choices=["active", "passive"],
                        default="",
                        help="Data channel mode to demonstrate")
    parser.add_argument("--show-codes", action="store_true",
                        help="Print FTP response code reference")
    args = parser.parse_args()

    if args.show_codes:
        show_codes()
    elif args.mode:
        simulate_session(mode=args.mode)
    else:
        demo()


if __name__ == "__main__":
    main()
