import asyncio
import os

from telethon import TelegramClient, events
from telethon.sessions import StringSession

TG_API_ID = int(os.environ.get("TG_API_ID"))
TG_API_HASH = str(os.environ.get("TG_API_HASH"))
TG_SESSION_STRING = str(os.environ.get("TG_SESSION_STRING"))

CHAT_ID = int(-1001190868633)
SOURCE_CHAT_ID = int(-1001766138888)


@events.register(events.NewMessage(pattern=r"(?i).*м. Київ", chats=[SOURCE_CHAT_ID], incoming=True))
async def handler(event):
    client = event.client

    if 'Повітряна тривога' in event.message.raw_text:
        await client.send_file(CHAT_ID, './bledina_start.png')

    elif 'Відбій тривоги' in event.message.raw_text:
        await client.send_file(CHAT_ID, './bledina_end.png')


client = TelegramClient(StringSession(TG_SESSION_STRING), TG_API_ID, TG_API_HASH)

with client:
    client.add_event_handler(handler)
    client.run_until_disconnected()
