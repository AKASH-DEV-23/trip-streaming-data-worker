import os
from dotenv import load_dotenv

load_dotenv()

EVENTHUB_CONNECTION_STRING = os.getenv("EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

if not EVENTHUB_CONNECTION_STRING or not EVENTHUB_NAME:
    raise ValueError("Missing EVENTHUB configuration in .env")
