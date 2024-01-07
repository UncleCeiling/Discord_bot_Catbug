# pip install python-dotenv
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))
APPLICATION_ID = int(str(os.getenv("APPLICATION_ID")))