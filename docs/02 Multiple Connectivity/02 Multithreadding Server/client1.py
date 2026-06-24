import socket
import time

start = time.time()

with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as s:

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-1 connected"
    )

    s.connect(("localhost", 50000))

    time.sleep(6)

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-1 sending"
    )

    s.sendall(b"Client-1")

    response = s.recv(1024)

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-1 received: {response.decode()}"
    )

print(
    f"Client-1 total runtime: "
    f"{time.time() - start:.2f} sec"
)