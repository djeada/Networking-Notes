#!/usr/bin/env python3
"""
URL Parser & Analyzer
=====================
Parses and analyzes URLs using Python's urllib.parse module.

A URL (Uniform Resource Locator) has this general structure:

    scheme://user:pass@host:port/path;params?query=value#fragment
    \\____/   \\_______/ \\__/ \\__/\\___/ \\____/ \\_________/ \\______/
    scheme   userinfo  host port path params   query     fragment
           \\_________________/
                 netloc

This script demonstrates:
  - Breaking a URL into its components
  - Reconstructing a URL from parts
  - URL encoding and decoding (percent-encoding)
  - Query string parsing
  - Joining/resolving relative URLs

Usage:
    python url_parser.py "https://example.com/path?key=value#section"
    python url_parser.py --encode "hello world & goodbye"
    python url_parser.py --decode "hello%20world%20%26%20goodbye"
    python url_parser.py --join "https://example.com/a/b" "../c"
"""

import argparse
import sys
from urllib.parse import (
    parse_qs,
    parse_qsl,
    quote,
    unquote,
    urldefrag,
    urlencode,
    urljoin,
    urlparse,
    urlunparse,
)


def analyze_url(url):
    """Parse a URL and display each component with explanations."""
    parsed = urlparse(url)

    print(f"\n--- URL Analysis ---")
    print(f"  Original : {url}")
    print()

    components = [
        ("scheme", parsed.scheme, "Protocol (http, https, ftp, etc.)"),
        ("netloc", parsed.netloc, "Network location (host:port)"),
        ("path", parsed.path, "Resource path on the server"),
        ("params", parsed.params, "Path segment parameters (rarely used)"),
        ("query", parsed.query, "Query string (key=value pairs after ?)"),
        ("fragment", parsed.fragment, "Fragment / anchor (after #, client-side only)"),
    ]

    for name, value, description in components:
        indicator = "✓" if value else "·"
        print(f"  {indicator} {name:10s}: {value or '(empty)':30s}  — {description}")

    # Additional derived attributes
    print()
    if parsed.hostname:
        print(f"    hostname : {parsed.hostname}")
    if parsed.port:
        print(f"    port     : {parsed.port}")
    if parsed.username:
        print(f"    username : {parsed.username}")
    if parsed.password:
        print(f"    password : {parsed.password}")

    # Parse query parameters
    if parsed.query:
        print(f"\n  [Query Parameters]")
        params = parse_qs(parsed.query)
        for key, values in params.items():
            for v in values:
                print(f"    {key} = {v}")

    # Show reconstruction
    reconstructed = urlunparse(parsed)
    print(f"\n  Reconstructed: {reconstructed}")

    # Fragment separation
    url_no_frag, frag = urldefrag(url)
    if frag:
        print(f"  Without fragment: {url_no_frag}")


def encode_string(text):
    """Demonstrate URL percent-encoding."""
    encoded = quote(text, safe="")
    print(f"\n--- URL Encoding ---")
    print(f"  Original : {text}")
    print(f"  Encoded  : {encoded}")
    print()
    print("  Percent-encoding replaces unsafe characters with %XX,")
    print("  where XX is the hex value of the character's byte.")
    # Show character-by-character breakdown for non-ASCII or special chars
    special = [c for c in text if quote(c, safe="") != c]
    if special:
        print(f"\n  Character breakdown:")
        for c in special:
            print(f"    '{c}' -> {quote(c, safe='')}")


def decode_string(text):
    """Demonstrate URL percent-decoding."""
    decoded = unquote(text)
    print(f"\n--- URL Decoding ---")
    print(f"  Encoded  : {text}")
    print(f"  Decoded  : {decoded}")


def join_urls(base, relative):
    """Demonstrate URL resolution (joining a base URL with a relative URL)."""
    result = urljoin(base, relative)
    print(f"\n--- URL Join / Resolution ---")
    print(f"  Base     : {base}")
    print(f"  Relative : {relative}")
    print(f"  Result   : {result}")
    print()
    print("  urljoin resolves a relative URL against a base, following")
    print("  the same rules a browser uses for relative links.")


def build_query_string(pairs):
    """Demonstrate building a query string from key-value pairs."""
    qs = urlencode(pairs)
    print(f"\n--- Build Query String ---")
    print(f"  Pairs  : {pairs}")
    print(f"  Result : ?{qs}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse, encode, decode, and analyze URLs."
    )
    parser.add_argument("url", nargs="?", help="URL to parse and analyze")
    parser.add_argument("--encode", "-e", metavar="TEXT", help="URL-encode a string")
    parser.add_argument("--decode", "-d", metavar="TEXT", help="URL-decode a string")
    parser.add_argument(
        "--join", "-j",
        nargs=2,
        metavar=("BASE", "RELATIVE"),
        help="Join a base URL with a relative URL",
    )
    args = parser.parse_args()

    actions = 0
    if args.url:
        analyze_url(args.url)
        actions += 1
    if args.encode:
        encode_string(args.encode)
        actions += 1
    if args.decode:
        decode_string(args.decode)
        actions += 1
    if args.join:
        join_urls(args.join[0], args.join[1])
        actions += 1

    if actions == 0:
        parser.print_help()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=" * 55)
        print("  URL Parser & Analyzer — Educational Demo")
        print("=" * 55)
        print()
        print("URLs are the addresses of the web. Understanding their")
        print("structure is fundamental to networking and web development.")
        print()

        # Demo: parse a complex URL
        demo_url = "https://user:pass@example.com:8080/path/page;type=a?q=hello&lang=en#results"
        analyze_url(demo_url)

        # Demo: encoding
        encode_string("search query: hello world & more!")

        # Demo: decoding
        decode_string("search%20query%3A%20hello%20world%20%26%20more%21")

        # Demo: URL join
        join_urls("https://example.com/docs/chapter1/", "../chapter2/intro.html")

        # Demo: building a query string
        build_query_string([("q", "python networking"), ("page", "1"), ("lang", "en")])

        print("\n--- Usage ---")
        print('  python url_parser.py "https://example.com/path?q=1#top"')
        print('  python url_parser.py --encode "hello world"')
        print('  python url_parser.py --decode "hello%20world"')
        print('  python url_parser.py --join "https://example.com/a/" "../b"')
    else:
        main()
