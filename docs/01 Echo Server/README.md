# Echo Server in Python

## Overview

This project demonstrates the most basic TCP socket communication between a client and a server using Python's built-in `socket` module.

The server waits for a client connection, receives data from the client, and immediately sends the same data back. This behavior is called an **Echo Server**.

---

## Learning Objectives

By completing this project, you will learn:

* What a socket is
* TCP client-server architecture
* Creating sockets with Python
* Binding a socket to an IP and Port
* Listening for incoming connections
* Accepting client connections
* Sending and receiving data
* Connection lifecycle management

---

## Architecture

```text
Client
   |
   |  "Hello Server"
   |
   v
Server
   |
   |  Echo Back
   |
   v
Client
```

---

## Server Lifecycle

```text
socket()
    ↓
bind()
    ↓
listen()
    ↓
accept()
    ↓
recv()
    ↓
sendall()
    ↓
close()
```

---

## Key Concepts

### socket()

Creates a communication endpoint.

### bind()

Assigns an IP address and port number to the server.

### listen()

Puts the server into listening mode.

### accept()

Waits for a client connection and creates a dedicated connection socket.

### recv()

Receives data from the connected client.

### sendall()

Sends all bytes back to the client.

---

## Limitations

* Supports only one client.
* Server exits after handling a single connection.
* No concurrency.
* Not suitable for production systems.

---

## Skills Learned

* TCP Fundamentals
* Socket Lifecycle
* Client-Server Communication
* Blocking I/O Basics

---

## Next Step

Build a server capable of accepting multiple clients sequentially using an infinite accept loop.