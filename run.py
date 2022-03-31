import binascii
from multiprocessing.connection import wait
import random
import time
from telegram_upload.config import default_config
from telegram_upload.management import upload
from telethon import TelegramClient, events
import json
import os
from requests import Session, exceptions as rexcep
import requests
import subprocess as sp
import sys

from ffmpeg_progress import start
from telethon.tl.types import DocumentAttributeVideo

from ffprobe import FFProbe

s = Session()

CONFIG_DIRECTORY = os.environ.get('TELEGRAM_UPLOAD_CONFIG_DIRECTORY', '~/.config')
SESSION_FILE = os.path.expanduser('{}/telegram-upload'.format(CONFIG_DIRECTORY))
with open(default_config()) as f:
    config = json.load(f)

url = "https://coomer.party"

cookies = {}

def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
    return sp.Popen(['ffmpeg',
                     '-nostats',
                     '-loglevel', '0',
                     '-y',
                     '-vstats_file', vstats_path,
                     '-i', infile,
                     '-vf', 'scale=-1:720',
                     '-crf','25',
                     '-preset','veryfast',
                     '-c:a','copy',
                      outfile]).pid

def get_ddg_cookies(url1):
    global cookies
    r = s.get('https://check.ddos-guard.net/check.js', headers = {
        'referer': url1
    })
    cookies = r.cookies.get_dict()
    r.raise_for_status()
    return r.cookies.get_dict()['__ddg2']

def generate_token(size=16):
    """Generate a random token with hexadecimal digits"""
    data = random.getrandbits(size * 8).to_bytes(size, "big")
    return binascii.hexlify(data).decode()

async def get_artist_info(artist, message):
    data = []
    m4v = 0
    jpg = 0
    png = 0
    skip = 0
    looping = True
    while looping:
        try:
            get_ddg_cookies("https://coomer.party")
            token = generate_token()
            print(token)
            r = s.get(url+"/api/onlyfans/user/"+artist+f"?o={skip}", cookies={"__ddg2": token})

            r.cookies.set("_ddg2", token, domain="https://coomer.party")
            print(r.cookies.get_dict())
            
            print(r.raise_for_status())
            r = r.json()
            # print(r)
            if r != []:
                for a in r:
                    tgl = a['published'].split(" ")
                    # print(tgl)
                    filetype = ""
                    data.append(a)
                    if "path" in a['file'] and str(a['file']['path']).find(".m4v") != -1:
                        m4v = m4v + 1
                    elif "path" in a['file'] and str(a['file']['path']).find(".jpg") != -1:
                        jpg = jpg + 1
                    elif "path" in a['file'] and str(a['file']['path']).find(".png") != -1:
                        png = png + 1
                skip = skip + 25
            else:
                looping = False
        except (rexcep.JSONDecodeError, rexcep.HTTPError) as E:
            print("DDoS doing DDoS Thing, restartting")
            sec = 15
            for a in range(1,16):
                
                await message.edit(f"Host get blocked, retrying in {sec} Second")
                sec = sec - 1
                time.sleep(1)
            await message.edit("Getting Artist Info...")
        # except rexcep.HTTPError:
        #     return [], [], "coomer.party Error, try again later!"
    try:
        info = {
            'name': data[0]['user'],
            'service': data[0]['service'],
            'total_post': len(data),
            'total_file': {
                'm4v': m4v,
                'jpg': jpg,
                'png': png
            }
        }
        return data, info, ""

    except:
        return [], [], "Error, Artist not found"

async def downloadvideo(artist):
    s = Session()
    get_ddg_cookies("https://coomer.party")
    data = []
    path = []
    filename = []
    skip = 0
    looping = True
    while looping:
        try:
            r = s.get(url+"/api/onlyfans/user/"+artist+f"?o={skip}", cookies=cookies)
            
            print(r.raise_for_status())
            r = r.json()
            # print(r)
            if r != []:
                for a in r:
                    tgl = a['published'].split(" ")
                    # print(tgl)
                    filetype = ""
                    data.append(a)
                    # if "path" in a['file'] and "25dba641-fa59-40a6-be7d-221bd3082d46.m4v" in a['file']['name']:
                    #     continue
                    if "path" in a['file'] and str(a['file']['path']).find(".m4v") != -1:
                        path.append(a['file']['path'])
                        filename.append(" ".join(z for z in tgl))
                skip = skip + 25
            else:
                looping = False
        except (rexcep.JSONDecodeError, rexcep.HTTPError) as E:
            print("DDoS doing DDoS Thing, restartting")
            time.sleep(1)
        # except rexcep.HTTPError:
        #     return [], [], "coomer.party Error, try again later!"
    try:
        info = {
            'name': data[0]['user'],
            'service': data[0]['service'],
        }
        return path, filename, info

    except:
        return [], [], "Error, Artist not found"
        

        # print (tgl[1], tgl[2], tgl[3])
        # print(filetype)
        # print()


