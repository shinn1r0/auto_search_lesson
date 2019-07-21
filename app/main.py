from datetime import datetime, timedelta
from time import sleep
import schedule
from ifttt import ifttt_webhook
from scraping import Scraping


scraper = Scraping(headless=True)
last_status = {
    "tutor_book": None,
    "reserve_day": None,
    "lesson_time": None,
    "exec_day": None
}


def job():
    print("do job at", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    fail_frag = False
    lessons = None
    today = datetime.today()
    lesson_time: datetime = last_status["lesson_time"]
    if last_status["lesson_time"] is not None and \
         lesson_time - timedelta(hours=1) < today < lesson_time + timedelta(hours=1):
        print("lesson time")
    elif last_status["tutor_book"] is not None and \
        last_status["tutor_book"] == True and \
        last_status["reserve_day"] == "today" and \
        lesson_time > today:
        print("already booked")
    elif last_status["tutor_book"] is not None and \
        last_status["tutor_book"] == True and \
        last_status["reserve_day"] == "tomorrow" and \
        last_status["exec_day"].day == today.day:
        print("already booked")
    else:
        status = scraper.get_status()
        if type(status[0]) == str:
            if status[0] == "normal":
                print(status[1])
            elif status[0] == "serious":
                payload = {"value1": status}
                ifttt_webhook("system_error", payload=payload)
                print(status[1])
            fail_frag = True
        if not fail_frag:
            tutor_book, reserve_day, lesson_time, exec_day = status
            result = scraper.get_open_lesson()
            if type(result) == tuple:
                if result[0] == "normal":
                    print(result[1])
                elif result[0] == "serious":
                    payload = {"value1": result}
                    ifttt_webhook("system_error", payload=payload)
                    print(result[1])
                fail_frag = True
            else:
                lessons = result
                last_status["tutor_book"] = tutor_book
                last_status["reserve_day"] = reserve_day
                last_status["lesson_time"] = lesson_time
                last_status["exec_day"] = exec_day

            if lessons is not None:
                if len(lessons) != 0:
                    payload = {"value1": len(lessons),
                               "value2": lessons}
                    r = ifttt_webhook("open_lesson", payload=payload)
                    print(r.text)
                else:
                    print("no lessons left")


def main():
    print('start scheduler')
    schedule.every(15).minutes.do(job)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
