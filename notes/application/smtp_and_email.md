# SMTP and Email Protocols

## Introduction

Email delivery relies on a family of protocols — **SMTP** for sending mail, and
**POP3** or **IMAP** for retrieving it. Together they form the backbone of internet
email communication.

## How Email Works

```text
  Sender                                                    Recipient
  (alice@a.com)                                            (bob@b.com)
       |                                                        |
       |--- Compose message in email client (MUA) ------------>|
       |                                                        |
  [Mail Client]                                          [Mail Client]
       |                                                        ▲
       | SMTP                                            IMAP/POP3
       ▼                                                        |
  [SMTP Server]                                          [Mail Server]
  (a.com MTA)                                            (b.com MTA)
       |                                                        ▲
       |--- DNS MX lookup for b.com -----> [DNS]               |
       |                                                        |
       |--- SMTP delivery ─────────────────────────────────────>|
```

**Key terminology:**
- **MUA** (Mail User Agent) — The email client (Outlook, Thunderbird, Gmail web).
- **MTA** (Mail Transfer Agent) — The server that routes email (Postfix, Sendmail, Exchange).
- **MDA** (Mail Delivery Agent) — Delivers mail to the recipient's mailbox.

## SMTP (Simple Mail Transfer Protocol)

SMTP is used to **send and relay** email between servers.

- Uses **TCP port 25** (server-to-server relay), **port 587** (client submission with
  STARTTLS), or **port 465** (implicit TLS).
- Defined in **RFC 5321**.
- Text-based command/response protocol.

### SMTP Dialog Example

```text
  Client                                    Server
    |                                          |
    |--- EHLO client.example.com ------------->|
    |<-- 250 Hello client.example.com ---------|
    |                                          |
    |--- MAIL FROM:<alice@a.com> ------------->|
    |<-- 250 OK -------------------------------|
    |                                          |
    |--- RCPT TO:<bob@b.com> ----------------->|
    |<-- 250 OK -------------------------------|
    |                                          |
    |--- DATA -------------------------------->|
    |<-- 354 Start mail input -----------------|
    |                                          |
    |--- Subject: Hello                        |
    |    From: alice@a.com                     |
    |    To: bob@b.com                         |
    |                                          |
    |    This is the message body.             |
    |    . ---------------------------------->|
    |<-- 250 Message accepted -----------------|
    |                                          |
    |--- QUIT -------------------------------->|
    |<-- 221 Bye ------------------------------|
```

### Common SMTP Commands

| Command       | Description                                    |
|---------------|------------------------------------------------|
| `EHLO`        | Extended hello — identify the client            |
| `MAIL FROM:`  | Specify the sender's address                   |
| `RCPT TO:`    | Specify the recipient's address                |
| `DATA`        | Begin message content (ends with a lone `.`)   |
| `QUIT`        | Close the connection                           |
| `STARTTLS`    | Upgrade connection to TLS encryption           |
| `AUTH`        | Authenticate the client                        |

## POP3 (Post Office Protocol v3)

POP3 is used to **retrieve** email from a server.

- Uses **TCP port 110** (plaintext) or **port 995** (TLS).
- Defined in **RFC 1939**.
- Downloads messages to the client and typically **deletes them from the server**.
- Simple, lightweight protocol.

```text
  Client                          Server
    |                                |
    |--- USER alice ---------------->|
    |<-- +OK ------------------------|
    |--- PASS secret --------------->|
    |<-- +OK 3 messages -------------|
    |--- LIST ---------------------->|
    |<-- +OK (message list) ---------|
    |--- RETR 1 ------------------->|
    |<-- +OK (message content) ------|
    |--- DELE 1 ------------------->|
    |<-- +OK deleted ----------------|
    |--- QUIT ---------------------->|
```

## IMAP (Internet Message Access Protocol)

IMAP is used to **access and manage** email on the server.

- Uses **TCP port 143** (plaintext) or **port 993** (TLS).
- Defined in **RFC 9051** (IMAP4rev2).
- Messages **stay on the server** — synchronized across multiple devices.
- Supports folders, flags, search, and partial message fetching.

## POP3 vs IMAP

| Feature              | POP3                              | IMAP                               |
|----------------------|-----------------------------------|-------------------------------------|
| Message storage      | Downloaded to client              | Kept on server                      |
| Multi-device access  | Difficult (messages on one device)| Seamless (all devices see same mail)|
| Bandwidth usage      | Downloads all messages            | Can fetch headers only              |
| Server storage       | Minimal                           | Requires more server space          |
| Offline access       | Full (messages are local)         | Depends on client caching           |
| Folder management    | Not supported                     | Full server-side folder support     |
| Best for             | Single-device users               | Users with multiple devices         |

## Email Security

### SPF (Sender Policy Framework)

A DNS TXT record that lists which mail servers are authorized to send email for a domain.

```text
example.com.  IN  TXT  "v=spf1 mx ip4:192.0.2.0/24 -all"
```

### DKIM (DomainKeys Identified Mail)

The sending server signs each message with a private key. The recipient verifies the
signature using a public key published in DNS.

### DMARC (Domain-based Message Authentication, Reporting and Conformance)

Builds on SPF and DKIM. Tells receiving servers what to do when authentication fails
(none, quarantine, or reject) and provides reporting.

```text
  Email authentication stack:
  ┌──────────────────────┐
  │ DMARC                │  policy: reject, quarantine, or none
  ├──────────────────────┤
  │ DKIM    │  SPF       │  signature verification │ sender IP check
  ├──────────────────────┤
  │ SMTP (email delivery)│
  └──────────────────────┘
```

### STARTTLS vs Implicit TLS

- **STARTTLS** — Upgrade an existing plaintext connection to TLS. Used on ports 25, 587, 143.
- **Implicit TLS** — Connection starts encrypted immediately. Used on ports 465, 993, 995.

## Email Port Summary

| Protocol | Plaintext Port | TLS Port  | Purpose            |
|----------|:--------------:|:---------:|--------------------|
| SMTP     | 25             | 465 / 587 | Send / relay email |
| POP3     | 110            | 995       | Retrieve email     |
| IMAP     | 143            | 993       | Access email       |
