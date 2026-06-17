import asyncio
import time

clients=set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Connected: {addr}")
    clients.add(writer)

    try:
        while True:
            data = await reader.readline()

            if not data:
                break

            print(data.decode().strip())

    finally:
        clients.remove(writer)

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