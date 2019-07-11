import os
from pathlib import Path
from dotenv import load_dotenv


env_path = (Path(__file__) / '..' / '..' / '.env').resolve()
load_dotenv(dotenv_path=env_path)
IFTTT_WEBHOOKS_KEY = os.getenv("IFTTT_WEBHOOKS_KEY")
SITE_ID = os.getenv("SITE_ID")
SITE_PASS = os.getenv("SITE_PASS")