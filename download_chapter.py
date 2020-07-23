from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import config
import urllib.request
import os


def download(url, chapter_number, class_name, folder):
    driver = webdriver.Chrome(config.DRIVER_PATH)
    driver.get(url)

    try:
        separators = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, class_name))
        )
        page_counter = 1
        for sep in separators:
            # find img tag
            img = sep.find_element_by_tag_name("img")
            # get src
            if img:
                src = img.get_attribute('src')
                # download the image
                urllib.request.urlretrieve(
                    src, folder+'page_'+str(page_counter)+".jpg")
                page_counter += 1
    except Exception as err:
        print(err)
        driver.quit()
    finally:
        driver.quit()


def get_chapters(url):
    try:
        chapters_folder = os.getcwd() + "/chapters"
        if os.path.isdir(chapters_folder):
            print("Directory already exists.")
        else:
            os.mkdir(chapters_folder)
    except OSError:
        print("Directory creation failed.")
    finally:
        chapter_list = ["983", "984", "985"]
        # constants
        class_name = "separator"
        folder = "chapters/"
        # loop over all chapters
        for chapter_number in chapter_list:
            new_chapter_folder = os.getcwd() + "/"+folder+chapter_number+"/"
            if os.path.isdir(new_chapter_folder):
                print("Chapter " + chapter_number+" already downloaded")
            else:
                os.mkdir(new_chapter_folder)
                chapter_url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"+chapter_number+"/"
                download(chapter_url, chapter_number,
                         class_name, new_chapter_folder)
                print(chapter_number+" downloaded")
        print("--- Download completed")


url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"
get_chapters(url)
