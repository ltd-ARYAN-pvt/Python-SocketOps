import socket
import time

start = time.time()

with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as s:

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-2 connected"
    )

    s.connect(("localhost", 50000))

    time.sleep(5)

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-2 sending"
    )

    s.sendall(b"Client-2")

    response = s.recv(1024)

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"Client-2 received: {response.decode()}"
    )

print(
    f"Client-2 total runtime: "
    f"{time.time() - start:.2f} sec"
)