client = TelegramClient(config.get('session', SESSION_FILE), config['api_id'], config['api_hash'],)
print("Custom Bot Running!")

# Artist handler
@client.on(events.NewMessage(chats=[-1001552840012]))
async def pesanHandler(event):
    pesan = str(event.message.message).split(" ")
    for a in range(1, len(pesan)):
        (pesan[a])
    
    if "/artist" in pesan[0] and len(pesan) <= 1:
        await event.reply("Please insert artist name, use /artist <name artist>")
    
    elif "/artist" in pesan[0] and len(pesan) > 1:
        waitmsg = await event.reply("Getting Artist Info...")
        data, info, message = await get_artist_info(pesan[1], waitmsg)
        if str(message).find("Error") != -1:
            await waitmsg.edit(message)
        else:
            await waitmsg.edit(f"""
        
    Artist Info:

    Name : {info['name']}
    Service : {info['service']}
    Total Post : {info['total_post']}
    Total File : {info['total_file']['m4v']} m4v, {info['total_file']['jpg']} jpg, {info['total_file']['png']} png
    """)
       
    
    # print(event.message.message)
    print(pesan)
    print(len(pesan))

# Download handler
@client.on(events.NewMessage(chats=[-1001552840012]))
async def downloadHandler(event):
    pesan = str(event.message.message).split(" ")
    for a in range(1, len(pesan)):
        (pesan[a])


    if "/ping" in pesan[0]:
        await event.reply("Pong!")
        print(await client.get_entity(event.chat_id))
    elif "/download" in pesan[0] and len(pesan) <= 1:
        await event.reply("Please insert artist name, use /download <name artist>")
    
    # elif "/download" in pesan[0] and len(pesan) > 1:
    #     pathContent, filename = await downloadvideo(pesan[1])

    #     for a in 
    elif "/download" in pesan[0] and len(pesan) > 1:
        async def fdl(path, filename, message, infos):
            async def editprogress(message, id):
                time.sleep(5)
                return await id.edit(message)

            async def on_message_handler(percent: float,
                        fr_cnt: int,
                        total_frames: int,
                        elapsed: float):
                sys.stdout.write('\r{:.2f}%'.format(percent))
                sys.stdout.flush()
                
                try:
                    await editprogress(f"Progres downloading {info['name']}_{filename} ... "+'\r{:.2f}%'.format(percent), message)
                except:
                    pass

            async def on_done_handle(filenames):
                metadata = FFProbe(filenames)
                # print(metadata)
                print("Uploading", filenames)     
                await client.send_file(entity=event.chat_id, file=filenames,  attributes=(DocumentAttributeVideo(int(float(metadata.streams[0].duration)), int(metadata.streams[0].width), int(metadata.streams[0].height), supports_streaming=True),), caption=filenames)

                os.remove(filenames)

            async def on_done_caller():
                nama = filename
                return on_done_handle
            # print('aaaa')
            try:
                if os.path.exists(str(infos['name']+"_"+filename+".mp4")):
                    # print(f"{infos['name']}_{filename}.mp4")
                    await on_done_handle(f"{infos['name']}_{filename}.mp4")
                else:
                    await start(f'https://coomer.party{path}',
                    f"{infos['name']}_{filename}.mp4",
                    ffmpeg_callback,
                    on_message=on_message_handler,
                    on_done=lambda: print(f"{infos['name']}_{filename}.mp4"),
                    wait_time=1)  # seconds

                    try:
                        await message.delete()
                        uploadmsg = await event.respond(f"Progres downloading {info['name']}_{filename}, Uploading ...")
                        await on_done_handle(f"{infos['name']}_{filename}.mp4")
                        await uploadmsg.delete()
                    except IOError :
                        return await fdl(path, filename, message, info)
            except (rexcep.JSONDecodeError, rexcep.HTTPError, sp.CalledProcessError) as E:
                print("Get DDoSed")
                get_ddg_cookies("https://coomer.party")
                time.sleep(10)
                return await fdl(path, filename, message, info)

        path, filename, info = await downloadvideo(pesan[1])

        await event.reply(f"Downloading all video of {info['name']}")
        
        allchat = await client.get_messages(event.chat_id,limit=10000)
        list_uploaded = []
        for a in allchat:
            if str(a.message).find(pesan[1]+"_") != -1:
                list_uploaded.append(a.message)
        print(list_uploaded)
        msg_existed = ""

        for p, f, in zip(path, filename):
            if info['name']+"_"+f+".mp4" in list_uploaded:
                if msg_existed == "":
                    msg_existed = await event.respond(info['name']+" is exist on chat, continuing.")
                else:
                    pass
                print(info['name']+"_"+f+".mp4", "is uploaded before, skipping")
                continue
            else:
                
                test = await event.respond(f"Progres downloading {info['name']}_{f} ... ")
                await fdl(p, f, test, info)
        await event.respond("Download complete!")
            

client.start()
client.run_until_disconnected()