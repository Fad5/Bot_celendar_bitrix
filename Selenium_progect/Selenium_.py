import time
from selenium import webdriver
import json
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from Selenium_progect.handler_date import get_date

time.sleep(1)

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
LOGIN_PHONE = os.getenv("LOGIN")


# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Включить headless-режим
# chrome_options.add_argument("--disable-gpu")  # Отключить GPU (рекомендуется для стабильности)
# chrome_options.add_argument("--no-sandbox")  # Полезно для серверов
# chrome_options.add_argument("--disable-dev-shm-usage")  # Исправляет ошибки с памятью на некоторых системах

def open_site():
    cService = webdriver.ChromeService(
        executable_path='C:/Users/MK/PycharmProjects/Celendar_bitrix/Selenium_progect/chromedriver.exe')
    driver = webdriver.Chrome(service=cService)
    driver.get('https://apihide.com/bitrix/calendar/dashboard.php')
    return driver


def time_sleep():
    time.sleep(5)


def login(driver):
    """
    Функция для входа в битрикс24
    :return: None
    """
    btn_login = driver.find_element(By.CLASS_NAME, 'btn-link')
    btn_login.click()
    driver.find_element(By.ID, 'login').send_keys(LOGIN_PHONE)
    time_sleep()
    btn_con = driver.find_element(By.XPATH, f'//button[text()="Далее"]')
    btn_con.click()
    time_sleep()
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    btn_login_finish = driver.find_element(By.XPATH, f'//button[text()="Далее"]')
    btn_login_finish.click()
    time_sleep()


def click_next_day(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'fc-button-group')
    next_day = elements[0].find_elements(By.TAG_NAME, 'button')
    next_day[1].click()
    time_sleep()


def formatting_calendar(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'fc-button-group')
    time_sleep()
    btn_day = elements[1].find_elements(By.TAG_NAME, 'button')
    time_sleep()
    btn_day[1].click()


def get_order(driver):
    """
    Функция для отображения заказов
    :return:
    """
    time_sleep()
    decor = driver.find_elements(By.XPATH, './/div[@class="p-1" and text()="Д"]/../../../..')
    print(decor)
    return decor


def get_info_order(dddd, title_order, data_start, count=-1):
    date_today_correct = get_date()

    list_tr = []
    for i in dddd:
        print(data_start)
        td = i.find_elements(By.TAG_NAME, 'td')
        if count == -1:
            count += 1
        else:
            data = {
                'data_start': data_start.text,
                'title': title_order.text,
                "product": td[0].text,
                "count": td[2].text
            }
            list_tr.append(data)
            print(list_tr)
    return list_tr


def open_order(data, driver):
    list_order = []
    for i in data:
        i.click()
        time_sleep()
        dd = driver.find_element(By.CLASS_NAME, 'table-caption')
        tr = dd.find_elements(By.TAG_NAME, 'tr')
        title_order = driver.find_element(By.ID, 'details-body-title')
        data_start = driver.find_element(By.XPATH, '//h4[contains(@id, "details-body-title")]/div/span')
        result = get_info_order(tr, data_start=data_start, title_order=title_order)
        list_order.append(result)
        btn_close = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
        btn_close.click()
        time_sleep()
    return list_order


def write_json(name, data):
    with open(f'{name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def today_parsing(driver):
    data = get_order(driver)
    data_correct = open_order(data, driver)
    write_json('today', data_correct)


def tomorrow_parsing(driver):
    click_next_day(driver)
    data = get_order(driver)
    data_correct = open_order(data, driver)
    write_json('tomorrow', data_correct)


def after_tomorrow_parsing(driver):
    click_next_day(driver)
    data = get_order(driver)
    data_correct = open_order(data, driver)
    print(data_correct)
    write_json('after_tomorrow', data_correct)


def script():
    driver = open_site()
    login(driver)
    time_sleep()
    formatting_calendar(driver)
    time_sleep()
    today_parsing(driver)
    driver.close()


def script_tomorrow():
    driver = open_site()
    login(driver)
    time_sleep()
    formatting_calendar(driver)
    time_sleep()
    tomorrow_parsing(driver)
    driver.close()


def script_tomorrow2():
    driver = open_site()
    login(driver)
    time_sleep()
    formatting_calendar(driver)
    time_sleep()
    after_tomorrow_parsing(driver)
    driver.close()


try:
    script()
    script_tomorrow()
    script_tomorrow2()
    print('Ok')
except NoSuchElementException:
    script()
    script_tomorrow()
    script_tomorrow2()
    print('One more time')
    time.sleep(60)
