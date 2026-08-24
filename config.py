import os

from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_PREFIX = "!"
DATABASE_PATH = "storage/jjk.db"
