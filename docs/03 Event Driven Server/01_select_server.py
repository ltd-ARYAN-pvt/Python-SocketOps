import socket
import select

HOST='localhost'
PORT=50000

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listning on {HOST}:{PORT}")

sockets=[server]

while True:
    readable,_,_=select.select(sockets,[],[])

    for sock in readable:
        #--> New Connection
        if sock == server:
            conn,addr = server.accept()
            print(f"Connected to {addr}")
            sockets.append(conn)

        #--> Existing Client sent data
        else:
            data=sock.recv(1024)
            if not data:
                print("Client disconnected!!")
                sockets.remove(sock)
                sock.close()

                continue
            print(f"Message From client: {data.decode()}")

            sock.send(f"Server received : {data.decode()}".encode())