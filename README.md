# one-piece
Web scraper to notify when a new one piece chapter is out

## How it works

1. Scans the main webpage e get the list of all the available chapters
1. Compares the list to the previous list saved
1. For every chapter not in the saved list:
    - download the images
    - zip into a folder
    - send email

## Requirements

### python libs

- [Selenium](https://www.selenium.dev/) : `pip install selenium`
- [Pandas](https://pandas.pydata.org/) : `pip install pandas`

### others

- [Chrome](https://www.google.com/chrome/)
- [Chrome WebDriver](https://chromedriver.chromium.org/downloads)

## File organization

``` c
one-piece/
    - data/
        - chapters.csv
        - chapters/
            /* all the chapters downloaded*/
            - imgs/
            - zips/
    - scripts/
        - config.py /* store env config variables */
        - download_chapters.py
        - get_chapters.py
        - main.py 
        - send_mail.py
    - .gitignore
    - LICENSE
    - README.md
```