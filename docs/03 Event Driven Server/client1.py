import socket
import time

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(("127.0.0.1", 50000))

print("Connected")
print("Sleeping for 20 seconds...")

time.sleep(20)

client.send(b"Hello after sleeping from client1")

print(client.recv(1024).decode())