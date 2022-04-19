import os
import json
import lxml
import cchardet
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from guide import categories

requests_session = requests.Session()
baseURL = "https://artvee.com/c/"


def scraper(method, path, category):
    print("this will definitely take a while..")
    if category == "all":
        try:
            for f in categories:
                page = requests_session.get(baseURL + f + '/page/' + "1")
                soup = BeautifulSoup(page.text, "lxml")
                total_pages = soup.select_one(
                    "ul.page-numbers").find_all("li")[-2].get_text().replace(',', '')
                if method == True:
                    savetoFolder(f, total_pages, path)
                    print()
                else:
                    savetoJSON(f, total_pages, path)
                    print()
            successInformer(path)
        except Exception as e:
            errorInformer(e)
    else:
        try:
            page = requests_session.get(baseURL + category + '/page/' + "1")
            soup = BeautifulSoup(page.text, "lxml")
            total_pages = soup.select_one(
                "ul.page-numbers").find_all("li")[-2].get_text().replace(',', '')
            if method == True:
                savetoFolder(category, total_pages, path)
                print()
            else:
                savetoJSON(category, total_pages, path)
                print()
            successInformer(path)
        except Exception as e:
            errorInformer(e)


def savetoFolder(cat, total_pages, path):
    Path(path + cat).mkdir(parents=True, exist_ok=True)
    for i in range(1, int(total_pages)+1):
        pageInformer(i, total_pages, cat)
        page = requests_session.get(baseURL + cat + '/page/' + str(i))
        soup = BeautifulSoup(page.text, "lxml")
        artwork_divs = soup.find_all("div", class_="product-wrapper")
        try:
            for i in artwork_divs:
                anchor = i.find(
                    'div', class_="product-element-top").find("a", class_="product-image-link")
                imgurl = anchor.find('img')['src']
                info = i.find('div', class_="product-element-bottom")
                art_info = info.find("h3", class_="product-title").a.get_text()
                title = art_info.split("(")[0].rstrip()
                img_data = requests.get(imgurl).content
                with open(path + cat + "/" + title + '.jpg', 'wb') as handler:
                    handler.write(img_data)
        except:
            continue


def savetoJSON(cat, total_pages, path):
    artworkArr = []
    for i in range(1, int(total_pages)+1):
        pageInformer(i, total_pages, cat)
        page = requests_session.get(baseURL + cat + '/page/' + str(i))
        soup = BeautifulSoup(page.text, "lxml")
        artwork_divs = soup.find_all("div", class_="product-wrapper")
        try:
            for i in artwork_divs:
                anchor = i.find(
                    'div', class_="product-element-top").find("a", class_="product-image-link")
                dataid = anchor['data-id']
                imgurl = anchor.find('img')['src']

                info = i.find('div', class_="product-element-bottom")
                author = info.find(
                    "div", class_="woodmart-product-brands-links").a.get_text()
                art_info = info.find("h3", class_="product-title").a.get_text()
                title = art_info.split("(")[0].rstrip()
                year = art_info[art_info.rfind("(")+1:art_info.rfind(")")]
                int_check = year[0:4]
                if not int_check.isdigit():
                    year = "unknown"
                artwork = {"id": dataid, "title": title, "year": year,
                           "author": author, "category": cat, "image_url": imgurl}
                artworkArr.append(artwork)
        except:
            continue
    with open(path + "artvee-" + cat + ".json", 'w', encoding='utf-8') as f:
        json.dump(artworkArr, f, ensure_ascii=False, indent=4)


def pageInformer(page, totalpages, category):
    print("scraping page " + str(page) + "/" + str(totalpages) +
          " on " + category + " category", end='\r')


def successInformer(path):
    print()
    print("whew.. we're finally done.")
    os.startfile(path)


def errorInformer(e):
    print()
    print(e)
