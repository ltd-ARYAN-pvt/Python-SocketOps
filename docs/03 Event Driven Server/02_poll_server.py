#--> Note: Only for linux or WSL users only. Window don't have poll and epoll.
import socket
import select

HOST = "127.0.0.1"
PORT = 50000

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print(f"Listening on {HOST}:{PORT}")

poller = select.poll()

poller.register(
    server,
    select.POLLIN
)

fd_to_socket = {
    server.fileno(): server
}

while True:

    events = poller.poll()

    for fd, event in events:

        sock = fd_to_socket[fd]

        #--> New Connection
        if sock == server:

            conn, addr = server.accept()

            print(
                f"Connected: {addr}"
            )

            fd_to_socket[
                conn.fileno()
            ] = conn

            poller.register(
                conn,
                select.POLLIN
            )

        #--> Client Message
        elif event & select.POLLIN:

            data = sock.recv(1024)

            if not data:

                print(
                    "Client disconnected"
                )

                poller.unregister(sock)

                fd_to_socket.pop(
                    sock.fileno()
                )

                sock.close()

                continue

            print(
                f"Received: "
                f"{data.decode()}"
            )

            sock.send(
                f"Echo: {data.decode()}".encode()
            )