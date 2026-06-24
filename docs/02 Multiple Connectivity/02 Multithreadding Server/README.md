# Multithreaded TCP Server in Python

## Overview

This project improves the synchronous server by introducing concurrency using Python threads.

Each client connection is assigned its own thread, allowing multiple clients to communicate with the server simultaneously.

This is one of the most common beginner-friendly concurrency models used in network programming.

---

## Learning Objectives

By completing this project, you will learn:

* Concurrency fundamentals
* Thread-per-connection architecture
* Using Python's threading module
* Handling multiple clients simultaneously
* Blocking I/O inside worker threads

---

## Architecture

```text
Main Thread
      |
      +---- Client A Thread
      |
      +---- Client B Thread
      |
      +---- Client C Thread
```

---

## Workflow

```text
accept()
    ↓
Create Thread
    ↓
Thread Handles Client
    ↓
Main Thread Returns To accept()
```

---

## Thread Lifecycle

```text
Client Connects
       ↓
accept()
       ↓
Thread Created
       ↓
handle_client()
       ↓
recv()
       ↓
sendall()
       ↓
Thread Ends
```

---

## Concurrency Demonstration

Assume:

```text
Client A sleeps 6 seconds
Client B sleeps 5 seconds
```

Timeline:

```text
00:00 Thread-A Created
00:00 Thread-B Created

00:05 Thread-B Receives Data
00:06 Thread-A Receives Data

00:15 Thread-B Finishes
00:16 Thread-A Finishes
```

Notice:

* Both clients are active simultaneously.
* One client does not block the other.
* Work overlaps in time.

---

## Advantages

* Easy concurrency model
* Supports multiple active clients
* Good learning step before async programming

---

## Disadvantages

* One thread per client
* Memory overhead grows with connections
* Excessive context switching
* Poor scalability at thousands of clients

---

## Industry Evolution

```text
Single Client Server
        ↓
Synchronous Server
        ↓
Threaded Server
        ↓
Thread Pool
        ↓
select()/poll()/epoll()
        ↓
asyncio
        ↓
Modern Frameworks
```

---

## Important Concepts Learned

* Threading
* Concurrency
* Blocking I/O
* Context Switching
* Thread-per-Connection Model

---

## What's Next?

After understanding multithreaded servers, the next step is learning:

* select.select()
* selectors module
* asyncio
* Event Loops
* WebSockets
* FastAPI Internals

These concepts form the foundation of modern high-performance backend systems.