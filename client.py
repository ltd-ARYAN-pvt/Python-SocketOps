import asyncio

HOST = "127.0.0.1"
PORT = 50000


async def receive_messages(reader):
    while True:
        data = await reader.readline()

        if not data:
            print("\nDisconnected from server")
            break

        print("\n" + data.decode().strip())


async def send_messages(writer):
    while True:
        msg = await asyncio.to_thread(input, "> ")

        writer.write((msg + "\n").encode())
        await writer.drain()


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    print("Connected to chat server!")

    receive_task = asyncio.create_task(receive_messages(reader))
    send_task = asyncio.create_task(send_messages(writer))

    await asyncio.gather(receive_task, send_task)

    writer.close()
    await writer.wait_closed()


asyncio.run(main())