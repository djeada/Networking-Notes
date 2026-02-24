# Cryptography Algorithms

## Introduction

Cryptography is the foundation of secure communication in modern networks. It provides
four essential security properties:

- **Confidentiality** — Only authorized parties can read the data
- **Integrity** — Data has not been altered in transit
- **Authentication** — The sender is who they claim to be
- **Non-repudiation** — The sender cannot deny having sent the message

Every time you visit an HTTPS website, send an encrypted email, or connect to a VPN,
cryptographic algorithms are working behind the scenes to protect your data.

---

## Symmetric vs Asymmetric Encryption

There are two fundamental approaches to encryption:

| Property | Symmetric | Asymmetric |
|---|---|---|
| Keys used | Same key to encrypt and decrypt | Public key encrypts, private key decrypts |
| Speed | Fast | Slow |
| Key distribution | Difficult (must share secret key securely) | Easy (public key can be shared openly) |
| Common use | Bulk data encryption | Key exchange, digital signatures |

```text
Symmetric Encryption
====================

        Shared Secret Key (K)
              |
    +---------+---------+
    |                   |
    v                   v
+--------+         +--------+
| Sender |         |Receiver|
|        |         |        |
| Plain  |---K--->| Cipher |---K--->| Plain  |
| Text   | Encrypt| Text   | Decrypt| Text   |
+--------+         +--------+        +--------+


Asymmetric Encryption
=====================

  Receiver's          Receiver's
  Public Key          Private Key
     |                    |
     v                    v
+--------+          +--------+
| Sender |          |Receiver|
|        |          |        |
| Plain  |--PubK-->| Cipher |--PrivK-->| Plain  |
| Text   | Encrypt | Text   | Decrypt  | Text   |
+--------+          +--------+          +--------+
```

In practice, both are used together. Asymmetric encryption secures the initial key
exchange, then symmetric encryption handles the bulk data transfer (this is exactly
how TLS works).

---

## Key Requirements

### Symmetric Keys

- **Formula**: n * (n - 1) / 2 keys are needed for n nodes
- **Reason**: Every unique pair of nodes requires its own shared secret key

For example, with 4 nodes you need 4 * 3 / 2 = **6 keys**. With 100 nodes you
need 100 * 99 / 2 = **4,950 keys**. This scales poorly.

```text
Key Distribution for 4 Nodes (Symmetric)
=========================================

  Keys needed: 4 * (4-1) / 2 = 6

      A ----K1---- B
      |  \      /  |
      |   K3  K4   |
      |    \  /    |
     K2     \/    K5
      |     /\     |
      |   K4  \    |
      |  /     \   |
      C ----K6---- D

  K1 = Key(A,B)    K4 = Key(B,C)
  K2 = Key(A,C)    K5 = Key(B,D)
  K3 = Key(A,D)    K6 = Key(C,D)

  Each pair has a unique key: AB, AC, AD, BC, BD, CD = 6 keys
```

### Asymmetric (Public) Keys

- **Formula**: 2 * n keys are needed for n nodes
- **Reason**: Each node has one public key and one private key

For 4 nodes you need 2 * 4 = **8 keys**. For 100 nodes, only **200 keys**.
This scales much better.

```text
Key Distribution for 4 Nodes (Asymmetric)
==========================================

  Keys needed: 2 * 4 = 8

      A (PubA, PrivA)
      B (PubB, PrivB)
      C (PubC, PrivC)
      D (PubD, PrivD)

  Anyone can encrypt with a node's public key.
  Only that node can decrypt with its private key.

      A ---encrypt with PubB---> B (decrypts with PrivB)
      C ---encrypt with PubA---> A (decrypts with PrivA)
```

---

## Major Algorithms

### RSA (Rivest-Shamir-Adleman)

RSA is the most widely used asymmetric encryption algorithm. Its security relies on
the mathematical difficulty of factoring the product of two large prime numbers.

**How RSA Works — Step by Step:**

1. **Key Generation**
   - Choose two large prime numbers: p and q
   - Compute n = p * q
   - Compute the totient: phi(n) = (p - 1) * (q - 1)
   - Choose public exponent e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
   - Compute private exponent d such that d * e mod phi(n) = 1

2. **Encryption**
   - Ciphertext C = M^e mod n (where M is the plaintext message as a number)

3. **Decryption**
   - Plaintext M = C^d mod n

```text
RSA Key Generation and Usage
=============================

  Step 1: Key Generation
  ----------------------
  Choose primes:      p = 61, q = 53
  Compute n:          n = 61 * 53 = 3233
  Compute phi(n):     phi = 60 * 52 = 3120
  Choose e:           e = 17        (gcd(17, 3120) = 1)
  Compute d:          d = 2753      (2753 * 17 mod 3120 = 1)

  Public Key:  (e, n) = (17, 3233)   --> shared openly
  Private Key: (d, n) = (2753, 3233) --> kept secret

  Step 2: Encryption (Sender uses receiver's public key)
  ------------------------------------------------------
  Message M = 65
  C = 65^17 mod 3233 = 2790

  Step 3: Decryption (Receiver uses their private key)
  ----------------------------------------------------
  M = 2790^2753 mod 3233 = 65  --> original message recovered

  +--------+                          +----------+
  | Sender |  -- C = M^e mod n ---->  | Receiver |
  |        |                          |          |
  | knows: |                          | knows:   |
  |  PubKey|                          |  PrivKey |
  |  (e,n) |                          |  (d,n)   |
  +--------+                          +----------+
```

