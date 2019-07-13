from datetime import datetime
from time import sleep
import schedule
from ifttt import ifttt_webhook


def job():
    print("do job at", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    payload = {"value1": 3,
               "value2": ["21:00", "21:30", "23:00"]}
    r = ifttt_webhook("open_lesson", payload=payload)
    print(r.text)


def main():
    print('start scheduler')
    schedule.every(2).minutes.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
