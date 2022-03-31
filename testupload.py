from telegram_upload.config import default_config
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo
import json
import os
from ffprobe import FFProbe
from telegram_upload.management import upload

CONFIG_DIRECTORY = os.environ.get('TELEGRAM_UPLOAD_CONFIG_DIRECTORY', '~/.config')
SESSION_FILE = os.path.expanduser('{}/telegram-upload'.format(CONFIG_DIRECTORY))
with open(default_config()) as f:
    config = json.load(f)
client = TelegramClient(config.get('session', SESSION_FILE), config['api_id'], config['api_hash'],)



@client.on(events.NewMessage(chats=[-664002905]))
async def start(event):
    # metadata = FFProbe('cosplayers.momodayo_Sat, 19 Feb 2022 08:19:16 GMT.mp4')
    pesan = str(event.message.message).split(" ")
    for a in range(1, len(pesan)):
        (pesan[a])
    
    if "/list" in pesan[0]:
        allchat = await client.get_messages(event.chat_id,limit=10)
        
        for a in allchat:
            print(a.message)
        
        # upload("cosplayers.momodayo_Sat, 19 Feb 2022 08:19:16 GMT.mp4", "Nexia Sonarr")
        # await client.send_file(entity='Nexia Sonarr', file='cosplayers.momodayo_Sat, 19 Feb 2022 08:19:16 GMT.mp4',  attributes=(DocumentAttributeVideo(int(float(metadata.streams[0].duration)), int(metadata.streams[0].width), int(metadata.streams[0].height), supports_streaming=True),))

    
client.start()
client.run_until_disconnected()