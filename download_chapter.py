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
                    src, folder+'/page_'+str(page_counter)+".jpg")
                page_counter += 1
    except Exception as err:
        print(err)
        driver.quit()
    finally:
        driver.quit()


def get_chapters(url):
    try:
        chapters_folder = os.getcwd() + "/chapters"
        if not os.path.isdir(chapters_folder):
            os.mkdir(chapters_folder)
    except OSError:
        print("Directory creation failed.")
    finally:
        # ------------------------------------------------------------- need to get these with scraping and keep track of the past, already downloaded chapters
        chapter_list = ["983", "984", "985"]
        # constants
        class_name = "separator"
        folder = "chapters/"
        # loop over all chapters
        for chapter_number in chapter_list:
            new_chapter_folder = os.getcwd() + "/"+folder+chapter_number
            if os.path.isdir(new_chapter_folder):
                print("Chapter " + chapter_number+" already downloaded")
            else:
                os.mkdir(new_chapter_folder)
                chapter_url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"+chapter_number+"/"
                download(chapter_url, chapter_number,
                         class_name, new_chapter_folder)
                print("Chapter "+chapter_number+" downloaded")
                # zip files
                zipf = zipfile.ZipFile(
                    new_chapter_folder+'.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir(folder, chapter_number, zipf)
                zipf.close()
                print("Zip created")
                # send email
                send_mail_with_attachment(chapter_number)
                print("Email sent")


def zipdir(path, folder, ziph):
    # save current cwd
    cwd = os.getcwd()
    # ziph is zipfile handle
    os.chdir(path)
    for root, dirs, files in os.walk(folder):
        for file in files:
            ziph.write(os.path.join(root, file))
    # reset dir
    os.chdir(cwd)


url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"
get_chapters(url)

print("\n#################\n")
print("Finished")
