from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from send_mail import send_email

PATH = "C:\\Program Files (x86)\\chromedriver.exe"


def download_images():
    class_name = "zao-image"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mangaplus.shueisha.co.jp/viewer/1006998")

    try:
        image_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        print(image_list)
        for img in image_list:
            src = img.get_attribute('src')
            print(src)
            print("---------")
            # download the image
    except:
        print("Error")
        driver.quit()
    finally:
        driver.quit()


download_images()
