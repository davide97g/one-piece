import os
import zipfile
# custom file imports
from send_mail import send_mail
from get_chapters import get_chapter_list
from download_chapter import download

DRIVER_PATH = "C:\\Program Files (x86)\\chromedriver.exe"


def get_chapters(path, url, folder, chapter_list, send_mail):
    try:
        chapters_folder = os.getcwd() + folder
        print(chapters_folder)
        if not os.path.isdir(chapters_folder):
            os.mkdir(chapters_folder)
    except OSError:
        print("Directory creation failed.")
    finally:
        # constants
        class_name = "separator"
        # loop over all chapters
        for chapter_number in chapter_list:
            new_chapter_folder = os.getcwd() + folder+chapter_number
            if os.path.isdir(new_chapter_folder):
                print("! chapter " + chapter_number+" already downloaded")
            else:
                os.mkdir(new_chapter_folder)
                chapter_url = "https://w16.read-onepiece.com/manga/one-piece-chapter-"+chapter_number+"/"
                # download chapter
                download(path, chapter_url, chapter_number,
                         class_name, new_chapter_folder)
                print("- chapter "+chapter_number+" downloaded")
                # zip files
                zipf = zipfile.ZipFile(
                    new_chapter_folder+'.zip', 'w', zipfile.ZIP_DEFLATED)
                zipdir(folder, chapter_number, zipf)
                zipf.close()
                print("- zip created")
                # send email
                if send_mail:
                    send_mail(chapter_number)
                    print("- email sent")


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


# almost same website, small difference in structure
domain1 = "w16.read-onepiece.com"
domain2 = "one-pieceonline.com"
useDomainOne = input("Which domain you wanna use?\n1:\'" +
                     domain1+"\' (1)\n2:\'"+domain2+"\' (2)\n")
if useDomainOne == "1":
    # find N-chapter
    domain = domain1
    print("Using "+domain)
    url_chapter_prefix = "https://w16.read-onepiece.com/manga/one-piece-chapter-"
    url_chapters = "https://w16.read-onepiece.com/"  # url to find list of chapters
    id = "ceo_latest_comics_widget-3"  # id to find list of chapters
    folder = "/../data/chapters/"  # where to download chapters
    chapter_list = get_chapter_list(DRIVER_PATH, url_chapters, id)
    get_chapters(DRIVER_PATH, url_chapter_prefix, folder, chapter_list, False)
else:
    domain = domain2
    print("Using "+domain)
