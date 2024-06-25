
"""
from os import getenv


API_ID = int(getenv("API_ID", "252674"))
API_HASH = getenv("API_HASH", "87c231f0e88239d06965b4351")
BOT_TOKEN = getenv("BOT_TOKEN", "719860076:AlCWppTjwTceBxWqDwpWP7UCEWuzI")
OWNER_ID = int(getenv("OWNER_ID", "680534720"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "99974195 20000898623").split()))
MONGO_URL = getenv("MONGO_DB", "mongodb+srv://daxxop:daxxop@daxxop.dg3umlc.mongodb.net/?retryWrites=true&w=majority")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-100285084"))

"""
#

import os
from os import getenv
# ---------------R---------------------------------
API_ID = int(os.environ.get("API_ID"))
# ------------------------------------------------
API_HASH = os.environ.get("API_HASH")
# ----------------D--------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# -----------------A-------------------------------
BOT_USERNAME = os.environ.get("BOT_USERNAME")
# ------------------X------------------------------
OWNER_ID = int(os.environ.get("OWNER_ID"))
# ------------------X------------------------------

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
# ------------------------------------------------
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))
# ------------------------------------------------
MONGO_URL = os.environ.get("MONGO_URL")
