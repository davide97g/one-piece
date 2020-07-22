from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
class_name = "ChapterListItem-module_chapterListItem_ykICp"
driver = webdriver.Chrome(PATH)

driver.get("https://mangaplus.shueisha.co.jp/titles/100020")

chapters = {}

df_scraper = pd.DataFrame(
    {'number': [], 'title': [], 'date': []}
)

try:
    chapter_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
    )
    for chapter in chapter_list:
        chapter_data = chapter.text.split("\n")
        chapter_number = chapter_data[0].replace("#", "")
        df_chapter = pd.DataFrame(
            {
                'number': [int(chapter_number)],
                'title': [chapter_data[1]],
                'date': [chapter_data[2]]
            }
        )
        df_scraper = df_scraper.append(df_chapter)

    if len(df_scraper) > 0:
        df = pd.read_csv("chapters.csv")
        df.sort_values(by="number", ascending=True, inplace=True)
        df_scraper.sort_values(by="number", ascending=True, inplace=True)
        last_saved = int(df.tail(1)['number'])
        df_new_chapters = df_scraper.loc[df_scraper['number'] > last_saved]
        if len(df_new_chapters) > 0:
            print("New chapters are out!")
            print(df_new_chapters)
            df = df.append(df_new_chapters, ignore_index=True)
            df.to_csv("chapters.csv")
        else:
            print("Nothing new for now...")
except:
    print("Error")
    driver.quit()

driver.quit()