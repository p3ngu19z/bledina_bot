import logging
import os
from random import choice

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)

TG_API_ID = int(os.environ.get("TG_API_ID"))
TG_API_HASH = str(os.environ.get("TG_API_HASH"))
TG_SESSION_STRING = str(os.environ.get("TG_SESSION_STRING"))

CHAT_ID = int(-1001190868633)
SOURCE_CHAT_ID = int(-1001766138888)

TG_STICKER_SET_NAME = 'LoginDestroyer'

STICKERS = {
    'start': [11],
    'end': [12],
}


@events.register(events.NewMessage(pattern=r"(?i).*м. Київ", chats=[SOURCE_CHAT_ID], incoming=True))
async def handler(event):
    logging.info('Alert received')
    client: TelegramClient = event.client

    logging.info("Load stickers started")
    stickers = await client(GetStickerSetRequest(
        stickerset=InputStickerSetShortName(
            short_name=TG_STICKER_SET_NAME,
        )
    ))
    logging.info("Load stickers finished")

    if 'Повітряна тривога' in event.message.raw_text:
        logging.info("Sending sticker")
        await client.send_file(CHAT_ID, stickers.documents[choice(STICKERS['start']) - 1])
        logging.info('Air raid alert START sticker sent')

    elif 'Відбій тривоги' in event.message.raw_text:
        logging.info("Sending sticker")
        await client.send_file(CHAT_ID, stickers.documents[choice(STICKERS['end']) - 1])
        logging.info('Air raid alert CANCELED sticker sent')


tg_client = TelegramClient(StringSession(TG_SESSION_STRING), TG_API_ID, TG_API_HASH)

with tg_client:
    tg_client.add_event_handler(handler)
    tg_client.run_until_disconnected()
