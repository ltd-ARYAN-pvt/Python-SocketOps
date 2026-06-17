import asyncio
import time

clients=set()

async def broadcast(message, sender=None):
    for writer in clients:
        if writer != sender:
            writer.write(message.encode())

        await writer.drain()

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Connected: {addr}")
    clients.add(writer)

    try:
        while True:
            data = await reader.readline()

            if not data:
                break

            message=data.decode().strip()
            print(message)
            await broadcast(message + "\n", sender=writer)

    except ConnectionResetError:
        print(f"{addr} disconnected unexpectedly")

    finally:
        clients.discard(writer)

        writer.close()
        await writer.wait_closed()

        print(f"Disconnected: {addr}")


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