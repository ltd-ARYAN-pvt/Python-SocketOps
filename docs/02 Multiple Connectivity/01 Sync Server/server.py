import socket
import time

#--> Step-1 Host and Port defined
HOST='localhost'
PORT=50000

#--> Step-2 Started Socket Connection as context manager
with socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
) as s:
    #--> Step-3 Binding the socket object with host and port
    s.bind((HOST,PORT))

    #--> Step-4 Listening for client request
    s.listen()
    print('Server Started...')
    #--> Step-5 Waiting for Connection
    #--> Approach-1 for Multiconnection - Wrap accept() in a loop.
    while True:
        conn, addr=s.accept()

        #--> Step-6 Define Connection
        with conn:
            print(f'Connected by {addr}')
            data=conn.recv(1024)
            print(f"Received: {data.decode()}")
            print("Processing...")
            time.sleep(3)
            conn.sendall(b"Done")
