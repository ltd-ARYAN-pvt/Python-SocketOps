import asyncio
from utils import handle_client

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