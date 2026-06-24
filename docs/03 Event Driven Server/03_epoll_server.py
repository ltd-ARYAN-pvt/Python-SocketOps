#--> Note: Only for linux or WSL users only. Window don't have poll and epoll.
import socket
import select

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print(f"Listening on {HOST}:{PORT}")

epoll = select.epoll()

epoll.register(
    server.fileno(),
    select.EPOLLIN
)

fd_to_socket = {
    server.fileno(): server
}

while True:

    events = epoll.poll()

    for fd, event in events:

        sock = fd_to_socket[fd]

        # New connection
        if sock == server:

            conn, addr = server.accept()

            print(
                f"Connected: {addr}"
            )

            fd_to_socket[
                conn.fileno()
            ] = conn

            epoll.register(
                conn.fileno(),
                select.EPOLLIN
            )

        # Client sent data
        elif event & select.EPOLLIN:

            data = sock.recv(1024)

            if not data:

                print(
                    "Client disconnected"
                )

                epoll.unregister(fd)

                fd_to_socket.pop(fd)

                sock.close()

                continue

            print(
                f"Received: "
                f"{data.decode()}"
            )

            sock.send(
                f"Echo: {data.decode()}".encode()
            )