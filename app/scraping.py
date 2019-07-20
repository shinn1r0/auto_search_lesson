from datetime import datetime, timedelta
import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *
from app.ifttt import ifttt_webhook


class Scraping:
    def __init__(self, headless=True):
        self.init_driver(headless)

    def init_driver(self, headless=True):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        self.driver: Chrome = Chrome(options=options)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(15)

    def quit_driver(self):
        self.driver.close()
        self.driver.quit()

    def get_status(self):
        try:
            self.driver.get(URL_TOP)
            current_url = self.driver.current_url
            if current_url == URL_TOP:
                print("not yet login")
                self.login()
            elif current_url == URL_MYPAGE:
                print("already login")

            self.wait.until(EC.url_to_be(URL_MYPAGE))

            return self.check_status()

        except (TimeoutException, NoSuchElementException):
            self.quit_driver()
            self.init_driver()
            return 'normal', sys.exc_info()[0]
        except WebDriverException:
            self.quit_driver()
            self.init_driver()
            return 'serious', sys.exc_info()[0]

    def login(self):
        try:
            self.driver.get(URL_LOGIN)
            element_id: WebElement = self.wait.until(
                EC.presence_of_element_located((By.ID, ID_ID))
            )
            element_id.send_keys(SITE_ID)

            element_pass: WebElement = self.wait.until(
                EC.presence_of_element_located((By.ID, ID_PASS))
            )
            element_pass.send_keys(SITE_PASS)

            element_submit: WebElement = self.wait.until(
                EC.presence_of_element_located((By.NAME, NAME_SUBMIT))
            )
            element_submit.send_keys(Keys.RETURN)

        except WebDriverException:
            raise

    def check_status(self):
        try:
            element_lesson_list = self.driver.find_element(By.ID, ID_TIMELINE)
            element_lesson_days = element_lesson_list.find_element(By.TAG_NAME, "p")
            lesson_latest_day = datetime.strptime(
                element_lesson_days.text, '%Y-%m-%d')
            today = datetime.today()
            if lesson_latest_day.day > today.day:
                reserve_day = 'tomorrow'
            elif lesson_latest_day.day == today.day:
                reserve_day = 'today'
            else:
                reserve_day = 'past'
            element_latest_lesson = element_lesson_list.find_element(By.CLASS_NAME, CLASS_DAY)
            element_tutor_name = element_latest_lesson.find_element(By.CLASS_NAME, CLASS_TUTOR)
            element_tutor_link = element_tutor_name.find_element(By.TAG_NAME, "a").get_attribute("href")
            if element_tutor_link == URL_TUTOR:
                tutor_book = True
            else:
                tutor_book = False
            element_lesson_time = element_latest_lesson.find_element(By.CLASS_NAME, CLASS_TIME)
            lesson_time = element_lesson_time.text.split('～')[0]
            if lesson_time.split(':')[0] == '24':
                lesson_time = lesson_time.replace('24', '00')
                lesson_latest_day = lesson_latest_day + timedelta(days=1)
            lesson_time = datetime.strptime(
                lesson_time, '%H:%M')
            lesson_time = datetime.combine(lesson_latest_day.date(), lesson_time.time())
            return tutor_book, reserve_day, lesson_time, today

        except WebDriverException:
            raise

    def get_open_lesson(self):
        try:
            today = datetime.today()
            lessons = self.get_day_open_lesson(today)
            tomorrow = today + timedelta(days=1)
            tomorrow_lessons = self.get_day_open_lesson(tomorrow)
            for tomorrow_lesson in tomorrow_lessons:
                lessons.append('tomorrow: ' + tomorrow_lesson)
            return lessons

        except (TimeoutException, NoSuchElementException):
            self.quit_driver()
            self.init_driver()
            return 'normal', sys.exc_info()[0]
        except WebDriverException:
            self.quit_driver()
            self.init_driver()
            return 'serious', sys.exc_info()[0]

    def get_day_open_lesson(self, day: datetime):
        try:
            day_url = URL_BOOKMARK + f"{day.year}/{day.month}/{day.day}/#page=1"
            self.driver.get(day_url)
            self.wait.until(EC.url_to_be(day_url))
            self.wait.until(EC.text_to_be_present_in_element(
                (By.CLASS_NAME, CLASS_RESULT_TTL),
                f"{day.year}年{day.month}月{day.day}日の検索結果"))
            element_tutor = self.driver.find_element(By.ID, ID_TUTOR)
            element_open_lesson_div = element_tutor.find_element(By.CLASS_NAME, CLASS_OPEN_LESSON)
            elements_open_lesson = element_open_lesson_div.find_elements(By.TAG_NAME, "a")
            lessons = list()
            if len(elements_open_lesson) != 0:
                for element_open_lesson in elements_open_lesson:
                    lessons.append(element_open_lesson.text)
            return lessons

        except WebDriverException:
            raise


if __name__ == "__main__":
    scraper = Scraping(headless=False)
    status = scraper.get_status()
    if type(status[0]) == str:
        if status[0] == "normal":
            print(status[1])
        elif status[0] == "serious":
            payload = {"value1": status}
            ifttt_webhook("system_error", payload=payload)
            print(status[1])
        exit(1)
    tutor_book, reserve_day, lesson_time, today = status
    print(tutor_book)
    print(reserve_day)
    print(today)
    print(lesson_time)
    # lesson_time = datetime.today() + timedelta(minutes=20)
    if lesson_time - timedelta(minutes=45) < today < lesson_time + timedelta(hours=1):
        print("in time")
    else:
        print("out time")
    # exit(0)
    result = scraper.get_open_lesson()
    if type(result) == tuple:
        if result[0] == "normal":
            print(result[1])
        elif result[0] == "serious":
            payload = {"value1": result}
            ifttt_webhook("system_error", payload=payload)
            print(result[1])
        exit(1)
    lessons = result
    print(lessons)
