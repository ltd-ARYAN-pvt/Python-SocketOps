# Synchronous Multi-Connection TCP Server

## Overview

This project extends the Echo Server by allowing the server to handle multiple client connections.

Instead of terminating after serving one client, the server continuously accepts new connections using a loop around `accept()`.

However, the server still handles clients **one at a time**, making it a synchronous and blocking server.

---

## Learning Objectives

By completing this project, you will learn:

* Continuous connection acceptance
* Sequential client handling
* Blocking I/O behavior
* Limitations of synchronous servers
* Why concurrency becomes necessary

---

## Architecture

```text
Client A
     |
     v
Server

Client B
     |
     v
Waiting...

Client C
     |
     v
Waiting...
```

---

## Server Flow

```text
while True
    accept()
        ↓
    handle client completely
        ↓
    accept next client
```

---

## Example Timeline

Assume:

```text
Client A sleeps 6 seconds
Client B sleeps 5 seconds
```

Timeline:

```text
00:00 Client A connects
00:00 Client B connects

00:00 Server accepts A

00:06 A sends data
00:06 A finishes

00:06 Server accepts B

00:06 B sends data
00:06 B finishes
```

Even though Client B was ready earlier, the server could not serve it because it was busy handling Client A.

---

## Why This Happens

The server executes:

```python
conn.recv()
```

which is a blocking operation.

The server cannot move to:

```python
accept()
```

until the current client is completely handled.

---

## Advantages

* Simple design
* Easy to understand
* Good for learning socket fundamentals

---

## Disadvantages

* One slow client blocks others
* Poor scalability
* Not suitable for real-world applications

---

## Key Lesson

A server can support multiple connections but still be non-concurrent.

"Multi-connection" does not automatically mean "Concurrent".

---

## Next Step

Introduce threads so each client can be handled independently.