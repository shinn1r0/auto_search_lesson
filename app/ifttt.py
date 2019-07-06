import requests
from app.settings import IFTTT_WEBHOOKS_KEY


def ifttt_webhook(eventid, payload=None):
    url = "https://maker.ifttt.com/trigger/" + eventid + "/with/key/" + IFTTT_WEBHOOKS_KEY
    response = requests.post(url, data=payload)
    return response


if __name__ == "__main__":
    payload = {"value1": 3,
               "value2": ["21:00", "21:30", "23:00"]}
    r = ifttt_webhook("open_lesson", payload=payload)
    print(r.text)