### Diffie-Hellman Key Exchange

Diffie-Hellman allows two parties to establish a shared secret key over an insecure
channel without ever transmitting the key itself. It is used for key agreement, not
for encryption directly.

**How it works:**

1. Alice and Bob agree on public parameters: a large prime p and a generator g
2. Alice picks a secret number x, computes R1 = g^x mod p, sends R1 to Bob
3. Bob picks a secret number y, computes R2 = g^y mod p, sends R2 to Alice
4. Alice computes the shared secret: K = R2^x mod p = g^(xy) mod p
5. Bob computes the shared secret: K = R1^y mod p = g^(xy) mod p
6. Both now have the same key K without it ever crossing the network

```text
Diffie-Hellman Key Exchange
============================

  Public parameters: p (prime), g (generator)

  Alice                                          Bob
  =====                                          ===
  Secret: x                                      Secret: y
  Compute: R1 = g^x mod p                        Compute: R2 = g^y mod p
    |                                              |
    |              R1 (public value)                |
    |--------------------------------------------->>|
    |                                              |
    |              R2 (public value)                |
    |<<---------------------------------------------|
    |                                              |
  K = R2^x mod p                            K = R1^y mod p
    = (g^y)^x mod p                           = (g^x)^y mod p
    = g^(xy) mod p                            = g^(xy) mod p
    |                                              |
    +--- Same shared secret K! -------------------+

  An eavesdropper sees: p, g, R1, R2
  But cannot compute K without knowing x or y
  (This is the Discrete Logarithm Problem)
```

### AES (Advanced Encryption Standard)

AES is a symmetric block cipher adopted as the encryption standard by NIST in 2001,
replacing DES. It is the most widely used symmetric encryption algorithm today.

- **Type**: Symmetric block cipher
- **Block size**: 128 bits
- **Key sizes**: 128, 192, or 256 bits
- **Rounds**: 10 (128-bit), 12 (192-bit), or 14 (256-bit) rounds of substitution and permutation
- **Used in**: TLS, VPNs (IPsec), Wi-Fi (WPA2/WPA3), disk encryption, and more

AES operates on a 4x4 grid of bytes called the "state" and applies multiple rounds of:
SubBytes, ShiftRows, MixColumns, and AddRoundKey transformations.

### DES and 3DES (Historical)

- **DES (Data Encryption Standard)**: Adopted in 1977. Uses a 56-bit key and 64-bit
  block size. Considered insecure today because the key is too short — it can be
  brute-forced in hours.
- **3DES (Triple DES)**: Applies DES three times with two or three different keys,
  giving an effective key length of 112 or 168 bits. Much slower than AES and now
  deprecated by NIST (as of 2023).

---

## Hashing Algorithms

Hash functions take an input of any size and produce a fixed-size output (the hash or
digest). They are **one-way functions** — you cannot recover the original input from
the hash. Hashing is used for data integrity verification, password storage, and
digital signatures.

Properties of a good cryptographic hash:
- **Deterministic** — Same input always gives the same output
- **Fast to compute** — Efficient for large data
- **Pre-image resistant** — Cannot reverse the hash to find the input
- **Collision resistant** — Hard to find two different inputs with the same hash
- **Avalanche effect** — A small change in input produces a completely different hash

### Common Hash Algorithms

| Algorithm | Output Size | Status | Notes |
|---|---|---|---|
| MD5 | 128 bits | **Broken** | Vulnerable to collisions; do not use for security |
| SHA-1 | 160 bits | **Deprecated** | Collision attacks demonstrated in 2017 |
| SHA-256 | 256 bits | **Secure** | Part of SHA-2 family; widely used today |
| SHA-384 | 384 bits | **Secure** | Part of SHA-2 family |
| SHA-512 | 512 bits | **Secure** | Part of SHA-2 family |
| SHA-3 | 224-512 bits | **Secure** | Different internal structure (Keccak) |

### HMAC (Hash-Based Message Authentication Code)

HMAC combines a hash function with a secret key to provide both integrity and
authentication. It is computed as:

    HMAC(K, M) = Hash((K xor opad) || Hash((K xor ipad) || M))

HMAC is used in TLS, IPsec, and API authentication.

---

## Digital Signatures

A digital signature provides authentication, integrity, and non-repudiation. It
proves that a message was created by the claimed sender and has not been altered.

**How digital signatures work:**

1. The sender hashes the message to create a digest
2. The sender encrypts the digest with their **private key** (this is the signature)
3. The receiver decrypts the signature with the sender's **public key**
4. The receiver hashes the received message independently
5. If the two hashes match, the signature is valid

