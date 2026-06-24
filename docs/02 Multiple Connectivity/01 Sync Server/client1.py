import socket
import time

HOST = "localhost"
PORT = 50000

with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as s:

    s.connect((HOST, PORT))

    print("Client-1 connected")

    time.sleep(5)

    s.sendall(b"Client-1")

    print(s.recv(1024).decode())