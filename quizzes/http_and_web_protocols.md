
#### Q. Which HTTP method is used to retrieve data from a server without modifying any resources?

* [x] GET
* [ ] POST
* [ ] PUT
* [ ] DELETE

#### Q. What is the default port number for unencrypted HTTP traffic?

* [x] 80
* [ ] 443
* [ ] 8080
* [ ] 22

#### Q. Which HTTP status code indicates that the requested resource was not found on the server?

* [x] 404
* [ ] 403
* [ ] 500
* [ ] 302

#### Q. What transport protocol does HTTP/3 use instead of TCP?

* [x] QUIC (built on UDP)
* [ ] SCTP
* [ ] DCCP
* [ ] Raw UDP

#### Q. Which key feature of HTTP/2 allows multiple requests and responses to be sent simultaneously over a single TCP connection?

* [x] Multiplexed streams
* [ ] Persistent connections
* [ ] Chunked transfer encoding
* [ ] Pipelining

#### Q. What does FTP use port 21 for?

* [x] Control commands and responses
* [ ] Transferring file data
* [ ] Encrypted authentication
* [ ] Passive mode data connections

#### Q. Which FTP mode is more compatible with firewalls and NAT because the client initiates both control and data connections?

* [x] Passive mode
* [ ] Active mode
* [ ] Binary mode
* [ ] Extended mode

#### Q. What is the primary security concern with standard FTP?

* [x] Credentials and data are transmitted in plaintext
* [ ] It only supports small file transfers
* [ ] It cannot handle binary files
* [ ] It does not support directory listing

#### Q. Which protocol provides encrypted file transfer over SSH and uses a single connection on port 22?

* [x] SFTP
* [ ] FTPS
* [ ] SCP
* [ ] FTP

#### Q. What port does SSH use by default?

* [x] 22
* [ ] 23
* [ ] 443
* [ ] 3389

#### Q. Which authentication method is generally considered more secure and suitable for automated SSH access than passwords?

* [x] Public key authentication
* [ ] Password authentication
* [ ] Keyboard-interactive authentication
* [ ] Anonymous authentication

#### Q. What does the SMTP protocol handle in email communication?

* [x] Sending and relaying email messages between mail servers
* [ ] Retrieving email messages from a mail server
* [ ] Encrypting email attachments
* [ ] Filtering spam messages

#### Q. Which port is recommended for email client submission with STARTTLS encryption?

* [x] 587
* [ ] 25
* [ ] 110
* [ ] 143

#### Q. What is the main difference between POP3 and IMAP for retrieving email?

* [x] POP3 typically downloads and removes messages from the server, while IMAP keeps messages on the server for multi-device access
* [ ] POP3 is encrypted by default, while IMAP is not
* [ ] IMAP can only retrieve text emails, while POP3 handles attachments
* [ ] POP3 uses port 993, while IMAP uses port 995

#### Q. What is the relationship between TLS and SSL?

* [x] TLS is the successor to SSL and provides improved security
* [ ] TLS and SSL are two completely unrelated protocols
* [ ] SSL is the newer and more secure of the two protocols
* [ ] TLS is used only for web traffic, while SSL is used for email

#### Q. How many round trips does the TLS 1.3 handshake require compared to TLS 1.2?

* [x] TLS 1.3 requires 1 round trip, while TLS 1.2 requires 2
* [ ] Both require the same number of round trips
* [ ] TLS 1.3 requires 2 round trips, while TLS 1.2 requires 3
* [ ] TLS 1.3 requires 0 round trips in all cases

#### Q. What does Perfect Forward Secrecy (PFS) ensure in TLS connections?

* [x] That past session traffic cannot be decrypted even if the server's long-term private key is compromised
* [ ] That the connection will never be interrupted by network errors
* [ ] That both client and server are fully authenticated before any data is sent
* [ ] That data is compressed before encryption to save bandwidth

#### Q. Which HTTP status code range indicates a server-side error?

* [x] 5xx
* [ ] 4xx
* [ ] 3xx
* [ ] 2xx

#### Q. Which email authentication mechanism uses DNS TXT records to specify which mail servers are authorized to send email for a domain?

* [x] SPF (Sender Policy Framework)
* [ ] DKIM (DomainKeys Identified Mail)
* [ ] DMARC (Domain-based Message Authentication, Reporting and Conformance)
* [ ] S/MIME

#### Q. What is the primary purpose of a digital certificate in TLS?

* [x] To bind a domain name to a public key and verify the server's identity
* [ ] To encrypt all data with symmetric encryption
* [ ] To store the server's private key securely
* [ ] To compress data before transmission
