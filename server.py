import asyncio
from datetime import datetime 

clients={} #--> Changes for Writer : Username

async def broadcast(message, sender=None):
    dead_clients=[]
    for writer in clients:
        if writer == sender:
            continue

        try:
            writer.write(message.encode())
            await writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            dead_clients.append(writer)
    for writers in dead_clients:
        clients.pop(writers, None)

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    # print(f"Connected: {addr}")

    name_data = await reader.readline()
    if not name_data:
        return

    username = name_data.decode().strip()
    clients[writer] = username
    join_msg = f"{username} joined the chat"
    print(join_msg)
    await broadcast(join_msg + "\n", sender=writer)

    try:
        while True:
            data = await reader.readline()

            if not data:
                break

            message=data.decode().strip()
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted = f"[{timestamp}] {username}: {message}"

            print(formatted)

            await broadcast(
                formatted + "\n",
                sender=writer
            )

    except ConnectionResetError:
        print(f"{addr} disconnected unexpectedly")

    finally:
        username = clients.get(writer, "Unknown")
        clients.pop(writer, None)

        writer.close()
        try:
            await writer.wait_closed()
        except ConnectionResetError:
            pass

        leave_msg = f"{username} left the chat"
        print(leave_msg)
        await broadcast(leave_msg + "\n")


async def main():
    server=await asyncio.start_server(
        handle_client,
        "localhost",
        50000
    )

    print("Server listening on 127.0.0.1:50000")

    async with server:
        await server.serve_forever()

asyncio.run(main())