import asyncio
from telethon import TelegramClient, events
from config import *

async def main():
    client = TelegramClient(
    SESSION_STRING,
    API_ID,
    API_HASH
)


    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        text = event.text
        if not text:
            return

        lines = []
        for line in text.split("\n"):
            if any(word in line for word in REMOVE_WORDS):
                continue
            lines.append(line)

        new_text = "\n".join(lines)

        if new_text.strip():
            await client.send_message(DESTINATION_CHANNEL, new_text)

    
    print("✅ Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
    async def main():
    await client.connect()
    print("Bot is running ✅")
    await client.run_until_disconnected()

asyncio.run(main())


