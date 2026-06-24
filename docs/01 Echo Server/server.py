import socket

HOST = 'localhost'
PORT = 65432

#--> Started a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #--> Assigned (bind) a host and port to the socket object
    s.bind((HOST, PORT))

    #--> Listening to the client request
    s.listen()

    #--> Waiting for connection
    conn, addr = s.accept()
    
    with conn:
        print(f'Connected by {addr}')
        while True:
            data=conn.recv(1024)
            if not data:
                break
            # print(data)
            conn.sendall(data)

#--> conn is the server-side socket object endpoint of a TCP connection to a specific client.