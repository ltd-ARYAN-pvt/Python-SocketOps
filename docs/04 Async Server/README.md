# Asyncio Echo Server

A beginner-friendly implementation of an asynchronous TCP Echo Server using Python's `asyncio` library.

This project demonstrates the fundamental concepts behind event-driven networking, coroutines, asynchronous I/O, and how modern servers efficiently handle connections without blocking threads.

---

# What is an Echo Server?

An Echo Server is the simplest form of a network server.

It receives data from a client and sends the exact same data back.

Example:

```text
Client                    Server

Hello  ----------------->

        <---------------  Hello
```

If a client sends:

```text
Hello World
```

the server responds with:

```text
Hello World
```

This simple behavior makes an Echo Server a great starting point for learning socket programming and asynchronous networking.

---

# Why Asyncio?

Traditional socket servers often block while waiting for data:

```python
data = conn.recv(1024)
```

If no data is available, the thread waits.

With asyncio:

```python
data = await reader.read(1024)
```

the coroutine pauses and the event loop can continue executing other tasks.

This allows a single thread to manage many connections efficiently.

---

# Project Goal

Understand:

* Event Loops
* Coroutines
* Async/Await
* TCP Networking
* StreamReader
* StreamWriter
* Non-blocking I/O

before building more advanced applications such as chat servers, WebSocket servers, or multiplayer game servers.

---

# How It Works

## Server Startup

The server starts listening on a TCP port.

```python
server = await asyncio.start_server(
    handle_client,
    "127.0.0.1",
    50000
)
```

Internally this performs:

```text
socket()
bind()
listen()
accept()
```

while exposing a high-level asynchronous API.

---

## New Client Connection

Whenever a client connects:

```python
async def handle_client(reader, writer):
```

is invoked.

Asyncio automatically creates:

```text
reader  -> Incoming data stream
writer  -> Outgoing data stream
```

for that client connection.

---

## Reading Data

The server waits for incoming data:

```python
data = await reader.read(1024)
```

Important:

```text
await != block
```

When the coroutine reaches an await point:

```python
await reader.read()
```

it pauses execution.

The event loop is then free to execute other tasks.

---

## Echoing Data Back

Once data is received:

```python
writer.write(data)
await writer.drain()
```

the exact same bytes are sent back to the client.

---

# Event Loop Visualization

Assume three clients connect simultaneously.

```text
Client A
Client B
Client C
```

Internally:

```text
Event Loop

├── handle_client(A)
├── handle_client(B)
└── handle_client(C)
```

If Client A is waiting for data:

```python
await reader.read()
```

its coroutine pauses.

The event loop immediately switches to another ready coroutine.

```text
No thread is blocked.
```

---

# Architecture

```text
              Event Loop

                    │
                    ▼

        ┌───────────────────┐
        │ Asyncio Server    │
        └───────────────────┘

             ▲      ▲      ▲
             │      │      │

          Client Client Client
             A      B      C
```

---

# Key Asyncio Concepts

## Coroutines

Functions declared using:

```python
async def
```

Example:

```python
async def handle_client():
    pass
```

Coroutines can be paused and resumed by the event loop.

---

## Await

Used to suspend a coroutine until an operation completes.

Example:

```python
await reader.read()
```

While waiting:

```text
Current coroutine pauses
Other coroutines continue running
```

---

## Event Loop

The heart of asyncio.

Responsible for:

* Scheduling coroutines
* Monitoring sockets
* Resuming paused tasks
* Managing asynchronous operations

Think of it as a traffic controller for asynchronous code.

---

## StreamReader

Provides methods for receiving data.

Example:

```python
data = await reader.read(1024)
```

---

## StreamWriter

Provides methods for sending data.

Example:

```python
writer.write(data)
await writer.drain()
```

---

# Running The Project

## Start Server

```bash
python server.py
```

Expected output:

```text
Server listening on 127.0.0.1:50000
```

---

## Start Client

Open another terminal:

```bash
python client.py
```

Type:

```text
Hello
```

Server receives:

```text
Hello
```

Client receives:

```text
Hello
```

The same message is echoed back.

---

# Learning Outcomes

By completing this project, you will understand:

* TCP client-server communication
* Asynchronous programming fundamentals
* Coroutine lifecycle
* Event loops
* Asyncio streams
* Non-blocking I/O
* The foundation of modern network servers

---

# Next Steps

After understanding an Echo Server, natural progressions include:

### Phase 2

Multi-Client Chat Server

```text
Alice
Bob
Charlie
```

communicating through a central server.

### Phase 3

Username-based chat protocol

```text
Alice: Hello
Bob: Hi
```

with join and leave notifications.

### Phase 4

Web UI using Streamlit

```text
Browser
   │
   ▼
Chat UI
   │
   ▼
Asyncio Server
```

---

# Why This Project Matters

Although an Echo Server is simple, it introduces the exact same building blocks used by:

* Chat applications
* WebSocket servers
* Multiplayer games
* Reverse proxies
* API gateways
* Real-time collaboration tools

Understanding this project provides a strong foundation for building scalable event-driven systems.

---
