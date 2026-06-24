# Event-Driven Servers in Python 🚀

A beginner-friendly deep dive into Event-Driven Networking using Python sockets, `select()`, `poll()`, and `epoll()`.

This repository documents my journey from traditional socket servers to high-performance event-driven servers used by modern systems like Nginx, Node.js, FastAPI, and Uvicorn.

---

# 📚 Table of Contents

* What is an Event-Driven Server?
* Why Event-Driven Architecture?
* File Descriptors Explained
* Why Sockets are File Descriptors
* The Evolution of Network Servers
* Select Server
* Poll Server
* Epoll Server
* Client Implementations
* Idle Connections Demonstration
* Select vs Poll vs Epoll
* Real-World Usage
* Key Takeaways

---

# What is an Event-Driven Server?

An Event-Driven Server does **not** create one thread per client.

Instead, it:

1. Monitors many sockets simultaneously.
2. Waits for events.
3. Processes only sockets that become active.
4. Returns to waiting.

Instead of:

```text
Client 1 -> Thread 1
Client 2 -> Thread 2
Client 3 -> Thread 3
```

it uses:

```text
           Event Loop
                │
 ┌──────────────┼──────────────┐
 │              │              │
Client 1    Client 2      Client 3
```

One thread can manage thousands of connections.

---

# Why Event-Driven Servers?

Traditional blocking servers suffer from:

```python
data = conn.recv(1024)
```

If the client sends nothing:

```text
Server waits...
Server waits...
Server waits...
```

The server becomes stuck.

To solve this, operating systems introduced:

* select()
* poll()
* epoll()

These allow servers to monitor many connections simultaneously.

---

# What is an Event?

An event means:

```text
Something happened on a socket.
```

Examples:

| Event    | Meaning              |
| -------- | -------------------- |
| Readable | Data arrived         |
| Writable | Ready to send data   |
| Error    | Something went wrong |
| Hangup   | Client disconnected  |

---

# File Descriptors

A File Descriptor (FD) is simply an integer used by the operating system to identify an open resource.

Examples:

```text
0 -> stdin
1 -> stdout
2 -> stderr
3 -> socket
4 -> socket
5 -> socket
```

Everything is treated like a file in Linux:

* Files
* Sockets
* Pipes
* Terminals

---

# Why is a Socket a File Descriptor?

When a socket is created:

```python
sock = socket.socket()
```

The kernel assigns:

```text
FD = 3
```

Retrieve it using:

```python
sock.fileno()
```

Example:

```python
print(sock.fileno())
```

Output:

```text
3
```

This is why select(), poll(), and epoll() can monitor sockets.

---

# Evolution of Network Servers

## 1. Synchronous Server

```text
One Client
    ↓
Process Request
    ↓
Next Client
```

Pros:

* Simple

Cons:

* Poor scalability

---

## 2. Multi-Threaded Server

```text
Client 1 -> Thread 1
Client 2 -> Thread 2
Client 3 -> Thread 3
```

Pros:

* Multiple clients

Cons:

* High memory usage
* Context switching overhead

---

## 3. Thread Pool Server

```text
Fixed Number of Threads
```

Pros:

* Better resource control

Cons:

* Threads still consume memory

---

## 4. Event-Driven Server

```text
One Event Loop
Many Clients
```

Pros:

* Extremely scalable
* Minimal memory usage

---

# select()

The oldest event notification mechanism.

---

## Syntax

```python
readable, writable, exceptional = select.select(
    rlist,
    wlist,
    xlist,
    timeout
)
```

---

## Arguments

### rlist

Sockets monitored for incoming data.

```python
[server_socket, client1, client2]
```

---

### wlist

Sockets monitored for outgoing writes.

```python
[]
```

Usually empty in beginner examples.

---

### xlist

Sockets monitored for errors.

```python
[]
```

---

### timeout

```python
None
```

Wait forever.

```python
5
```

Wait 5 seconds.

```python
0
```

Return immediately.

---

## Returns

Example:

```python
readable = [client2]
```

Meaning:

```text
Client2 has data ready to read.
```

---

# Select Server Architecture

