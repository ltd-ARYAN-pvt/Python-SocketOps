import asyncio

async def handle_client(reader, writer):
    addr= writer.get_extra_info("peername")
    print(f"Connected: {addr}")

    while True:
        data= await reader.read(1024)

        if not data:
            break

        print(f"Received: {data.decode()}")

        writer.write(data)
        await writer.drain()

    print(f"Disconnected: {addr}")

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client,
        "localhost",
        50000
    )

    print("Server listening on 121.0.0.1:50000")

    async with server:
        await server.serve_forever()

asyncio.run(main())