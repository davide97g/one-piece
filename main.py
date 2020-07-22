from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from send_mail import send_email

PATH = "C:\\Program Files (x86)\\chromedriver.exe"

time_to_wait = int(input("Time to wait:"))


def check_new_chapters():

    print("Check")

    class_name = "ChapterListItem-module_chapterListItem_ykICp"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mangaplus.shueisha.co.jp/titles/100020")

    # udpate_info = driver.find_element_by_class_name(
    #     "TitleDetailHeader-module_updateInfo_L3R3R")
    # if udpate_info.text is not None:
    #     release_info = udpate_info.text.split("\n")
    #     if len(release_info) > 1:
    #         release_date = release_info[1]
    #         print("Next release on ", release_date)
    # else:
    #     print("No release info available")

    df_scraper = pd.DataFrame(
        {'number': [], 'title': [], 'date': []}
    )

    try:
        chapter_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        for chapter in chapter_list:
            # find link
            links = chapter.find_elements_by_tag_name('a')
            link = links[0].get_attribute(
                'href') if len(links) > 0 else "-"
            link_parts = link.split("/")
            l = len(link_parts)
            chapter_id = link_parts[l-1] if l > 0 else '-'
            chapter_link = "https://mangaplus.shueisha.co.jp/viewer/"+chapter_id
            # find chapter metadata
            chapter_data = chapter.text.split("\n")
            chapter_number = chapter_data[0].replace("#", "")
            df_chapter = pd.DataFrame(
                {
                    'number': [int(chapter_number)],
                    'title': [chapter_data[1]],
                    'date': [chapter_data[2]],
                    'link': [chapter_link]
                }
            )
            df_scraper = df_scraper.append(df_chapter)

        if len(df_scraper) > 0:
            df = pd.read_csv("chapters.csv")
            df.sort_values(by="number", ascending=True, inplace=True)
            df_scraper.sort_values(by="number", ascending=True, inplace=True)
            if len(df) > 0:
                last_saved = int(df.tail(1)['number'])
            else:
                last_saved = 0  # take everything there is
            df_scraper['number'] = df_scraper['number'].astype(int)
            df_new_chapters = df_scraper.loc[df_scraper['number'] > last_saved]
            if len(df_new_chapters) > 0:
                # write to file
                df = df.append(df_new_chapters, ignore_index=True)
                df['number'] = df['number'].astype(int)
                df.to_csv("chapters.csv", index=False)
                # send notification
                if len(df_new_chapters) == 1:
                    # single new chapter
                    last_out = str(df_new_chapters.iloc[0]['number'])
                    last_link = str(df_new_chapters.iloc[0]['link'])
                    last_title = str(df_new_chapters.iloc[0]['title'])
                    subject = "One Piece "+last_out+" : \""+last_title+"\""
                    message = "Read chapter "+last_out+" : "+last_link
                    send_email(subject, message)
                else:
                    # multiple new chapters
                    chapters_number = list(df_new_chapters['number'])
                    chapters_link = list(df_new_chapters['link'])
                    C = len(df_new_chapters)
                    message = ""
                    for i in range(C):
                        message += "Read chapter " + \
                            str(chapters_number[i])+" : " + \
                            str(chapters_link[i])+"\n"
                    send_email("New One Piece Chapters are out!", message)
            else:
                print("---")
    except:
        print("Error")
        driver.quit()
        send_email("One piece Error",
                   "Hi sir developer, there was an error with your code. Pleae check.")
    finally:
        driver.quit()


while True:
    check_new_chapters()
    sleep(time_to_wait)
