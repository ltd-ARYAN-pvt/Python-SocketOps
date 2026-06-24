import socket

client = socket.socket()
client.connect(("127.0.0.1", 50000))

while True:
    msg = input("Message: ")

    if msg == "quit":
        break

    client.send(msg.encode())

    data = client.recv(1024)

    print("Echo:", data.decode())

client.close()