import socket

client = socket.socket()
client.connect(("127.0.0.1", 50000))

while True:
    msg = input("> ")
    client.sendall((msg + "\n").encode())