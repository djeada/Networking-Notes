# Stateless vs Stateful

## Introduction

One of the most important design decisions in networked systems is whether a protocol
or service is **stateless** or **stateful**. This choice affects scalability,
reliability, complexity, and how clients and servers interact.

- **Stateless**: The server does not retain any memory of previous requests. Each
  request is self-contained and includes all the information the server needs.
- **Stateful**: The server keeps track of the client's state across multiple
  requests. The meaning of a request may depend on what came before.

## Comparing Architectures

```text
  Stateless Architecture              Stateful Architecture
  +--------+     +--------+           +--------+     +--------+
  | Client |     | Server |           | Client |     | Server |
  +--------+     +--------+           +--------+     +--------+
      |               |                   |               |
      |-- Request 1 ->|  (self-contained) |-- Connect --->|
      |<- Response 1 -|                   |<- Session ID -|
      |               |  no memory kept   |               | server stores
      |-- Request 2 ->|  (self-contained) |-- Request 1 ->| session state
      |<- Response 2 -|                   |<- Response 1 -|
      |               |                   |-- Request 2 ->| references
      | Any server    |                   |<- Response 2 -| prior context
      | can handle    |                   |               |
      | any request   |                   | Must go to    |
      |               |                   | SAME server   |
```

## Stateless Protocols

Stateless is like **IPO: Input → Processing → Output**. Each request stands alone.

**Characteristics:**
- Server treats every request independently
- No session information stored on the server
- Easier to scale horizontally (any server can handle any request)
- More resilient to server failures
- Client must send all necessary context with each request

**Examples:**
- **HTTP** — each request is independent (state is managed externally via cookies/tokens)
- **DNS** — each query is independent
- **REST APIs** — designed to be stateless by principle
- **IP** — each packet is routed independently

## Stateful Protocols

Stateful protocols maintain a conversation with ongoing context between client
and server.

**Characteristics:**
- Server remembers previous interactions
- Requests may depend on prior commands or state
- Harder to scale (sessions are tied to specific servers)
- More complex failure recovery
- Can be more efficient for multi-step operations

**Examples:**
- **FTP** — login session, current directory, transfer mode
- **IMAP** — mailbox selection, message flags, pending deletes
- **SMTP** — multi-step mail submission dialog
- **SSH** — authenticated session with state
- **Database connections** — transactions, cursors, session variables

### IMAP Dialog Example

A classic illustration of a stateful protocol's "chatty" nature:

```text
Client: My name is Bob
Server: Hi Bob, nice to meet you.
Server: But are you really Bob?
Server: Please prove to me that you're Bob. You can use method foo, bar, blu
        for authentication
Client: I choose method "blu"
Server: Ok, then please send the magic blu token
Client: Here it is xyuasdusd8... I hope you like it.
Server: Fine, I accept this. Now I trust you. Now I know you are Bob
Client: Please show me the first message
Server: Here it is:
Server: ...
Client: Looks like spam. Please delete this message
Server: Now I know that you want to delete this message.
Server: But I won't delete it now. Please send me EXPUNGE to execute the delete.
Client: grrrr, this is complicated. I already told you that I want the message
        to be deleted.
Client: EXPUNGE
...
```

The IMAP `EXPUNGE` is analogous to a `COMMIT` in relational databases. While having
a transactional database to implement a service is very handy, it makes no sense to
expose the transaction semantics directly to the client.

## Comparison Table

| Aspect               | Stateless                          | Stateful                            |
|----------------------|------------------------------------|-------------------------------------|
| Server memory        | None between requests              | Maintains session/context           |
| Scalability          | Easy (horizontal scaling)          | Harder (session affinity needed)    |
| Load balancing       | Any server handles any request     | Requires sticky sessions or sharing |
| Fault tolerance      | High (retry with any server)       | Lower (state lost on crash)         |
| Request size         | Larger (carries all context)       | Smaller (references stored state)   |
| Complexity           | Simpler server logic               | More complex server logic           |
| Performance          | May repeat work                    | Can optimize across requests        |
| Examples             | HTTP, DNS, REST                    | FTP, IMAP, SMTP, SSH                |

## Practical Implications for Web Architecture

HTTP is fundamentally stateless, but web applications often need state. The solution
is to manage state *outside* the protocol:

```text
  Client         Load Balancer       Server A        Server B
    |                 |                  |               |
    |-- Request 1 --->|-- forward ------>|               |
    |<- Response + ---|<- Set-Cookie ----|               |
    |   Cookie        |                  |               |
    |                 |                  |               |
    |-- Request 2 --->|-- forward ---------------------->|
    |   + Cookie      |                 |               |
    |<- Response -----|<--------------------------------|
    |                 |  (Cookie/token contains state)  |
```

- **Cookies**: Small pieces of data stored in the browser, sent with every request.
- **Session tokens**: A cookie contains a session ID; the actual session data lives
  in a shared store (e.g., Redis, a database).
- **JWTs (JSON Web Tokens)**: Self-contained tokens that carry claims, enabling
  stateless authentication without server-side session storage.

### REST and Statelessness

REST (Representational State Transfer) explicitly requires statelessness as a
constraint. Each request must contain all information necessary for the server to
fulfill it. This enables:
- Horizontal scaling behind load balancers
- Caching at multiple levels
- Simpler server implementation

### Modern Microservices

In cloud environments, containers are created and destroyed in seconds. Stateless
services are strongly preferred because:
- Any instance can handle any request
- Auto-scaling works naturally
- Failures are handled by simply routing to another instance
- No need for sticky sessions or session replication

When state is needed, it is externalized to dedicated stateful services
(databases, caches, message queues) rather than kept in application servers.
