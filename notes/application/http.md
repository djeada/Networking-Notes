# HTTP (Hypertext Transfer Protocol)

## Introduction

HTTP is the application-layer protocol for requesting and transferring resources
(HTML pages, images, API data, etc.) over the web. It follows a **request-response**
model: a client (usually a browser) sends a request, and a server returns a response.

HTTP messages are transferred via a _lower-level_ transport protocol, most commonly **TCP**
(and **QUIC/UDP** for HTTP/3).

## HTTP Request-Response Cycle

```text
  +-----------+                           +------------+
  |           |  ----  HTTP Request  ----> |            |
  |  Client   |                           |   Server   |
  | (Browser) |  <--- HTTP Response ----  |            |
  +-----------+                           +------------+
       |                                        |
       |   1. Client opens TCP connection       |
       |   2. Client sends HTTP request         |
       |   3. Server processes request          |
       |   4. Server sends HTTP response        |
       |   5. Connection closed or reused       |
```

## HTTP Message Structure

```text
  HTTP Request                        HTTP Response
  +---------------------------+       +---------------------------+
  | Request Line              |       | Status Line               |
  | GET /index.html HTTP/1.1  |       | HTTP/1.1 200 OK           |
  +---------------------------+       +---------------------------+
  | Headers                   |       | Headers                   |
  | Host: example.com         |       | Content-Type: text/html   |
  | Accept: text/html         |       | Content-Length: 1234      |
  | Cookie: session=abc       |       | Set-Cookie: id=xyz        |
  +---------------------------+       +---------------------------+
  | (empty line)              |       | (empty line)              |
  +---------------------------+       +---------------------------+
  | Body (optional)           |       | Body                      |
  | (form data, JSON, etc.)   |       | <!DOCTYPE html>...        |
  +---------------------------+       +---------------------------+
```

## HTTP Methods

| Method    | Purpose                                  | Request Body | Idempotent | Safe |
|-----------|------------------------------------------|:------------:|:----------:|:----:|
| `GET`     | Retrieve a resource                      | No           | Yes        | Yes  |
| `HEAD`    | Same as GET but returns headers only     | No           | Yes        | Yes  |
| `POST`    | Submit data / create a resource          | Yes          | No         | No   |
| `PUT`     | Replace a resource entirely              | Yes          | Yes        | No   |
| `PATCH`   | Partially update a resource              | Yes          | No         | No   |
| `DELETE`  | Remove a resource                        | Optional     | Yes        | No   |
| `OPTIONS` | Describe communication options (CORS)    | No           | Yes        | Yes  |

- **Safe** methods do not modify server state.
- **Idempotent** methods produce the same result if called multiple times.

## Experimenting with HTTP

- Firefox / Chrome DevTools under the **Network** tab
- VS Code extension **REST Client**
- Command-line tools: `curl`, `httpie`

## HTTP Examples

### Wikipedia — GET page

Request:

```http
GET /wiki/Main_Page HTTP/2.0
Host: en.wikipedia.org
Connection: keep-alive
```

Response:

```http
HTTP/2.0 200 OK
Date: Wed, 24 Apr 2019 07:50:41 GMT
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html ...
```

### Wikipedia — search with redirect (1)

Request:

```http
GET /w/index.php?search=test&title=Special:Search&go=Go HTTP/2.0
Host: en.wikipedia.org
Connection: keep-alive
```

Response:

```http
HTTP/2.0 302 Found
Location: https://en.wikipedia.org/wiki/Test
Content-Length: 0
```

### Wikipedia — following the redirect (2)

Request:

```http
GET /wiki/Test HTTP/2.0
Host: en.wikipedia.org
Connection: keep-alive
```

Response:

```http
HTTP/2.0 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html ...
```

### POST request

Request:

```http
POST /submit-posting HTTP/2.0
Host: example.com
Connection: keep-alive
Content-Type: text/plain; encoding=UTF-8
Content-Length: 33

This is the post content (body)
```

Response:

```http
HTTP/2.0 200 OK
Content-Type: text/html; charset=UTF-8

...
```

### JSON API

```http
GET /todos/12
Host: jsonplaceholder.typicode.com
Connection: keep-alive
```

```http
HTTP/2.0 200 OK
Content-Type: application/json; charset=utf-8
Etag: W/"5c-cn8o...

{
  "userId": 1,
  "id": 12,
  "title": "ipsa repellendus fugit nisi",
  "completed": true
}
```

## Important Request Header Fields

- **`Host`** — target hostname (required in HTTP/1.1)
- **`Connection`** — control options for the connection (`keep-alive`, `close`)
- `Origin` — where the request originated (used in CORS)
- `Accept` — media types the client can handle
- `Accept-Encoding` — compression algorithms supported (`gzip`, `br`)
- `Cookie` — previously stored cookies sent back to the server
- `Cache-Control` — caching directives
- `DNT` — Do Not Track preference

