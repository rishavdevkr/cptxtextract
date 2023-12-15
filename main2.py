import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters, idle
from pyrogram.types.messages_and_media import message
from pyrogram.types import User, Message
from details import api_id, api_hash, bot_token, auth_users, sudo_user, log_channel, txt_channel
from subprocess import getstatusoutput
from utils import get_datetime_str, create_html_file
import asyncio, logging
from logging.handlers import RotatingFileHandler
import tgcrypto
import os
import sys
import re
import requests

from datetime import datetime

def get_datetime_str():
    # This function returns the current date and time as a string
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_html_file(filename, course_name, course_content):
    # This function creates an HTML file with the provided content
    with open(filename, 'w') as f:
        f.write('<html><body>\n')
        f.write(f'<h1>{course_name}</h1>\n')
        for item in course_content:
            f.write(f'<p>{item}</p>\n')
        f.write('</body></html>\n')

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

bot = Client(
    "bot",
    api_id= 22779671,
    api_hash= "125d8d88b77309dc3b154cbbfc2dacb2",    
    bot_token= "6847175705:AAHbkU8GFmzoxR9dCQTr6RuZ4NQsev5ufz0"
)

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i am **Classplus txt Downloader**.\n\n"
                              "**NOW:-** "
                                       
                                       "Press **/classplus** to continue..\n\n")

