import requests
from bs4 import BeautifulSoup
import csv

CSV = 'obj.csv'
HOST = 'http://atech-parts.ru/'
URL = 'http://atech-parts.ru/catalog/special-oil/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,applic',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.5'
}

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

def get_cotnent(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-md-4 col-sm-6 col-xs-6')
    obj = []

    for item in items:
        obj.append(
            {
                'title': item.find('div', class_='title').get_text(strip=True),
                'link_prod': HOST + item.find('div', class_='title').find('a').get('href'),
                'image': HOST + item.find('div', class_='image').find('img').get('src')
            }
        )
    return obj

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название прдукта', 'Ссылка на продукт', 'Ссылка на изображение'])
        for item in items:
            writer.writerow([item['title'], item['link_prod'], item['image']])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        obj = []
        html = get_html(URL)
        obj.extend(get_cotnent(html.text))
        save_doc(obj, CSV)
    else:
        print('Error')

parser()