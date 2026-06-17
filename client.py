import socket
import threading

client = socket.socket()
client.connect(("127.0.0.1", 50000))

def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break

            print("\n" + data.decode())

        except:
            break

threading.Thread(
    target=receive_messages,
    daemon=True
).start()

while True:
    msg = input("> ")
    client.sendall((msg + "\n").encode())