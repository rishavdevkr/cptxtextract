import json
import subprocess
import tgcrypto
import time
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message
import helper
import os
import re
import requests

os.makedirs("./downloads", exist_ok=True)
bot = Client(
    "MG Concept",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i can download **Videos** from **MgConcept.**\n\nstart downloading pdfs with command /url")           
@bot.on_message(filters.command(["url"])& ~filters.edited)
async def pdf_url(bot: Client, m: Message):
    editable = await m.reply_text("INPUT URL")

    input1: Message = await bot.listen(editable.chat.id)    
    mm=str(input1.text)
    await input1.delete(True)
    topicUrl = requests.get(input1.text).json()
    for data in topicUrl:
         await m.reply_text((data["topic_id"]) +": "+str(data["topic_name"]))
    input3=Message=await bot.listen(editable.chat.id)
    mn=str(input3.text)
    await input3.delete(True)
    s1=str(mm).replace('get_content_topic','course_details_video') +"/"+ (mn)
    request=requests.get(s1).json()
    
    for data in request:
       try:
        name=(data["content_title"])
        await m.reply_text(f"**Downloading :- **'{name}'")
        s="https://youtu.be/"+ str(data["video_id"]) 
        
        cmd=f'yt-dlp -o "{name}.webm" "{s}"'
        os.system(cmd)
        #s1=re.sub('\s+', '%20', s)
        filename=f"{name}.webm"
        
        #dl=(f'yt-dlp "{s1}"')
        
        #subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:19 -vframes 1 "{filename}.jpg"', shell=True)
        #thumbnail=f"{filename}.jpg"
       # dur = int(helper.duration(filename))
        
        await m.reply_document(f"{name}.webm",caption=name)
        os.remove(f"{name}.webm")
        #os.remove(f"{name}.jpg")
        
       except Exception as e:
        await m.reply_text(str(e))
       await m.reply_text("Done")
        

            
        
         
       
bot.run()
