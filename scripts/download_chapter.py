from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request


def download(path, url, chapter_number, class_name, folder):
    driver = webdriver.Chrome(path)
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
                    src, folder+'/page_'+str(page_counter)+".jpg")
                page_counter += 1
    except Exception as err:
        print(err)
        driver.quit()
    finally:
        driver.quit()
