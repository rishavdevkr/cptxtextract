import requests, os, sys, re
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
from details import SUDO_USERS
from subprocess import getstatusoutput
from utils import get_datetime_str, create_html_file
import asyncio, logging
from logging.handlers import RotatingFileHandler
import tgcrypto
import datetime

api = 'https://api.classplusapp.com/v2'

# ------------------------------------------------------------------------------------------------------------------------------- #

def create_html_file(file_name, batch_name, contents):
    tbody = ''
    parts = contents.split('\n')
    for part in parts:
        split_part = [item.strip() for item in part.split(':', 1)]
    
        text = split_part[0] if split_part[0] else 'Untitled'
        url = split_part[1].strip() if len(split_part) > 1 and split_part[1].strip() else 'No URL'

        tbody += f'<tr><td>{text}</td><td><a href="{url}" target="_blank">{url}</a></td></tr>'

    with open('cptxtextract/template.html', 'r') as fp:
        file_content = fp.read()
    title = batch_name.strip()
    with open(file_name, 'w') as fp:
        fp.write(file_content.replace('{{tbody_content}}', tbody).replace('{{batch_name}}', title))

def get_course_content(session, course_id, folder_id=0):
        fetched_contents = ""

        params = {
            'courseId': course_id,
            'folderId': folder_id,
        }

        res = session.get(f'{api}/course/content/get', params=params)

        if res.status_code == 200:
            res_json = res.json() 

            contents = res_json.get('data', {}).get('courseContent', [])

            for content in contents:
                if content['contentType'] == 1:
                    resources = content.get('resources', {})

                    if resources.get('videos') or resources.get('files'):
                        sub_contents = get_course_content(session, course_id, content['id'])
                        fetched_contents += sub_contents
                
                elif content['contentType'] == 2:
                    name = content.get('name', '')
                    id = content.get('contentHashId', '')

                    headers = {
                        "Host": "api.classplusapp.com",
                        "x-access-token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6OTIzNDIwMDUsIm9yZ0lkIjo1NDI0MjEsInR5cGUiOjEsIm1vYmlsZSI6IjkxODI5ODczMDAzNiIsIm5hbWUiOiJTdWRoYW5zaHUgSmhhIiwiZW1haWwiOiJzdWRoYW5zaHVqaGExNTFAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOnRydWUsIm9yZ0NvZGUiOiJ1Y3Z2YW8iLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiOGE5NTlhMGQ1Y2UyNjBkNzJhMDVhMzcxYTBhYzk5YmUiLCJpYXQiOjE3MDc0OTc2OTAsImV4cCI6MTcwODEwMjQ5MH0.68JhYbWAjf1B0a6hD4OGSmVhhH2WF97DX8DMJAfo5CkIwIVWABMugHN0Mz43LUoY",
                        "User-Agent": "Mobile-Android",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en",
                        "Origin": "https://web.classplusapp.com",
                        "Referer": "https://web.classplusapp.com/",
                        "Region": "IN",
                        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": "\"Windows\"",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                    }

                    params = {
                        'contentId': id
                    }

                    r = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                    url = r.json()['url']

                    content = f'{name}:{url}\n'
                    fetched_contents += content

                else:
                    name = content.get('name', '')
                    url = content.get('url', '')
                    content = f'{name}:{url}\n'
                    fetched_contents += content

        return fetched_contents



# ------------------------------------------------------------------------------------------------------------------------------- #

async def classplus_txt(app, message):   

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

    headers2 = {
        "Api-Version": "43",
        "Content-Type": "application/json;charset=UTF-8",
        "Device-Id": "1706954623055",
        "Origin": "https://web.classplusapp.com",
        "Referer": "https://web.classplusapp.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }
    
    try:
        input = await app.ask(message.chat.id, text="SEND YOUR CREDENTIALS AS SHOWN BELOW\n\nORGANISATION CODE:\n\nPHONE NUMBER:\n\nOR SEND\nACCESS TOKEN:")

        creds = input.text
        session = requests.Session()
        session.headers.update(headers2)

        logged_in = False

        if '\n' in creds:
            org_code, phone_no = [cred.strip() for cred in creds.split('\n')]

            if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                res = session.get(f'{api}/orgs/{org_code}')

                if res.status_code == 200:
                    res = res.json()

                    org_id = int(res['data']['orgId'])

                    data = {
                        'countryExt': '91',
                        'mobile'    : phone_no,
                        'orgCode'   : org_code,
                        'orgId'     : org_id,
                        'viaSms'    : 1,
                    }
        
                    res = session.post(f'{api}/otp/generate', data=json.dumps(data))

                    if res.status_code == 200:
                        res = res.json()

                        session_id = res['data']['sessionId']

                        user_otp = await app.ask(message.chat.id, text="Send your otp ")

                        if user_otp.text.isdigit():
                            otp = user_otp.text.strip()

                            data = {
                                "otp": otp,
                                "countryExt": "91",
                                "sessionId": session_id,
                                "orgId": org_id,
                                "fingerprintId": "",
                                "mobile": phone_no
                            }

                            res = session.post(f'{api}/users/verify', data=json.dumps(data))
                            res = res.json()
                            if res['status'] == 'success':
                                await app.send_message(message.chat.id, res)
                                user_id = res['data']['user']['id']
                                token = res['data']['token']
                                session.headers['x-access-token'] = token

                                await message.reply_text(f"Your access token for future uses -\n\n{token}")
                                
                                logged_in = True

                            else:
                                raise Exception('Failed to verify OTP.')  
                        raise Exception('Failed to validate OTP.')
                    raise Exception('Failed to generate OTP.')    
                raise Exception('Failed to get organization Id.')
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

                    num = await app.ask(message.chat.id, text=f"send index number of the course to download\n\n{text}")
                        
                    if num.text.isdigit() and len(num.text) <= len(courses):

                        selected_course_index = int(num.text.strip())

                        course = courses[selected_course_index - 1]

                        selected_course_id = course['id']
                        selected_course_name = course['name']

                        msg  = await message.reply_text("Now your extracting your course")
                            

                        course_content = get_course_content(session, selected_course_id)
                        await msg.delete()

                        if course_content:

                            caption = (f"App Name : Classplus\nBatch Name : {selected_course_name}")

                            
                            text_file = "Classplus"
                            with open(f'{text_file}.txt', 'w') as f:
                                f.write(f"{course_content}")

                            await app.send_document(message.chat.id, document=f"{text_file}.txt", caption=caption)

                            html_file = f'{text_file}.html'
                            create_html_file(html_file, selected_course_name, course_content)

                            await app.send_document(message.chat.id, html_file, caption=caption)
                            os.remove(f'{text_file}.txt')
                            os.remove(html_file)
                            

                        else:
                            raise Exception('Did not found any content in course.')
                    raise Exception('Failed to validate course selection.')
                raise Exception('Did not found any course.')
            raise Exception('Failed to get courses.')
            

   
    except Exception as e:
        print(f"Error: {e}")

bot.run()
