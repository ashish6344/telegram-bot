import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ===== ENV =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# Channels (fixed)
SOURCE_CHANNEL = "@pc_alert"
DESTINATION_CHANNEL = "@alertbyotpman"

# Remove lines containing these
REMOVE_WORDS = [
    "Powered By",
    "@ProCampaign"
]

# ===== AMOUNT LOGIC =====
def rupees_done_logic(text):
    def check(num_str):
        value = float(num_str)
        if value <= 1:
            # same as it is
            if value.is_integer():
                return str(int(value))
            else:
                return str(value).rstrip('0').rstrip('.')
        else:
            return "DONE ✅"

    # ₹50 , ₹0.5 , ₹1.00
    text = re.sub(
        r'₹\s*(\d+(?:\.\d+)?)',
        lambda m: f"₹{check(m.group(1))}" if check(m.group(1)) != "DONE ✅" else "DONE ✅",
        text
    )

    # 50 rs , 0.10 rs
    text = re.sub(
        r'(\d+(?:\.\d+)?)\s*(rs|Rs)',
        lambda m: f"{check(m.group(1))} {m.group(2)}" if check(m.group(1)) != "DONE ✅" else "DONE ✅",
        text
    )

    # Rs 50 , Rs 0.5
    text = re.sub(
        r'(Rs)\s*(\d+(?:\.\d+)?)',
        lambda m: f"{m.group(1)} {check(m.group(2))}" if check(m.group(2)) != "DONE ✅" else "DONE ✅",
        text
    )

    return text

# ===== CLIENT =====
client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
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

    # 👉 AMOUNT RULE APPLY HERE
    text = rupees_done_logic(text)

    if text:
        await client.send_message(DESTINATION_CHANNEL, text)

async def main():
    await client.connect()
    print("Bot is running ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
