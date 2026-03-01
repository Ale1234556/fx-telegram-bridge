import os
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def send_to_discord(text):
    if not text:
        return
    if len(text) > 1900:
        text = text[:1900] + "..."
    requests.post(DISCORD_WEBHOOK, json={"content": text})

@client.on(events.NewMessage)
async def handler(event):
    if event.chat_id != TARGET_CHAT_ID:
        return

    sender = await event.get_sender()
    if not getattr(sender, "bot", False):
        return

    text = event.raw_text
    if text:
        send_to_discord(text)

client.start()
client.run_until_disconnected()
