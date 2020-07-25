from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import config
import urllib.request
import os
import zipfile
from send_mail import send_mail_with_attachment


def get_chapter_list(url):
    driver = webdriver.Chrome(config.DRIVER_PATH)
    driver.get(url)
    chapter_list = []
    id = "ceo_latest_comics_widget-3"
    try:
        chapter_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, id))
        )
        chapters = WebDriverWait(chapter_container, 10).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, "li"))
        )
        for chapter in chapters:
            text = chapter.text
            splitting = text.split(" ")
            if len(splitting) > 0:
                chapter_list.append(splitting[len(splitting)-1])
    except Exception as err:
        print(err)
        driver.quit()
        return []
    finally:
        driver.quit()
        return chapter_list
