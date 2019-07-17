from datetime import datetime, timedelta
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *


def get_status():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(URL_TOP)
        current_url = driver.current_url
        if current_url == URL_TOP:
            print("not yet login")
            login(driver, wait)
        elif current_url == URL_MYPAGE:
            print("already login")

        wait.until(EC.url_to_be(URL_MYPAGE))

        return driver, wait, check_status(driver)

    except WebDriverException as e:
        print(e)
        driver.close()
        driver.quit()
        return None


def login(driver: Chrome, wait: WebDriverWait):
    try:
        driver.get(URL_LOGIN)
        element_id: WebElement = wait.until(
            EC.presence_of_element_located((By.ID, ID_ID))
        )
        element_id.send_keys(SITE_ID)

        element_pass: WebElement = wait.until(
            EC.presence_of_element_located((By.ID, ID_PASS))
        )
        element_pass.send_keys(SITE_PASS)

        element_submit: WebElement = wait.until(
            EC.presence_of_element_located((By.NAME, NAME_SUBMIT))
        )
        element_submit.send_keys(Keys.RETURN)

    except WebDriverException:
        raise WebDriverException


def check_status(driver: Chrome):
    try:
        element_lesson_list = driver.find_element(By.ID, ID_TIMELINE)
        element_lesson_days = element_lesson_list.find_elements(By.TAG_NAME, "p")
        lesson_latest_day = datetime.strptime(
            element_lesson_days[0].text, '%Y-%m-%d')
        today = datetime.today()
        if lesson_latest_day.day > today.day:
            reserve_day = 'tomorrow'
        elif lesson_latest_day.day == today.day:
            reserve_day = 'today'
        else:
            reserve_day = 'past'
        element_lesson_summary = element_lesson_list.find_elements(By.CLASS_NAME, CLASS_DAY)
        element_latest_lesson = element_lesson_summary[0]
        element_tutor_name = element_latest_lesson.find_element(By.CLASS_NAME, CLASS_TUTOR)
        element_tutor_link = element_tutor_name.find_element(By.TAG_NAME, "a").get_attribute("href")
        if element_tutor_link == URL_TUTOR:
            tutor_book = True
        else:
            tutor_book = False
        return tutor_book, reserve_day, today

    except WebDriverException:
        raise WebDriverException


def get_open_lesson(driver: Chrome, wait: WebDriverWait):
    try:
        today = datetime.today()
        lessons = get_day_open_lesson(driver, wait, today)
        tomorrow = today + timedelta(days=1)
        tomorrow_lessons = get_day_open_lesson(driver, wait, tomorrow)
        for tomorrow_lesson in tomorrow_lessons:
            lessons.append('tomorrow: ' + tomorrow_lesson)
        if len(lessons) == 0:
            return None
        else:
            return lessons

    except WebDriverException as e:
        print(e)
        return None
    finally:
        driver.close()
        driver.quit()


def get_day_open_lesson(driver: Chrome, wait: WebDriverWait, day: datetime):
    try:
        day_url = URL_BOOKMARK + f"{day.year}/{day.month}/{day.day}/#page=1"
        driver.get(day_url)
        wait.until(EC.url_to_be(day_url))
        wait.until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, CLASS_RESULT_TTL),
            f"{day.year}年{day.month}月{day.day}日の検索結果"))
        element_tutor = driver.find_element(By.ID, ID_TUTOR)
        element_open_lesson_div = element_tutor.find_element(By.CLASS_NAME, CLASS_OPEN_LESSON)
        elements_open_lesson = element_open_lesson_div.find_elements(By.TAG_NAME, "a")
        lessons = list()
        if len(elements_open_lesson) != 0:
            for element_open_lesson in elements_open_lesson:
                lessons.append(element_open_lesson.text)
        return lessons

    except WebDriverException:
        raise WebDriverException


if __name__ == "__main__":
    driver, wait, (tutor_book, reserve_day, today) = get_status()
    print(tutor_book)
    print(reserve_day)
    print(today)
    lessons = get_open_lesson(driver, wait)
    print(lessons)
