#!/usr/bin/env python3
"""
Minimal Educational HTTP Server
================================
A simple HTTP server built on Python's http.server module.

This script demonstrates:
  - Handling HTTP GET requests
  - Serving static files from a directory
  - Content-type detection based on file extension
  - Custom request logging with educational annotations
  - HTTP response codes and headers

The server listens on a configurable port and serves files from the
current working directory (or a specified directory).

Usage:
    python http_server.py                     # Serve cwd on port 8080
    python http_server.py --port 9000         # Custom port
    python http_server.py --directory ./site  # Serve a specific directory
"""

import argparse
import datetime
import mimetypes
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


class EducationalHTTPHandler(SimpleHTTPRequestHandler):
    """Custom handler that logs educational information about each request.

    SimpleHTTPRequestHandler already handles serving static files.
    We override log_request and do_GET to add educational output.
    """

    def do_GET(self):
        """Handle GET requests with extra educational logging."""
        self._print_request_info()
        # Delegate to the parent class to actually serve the file
        super().do_GET()

    def do_HEAD(self):
        """Handle HEAD requests (same as GET but no body)."""
        self._print_request_info()
        super().do_HEAD()

    def _print_request_info(self):
        """Print detailed, educational information about the incoming request."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "-" * 55)
        print(f"  [{now}] Incoming Request")
        print("-" * 55)
        # Request line — the first line the client sends
        print(f"  Method  : {self.command}")
        print(f"  Path    : {self.path}")
        print(f"  Version : {self.request_version}")
        print(f"  Client  : {self.client_address[0]}:{self.client_address[1]}")

        # Show select request headers
        print("  Headers :")
        for key in ("Host", "User-Agent", "Accept", "Accept-Encoding"):
            value = self.headers.get(key)
            if value:
                print(f"    {key}: {value}")

        # Determine what file will be served
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            # Look for index files
            for index in ("index.html", "index.htm"):
                candidate = os.path.join(path, index)
                if os.path.exists(candidate):
                    path = candidate
                    break

        if os.path.isfile(path):
            content_type, _ = mimetypes.guess_type(path)
            size = os.path.getsize(path)
            print(f"  File    : {path}")
            print(f"  Type    : {content_type or 'application/octet-stream'}")
            print(f"  Size    : {size} bytes")
        elif os.path.isdir(path):
            print(f"  Action  : Directory listing for {path}")
        else:
            print(f"  Action  : 404 — file not found ({path})")

    def log_message(self, format, *args):
        """Override default logging to include a concise summary line."""
        # args are typically (request_line, status_code, size)
        print(f"  Response: {args[1] if len(args) > 1 else '?'} "
              f"({args[0] if args else '?'})")


def run_server(port, directory):
    """Start the HTTP server on the given port, serving from directory."""
    # Change working directory so SimpleHTTPRequestHandler serves from there
    os.chdir(directory)

    server_address = ("", port)
    httpd = HTTPServer(server_address, EducationalHTTPHandler)

    print("=" * 55)
    print("  Educational HTTP Server")
    print("=" * 55)
    print(f"\n  Serving : {os.path.abspath(directory)}")
    print(f"  Address : http://localhost:{port}/")
    print(f"  Press Ctrl+C to stop.\n")
    print("How it works:")
    print("  1. The server listens for TCP connections on the port.")
    print("  2. When a client connects, it reads the HTTP request.")
    print("  3. It maps the URL path to a file on disk.")
    print("  4. It sends back an HTTP response with the file contents.")
    print("  5. Each request/response pair is logged below.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.server_close()


def main():
    parser = argparse.ArgumentParser(
        description="A minimal educational HTTP server."
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="Port to listen on (default: 8080)",
    )
    parser.add_argument(
        "--directory", "-d",
        default=".",
        help="Directory to serve files from (default: current directory)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        sys.exit(1)

    run_server(args.port, args.directory)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=" * 55)
        print("  Educational HTTP Server — Demo Mode")
        print("=" * 55)
        print()
        print("This script starts a simple HTTP server that serves files")
        print("from a directory and logs educational details about every")
        print("request it receives.")
        print()
        print("--- Usage ---")
        print("  python http_server.py                     # port 8080, cwd")
        print("  python http_server.py --port 9000")
        print("  python http_server.py --directory ./site")
        print()
        print("Starting server on port 8080 (Ctrl+C to stop) ...")
        print()
        run_server(port=8080, directory=".")
    else:
        main()
