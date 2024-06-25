import os
from os import getenv


API_ID = int(getenv("API_ID", 25218674))
API_HASH = getenv("API_HASH", "87c231f0e8704795b8239d06965b4351")
BOT_TOKEN = getenv("BOT_TOKEN", "7198600769:AAGW4WAlCWppTjwTceBxWqDwpWP7UCEWuzI")
OWNER_ID = int(getenv("OWNER_ID", "6805344720"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "999741495  20000898623").split()))
MONGO_URL = getenv("MONGO_DB", "mongodb+srv://daxxop:daxxop@daxxop.dg3umlc.mongodb.net/?retryWrites=true&w=majority")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002038285084"))
