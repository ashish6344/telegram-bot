import os
import asyncio
from telethon import TelegramClient, events

# ===== ENV =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# Channels
SOURCE_CHANNEL = "@pc_alert"
DESTINATION_CHANNEL = "@alertbyotpman"

# Remove lines containing these
REMOVE_WORDS = [
    "Powered By",
    "@ProCampaign"
]

# ===== CLIENT (USER ACCOUNT ONLY) =====
client = TelegramClient(
    session=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    if not event.text:
        return

    lines = []
    for line in event.text.split("\n"):
        if any(w.lower() in line.lower() for w in REMOVE_WORDS):
            continue
        lines.append(line)

    text = "\n".join(lines).strip()
    if text:
        await client.send_message(DESTINATION_CHANNEL, text)

async def main():
    await client.connect()   # ❌ no start(), no bot_token
    print("Bot is running ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
