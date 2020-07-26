from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chapter_list(path, url, id):
    driver = webdriver.Chrome(path)
    driver.get(url)
    chapter_list = []
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
