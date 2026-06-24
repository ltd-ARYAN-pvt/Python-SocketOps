import socket

HOST = "localhost"  #--> The server's hostname or IP address
SERVER_PORT = 65432  #--> The port used by the server
CLIENT_PORT = 50000  #--> This port is used by the client

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.bind((HOST, CLIENT_PORT))
    #--> The client does use a port and IP, but it usually doesn't need to call bind() manually because the OS does it automatically. This automatic port is called an ephemeral port.

    #--> So whether you use bind or not in client its up to you.
    s.connect((HOST, SERVER_PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")