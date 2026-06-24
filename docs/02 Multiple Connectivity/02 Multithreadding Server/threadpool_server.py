import socket
import time
from concurrent.futures import ThreadPoolExecutor
import threading

pool = ThreadPoolExecutor(max_workers=2)

def handle_client(conn, addr):
    thread_id = threading.current_thread().name
    start_time = time.time()

    with conn:
        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{thread_id} -> Connected: {addr}"
        )

        data = conn.recv(1024)

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{thread_id} -> Received: {data.decode()}"
        )

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{thread_id} -> Simulating work for 5 sec..."
        )

        time.sleep(5)

        conn.sendall(b"Done")

    end_time = time.time()

    print(
        f"[{time.strftime('%H:%M:%S')}] "
        f"{thread_id} -> Finished in "
        f"{end_time - start_time:.2f} sec"
    )

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("localhost", 50000))
server.listen()

print("Server started...\n")

while True:
    conn, addr = server.accept()

    pool.submit(
        handle_client,
        conn,
        addr
    )