```text
Digital Signature Process
=========================

  Sender (Alice)                           Receiver (Bob)
  ==============                           ===============

  Original                                 Received
  Message                                  Message
     |                                        |
     v                                        v
  +------+                                +------+
  | Hash |                                | Hash |
  +------+                                +------+
     |                                        |
     v                                        v
  Digest_1                                Digest_2
     |                                        |
     v                                        |
  +------------------+                        |
  | Encrypt with     |                        |
  | Alice's PRIVATE  |                        |
  | key              |                        |
  +------------------+                        |
     |                                        |
     v                                        |
  Signature -------- sent with message --->>  |
                                              v
                                     +------------------+
                                     | Decrypt with     |
                                     | Alice's PUBLIC   |
                                     | key              |
                                     +------------------+
                                              |
                                              v
                                          Digest_1'
                                              |
                                     +------------------+
                                     | Compare          |
                                     | Digest_1' == Digest_2? |
                                     +------------------+
                                        |           |
                                      YES          NO
                                        |           |
                                     Valid       Tampered /
                                     Signature   Forged
```

---

## TLS/SSL and HTTPS

TLS (Transport Layer Security) is the protocol that secures HTTPS connections. It
combines asymmetric encryption, symmetric encryption, hashing, and digital signatures
to establish a secure channel.

### TLS 1.2 Handshake

```text
TLS 1.2 Handshake
==================

  Client                                        Server
  ======                                        ======
     |                                             |
     |  1. ClientHello                             |
     |  (supported ciphers, random number)         |
     |-------------------------------------------->>|
     |                                             |
     |  2. ServerHello                             |
     |  (chosen cipher, random number)             |
     |<<--------------------------------------------|
     |                                             |
     |  3. Server Certificate                      |
     |  (server's public key + CA signature)       |
     |<<--------------------------------------------|
     |                                             |
     |  4. ServerHelloDone                         |
     |<<--------------------------------------------|
     |                                             |
     |  [Client verifies certificate]              |
     |                                             |
     |  5. ClientKeyExchange                       |
     |  (pre-master secret encrypted with          |
     |   server's public key)                      |
     |-------------------------------------------->>|
     |                                             |
     |  [Both derive session keys from             |
     |   pre-master secret + random numbers]       |
     |                                             |
     |  6. ChangeCipherSpec                        |
     |-------------------------------------------->>|
     |                                             |
     |  7. Finished (encrypted)                    |
     |-------------------------------------------->>|
     |                                             |
     |  8. ChangeCipherSpec                        |
     |<<--------------------------------------------|
     |                                             |
     |  9. Finished (encrypted)                    |
     |<<--------------------------------------------|
     |                                             |
     |  ========= Secure Channel ==========       |
     |  (All data encrypted with AES using         |
     |   the derived session keys)                 |
     |<------------------------------------------>>|
```

**Key points:**
- Steps 1–4 use **asymmetric encryption** (RSA or Diffie-Hellman) for key exchange
- Steps 6–9 onward use **symmetric encryption** (AES) for speed
- The server certificate is verified using **digital signatures** from a Certificate Authority
- Message integrity is ensured using **HMAC**

### TLS 1.3 Improvements

TLS 1.3 (2018) simplifies the handshake to just one round-trip, removes insecure
algorithms (RSA key exchange, DES, RC4, MD5, SHA-1), and mandates forward secrecy
using Diffie-Hellman.

---

## Algorithm Comparison

| Algorithm | Type | Key Size (bits) | Use Case |
|---|---|---|---|
| AES | Symmetric | 128, 192, 256 | Bulk data encryption (TLS, VPN, disk) |
| DES | Symmetric | 56 | Legacy systems (insecure, deprecated) |
| 3DES | Symmetric | 112 or 168 | Legacy systems (deprecated since 2023) |
| RSA | Asymmetric | 2048, 3072, 4096 | Key exchange, digital signatures |
| Diffie-Hellman | Key Exchange | 2048+ | Establishing shared secrets |
| ECDH | Key Exchange | 256, 384 | Efficient key exchange (elliptic curves) |
| ECDSA | Asymmetric | 256, 384 | Digital signatures (elliptic curves) |
| MD5 | Hash | 128 (output) | Checksums only (broken for security) |
| SHA-1 | Hash | 160 (output) | Legacy (deprecated) |
| SHA-256 | Hash | 256 (output) | Integrity, certificates, blockchain |
| SHA-3 | Hash | 224–512 (output) | Modern alternative to SHA-2 |

---

## Conclusion

Understanding cryptographic algorithms is essential for implementing and
troubleshooting secure network communication. In practice, these algorithms are
combined in protocol suites like TLS, IPsec, and SSH:

- **Asymmetric algorithms** (RSA, Diffie-Hellman) handle key exchange and signatures
- **Symmetric algorithms** (AES) handle fast bulk encryption
- **Hash functions** (SHA-256) ensure data integrity
- **Digital signatures** provide authentication and non-repudiation

Always use current, well-vetted algorithms with recommended key sizes. Avoid
deprecated algorithms (DES, MD5, SHA-1, RC4) in any new implementation.
