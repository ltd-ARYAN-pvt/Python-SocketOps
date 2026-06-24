# Asyncio Multi-Client Chat Server

A real-time chat application built using Python's `asyncio` library and raw TCP sockets.

This project was created as a hands-on exploration of event-driven networking, coroutine scheduling, and asynchronous I/O. Instead of relying on frameworks, the implementation focuses on understanding how modern servers efficiently handle multiple concurrent connections using a single event loop.

---

# Demo

<video controls>
  <source src="/assets/Vid1.mp4" type="video/mp4">
</video>
---

# Features

* Asyncio-based TCP server
* Multiple concurrent clients
* Username-based chat
* Join/Leave notifications
* Message broadcasting
* Graceful connection handling
* Connection reset handling
* Asyncio-based client
* Event-driven architecture
* Single-threaded server implementation

---

# Tech Stack

* Python 3.11+
* Asyncio
* TCP Sockets
* StreamReader / StreamWriter

---

# Project Structure

```text
.
├── server.py
├── client.py
└── README.md
```

---

# Project Evolution

This project was built incrementally to understand how asynchronous networking works under the hood.

---

## Phase 1 — Asyncio Echo Server

The journey started with a simple echo server.

### Goal

Receive a message from a client and send the same message back.

```text
Client
   |
Hello
   |
Server
   |
Hello
```

### Concepts Learned

* `asyncio.start_server()`
* `StreamReader`
* `StreamWriter`
* `await reader.read()`
* `writer.write()`
* `writer.drain()`
* Event Loop basics

### Key Insight

Instead of blocking on:

```python
conn.recv()
```

asyncio uses:

```python
await reader.read()
```

allowing other coroutines to run while waiting for network I/O.

---

## Phase 2 — Multi-Client Broadcast Chat

The server evolved from an echo server into a broadcast server.

### Goal

Allow multiple clients to communicate through a single server.

```text
Alice
   |
   v

 Server

 /  |  \

Bob Charlie David
```

### Features Added

* Multiple simultaneous clients
* Broadcast messaging
* Connected client tracking
* Asyncio task scheduling

### Concepts Learned

* Concurrent client handling
* Shared application state
* Event-driven message delivery
* Coroutine suspension and resumption

### Key Insight

Each connected client gets its own coroutine:

```text
Event Loop

├── handle_client(Alice)
├── handle_client(Bob)
└── handle_client(Charlie)
```

without creating additional OS threads.

---

## Phase 3 — Username-Based Chat System

The chat server was upgraded to support user identities.

### Features Added

* Username registration
* Join notifications
* Leave notifications
* User tracking
* Bidirectional user lookup design
* Private Messaging
* Online Users List
* Command System
```
Examples:
> /users
> /msg Bob Hello
> /help
```
* User Presence
* Chat Rooms

### Example

```text
Alice joined the chat

Bob joined the chat

Alice: Hello

Bob: Hi

Charlie joined the chat

Charlie: Asyncio is awesome

Bob left the chat
```

### Data Structures

```python
writer_to_user = {}
user_to_writer = {}
```

### Why Two Dictionaries?

#### Lookup Username From Connection

```python
writer -> username
```

Useful during:

* Message handling
* Disconnect handling
* Logging

#### Lookup Connection From Username

```python
username -> writer
```

Useful for future features like:

* Private messaging
* User lookup
* Presence management

### Concepts Learned

* Application-level protocols
* User session management
* Efficient lookup strategies
* Connection lifecycle management

---

# How It Works

## Server Startup

The server begins listening for incoming TCP connections.

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

## Client Connection

When a client connects:

```python
async def handle_client(reader, writer):
```

asyncio creates:

```text
reader  -> incoming stream
writer  -> outgoing stream
```

for that specific connection.

---

## Event Loop Visualization

Assume three connected users:

```text
Alice
Bob
Charlie
```

Internally:

```text
Event Loop

├── handle_client(Alice)
├── handle_client(Bob)
└── handle_client(Charlie)
```

When Alice waits:

```python
await reader.readline()
```

her coroutine pauses.

The event loop immediately serves Bob or Charlie instead.

No thread is blocked.

---

## Broadcasting Messages

When Alice sends:

```text
Hello Everyone
```

The server formats:

```text
Alice: Hello Everyone
```

and broadcasts it to all connected users.

---

# Async Client Architecture

The client also uses asyncio.

Two independent coroutines run concurrently:

```python
receive_messages()
send_messages()
```

created using:

```python
asyncio.create_task()
```

This allows the client to:

* Send messages
* Receive messages

simultaneously without manually managing threads.

---

# Concepts Demonstrated

## TCP Networking

* bind()
* listen()
* accept()
* recv()
* send()

---

## Asyncio

* async / await
* Event Loop
* Coroutines
* Tasks
* asyncio.create_task()
* asyncio.gather()
* asyncio.wait()
* StreamReader
* StreamWriter

---

## Event-Driven Programming

This project indirectly uses:

```text
epoll()   -> Linux
kqueue()  -> macOS
IOCP      -> Windows
```

through Python's asyncio abstraction layer.

---

# Running The Project

## Start Server

```bash
python server.py
```

Output:

```text
Server listening on 127.0.0.1:50000
```

---

## Start Clients

Open multiple terminals:

```bash
python client.py
```

Example:

```text
Enter your name: Alice
```

```text
Enter your name: Bob
```

```text
Enter your name: Charlie
```

---

## Chat Example

```text
Alice joined the chat

Bob joined the chat

Charlie joined the chat

Alice: Hello Everyone

Bob: Hi Alice

Charlie: Asyncio is awesome

Bob left the chat
```

---

# Future Work

## Phase 4 — Web UI (In Development)

The next phase of the project is building a web-based interface using Streamlit.

### Planned Features

* Modern chat interface
* Chat bubbles
* Online users sidebar
* Join/Leave indicators
* Auto-refresh messages
* Private messaging support
* Improved user experience

### Planned Architecture

```text
Browser
   |
   v
Streamlit UI
   |
   v
TCP Client
   |
   v
Asyncio Server
```

The networking layer and server implementation will remain unchanged. The UI will act as a client layer on top of the existing chat protocol.

---

# Learning Outcomes

This project explores:

* Asynchronous networking
* Event-driven server architecture
* Coroutine scheduling
* TCP communication
* Concurrent client handling
* User session management
* Real-world chat server design

The implementation intentionally avoids high-level frameworks to focus on understanding the underlying networking model and how asyncio interacts with operating system event notification mechanisms.

---