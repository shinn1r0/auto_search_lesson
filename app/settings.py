import os
from pathlib import Path
from dotenv import load_dotenv


env_path = (Path(__file__) / '..' / '..' / '.env').resolve()
load_dotenv(dotenv_path=env_path)
IFTTT_WEBHOOKS_KEY = os.getenv("IFTTT_WEBHOOKS_KEY")
SITE_ID = os.getenv("SITE_ID")
SITE_PASS = os.getenv("SITE_PASS")
URL_TOP = os.getenv("URL_TOP")
URL_MYPAGE = os.getenv("URL_MYPAGE")
URL_LOGIN = os.getenv("URL_LOGIN")
ID_ID = os.getenv("ID_ID")
ID_PASS = os.getenv("ID_PASS")
NAME_SUBMIT = os.getenv("NAME_SUBMIT")
ID_TIMELINE = os.getenv("ID_TIMELINE")
CLASS_DAY = os.getenv("CLASS_DAY")
CLASS_TUTOR = os.getenv("CLASS_TUTOR")
URL_TUTOR = os.getenv("URL_TUTOR")
URL_BOOKMARK = os.getenv("URL_BOOKMARK")
ID_TUTOR = os.getenv("ID_TUTOR")
CLASS_RESULT_TTL = os.getenv("CLASS_RESULT_TTL")
CLASS_OPEN_LESSON = os.getenv("CLASS_OPEN_LESSON")
