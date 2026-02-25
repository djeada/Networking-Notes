# curl — Transferring Data with URLs

`curl` (Client URL) is a command-line tool for transferring data using various network protocols. It supports HTTP, HTTPS, FTP, SFTP, SMTP, and many others. For networking purposes it is the go-to tool for testing HTTP/HTTPS endpoints, inspecting headers, and diagnosing web services.

---

## Basic Usage

```bash
curl https://example.com                  # GET request, print response body
curl -o output.html https://example.com  # Save response to a file
curl -O https://example.com/file.zip     # Save with the remote filename
curl -L https://example.com              # Follow redirects
curl -s https://example.com              # Silent mode (no progress bar)
curl -v https://example.com              # Verbose (show request + response headers)
curl -I https://example.com              # HEAD request (headers only, no body)
```

---

## HTTP Methods

```bash
# GET (default)
curl https://api.example.com/users

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H 'Content-Type: application/json' \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# PUT
curl -X PUT https://api.example.com/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"name": "Alice Updated"}'

# DELETE
curl -X DELETE https://api.example.com/users/1

# PATCH
curl -X PATCH https://api.example.com/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"email": "new@example.com"}'
```

---

## Request Headers

```bash
# Add a custom header
curl -H 'Authorization: Bearer mytoken123' https://api.example.com/data

# Add multiple headers
curl -H 'Accept: application/json' \
     -H 'X-API-Key: abc123' \
     https://api.example.com/data

# Send a specific User-Agent
curl -A 'Mozilla/5.0 (compatible; MyBot/1.0)' https://example.com
```

---

## Inspecting Response Headers

```bash
# Show response headers only (HEAD request)
curl -I https://example.com

# Show both headers and body
curl -i https://example.com

# Verbose: shows request headers, response headers, and body
curl -v https://example.com

# Very verbose (debug-level TLS info)
curl --trace-ascii debug.txt https://example.com
```

Example `-I` output:
```text
HTTP/2 200
content-type: text/html; charset=UTF-8
content-length: 1256
server: ECS (nyb/1D10)
cache-control: max-age=604800
date: Tue, 01 Jan 2026 00:00:00 GMT
```

### Reading Header Output

| Header             | Meaning                                  |
|:-------------------|:-----------------------------------------|
| `HTTP/1.1 200 OK` | Protocol version and status code         |
| `Content-Type`     | MIME type of the response body           |
| `Content-Length`   | Size of the response body in bytes       |
| `Cache-Control`    | Caching directives                       |
| `ETag`             | Entity tag for cache validation          |

---

## HTTP Status Codes

| Code | Meaning                       | Common Cause                            |
|:-----|:------------------------------|:----------------------------------------|
| 200  | OK                            | Request succeeded                       |
| 201  | Created                       | Resource created (POST)                 |
| 301  | Moved Permanently             | Redirect to new URL                     |
| 302  | Found (Temporary Redirect)    | Temporary redirect                      |
| 400  | Bad Request                   | Malformed request syntax                |
| 401  | Unauthorized                  | Authentication required                 |
| 403  | Forbidden                     | Authenticated but not authorized        |
| 404  | Not Found                     | Resource does not exist                 |
| 429  | Too Many Requests             | Rate limit exceeded                     |
| 500  | Internal Server Error         | Server-side error                       |
| 502  | Bad Gateway                   | Upstream server returned invalid response |
| 503  | Service Unavailable           | Server overloaded or down               |
| 504  | Gateway Timeout               | Upstream server timed out               |

```bash
# Print only the HTTP status code
curl -o /dev/null -s -w '%{http_code}\n' https://example.com
```

---

## Authentication

```bash
# HTTP Basic Auth
curl -u username:password https://example.com/protected

# Bearer token (OAuth2 / JWT)
curl -H 'Authorization: Bearer eyJhbGci...' https://api.example.com/data

# API key as a query parameter
curl 'https://api.example.com/data?api_key=abc123'

# Digest authentication
curl --digest -u username:password https://example.com/digest
```

---

## Cookies

```bash
# Send a cookie with a request
curl -b 'session=abc123' https://example.com

# Save cookies from a response to a file
curl -c cookies.txt https://example.com/login -d 'user=alice&pass=secret'

# Send saved cookies with a subsequent request
curl -b cookies.txt https://example.com/dashboard
```

---

## HTTPS / TLS

```bash
# Ignore SSL certificate errors (INSECURE — use only for testing)
curl -k https://self-signed.example.com

# Specify a custom CA certificate
curl --cacert /path/to/ca.crt https://example.com

# Use a client certificate (mutual TLS)
curl --cert /path/to/client.crt --key /path/to/client.key https://example.com

# Show TLS certificate information
curl -v --head https://example.com 2>&1 | grep -E 'SSL|TLS|cert|expire'
```

---

## Uploading Files

```bash
# Upload a file using multipart form (like a browser form upload)
curl -F 'file=@/path/to/photo.jpg' https://api.example.com/upload

# Upload raw file content (PUT)
curl -X PUT -T /path/to/file.txt https://example.com/upload

# Send form data (URL-encoded, like a standard HTML form)
curl -d 'username=alice&password=secret' https://example.com/login
```

---

## Timeouts and Retries

