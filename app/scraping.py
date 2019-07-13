from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *


def scraping():
    options = ChromeOptions()
    # options.add_argument('--headless')
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

        wait.until(EC.title_contains("マイページ"))

        check_lesson(driver, wait)
    except WebDriverWait:
        print("Error")
        raise
    finally:
        driver.close()
        driver.quit()


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


def check_lesson(driver: Chrome, wait: WebDriverWait):
    try:
        element_lesson_list = driver.find_element(By.ID, ID_TIMELINE)
        element_lesson_today = element_lesson_list.find_elements(
            By.TAG_NAME, "p")
        if len(element_lesson_today) != 0:
            print(element_lesson_today[0].text)

    except WebDriverException:
        raise WebDriverException


if __name__ == "__main__":
    scraping()