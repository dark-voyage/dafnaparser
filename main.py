import json
import re

from utils import get_links
import requests
from bs4 import BeautifulSoup

links = ['https://mebel.dafna.uz' + i if 'https://mebel.dafna.uz' not in i else i for i in get_links()]
session = requests.Session()
category_names = []
for i in links:
    s = session.get(i)
    soup = BeautifulSoup(s.text, 'html.parser')
    text = soup.findAll('h1', class_='df-block-title')[0].get_text()
    category_names.append([text, i])
f = open('categories.json')
categories = json.load(f)['categories']
f.close()
for i in range(len(categories)):
    categories[i]['link'] = None
    for j in range(len(category_names)):
        if category_names[j][0] == categories[i]['name']:
            categories[i]['link'] = category_names[j][1]
            del category_names[j]
            break
for i in range(len(categories)):
    categories[i]['product_ids'] = []
    if categories[i]['link'] is not None:
        s = session.get(categories[i]['link'])
        soup = BeautifulSoup(s.text, 'html.parser')
        product_ids = soup.findAll('a', href=True)
        pat = re.compile("\/category\/detail\?id=\S{36}")
        product_ids = [i['href'].split('=')[-1] for i in product_ids if pat.match(i['href'])]
        categories[i]['product_ids'] = product_ids

f = open('products.json')
products = json.load(f)['products']
f.close()
for i in range(len(products)):
    products[i]['category_ids'] = []
    for j in categories:
        if products[i]['id'] in j['product_ids']:
            products[i]['category_ids'].append(j['id'])
import os

if not os.path.exists('/output'):
    os.makedirs('/output')
json_object = json.dumps(products, indent=4)
with open("output/products_parsed.json", "w") as outfile:
    outfile.write(json_object)

json_object = json.dumps(categories, indent=4)
with open("output/categories_parsed.json", "w") as outfile:
    outfile.write(json_object)
