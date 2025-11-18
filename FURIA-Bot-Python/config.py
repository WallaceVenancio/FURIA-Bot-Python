# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PANDASCORE_TOKEN = os.getenv("PANDASCORE_TOKEN")

TEAM_ID = 124530
TEAM_NAME = "FURIA"