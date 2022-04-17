import os
from pathlib import Path

scraping_method = None  # true for Folder, false for JSON
folder_dir = os.path.abspath(os.path.dirname(__file__))
baseURL = "https://artvee.com/"

print(folder_dir)
confirm_method = input(
    'Scrape into a folder with images or JSON with links? Type folder/json to continue \n')
if confirm_method.lower() == 'folder':
    scraping_method = True
    Path(folder_dir + "/downloads").mkdir(parents=True, exist_ok=True)
elif confirm_method.lower() == 'json':
    scraping_method = False
    Path(folder_dir + "/json").mkdir(parents=True, exist_ok=True)
