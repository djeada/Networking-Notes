# curl

## Overview

`curl` (Client URL) is a command-line tool for transferring data using various protocols, most commonly HTTP and HTTPS. It is invaluable for testing APIs, inspecting HTTP headers, downloading files, and debugging web server behavior from the command line.

## Basic Usage

```bash
# Fetch a web page
curl http://example.com

# Fetch and follow redirects
curl -L http://example.com

# Fetch and save to a file
curl -o page.html http://example.com

# Fetch and save with the remote filename
curl -O http://example.com/file.zip

# Fetch silently (no progress bar)
curl -s http://example.com
```

## Inspecting HTTP Headers

```bash
# Show response headers only
curl -I http://example.com

# Show both headers and body
curl -i http://example.com

# Verbose output (request + response headers, TLS handshake details)
curl -v https://example.com

# Extra-verbose (includes hex dump of data)
curl --trace - https://example.com
```

### Reading Header Output

```text
$ curl -I http://example.com
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 1256
Connection: keep-alive
Cache-Control: max-age=604800
ETag: "3147526947"
Expires: Mon, 01 Jan 2024 12:00:00 GMT
```

| Header           | Meaning                                            |
|------------------|----------------------------------------------------|
| `HTTP/1.1 200 OK` | Protocol version and status code                 |
| `Content-Type`   | MIME type of the response body                     |
| `Content-Length`  | Size of the response body in bytes                 |
| `Cache-Control`  | Caching directives                                 |
| `ETag`           | Entity tag for cache validation                    |

## HTTP Methods

```bash
# GET (default)
curl http://example.com/api/users

# POST with data
curl -X POST -d 'name=Alice&age=30' http://example.com/api/users

# POST with JSON
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice","age":30}' \
  http://example.com/api/users

# PUT
curl -X PUT \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alice","age":31}' \
  http://example.com/api/users/1

# DELETE
curl -X DELETE http://example.com/api/users/1

# PATCH
curl -X PATCH \
  -H 'Content-Type: application/json' \
  -d '{"age":31}' \
  http://example.com/api/users/1
```

## Custom Headers and Authentication

```bash
# Set custom headers
curl -H 'Authorization: Bearer TOKEN123' \
     -H 'Accept: application/json' \
     http://example.com/api/data

# Basic authentication
curl -u username:password http://example.com/api/data

# Send cookies
curl -b 'session=abc123' http://example.com

# Save and send cookies across requests
curl -c cookies.txt http://example.com/login -d 'user=alice&pass=secret'
curl -b cookies.txt http://example.com/dashboard
```

## Useful Options

| Option              | Description                                           |
|---------------------|-------------------------------------------------------|
| `-o <file>`         | Write output to a file                                |
| `-O`                | Save with the remote filename                         |
| `-L`                | Follow redirects                                      |
| `-I`                | Fetch headers only (HEAD request)                     |
| `-i`                | Include response headers in output                    |
| `-v`                | Verbose output                                        |
| `-s`                | Silent mode (no progress bar)                         |
| `-S`                | Show errors in silent mode                            |
| `-X <method>`       | Specify HTTP method (GET, POST, PUT, DELETE, etc.)    |
| `-d <data>`         | Send data in request body                             |
| `-H <header>`       | Add a custom header                                   |
| `-u user:pass`      | HTTP basic authentication                             |
| `-k`                | Allow insecure TLS connections (skip cert verification)|
| `-w <format>`       | Write out specific info after transfer                |
| `--connect-timeout` | Maximum time to wait for connection (seconds)         |
| `-m <seconds>`      | Maximum time for the entire operation                 |

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