## HTTP Status Codes

| Code  | Text                  | Category      | Meaning                                        |
|-------|-----------------------|---------------|-------------------------------------------------|
| `200` | OK                    | Success       | Request succeeded                               |
| `201` | Created               | Success       | Resource created (typically after POST)          |
| `204` | No Content            | Success       | Success with no response body                   |
| `301` | Moved Permanently     | Redirection   | Resource permanently moved to new URL            |
| `302` | Found                 | Redirection   | Temporary redirect (commonly used)               |
| `303` | See Other             | Redirection   | Redirect with method changed to GET              |
| `304` | Not Modified          | Redirection   | Resource unchanged since last request            |
| `307` | Temporary Redirect    | Redirection   | Temporary redirect, method preserved             |
| `308` | Permanent Redirect    | Redirection   | Permanent redirect, method preserved             |
| `400` | Bad Request           | Client Error  | Malformed request syntax                         |
| `401` | Unauthorized          | Client Error  | Authentication required                          |
| `403` | Forbidden             | Client Error  | Server refuses to authorize the request          |
| `404` | Not Found             | Client Error  | Resource does not exist                          |
| `405` | Method Not Allowed    | Client Error  | HTTP method not supported for this resource      |
| `429` | Too Many Requests     | Client Error  | Rate limit exceeded                              |
| `500` | Internal Server Error | Server Error  | Generic server-side failure                      |
| `502` | Bad Gateway           | Server Error  | Invalid response from upstream server            |
| `503` | Service Unavailable   | Server Error  | Server temporarily overloaded or under maintenance |

See also: <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>

## Important Response Header Fields

- `Content-Length` — size of the response body in bytes
- `Content-Type` — media type of the response body
- `Set-Cookie` — instruct the client to store a cookie
- `Location` — URL for redirects (`3xx` responses)
- `Cache-Control` — caching directives for the response

## Header Field "Content-Type"

Common values:

- `text/plain; charset=utf-8`
- `text/html; charset=utf-8`
- `application/json`
- `application/javascript`
- `application/ecmascript`
- `image/jpeg`
- `image/png`
- `multipart/form-data`
- ...

## Header Field "Set-Cookie"

Example:

```http
GET /
Host: www.google.com

Set-Cookie: 1P_JAR=2019-04-24-08; expires=...; path=/; domain=.google.com
Set-Cookie: IDCC=AN0-TYtU7...fo; expires=...; path=/; domain=.google.com
```

## HTTP Versions: HTTP/1.1 vs HTTP/2 vs HTTP/3

```text
  HTTP/1.1                HTTP/2                  HTTP/3
  +---------------+       +---------------+       +---------------+
  | TCP           |       | TCP           |       | QUIC (UDP)    |
  | Text-based    |       | Binary framing|       | Binary framing|
  | One req/resp  |       | Multiplexed   |       | Multiplexed   |
  | per connection|       | streams       |       | streams       |
  | (pipelining   |       | Header        |       | 0-RTT handshk |
  |  rarely used) |       | compression   |       | No head-of-   |
  |               |       | (HPACK)       |       | line blocking  |
  +---------------+       +---------------+       +---------------+
```

| Feature              | HTTP/1.1              | HTTP/2               | HTTP/3               |
|----------------------|-----------------------|----------------------|----------------------|
| Transport            | TCP                   | TCP                  | QUIC (over UDP)      |
| Format               | Text                  | Binary frames        | Binary frames        |
| Multiplexing         | No (1 req per conn)   | Yes (streams)        | Yes (streams)        |
| Header compression   | No                    | HPACK                | QPACK                |
| Server push          | No                    | Yes                  | No (deprecated)      |
| Head-of-line blocking| Yes (TCP level)       | Yes (TCP level)      | No (per-stream)      |
| Connection setup     | TCP + TLS handshake   | TCP + TLS handshake  | 0-RTT or 1-RTT      |

## HTTPS and TLS

HTTPS is HTTP over TLS (Transport Layer Security). It encrypts all communication
between client and server.

```text
  Client                                Server
    |                                      |
    |---1. ClientHello (supported ciphers)->|
    |<--2. ServerHello + Certificate--------|
    |---3. Key Exchange-------------------->|
    |<--4. Finished-------------------------|
    |                                      |
    |====  Encrypted HTTP traffic  ========|
```

- **TLS handshake** establishes a shared secret using asymmetric cryptography,
  then switches to faster symmetric encryption for the session.
- **Certificates** are issued by Certificate Authorities (CAs) and verify the
  server's identity.
- HTTPS uses **port 443** by default (HTTP uses port 80).
- Modern best practice: all websites should use HTTPS.
