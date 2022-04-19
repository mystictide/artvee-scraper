import os
from pathlib import Path
from functions import scraper
from guide import categories

scraping_method = None  # true for Folder, false for JSON
folder_dir = os.path.abspath(os.path.dirname(__file__))

print(" Scrape Artvee")
print()
confirm_method = input(
    ' scrape into a folder with downloaded images or JSON with direct links?\n type folder or json to continue \n')
print()
for f in categories:
    print("  "+f)
print()
confirm_cat = input(
    ' type all or a category name to begin\n')
if confirm_method.lower() == 'folder':
    scraping_method = True
    folder_dir += "/artvee-downloads/"
    Path(folder_dir).mkdir(parents=True, exist_ok=True)
elif confirm_method.lower() == 'json':
    scraping_method = False
    folder_dir += "/artvee-json/"
    Path(folder_dir).mkdir(parents=True, exist_ok=True)
print()
scraper(scraping_method, folder_dir, confirm_cat)