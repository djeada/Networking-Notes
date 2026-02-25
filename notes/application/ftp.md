# FTP (File Transfer Protocol)

## Introduction

The File Transfer Protocol (FTP) is an application-layer protocol for transferring
files between a client and a server over a TCP network. It is one of the oldest internet
protocols, defined originally in **RFC 959**.

- Uses **TCP port 21** for control commands and **TCP port 20** for data transfer
  (in active mode).
- FTP transmits credentials and data in **plaintext** — it should be used only on
  trusted networks or replaced by SFTP/FTPS.

## How FTP Works

FTP uses **two separate TCP connections**:

```text
  Client                                    Server
    |                                          |
    |--- Control connection (port 21) -------->|
    |    (commands: USER, PASS, LIST, RETR)    |
    |                                          |
    |<== Data connection (port 20) ============|
    |    (file contents, directory listings)    |
    |                                          |
```

1. **Control connection** — Persistent connection used to send FTP commands and receive
   status replies. Stays open for the duration of the session.
2. **Data connection** — Opened separately for each file transfer or directory listing,
   then closed when the transfer completes.

## Active vs Passive Mode

### Active Mode

The server initiates the data connection back to the client.

```text
  Client                              Server
    |                                    |
    |-- PORT 192,168,1,10,19,136 ------->|  (client tells server its IP + port)
    |                                    |
    |<== Data connection FROM port 20 ===|  (server connects to client)
```

- Can cause problems when the client is behind a NAT or firewall (incoming connections
  may be blocked).

### Passive Mode

The client initiates the data connection to the server. More firewall-friendly.

```text
  Client                              Server
    |                                    |
    |-- PASV --------------------------->|
    |<-- 227 (192,168,1,1,39,12) --------|  (server tells client which port to use)
    |                                    |
    |=== Data connection TO server ======>|  (client connects to server)
```

Passive mode is the preferred mode for most modern FTP clients.

## Common FTP Commands

| Command   | Description                                |
|-----------|--------------------------------------------|
| `USER`    | Send username                              |
| `PASS`    | Send password                              |
| `LIST`    | List files in current directory             |
| `CWD`     | Change working directory                   |
| `PWD`     | Print working directory                    |
| `RETR`    | Retrieve (download) a file                 |
| `STOR`    | Store (upload) a file                      |
| `DELE`    | Delete a file                              |
| `MKD`     | Make a directory                           |
| `QUIT`    | End the FTP session                        |
| `TYPE`    | Set transfer mode (A = ASCII, I = Binary)  |
| `PASV`    | Enter passive mode                         |

## FTP Reply Codes

| Code Range | Category               | Examples                            |
|------------|------------------------|-------------------------------------|
| 1xx        | Positive preliminary   | `150` — File status OK, opening data connection |
| 2xx        | Positive completion    | `200` — OK, `226` — Transfer complete, `230` — Login successful |
| 3xx        | Positive intermediate  | `331` — Username OK, need password  |
| 4xx        | Transient negative     | `421` — Service not available       |
| 5xx        | Permanent negative     | `530` — Not logged in, `550` — File not found |

## FTP Security Variants

### FTPS (FTP Secure / FTP over TLS)

- Adds **TLS/SSL** encryption to standard FTP.
- Two modes:
  - **Explicit FTPS** — Client sends `AUTH TLS` command to upgrade the connection.
    Uses port 21 initially.
  - **Implicit FTPS** — Connection is TLS from the start. Typically uses port 990.

### SFTP (SSH File Transfer Protocol)

- **Not** related to FTP — it is a completely different protocol that runs over SSH.
- Uses a single **TCP port 22** connection (no separate data channel).
- Encrypted by default as part of the SSH session.
- Generally preferred over FTPS for simplicity and security.

### Comparison

| Feature            | FTP            | FTPS                  | SFTP             |
|--------------------|----------------|-----------------------|------------------|
| Encryption         | None           | TLS/SSL               | SSH              |
| Ports              | 21 + 20       | 21 (explicit) / 990   | 22               |
| Connections        | 2 (ctrl+data)  | 2 (ctrl+data)         | 1                |
| Firewall-friendly  | No (active)    | Somewhat              | Yes              |
| Authentication     | User/password  | User/password + cert  | Key or password  |

## Command-Line FTP Usage

```bash
# Connect to an FTP server
ftp ftp.example.com

# Or use lftp (more modern client with FTPS/SFTP support)
lftp -u username ftp.example.com

# Download a file with curl
curl -u username:password ftp://ftp.example.com/file.txt -o file.txt

# Upload a file with curl
curl -u username:password -T localfile.txt ftp://ftp.example.com/
```
