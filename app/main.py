from datetime import datetime
from time import sleep
import schedule
from ifttt import ifttt_webhook
from scraping import get_status, get_open_lesson


last_status = {
    "driver": None,
    "wait": None,
    "tutor_book": None,
    "reserve_day": None,
    "exec_day": None
}


def job():
    print("do job at", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    lessons = None
    today = datetime.today()
    if last_status["driver"] is not None and \
        last_status["tutor_book"] == True and \
        last_status["reserve_day"] == ("today" or "tomorrow") and \
        last_status["exec_day"].day == today.day:
        print("already booked")
    else:
        status = get_status(last_status["driver"], last_status["wait"])
        if status is None:
            exit(1)
        driver, wait, (tutor_book, reserve_day, exec_day) = status
        result = get_open_lesson(driver, wait)
        if result is None:
            exit(1)
        driver, wait, lessons = get_open_lesson(driver, wait)
        last_status["driver"] = driver
        last_status["wait"] = wait
        last_status["tutor_book"] = tutor_book
        last_status["reserve_day"] = reserve_day
        last_status["exec_day"] = exec_day
    if lessons is not None:
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
