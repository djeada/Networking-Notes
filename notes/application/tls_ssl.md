# TLS/SSL (Transport Layer Security)

## Introduction

Transport Layer Security (TLS) is a cryptographic protocol that provides **privacy**,
**data integrity**, and **authentication** for communication over a network. TLS is the
successor to SSL (Secure Sockets Layer) and is the standard for encrypting traffic on
the internet.

- SSL 3.0 was the last SSL version; **TLS 1.0** succeeded it in 1999.
- **TLS 1.2** (RFC 5246) and **TLS 1.3** (RFC 8446) are the versions in use today.
- TLS 1.0 and 1.1 are deprecated due to known vulnerabilities.
- Used by HTTPS, SMTPS, IMAPS, FTPS, and many other protocols.

## Where TLS Fits

TLS operates between the **transport layer** and the **application layer** — it encrypts
application data before it is sent over TCP.

```text
  +---------------------+
  | Application (HTTP)  |
  +---------------------+
  | TLS                 |  <-- encryption/decryption happens here
  +---------------------+
  | TCP                 |
  +---------------------+
  | IP                  |
  +---------------------+
```

## TLS Handshake (TLS 1.2)

The TLS handshake establishes the encrypted session. In TLS 1.2 it takes **two
round-trips**:

```text
  Client                                         Server
    |                                               |
    |--- ClientHello ------------------------------>|
    |    (supported cipher suites, TLS version,     |
    |     client random)                            |
    |                                               |
    |<-- ServerHello + Certificate + ServerKeyExchange + ServerHelloDone --|
    |    (chosen cipher, server random, public key) |
    |                                               |
    |--- ClientKeyExchange + ChangeCipherSpec       |
    |    + Finished -------------------------------->|
    |    (premaster secret encrypted with server    |
    |     public key)                               |
    |                                               |
    |<-- ChangeCipherSpec + Finished ---------------|
    |                                               |
    |======= Encrypted application data ============|
```

## TLS 1.3 Handshake

TLS 1.3 reduced the handshake to **one round-trip** (1-RTT) and supports **0-RTT**
for resumed connections:

```text
  Client                                         Server
    |                                               |
    |--- ClientHello + KeyShare ------------------>|
    |    (supported groups, key share,              |
    |     supported ciphers)                        |
    |                                               |
    |<-- ServerHello + KeyShare + EncryptedExtensions
    |    + Certificate + CertificateVerify          |
    |    + Finished --------------------------------|
    |                                               |
    |--- Finished --------------------------------->|
    |                                               |
    |======= Encrypted application data ============|
```

**Key TLS 1.3 improvements:**
- Removed insecure algorithms (RSA key exchange, RC4, SHA-1, CBC mode ciphers).
- Only supports **forward-secret** key exchanges (ECDHE, DHE).
- Encrypted more of the handshake (server certificate is encrypted).
- 0-RTT resumption for repeat connections (at the cost of replay risk).

## Key Concepts

### Symmetric vs Asymmetric Encryption in TLS

| Phase          | Type        | Purpose                                    |
|----------------|-------------|--------------------------------------------|
| Handshake      | Asymmetric  | Authenticate server, exchange key material |
| Data transfer  | Symmetric   | Encrypt/decrypt application data (fast)    |

The handshake uses asymmetric cryptography (slow but allows key exchange without a
pre-shared secret). Once both sides derive the **session keys**, all data is encrypted
with fast symmetric ciphers (AES-GCM, ChaCha20-Poly1305).

### Forward Secrecy

Forward secrecy (also called perfect forward secrecy, PFS) means that compromising a
server's long-term private key does not allow decryption of past sessions. This is
achieved by using **ephemeral Diffie-Hellman** (DHE or ECDHE) key exchanges — each
session generates new key pairs that are discarded after use.

### Certificates and Certificate Authorities

- A TLS **certificate** binds a domain name to a public key.
- Certificates are issued by **Certificate Authorities (CAs)** — trusted third parties.
- The client verifies the certificate chain up to a **root CA** stored in its trust store.
- **Let's Encrypt** provides free, automated TLS certificates.

```text
  Root CA (trusted by browsers)
       │
  Intermediate CA
       │
  Server Certificate (example.com)
       │
  Server's Public Key
```

## TLS Cipher Suite

A cipher suite defines the algorithms used for each phase:

```text
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
  │     │     │        │     │      │
  │     │     │        │     │      └─ PRF hash (key derivation)
  │     │     │        │     └──────── AEAD mode
  │     │     │        └────────────── Symmetric cipher + key size
  │     │     └─────────────────────── Authentication algorithm
  │     └───────────────────────────── Key exchange algorithm
  └─────────────────────────────────── Protocol
```

TLS 1.3 simplified cipher suite names (e.g., `TLS_AES_256_GCM_SHA384`) because key
exchange and authentication are negotiated separately.

## Common TLS Ports

| Protocol | Plaintext Port | TLS Port |
|----------|:--------------:|:--------:|
| HTTP     | 80             | 443      |
| SMTP     | 25             | 465/587  |
| IMAP     | 143            | 993      |
| POP3     | 110            | 995      |
| FTP      | 21             | 990      |
| LDAP     | 389            | 636      |

## Inspecting TLS Connections

```bash
# View the certificate and TLS details of a server
openssl s_client -connect example.com:443

# Show certificate details
openssl s_client -connect example.com:443 | openssl x509 -noout -text

# Test TLS 1.3 specifically
openssl s_client -connect example.com:443 -tls1_3

# Check certificate expiration
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

## Common TLS Vulnerabilities and Mitigations

| Vulnerability    | Description                                        | Mitigation                          |
|------------------|----------------------------------------------------|-------------------------------------|
| BEAST            | Attack on CBC ciphers in TLS 1.0                   | Use TLS 1.2+ and AEAD ciphers      |
| POODLE           | Downgrade attack forcing SSL 3.0                   | Disable SSL 3.0                     |
| Heartbleed       | OpenSSL bug leaking server memory                  | Patch OpenSSL; revoke affected certs|
| CRIME / BREACH   | Compression-based side-channel attacks             | Disable TLS compression             |
| Downgrade attacks| Attacker forces weaker protocol version            | TLS_FALLBACK_SCSV; use TLS 1.3     |

## SSL vs TLS

| Feature         | SSL 3.0           | TLS 1.2            | TLS 1.3            |
|-----------------|--------------------|--------------------|---------------------|
| Status          | Deprecated         | Widely used        | Current standard    |
| Handshake RTTs  | 2                  | 2                  | 1 (0-RTT possible)  |
| Forward secrecy | Optional           | Optional           | Required            |
| Cipher suites   | Includes weak ones | Many options       | Only strong ciphers |
| Certificate     | Sent in clear      | Sent in clear      | Encrypted           |