```text
            select()
                │
 ┌──────────────┼──────────────┐
 │              │              │
Client 1    Client 2      Client 3
```

Server waits only for active sockets.

---

# Demonstrating Idle Clients

Client:

```python
import time

time.sleep(10)
```

While sleeping:

```text
Connection exists
No data sent
No event generated
```

The server remains free to serve other clients.

This demonstrates the biggest advantage of event-driven servers:

> Idle connections do not block the server.

---

# poll()

An improvement over select().

---

## Why poll()?

Problems with select():

* FD limits
* Entire socket list passed every call
* O(n) scanning

---

## Create Poll Object

```python
poller = select.poll()
```

---

## Register Socket

```python
poller.register(
    sock,
    select.POLLIN
)
```

---

## Common Events

```python
select.POLLIN
```

Data available.

```python
select.POLLOUT
```

Ready to write.

```python
select.POLLHUP
```

Client disconnected.

```python
select.POLLERR
```

Error occurred.

---

## Poll Return Value

```python
[
    (fd, event)
]
```

Example:

```python
[
    (5, POLLIN)
]
```

Meaning:

```text
Socket 5 has data.
```

---

# Why poll() is Better

Registration occurs once:

```python
poller.register(sock)
```

Unlike select(), the socket list is not passed repeatedly.

However...

---

# Poll's Limitation

Even poll() still scans every socket:

```text
10,000 sockets
     ↓
scan all
     ↓
find 2 active
```

Complexity:

```text
O(n)
```

---

# epoll()

Linux's high-performance event notification system.

Used by:

* Nginx
* HAProxy
* Uvicorn
* AsyncIO
* FastAPI Internals

---

## Create Epoll Object

```python
epoll = select.epoll()
```

---

## Register Socket

```python
epoll.register(
    sock.fileno(),
    select.EPOLLIN
)
```

---

## Common Events

```python
select.EPOLLIN
```

Readable.

```python
select.EPOLLOUT
```

Writable.

```python
select.EPOLLHUP
```

Disconnected.

```python
select.EPOLLERR
```

Error.

---

## Polling

```python
events = epoll.poll()
```

Returns:

```python
[
    (fd, event)
]
```

---

# Why epoll is Fast

Poll:

```text
10,000 sockets
     ↓
scan all
```

Epoll:

```text
10,000 sockets
     ↓
Kernel tracks active sockets
     ↓
Return only active sockets
```

Example:

```python
[
    (6, EPOLLIN)
]
```

Only active sockets are returned.

---

# Complexity Comparison

| Mechanism | Complexity            |
| --------- | --------------------- |
| select()  | O(n)                  |
| poll()    | O(n)                  |
| epoll()   | O(active connections) |

---

# Level Triggered vs Edge Triggered

epoll supports:

## Level Triggered (LT)

Default mode.

If data remains unread:

```text
Kernel keeps notifying.
```

Easy to use.

---

## Edge Triggered (ET)

Notification occurs only when state changes.

```text
New data arrives
     ↓
One notification
```

Higher performance.

More difficult to implement correctly.

---

# Real World Mapping

When using:

```python
asyncio
```

Internally:

```text
asyncio
   ↓
selectors
   ↓
epoll (Linux)
```

When using:

```python
FastAPI
```

Internally:

```text
FastAPI
   ↓
Uvicorn
   ↓
AsyncIO
   ↓
epoll
```

---

# Key Takeaways

✅ Sockets are file descriptors.

✅ Event-driven servers avoid one-thread-per-client architecture.

✅ select() monitors many sockets.

✅ poll() improves registration handling.

✅ epoll() scales to massive numbers of connections.

✅ Modern Linux servers rely heavily on epoll.

✅ AsyncIO, Uvicorn, and FastAPI ultimately leverage epoll on Linux.

---

# Learning Path

```text
Socket Basics
      ↓
Blocking Server
      ↓
Threaded Server
      ↓
Thread Pool Server
      ↓
select()
      ↓
poll()
      ↓
epoll()
      ↓
AsyncIO
      ↓
FastAPI + Uvicorn
      ↓
High Performance Backend Systems
```

Happy Learning! 🚀