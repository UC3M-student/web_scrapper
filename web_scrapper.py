import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.dia.es/compra-online/"

def get_data(url_sample):
    r = requests.get(url_sample)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def parse(soup):
    link_list = []
    results = soup.find_all("a", {"class":"btn-category"})
    w = "https://www.dia.es/"
    n = 0
    for link in results:
        a = link.get("href")
        link_list.append(w + a)

    href_list = set(link_list)
    print(href_list)


    return href_list

soup = get_data(url)
link_list = parse(soup)
for i in link_list:
    r = requests.get(i)
    soup2 = BeautifulSoup(r.text,"html.parser")
    print("copy one seccion")
    try:
        productlist = []
        results = soup2.find_all("div",{"class":"product-list__item"})
        for item in results:
            product = {
                "title": item.find("span", {"class": "details"}).text,
                "price": (item.find("p", {"class":"price"}).text.replace("&nbsp€","").strip().split()[0]),
                #"link" : item.find("a").get("href").text, Can´t run the programm wtih this sentence
            }
            productlist.append(product)
        listdf = pd.DataFrame(productlist)
        print(listdf)
        listdf.to_csv("hello.csv" ,mode="a",header=False)
        read_file = pd.read_csv("hello.csv")
        read_file.to_excel("hello.xlsx", index=None)


    except:
        print("the recollection of data can´t be possible")
