import socket
import time

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(("127.0.0.1", 50000))

print("Connected")
# print("Sleeping for 10 seconds...")

# time.sleep(10)

client.send(b"Hello from client3")

print(client.recv(1024).decode())