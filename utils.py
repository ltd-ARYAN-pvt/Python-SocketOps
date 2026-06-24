import asyncio
import datetime

clients={} #--> Changes for Writer : Username

async def send_to_user(target_name, message):
    for writer, username in clients.items():

        if username == target_name:
            writer.write((message + "\n").encode())
            await writer.drain()
            return True

    return False

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

            message:str=data.decode().strip()
            if message.startswith("/"):
                if message == "/users":
                    online=" ,".join(clients.values())
                    writer.write(f"Online: {online}\n".encode())
                    await writer.drain()
                    continue

                if message == "/help":
                    help_txt="""
                        /user
                        /msg <user> <message>
                        /help
                    """

                    writer.write(help_txt.encode())
                    await writer.drain()
                    continue

                if message.startswith("/msg"):
                    parts=message.split(" ",2)
                    if len(parts)<3:
                        writer.write(
                            b"Usage: /msg <user> <message>\n"
                        )
                        await writer.drain()
                        continue
                    target=parts[1]
                    private_msg=parts[2]
                    delivered=await send_to_user(
                        target,
                        f"[Private] {username}: {private_msg}"
                    )

                    if not delivered:
                        writer.write(
                            f"User {target} not found\n".encode()
                        )
                        await writer.drain()
                    continue
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