@bot.on_message(filters.command(["classplus"]))
async def account_login(bot: Client, m: Message):
    try:
        def get_course_content(session, course_id, folder_id=0):

            fetched_contents = []

            params = {
                'courseId': course_id,
                'folderId': folder_id,
            }

            res = session.get(f'{api}/course/content/get', params=params)

            if res.status_code == 200:
                res = res.json()

                contents = res['data']['courseContent']

                for content in contents:

                    if content['contentType'] == 1:
                        resources = content['resources']

                        if resources['videos'] or resources['files']:
                            sub_contents = get_course_content(session, course_id, content['id'])
                            fetched_contents += sub_contents

                    else:
                        name = content['name']
                        url = content['url']
                        fetched_contents.append(f'{name}: {url}')

            return fetched_contents

        headers = {
            'accept-encoding': 'gzip',
            'accept-language': 'EN',
            'api-version'    : '35',
            'app-version'    : '1.4.73.2',
            'build-number'   : '35',
            'connection'     : 'Keep-Alive',
            'content-type'   : 'application/json',
            'device-details' : 'Xiaomi_Redmi 7_SDK-32',
            'device-id'      : 'c28d3cb16bbdac01',
            'host'           : 'api.classplusapp.com',
            'region'         : 'IN',
            'user-agent'     : 'Mobile-Android',
            'webengage-luid' : '00000187-6fe4-5d41-a530-26186858be4c'
        }

        api = 'https://api.classplusapp.com/v2'

        reply = await m.reply(
            (
                '**'
                'Send your credentials as shown below.\n\n'
                'Organisation Code\n'
                'Phone Number\n\n'
                'OR\n\n'
                'Access Token'
                '**'
            ),
        
        )
        creds = reply.text
    print(f"Received credentials: {creds}")  # Add this line for debugging
    session = requests.Session()
    session.headers.update(headers)

    logged_in = False

    if '\n' in creds:
        credentials = creds.split('\n')
        if len(credentials) != 2:
            raise Exception('Invalid credentials format. Please provide exactly two lines: Organisation Code and Phone Number.')
        org_code, phone_no = [cred.strip() for cred in credentials]
    
            if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                res = session.get(f'{api}/orgs/{org_code}')

                if res.status_code == 200:
                    res = res.json()

                    org_id = int(res['data']['orgId'])

                    data = {
                        'countryExt': '91',
                        'mobile'    : phone_no,
                        'viaSms'    : 1,
                        'orgId'     : org_id,
                        'eventType' : 'login',
                        'otpHash'   : 'j7ej6eW5VO'
                    }
        
                    res = session.post(f'{api}/otp/generate', data=json.dumps(data))

                    if res.status_code == 200:
                        res = res.json()

                        session_id = res['data']['sessionId']

                        reply = await message.chat.ask(
                            (
                                '**'
                                'Send OTP ?'
                                '**'
                            )
                            ,reply_to_message_id = reply.id
                        )

                        if reply.text.isdigit():
                            otp = reply.text.strip()

                            data = {
                                'otp'          : otp,
                                'sessionId'    : session_id,
                                'orgId'        : org_id,
                                'fingerprintId': 'a3ee05fbde3958184f682839be4fd0f7',
                                'countryExt'   : '91',
                                'mobile'       : phone_no,
                            }

                            res = session.post(f'{api}/users/verify', data=json.dumps(data))

                            if res.status_code == 200:
                                res = res.json()

                                user_id = res['data']['user']['id']
                                token = res['data']['token']

                                session.headers['x-access-token'] = token

                                reply = await reply.reply(
                                    (
                                        '**'
                                        'Your Access Token for future uses - \n\n'
                                        '**'
                                        '<pre>'
                                        f'{token}'
                                        '</pre>'
                                    ),
                                    quote=True
                                )

                                logged_in = True

                            else:
                                raise Exception('Failed to verify OTP.')
                            
                        else:
                            raise Exception('Failed to validate OTP.')
                        
                    else:
                        raise Exception('Failed to generate OTP.')
                    
                else:
                    raise Exception('Failed to get organization Id.')
                
            else:
                raise Exception('Failed to validate credentials.') 

        else:

            token = creds.strip()
            session.headers['x-access-token'] = token


            res = session.get(f'{api}/users/details')

            if res.status_code == 200:
                res = res.json()

                user_id = res['data']['responseData']['user']['id']
                logged_in = True
            
            else:
                raise Exception('Failed to get user details.')


        if logged_in:

            params = {
                'userId': user_id,
                'tabCategoryId': 3
            }

            res = session.get(f'{api}/profiles/users/data', params=params)

            if res.status_code == 200:
                res = res.json()

                courses = res['data']['responseData']['coursesData']

                if courses:
                    text = ''

                    for cnt, course in enumerate(courses):
                        name = course['name']
                        text += f'{cnt + 1}. {name}\n'

                    reply = await message.chat.ask(
                        (
                            '**'
                            'Send index number of the course to download.\n\n'
                            f'{text}'
                            '**'
                        ),
                        reply_to_message_id = reply.id
                    )

                    if reply.text.isdigit() and len(reply.text) <= len(courses):

                        selected_course_index = int(reply.text.strip())

                        course = courses[selected_course_index - 1]

                        selected_course_id = course['id']
                        selected_course_name = course['name']

                        loader = await reply.reply(
                            (
                                '**'
                                'Extracting course...'
                                '**'
                            ),
                            quote=True
                        )

                        course_content = get_course_content(session, selected_course_id)

                        await loader.delete()

                        if course_content:

                            caption = (
                                '**'
                                'App Name : Classplus\n'
                                f'Batch Name : {selected_course_name}'
                                '**'
                            )

                            text_file = f'assets/{get_datetime_str()}.txt'
                            open(text_file, 'w').writelines(course_content)

                            await client.send_document(
                                message.chat.id,
                                text_file,
                                caption=caption,
                                file_name=f"{selected_course_name}.txt",
                                reply_to_message_id=reply.id
                            )

                            html_file = f'assets/{get_datetime_str()}.html'
                            create_html_file(html_file, selected_course_name, course_content)

                            await client.send_document(
                                message.chat.id,
                                html_file,
                                caption=caption,
                                file_name=f"{selected_course_name}.html",
                                                                reply_to_message_id=reply.id
                            )

                            os.remove(text_file)
                            os.remove(html_file)

                        else:
                            raise Exception('Did not found any content in course.')

                    else:
                        raise Exception('Failed to validate course selection.')

                else:
                    raise Exception('Did not found any course.')

            else:
                raise Exception('Failed to get courses.')
            

    except Exception as error:

        print(f'Error : {error}')

        await m.reply(
            (
                '**'
                f'Error : {error}'
                '**'
            ),
            quote=True
        )

bot.run()

