import os
import asyncio
from telethon import TelegramClient, events

# ========= REQUIRED ENV VARIABLES =========
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SESSION_STRING = os.environ["SESSION_STRING"]

# ========= CHANNEL CONFIG =========
SOURCE_CHANNEL = "@pc_alert"
DESTINATION_CHANNEL = "@alertbyotpman"

# ========= TEXT FILTERS =========
REMOVE_WORDS = [
    "Powered By",
    "@ProCampaign"
]

# ========= TELEGRAM CLIENT =========
client = TelegramClient(
    SESSION_STRING,
    API_ID,
    API_HASH
)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def forward_message(event):
    if not event.text:
        return

    cleaned_lines = []
    for line in event.text.split("\n"):
        if any(word.lower() in line.lower() for word in REMOVE_WORDS):
            continue
        cleaned_lines.append(line)

    final_text = "\n".join(cleaned_lines).strip()

    if final_text:
        await client.send_message(DESTINATION_CHANNEL, final_text)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is running ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
