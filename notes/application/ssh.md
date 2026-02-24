# SSH (Secure Shell)

## Introduction

SSH (Secure Shell) is a cryptographic network protocol for secure remote login, command
execution, and file transfer over an unsecured network. It replaces insecure protocols
such as Telnet, rlogin, and plain FTP by encrypting all traffic between client and server.

- Uses **TCP port 22** by default.
- Current version is **SSH-2** (defined in RFCs 4251–4256).
- SSH-1 is deprecated due to security vulnerabilities.

## How SSH Works

SSH establishes a secure channel over an insecure network through a multi-step process:

```text
  Client                                         Server
    |                                               |
    |--- 1. TCP connection to port 22 ------------->|
    |                                               |
    |<-- 2. Server sends its public host key -------|
    |       (client verifies against known_hosts)   |
    |                                               |
    |--- 3. Key exchange (e.g., Diffie-Hellman) --->|
    |<-- (both derive shared session key) ----------|
    |                                               |
    |=== 4. Encrypted channel established ==========|
    |                                               |
    |--- 5. User authentication ------------------->|
    |       (password, public key, etc.)            |
    |                                               |
    |<-- 6. Shell / command session begins ---------|
```

### Key Exchange

The client and server negotiate a **shared secret** using algorithms like
Diffie-Hellman or Elliptic Curve Diffie-Hellman. This shared secret is used to derive
symmetric encryption keys for the session. Neither side ever sends the secret over the
wire.

### Host Verification

The first time a client connects to a server, it receives the server's **host key** and
stores it in `~/.ssh/known_hosts`. On subsequent connections, the client checks that the
server presents the same key — protecting against man-in-the-middle attacks.

## Authentication Methods

| Method              | Description                                                    |
|---------------------|----------------------------------------------------------------|
| **Password**        | User provides a password encrypted over the SSH channel.       |
| **Public key**      | Client proves possession of a private key matching a public key stored on the server. |
| **Keyboard-interactive** | Multi-step challenge-response (e.g., two-factor authentication). |
| **Certificate-based** | SSH certificates signed by a trusted CA, used in large environments. |

### Public Key Authentication

Public key authentication is the recommended method. It is more secure than passwords
and can be automated.

```text
  1. Generate key pair on client:
     ssh-keygen -t ed25519

  2. Copy public key to server:
     ssh-copy-id user@server
     (adds key to ~/.ssh/authorized_keys on server)

  3. Connect:
     ssh user@server
     (client proves it holds the private key; no password needed)
```

## Common SSH Commands

```bash
# Connect to a remote host
ssh user@hostname

# Connect on a non-standard port
ssh -p 2222 user@hostname

# Execute a single command remotely
ssh user@hostname "ls -la /var/log"

# Copy files with SCP
scp localfile.txt user@hostname:/remote/path/
scp user@hostname:/remote/file.txt ./local/path/

# Copy files with SFTP (interactive)
sftp user@hostname

# Generate a key pair
ssh-keygen -t ed25519 -C "comment"
```

## SSH Tunneling (Port Forwarding)

SSH can forward network traffic through an encrypted tunnel — useful for accessing
services behind firewalls or encrypting insecure protocols.

### Local Port Forwarding

Forward a local port to a remote destination through the SSH server:

```text
  Client:8080 ──(encrypted)──> SSH Server ──> target:80

  ssh -L 8080:target:80 user@sshserver
```

Traffic sent to `localhost:8080` on the client is forwarded through the SSH server
to `target:80`.

### Remote Port Forwarding

Make a local service accessible from the remote server:

```text
  SSH Server:9090 ──(encrypted)──> Client ──> localhost:3000

  ssh -R 9090:localhost:3000 user@sshserver
```

Anyone connecting to port 9090 on the SSH server is forwarded to port 3000 on the
client machine.

### Dynamic Port Forwarding (SOCKS Proxy)

Creates a SOCKS proxy on the client that routes traffic through the SSH server:

```bash
ssh -D 1080 user@sshserver
```

Configure applications to use `localhost:1080` as a SOCKS5 proxy.

## SSH Configuration

### Client Configuration (`~/.ssh/config`)

```text
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

After configuring, connect with just `ssh myserver`.

### Server Configuration (`/etc/ssh/sshd_config`)

Key security settings:

```text
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers admin deploy
```

## SSH vs Telnet

| Feature            | SSH                              | Telnet                          |
|--------------------|----------------------------------|---------------------------------|
| Encryption         | All traffic encrypted            | Plaintext (no encryption)       |
| Port               | 22                               | 23                              |
| Authentication     | Password, public key, MFA        | Password only (sent in clear)   |
| File transfer      | SCP, SFTP built-in               | None                            |
| Security           | Secure                           | Insecure — never use in production |
