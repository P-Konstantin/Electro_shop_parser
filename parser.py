from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv


url = 'https://roboshop.spb.ru/kits/'


def getData(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    

    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        product_list = []
        link_list = []
        for child in bsObj.findAll('h4'):
            product_list.append(child.text) 
            link_list.append(child.a.get('href'))
        price_list1 = []
        for price in bsObj.findAll('p', class_='price'):
            price_list1.append(price.text)
            price_list2 = [price.replace('\n', '').strip() for price in price_list1]
            data = list(zip(product_list, price_list2, link_list))
    except AttributeError as e:
        return None
    return data


def saveData(data):
    with open('data', 'wt') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


result = getData(url)
if result == None:
    print('Data could not be found')
else:
    saveData(result)
