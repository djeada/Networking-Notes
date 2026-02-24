#!/usr/bin/env python3
"""
SSL/TLS Certificate Checker
============================
Checks SSL/TLS certificates of HTTPS websites and displays their details.

When you visit an HTTPS website, the server presents a digital certificate
that proves its identity. This script connects to a server's TLS port (443),
performs the handshake, and inspects the certificate.

This script shows:
  - Subject (who the certificate was issued to)
  - Issuer (the Certificate Authority that signed it)
  - Validity period (notBefore / notAfter)
  - Serial number
  - Whether the certificate is currently valid or expired
  - TLS protocol version negotiated

Usage:
    python ssl_certificate_checker.py example.com
    python ssl_certificate_checker.py github.com --port 443
    python ssl_certificate_checker.py example.com --pem
"""

import argparse
import datetime
import hashlib
import socket
import ssl
import sys


def get_certificate(hostname, port=443, timeout=10):
    """Connect to a host via TLS and retrieve its certificate.

    Steps:
      1. Create a default SSL context (loads system CA certificates).
      2. Wrap a TCP socket with TLS.
      3. Perform the handshake — the server sends its certificate.
      4. Return the certificate dict and the PEM-encoded certificate.
    """
    context = ssl.create_default_context()
    # Enforce TLS 1.2+ to avoid insecure legacy protocol versions
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls_sock:
            # getpeercert() returns a dict with parsed certificate fields
            cert_dict = tls_sock.getpeercert()
            # Get the certificate in binary DER format for PEM conversion
            cert_der = tls_sock.getpeercert(binary_form=True)
            tls_version = tls_sock.version()
            cipher = tls_sock.cipher()

    return cert_dict, cert_der, tls_version, cipher


def format_distinguished_name(dn_tuples):
    """Format a certificate distinguished name (subject or issuer).

    Certificates use X.509 distinguished names — a sequence of
    attribute-value pairs like CN (Common Name), O (Organization), etc.
    """
    parts = []
    for rdn in dn_tuples:
        for key, value in rdn:
            parts.append(f"{key}={value}")
    return ", ".join(parts)


def check_expiry(cert_dict):
    """Check whether the certificate is currently valid, expired, or not yet valid."""
    # Python's ssl module provides dates in a specific format
    date_fmt = "%b %d %H:%M:%S %Y %Z"
    not_before = datetime.datetime.strptime(cert_dict["notBefore"], date_fmt)
    not_after = datetime.datetime.strptime(cert_dict["notAfter"], date_fmt)
    now = datetime.datetime.utcnow()

    if now < not_before:
        days = (not_before - now).days
        return "NOT YET VALID", f"Certificate becomes valid in {days} day(s)"
    elif now > not_after:
        days = (now - not_after).days
        return "EXPIRED", f"Certificate expired {days} day(s) ago"
    else:
        days = (not_after - now).days
        return "VALID", f"Certificate expires in {days} day(s)"


def display_certificate(hostname, cert_dict, cert_der, tls_version, cipher, show_pem=False):
    """Display certificate details in a readable format."""
    print("\n" + "=" * 55)
    print(f"  SSL/TLS Certificate — {hostname}")
    print("=" * 55)

    # Subject
    subject = format_distinguished_name(cert_dict.get("subject", ()))
    print(f"\n  [Subject] (who this certificate identifies)")
    print(f"    {subject}")

    # Issuer
    issuer = format_distinguished_name(cert_dict.get("issuer", ()))
    print(f"\n  [Issuer] (Certificate Authority that signed it)")
    print(f"    {issuer}")

    # Subject Alternative Names — modern certs list domains here
    san = cert_dict.get("subjectAltName", ())
    if san:
        names = [f"{typ}:{val}" for typ, val in san]
        print(f"\n  [Subject Alt Names] ({len(names)} entries)")
        for name in names[:10]:
            print(f"    {name}")
        if len(names) > 10:
            print(f"    ... and {len(names) - 10} more")

    # Validity
    print(f"\n  [Validity]")
    print(f"    Not Before : {cert_dict.get('notBefore', 'N/A')}")
    print(f"    Not After  : {cert_dict.get('notAfter', 'N/A')}")
    status, message = check_expiry(cert_dict)
    status_icon = "✓" if status == "VALID" else "✗"
    print(f"    Status     : {status_icon} {status} — {message}")

    # Serial number
    serial = cert_dict.get("serialNumber", "N/A")
    print(f"\n  [Serial Number]")
    print(f"    {serial}")

    # Certificate fingerprints
    sha256 = hashlib.sha256(cert_der).hexdigest()
    sha256_formatted = ":".join(sha256[i:i + 2] for i in range(0, len(sha256), 2))
    print(f"\n  [SHA-256 Fingerprint]")
    print(f"    {sha256_formatted}")

    # TLS connection details
    print(f"\n  [Connection]")
    print(f"    TLS Version : {tls_version}")
    if cipher:
        print(f"    Cipher      : {cipher[0]}")
        print(f"    Bits        : {cipher[2]}")

    # PEM output
    if show_pem:
        import base64
        pem = ssl.DER_cert_to_PEM_cert(cert_der)
        print(f"\n  [PEM Certificate]")
        print(pem)

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Check SSL/TLS certificates of HTTPS websites."
    )
    parser.add_argument("hostname", help="Hostname to check (e.g. example.com)")
    parser.add_argument("--port", type=int, default=443, help="TLS port (default: 443)")
    parser.add_argument("--pem", action="store_true", help="Show PEM-encoded certificate")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout in seconds")
    args = parser.parse_args()

    try:
        cert_dict, cert_der, tls_version, cipher = get_certificate(
            args.hostname, args.port, args.timeout
        )
    except socket.gaierror:
        print(f"Error: could not resolve hostname '{args.hostname}'")
        sys.exit(1)
    except socket.timeout:
        print("Error: connection timed out")
        sys.exit(1)
    except ssl.SSLCertVerificationError as e:
        print(f"Error: certificate verification failed — {e}")
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

    display_certificate(args.hostname, cert_dict, cert_der, tls_version, cipher, args.pem)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("=" * 55)
        print("  SSL/TLS Certificate Checker — Educational Demo")
        print("=" * 55)
        print()
        print("TLS (Transport Layer Security) encrypts communication between")
        print("your browser and a web server. Certificates verify the server's")
        print("identity so you know you're talking to the real site.")
        print()
        print("Checking certificate for example.com ...")

        try:
            cert_dict, cert_der, tls_version, cipher = get_certificate("example.com")
            display_certificate("example.com", cert_dict, cert_der, tls_version, cipher)
        except Exception as e:
            print(f"\nCould not complete demo: {e}")
            print("(This is expected if you have no internet access.)")

        print("--- Usage ---")
        print("  python ssl_certificate_checker.py example.com")
        print("  python ssl_certificate_checker.py github.com --pem")
        print("  python ssl_certificate_checker.py example.com --port 443")
    else:
        main()
