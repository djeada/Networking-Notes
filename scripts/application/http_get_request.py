#!/usr/bin/env python3
"""
Raw HTTP GET Request
====================
Demonstrates how HTTP works by building a raw GET request using sockets.

Instead of using a high-level library like urllib or requests, this script
opens a TCP socket to port 80 and manually constructs an HTTP/1.1 request.
This shows exactly what happens "on the wire" when your browser fetches a page.

An HTTP request looks like this:

    GET /path HTTP/1.1\\r\\n
    Host: example.com\\r\\n
    Connection: close\\r\\n
    \\r\\n

The server responds with a status line, headers, a blank line, then the body.

Usage:
    python http_get_request.py example.com
    python http_get_request.py example.com /index.html
    python http_get_request.py example.com / --port 80
"""

import argparse
import socket
import sys


def build_request(host, path="/", extra_headers=None):
    """Build a raw HTTP/1.1 GET request string.

    HTTP requests are plain text with a specific format:
      1. Request line:  METHOD PATH HTTP/VERSION
      2. Headers:       Key: Value  (one per line)
      3. Blank line:    signals end of headers
    """
    headers = {
        "Host": host,                        # Required in HTTP/1.1
        "User-Agent": "PythonNetworkingNotes/1.0",
        "Accept": "*/*",
        "Connection": "close",               # Tell server to close after response
    }
    if extra_headers:
        headers.update(extra_headers)

    # Construct the request line
    request = f"GET {path} HTTP/1.1\r\n"

    # Append each header
    for key, value in headers.items():
        request += f"{key}: {value}\r\n"

    # Blank line marks end of headers
    request += "\r\n"
    return request


def send_request(host, port, request_str, timeout=10):
    """Open a TCP connection, send the request, and return the raw response."""
    raw_response = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        # TCP three-way handshake happens here
        sock.connect((host, port))
        # Send our HTTP request as bytes
        sock.sendall(request_str.encode("utf-8"))
        # Read the response in chunks until the server closes the connection
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                raw_response += chunk
            except socket.timeout:
                break
    return raw_response


def parse_response(raw_response):
    """Split an HTTP response into status line, headers dict, and body.

    HTTP responses look like:
        HTTP/1.1 200 OK\\r\\n
        Content-Type: text/html\\r\\n
        Content-Length: 1234\\r\\n
        \\r\\n
        <html>...</html>
    """
    # The header/body boundary is a blank line (\r\n\r\n)
    header_end = raw_response.find(b"\r\n\r\n")
    if header_end == -1:
        return None, {}, raw_response

    header_section = raw_response[:header_end].decode("utf-8", errors="replace")
    body = raw_response[header_end + 4:]

    lines = header_section.split("\r\n")
    status_line = lines[0]  # e.g. "HTTP/1.1 200 OK"

    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    return status_line, headers, body


def display_results(status_line, headers, body, show_body_bytes=500):
    """Pretty-print the parsed HTTP response."""
    print("\n" + "=" * 55)
    print("  HTTP Response")
    print("=" * 55)

    # Status line
    print(f"\n[Status Line]")
    print(f"  {status_line}")
    if status_line:
        parts = status_line.split(" ", 2)
        if len(parts) >= 3:
            print(f"    Version : {parts[0]}")
            print(f"    Code    : {parts[1]}")
            print(f"    Reason  : {parts[2]}")

    # Headers
    print(f"\n[Headers] ({len(headers)} received)")
    for key, value in headers.items():
        print(f"  {key}: {value}")

    # Body (truncated for readability)
    body_text = body.decode("utf-8", errors="replace")
    print(f"\n[Body] ({len(body)} bytes total)")
    if len(body_text) > show_body_bytes:
        print(body_text[:show_body_bytes])
        print(f"\n  ... (truncated, {len(body_text) - show_body_bytes} more bytes)")
    else:
        print(body_text)


def main():
    parser = argparse.ArgumentParser(
        description="Send a raw HTTP GET request using sockets."
    )
    parser.add_argument("host", help="Hostname to connect to (e.g. example.com)")
    parser.add_argument("path", nargs="?", default="/", help="URL path (default: /)")
    parser.add_argument("--port", type=int, default=80, help="Port number (default: 80)")
    parser.add_argument("--timeout", type=int, default=10, help="Socket timeout in seconds")
    args = parser.parse_args()

    request_str = build_request(args.host, args.path)

    print("=" * 55)
    print("  Raw HTTP GET Request")
    print("=" * 55)
    print(f"\nConnecting to {args.host}:{args.port} ...")
    print(f"\n[Request Sent]")
    for line in request_str.split("\r\n"):
        print(f"  > {line}")

    try:
        raw = send_request(args.host, args.port, request_str, args.timeout)
    except socket.gaierror:
        print(f"\nError: could not resolve hostname '{args.host}'")
        sys.exit(1)
    except socket.timeout:
        print("\nError: connection timed out")
        sys.exit(1)
    except OSError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    status_line, headers, body = parse_response(raw)
    display_results(status_line, headers, body)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=" * 55)
        print("  Raw HTTP GET Request — Educational Demo")
        print("=" * 55)
        print()
        print("This script builds an HTTP request from scratch using TCP")
        print("sockets, showing exactly what your browser sends and receives.")
        print()
        print("Example HTTP request:")
        sample = build_request("example.com", "/")
        for line in sample.split("\r\n"):
            print(f"  > {line}")
        print()

        print("Sending request to example.com ...")
        try:
            raw = send_request("example.com", 80, sample)
            status_line, headers, body = parse_response(raw)
            display_results(status_line, headers, body)
        except Exception as e:
            print(f"\nCould not complete demo request: {e}")
            print("(This is expected if you have no internet access.)")

        print("\n--- Usage ---")
        print("  python http_get_request.py example.com")
        print("  python http_get_request.py example.com /index.html")
    else:
        main()
