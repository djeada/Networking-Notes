# SSH — Secure Shell

SSH (Secure Shell) is a cryptographic network protocol for secure remote login, command execution, file transfer, and port forwarding over an unsecured network. It is the standard tool for administering remote servers.

SSH uses **asymmetric encryption** (RSA, ECDSA, Ed25519) for authentication and **symmetric encryption** (AES, ChaCha20) for the data channel.

---

## How SSH Works

```text
  Client                                   Server
    │                                         │
    │──── TCP SYN ──────────────────────────>│  port 22
    │<─── TCP SYN-ACK ───────────────────────│
    │──── TCP ACK ──────────────────────────>│
    │                                         │
    │   ┌─── Protocol Version Exchange ──┐   │
    │   │  SSH-2.0-OpenSSH_8.9p1         │   │
    │   └────────────────────────────────┘   │
    │                                         │
    │   ┌─── Key Exchange (KEX) ──────────┐  │
    │   │  Diffie-Hellman / ECDH          │  │
    │   │  → derive shared session key    │  │
    │   └────────────────────────────────┘   │
    │                                         │
    │   ┌─── Authentication ──────────────┐  │
    │   │  password / public key / etc.   │  │
    │   └────────────────────────────────┘   │
    │                                         │
    │   ┌─── Encrypted Channel ───────────┐  │
    │   │  shell / SFTP / port forward    │  │
    │   └────────────────────────────────┘   │
```

---

## Basic Connections

```bash
# Connect to a remote host (default port 22)
ssh user@hostname
ssh user@192.168.1.100

# Connect on a non-default port
ssh -p 2222 user@hostname

# Specify an identity file (private key)
ssh -i ~/.ssh/id_ed25519 user@hostname

# Run a single command and exit
ssh user@hostname 'ls -la /var/log'

# Enable verbose output for debugging
ssh -v user@hostname       # -vv or -vvv for more detail
```

---

## SSH Key Authentication

Key-based authentication is more secure and convenient than passwords. It relies on a **key pair**: a private key (kept secret on your machine) and a public key (placed on the server).

### Generate a Key Pair

```bash
# Ed25519 (recommended — fast, small, secure)
ssh-keygen -t ed25519 -C "your_email@example.com"

# RSA 4096-bit (widely supported alternative)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# The command prompts for a file path and optional passphrase
# Default: ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public)
```

### Copy Public Key to Server

```bash
# Automated method (Linux/macOS)
ssh-copy-id user@hostname

# Specify a key explicitly
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname

# Manual method (if ssh-copy-id is unavailable)
cat ~/.ssh/id_ed25519.pub | ssh user@hostname 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```

### File Permissions (critical)

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519       # private key — must be readable only by owner
chmod 644 ~/.ssh/id_ed25519.pub   # public key
chmod 600 ~/.ssh/authorized_keys  # on the server
```

---

## SSH Config File (`~/.ssh/config`)

The config file lets you define shortcuts and settings for hosts you connect to frequently.

```text
# ~/.ssh/config

Host myserver
    HostName 192.168.1.100
    User alice
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

Host bastion
    HostName jump.example.com
    User ec2-user
    IdentityFile ~/.ssh/aws_key.pem

Host prod-via-bastion
    HostName 10.0.1.50
    User ubuntu
    ProxyJump bastion
    IdentityFile ~/.ssh/id_ed25519
```

With this config, `ssh myserver` is equivalent to the full `ssh -i ~/.ssh/id_ed25519 -p 22 alice@192.168.1.100`.

---

## File Transfer

### scp (Secure Copy)

```bash
# Copy a file from local to remote
scp file.txt user@hostname:/remote/path/

# Copy a file from remote to local
scp user@hostname:/remote/file.txt ./local/

# Copy a directory recursively
scp -r /local/dir user@hostname:/remote/

# Use a specific port
scp -P 2222 file.txt user@hostname:/remote/

# Use a specific key
scp -i ~/.ssh/id_ed25519 file.txt user@hostname:/remote/
```

### sftp (SSH File Transfer Protocol)

```bash
sftp user@hostname              # Interactive SFTP session

# SFTP commands:
# ls              - list remote directory
# lls             - list local directory
# cd / lcd        - change remote / local directory
# get file        - download a file
# put file        - upload a file
# mget *.log      - download multiple files
# mput *.csv      - upload multiple files
# mkdir / rmdir   - create / remove remote directory
# rm              - delete remote file
# exit            - quit
```

### rsync over SSH

```bash
# Sync local directory to remote (efficient, only transfers changes)
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Sync remote to local
rsync -avz user@hostname:/remote/dir/ /local/dir/