```bash
# Set connection timeout to 5 seconds
curl --connect-timeout 5 https://example.com

# Set maximum total time to 10 seconds
curl --max-time 10 https://example.com

# Retry on transient errors (3 retries, 5-second delay)
curl --retry 3 --retry-delay 5 https://example.com

# Retry on HTTP errors (4xx / 5xx) as well
curl --retry 3 --retry-all-errors https://example.com
```

---

## Measuring Performance

```bash
# Print detailed timing breakdown
curl -o /dev/null -s -w "
    namelookup:    %{time_namelookup}s
    connect:       %{time_connect}s
    appconnect:    %{time_appconnect}s
    pretransfer:   %{time_pretransfer}s
    redirect:      %{time_redirect}s
    starttransfer: %{time_starttransfer}s
    total:         %{time_total}s
    size:          %{size_download} bytes
" https://example.com
```

| Metric           | Meaning                                                   |
|:-----------------|:----------------------------------------------------------|
| `namelookup`     | Time for DNS resolution                                   |
| `connect`        | Time to establish TCP connection                          |
| `appconnect`     | Time to complete TLS handshake (0 for HTTP)               |
| `pretransfer`    | Time until transfer begins (after protocol negotiation)   |
| `starttransfer`  | Time to receive the first byte (TTFB)                     |
| `total`          | Total time for the complete request                       |

---

## Proxy Support

```bash
# Use an HTTP proxy
curl -x http://proxy.example.com:8080 https://target.example.com

# Use a SOCKS5 proxy
curl --socks5 127.0.0.1:1080 https://target.example.com

# Bypass proxy for specific hosts
curl --noproxy 'localhost,192.168.1.0/24' https://example.com
```

---

## Common Options Reference

| Option               | Description                                                          |
|:---------------------|:---------------------------------------------------------------------|
| `-v`                 | Verbose — show request/response headers                              |
| `-s`                 | Silent — no progress bar or error messages                           |
| `-S`                 | Show errors even in silent mode                                      |
| `-i`                 | Include response headers in output                                   |
| `-I`                 | HEAD request (headers only)                                          |
| `-L`                 | Follow redirects                                                     |
| `-o <file>`          | Write response body to file                                          |
| `-O`                 | Write response body to file named by URL                             |
| `-X <method>`        | HTTP method (GET, POST, PUT, DELETE, etc.)                           |
| `-H '<header>'`      | Add a request header                                                 |
| `-d '<data>'`        | Request body (implies POST)                                          |
| `-F '<field=value>'` | Multipart form upload                                                |
| `-u <user:pass>`     | HTTP Basic authentication                                            |
| `-b <cookies>`       | Send cookies (from string or file)                                   |
| `-c <file>`          | Save cookies to file                                                 |
| `-k`                 | Skip TLS certificate verification (insecure)                         |
| `--cacert <file>`    | Custom CA certificate                                                |
| `-A '<string>'`      | User-Agent string                                                    |
| `--connect-timeout`  | Timeout for connection establishment (seconds)                       |
| `--max-time`         | Maximum total time for the operation (seconds)                       |
| `--retry <n>`        | Number of retries on failure                                         |
| `-w '<format>'`      | Write-out format (timing, status code, etc.)                         |
| `-x <host:port>`     | HTTP/HTTPS proxy                                                     |
| `--socks5 <host:port>`| SOCKS5 proxy                                                        |
| `-4` / `-6`          | Force IPv4 / IPv6                                                    |

---

## Practical Exercises

### Exercise 1: Inspect HTTP Status Codes

Check the status codes for various URLs:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://example.com
curl -s -o /dev/null -w '%{http_code}\n' http://example.com/nonexistent
curl -s -o /dev/null -w '%{http_code}\n' http://google.com  # Should be a redirect (301/302)
```

### Exercise 2: Measure Response Time

Use the `-w` flag to measure connection and transfer timing:

```bash
curl -s -o /dev/null -w '\
  DNS Lookup:  %{time_namelookup}s\n\
  TCP Connect: %{time_connect}s\n\
  TLS Handshake: %{time_appconnect}s\n\
  First Byte:  %{time_starttransfer}s\n\
  Total Time:  %{time_total}s\n' \
  https://example.com
```

### Exercise 3: Follow a Redirect Chain

Trace all redirects from an HTTP URL to its final destination:

```bash
curl -v -L http://google.com 2>&1 | grep -E '< HTTP|< Location'
```

### Exercise 4: Test a REST API

Perform CRUD operations against a test API:

```bash
# Create
curl -s -X POST \
  -H 'Content-Type: application/json' \
  -d '{"title":"Test","body":"Hello","userId":1}' \
  https://jsonplaceholder.typicode.com/posts

# Read
curl -s https://jsonplaceholder.typicode.com/posts/1

# Update
curl -s -X PUT \
  -H 'Content-Type: application/json' \
  -d '{"title":"Updated","body":"World","userId":1}' \
  https://jsonplaceholder.typicode.com/posts/1

# Delete
curl -s -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

### Exercise 5: Inspect TLS Certificate Details

View the TLS certificate of a website:

```bash
curl -vI https://example.com 2>&1 | grep -A 6 'Server certificate'
```

Or get more detail with:

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text | head -20
```

### Exercise 6: Download with Progress

Download a file with a progress bar:

```bash
curl -O -# https://example.com/largefile.zip
```

### Exercise 7: Compare HTTP/1.1 vs HTTP/2

Check if a server supports HTTP/2:

```bash
curl -I --http2 https://example.com
```

Look for `HTTP/2 200` in the response.
