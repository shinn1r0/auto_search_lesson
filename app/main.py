from datetime import datetime
from time import sleep
import schedule
from ifttt import ifttt_webhook
from scraping import get_status, get_open_lesson


last_status = {
    "tutor_book": None,
    "reserve_day": None,
    "exec_day": None
}


def job():
    print("do job at", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    lessons = None
    today = datetime.today()
    if last_status["tutor_book"] is not None and \
        last_status["tutor_book"] == True and \
        last_status["reserve_day"] == ("today" or "tomorrow") and \
        last_status["exec_day"].day == today.day:
        print("already booked")
    else:
        status = get_status()
        if status is None:
            exit(1)
        driver, wait, (tutor_book, reserve_day, exec_day) = status
        last_status["tutor_book"] = tutor_book
        last_status["reserve_day"] = reserve_day
        last_status["exec_day"] = exec_day
        lessons = get_open_lesson(driver, wait)
    if lessons is not None:
        payload = {"value1": len(lessons),
                   "value2": lessons}
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
