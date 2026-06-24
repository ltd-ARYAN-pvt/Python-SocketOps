# 🚀 Socket Programming in Python

A hands-on journey through the evolution of network servers in Python.

This repository demonstrates how real-world servers evolved from simple blocking socket implementations to scalable event-driven architectures using `select`, `poll`, `epoll`, and finally `asyncio`.

The goal is not just to build servers, but to understand **why each approach exists**, **what problems it solves**, and **how operating systems handle thousands of connections efficiently**.

---

## 📚 Learning Path

The repository is organized as a progression of concepts.

```text
Socket Python
│
├── 01 Echo Server
├── 02 Multiple Connectivity
│   ├── Sync Server
│   └── Multithreading Server
│
├── 03 Event Driven Server
│   ├── select()
│   ├── poll()
│   └── epoll()
│
└── 04 Async Server
```

Each section builds on concepts learned in the previous one.

---

# Phase 1: Echo Server

## What You'll Learn

* TCP Socket Basics
* Client-Server Communication
* Connection Lifecycle
* Sending and Receiving Data

### Concepts Covered

* `socket()`
* `bind()`
* `listen()`
* `accept()`
* `recv()`
* `send()`
* `close()`

### Goal

Understand the minimum building blocks required to establish communication between a client and a server.

---

# Phase 2: Multiple Connectivity

A single-client server is useful for learning but impractical in production.

This phase explores different strategies for handling multiple clients.

---

## 2.1 Synchronous Server

### How it Works

```text
Client 1 ----\
              \
               Server
              /
Client 2 ----/
```

The server processes one connection at a time.

### Limitation

If one client blocks:

```python
data = conn.recv(1024)
```

every other client must wait.

---

## 2.2 Multithreaded Server

### How it Works

```text
Client 1 ---> Thread 1
Client 2 ---> Thread 2
Client 3 ---> Thread 3
```

Each connection gets its own thread.

### Advantages

✅ Easy to understand

✅ Handles multiple clients simultaneously

### Limitations

❌ Thread creation overhead

❌ Context switching cost

❌ Memory consumption grows with connections

❌ Does not scale to thousands of clients

---

# Phase 3: Event Driven Servers

This section explores how modern high-performance servers manage thousands of connections without creating thousands of threads.

---

## Why Event Driven I/O?

Imagine:

```text
10,000 clients
```

Creating:

```text
10,000 threads
```

would be extremely expensive.

Instead, the operating system notifies the server when a socket becomes ready.

```text
Ready for Read?
Ready for Write?
Connection Closed?
```

The server reacts only when work needs to be done.

---

## 3.1 select()

### Concept

The server asks the kernel:

> "Tell me which sockets are ready."

```python
select.select(
    read_list,
    write_list,
    exception_list
)
```

### Characteristics

✅ Portable

✅ Easy to understand

❌ O(n) scanning

❌ Limited scalability

---

## 3.2 poll()

### Concept

An improvement over `select()`.

### Characteristics

✅ No file descriptor limit

✅ More efficient

❌ Still scans all descriptors

---

## 3.3 epoll() (Linux)

### Concept

Instead of repeatedly asking:

```text
Are you ready?
Are you ready?
Are you ready?
```

the kernel notifies the application only when events occur.

### Characteristics

✅ O(1) scalability

✅ Handles thousands of connections

✅ Used in modern high-performance systems

Examples:

* Nginx
* HAProxy
* Redis
* High-performance APIs

---

# Phase 4: Async Server (asyncio)

Modern Python applications typically use `asyncio` instead of manually managing event loops.

---

## What You'll Learn

* Coroutines
* Event Loops
* Async Tasks
* Non-blocking I/O

### Example

```python
async def handle_client(reader, writer):
    data = await reader.read(1024)
```

### Benefits

✅ Cleaner code

✅ High concurrency

✅ No manual thread management

✅ Built on efficient OS event mechanisms

---

# Architecture Evolution

```text
Blocking Server
      │
      ▼
Multithreaded Server
      │
      ▼
select()
      │
      ▼
poll()
      │
      ▼
epoll()
      │
      ▼
asyncio
```

Each step exists to solve scalability limitations of the previous approach.

---

# Running Examples

## Server

```bash
python server.py
```

## Client

```bash
python client.py
```

For event-driven examples:

```bash
python 01_select_server.py
python 02_poll_server.py
python 03_epoll_server.py
```

---

# Repository Goals

This repository focuses on understanding:

* Network Programming
* TCP/IP Fundamentals
* Concurrent Servers
* Event Driven Architectures
* Operating System I/O Multiplexing
* Async Programming
* Scalability Concepts

Rather than simply using frameworks, the objective is to understand what happens underneath technologies such as:

* FastAPI
* Django
* Uvicorn
* Gunicorn
* Nginx

---

# Recommended Exploration

Visualize the development history:

```bash
git log --graph --decorate --oneline --all
```

View available branches:

```bash
git branch -a
```

Explore how the project evolved phase by phase.

---

# Future Enhancements

### Phase 4 (In Development)

* Interactive Chat Application UI
* Multi-room Communication
* User Management
* Message Broadcasting
* Better Client Experience

---

## References

* Python Socket Programming
* Python asyncio Documentation
* Linux epoll Documentation
* Stevens – UNIX Network Programming
* Beej's Guide to Network Programming

---

## Author

Built as a learning-first repository to understand how modern servers work from the ground up.

⭐ If this repository helps you understand networking and server internals, consider giving it a star.
### Aryan Pandey