# Dry run (show what would be transferred without doing it)
rsync -avzn /local/dir/ user@hostname:/remote/dir/

# Exclude files
rsync -avz --exclude '*.tmp' /local/dir/ user@hostname:/remote/dir/
```

---

## Port Forwarding (SSH Tunneling)

SSH can forward arbitrary TCP connections through the encrypted channel, effectively creating a VPN-like tunnel for specific ports.

### Local Port Forwarding

Forwards a local port to a remote host:port via the SSH server. Useful for accessing services on the remote network that are not exposed directly.

```bash
# Forward local port 8080 to remote:80
ssh -L 8080:localhost:80 user@ssh-server

# Access a database on the remote network through the SSH server
ssh -L 5432:db-server:5432 user@ssh-server

# Now connect to localhost:8080 / localhost:5432 locally
```

```text
  Local Machine         SSH Server            Remote Service
     :8080    ─────────────────────────────>    :80
              (encrypted SSH tunnel)
```

### Remote Port Forwarding

Exposes a local service to the remote network through the SSH server. Useful for making a local service temporarily accessible from the internet.

```bash
# Expose local port 3000 as port 8080 on the SSH server
ssh -R 8080:localhost:3000 user@ssh-server

# Anyone connecting to ssh-server:8080 is forwarded to your local :3000
```

### Dynamic Port Forwarding (SOCKS Proxy)

Creates a local SOCKS5 proxy that routes all traffic through the SSH server.

```bash
ssh -D 1080 user@ssh-server

# Then configure your browser/app to use SOCKS5 proxy at 127.0.0.1:1080
# All traffic is routed through the SSH server
curl --socks5 127.0.0.1:1080 https://example.com
```

---

## Jump Hosts (Bastion Servers)

A jump host (bastion host) is an intermediate SSH server used to reach hosts on an internal network.

```bash
# Connect to internal-host via jump-host in a single command
ssh -J user@jump-host user@internal-host

# Multiple jumps
ssh -J user@jump1,user@jump2 user@final-host

# In ~/.ssh/config
Host internal
    HostName 10.0.1.50
    ProxyJump bastion
```

---

## SSH Agent

`ssh-agent` caches your decrypted private keys in memory so you do not need to enter the passphrase every time.

```bash
# Start the agent
eval "$(ssh-agent -s)"

# Add your key to the agent
ssh-add ~/.ssh/id_ed25519

# List loaded keys
ssh-add -l

# Remove all keys from agent
ssh-add -D
```

---

## Server Configuration (`/etc/ssh/sshd_config`)

Key settings for hardening an SSH server:

```text
Port 22                        # Change to a non-standard port to reduce noise
PermitRootLogin no             # Disallow root login
PasswordAuthentication no      # Require key-based auth; disable passwords
PubkeyAuthentication yes       # Allow public key authentication
AuthorizedKeysFile .ssh/authorized_keys
AllowUsers alice bob           # Whitelist specific users
MaxAuthTries 3                 # Limit authentication attempts
X11Forwarding no               # Disable X11 forwarding if not needed
ClientAliveInterval 300        # Disconnect idle sessions after 5 minutes
ClientAliveCountMax 2
Banner /etc/issue.net          # Display a login banner
```

After editing, restart the SSH daemon:
```bash
sudo systemctl restart sshd
```

---

## Troubleshooting

```bash
# Debug connection issues
ssh -vvv user@hostname

# Check if sshd is running on the server
sudo systemctl status sshd

# Check sshd logs
sudo journalctl -u sshd -n 50

# Test if port 22 is open
nmap -p 22 hostname
nc -zv hostname 22

# Verify authorized_keys permissions on the server
ls -la ~/.ssh/
stat ~/.ssh/authorized_keys
```

### Common Errors

| Error                                         | Likely Cause                                       |
|:----------------------------------------------|:---------------------------------------------------|
| `Connection refused`                          | SSH daemon not running or port blocked by firewall |
| `Permission denied (publickey)`               | Key not in `authorized_keys` or wrong permissions  |
| `WARNING: REMOTE HOST IDENTIFICATION CHANGED` | Server host key changed (possible MITM or host rebuild) |
| `Too many authentication failures`            | Agent has too many keys; use `-i` to specify one   |
| `Connection timed out`                        | Firewall blocking port 22, or host unreachable     |
| `Host key verification failed`                | Known hosts entry mismatch                         |

To resolve a changed host key:
```bash
ssh-keygen -R hostname    # Remove old entry from known_hosts
```
