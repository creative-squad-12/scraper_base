

import json

import markdownify
import requests
from bs4 import BeautifulSoup
from flask import request
from torch import conv1d

from utils import convert_table

# url = 'https://cleartax.in/s/gst-on-iphone'

# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'lxml')
# div = soup.find(
#     'div', class_='styles__MainLayout-sc-aoq1me-1 kKRAHs').find('div', class_='')


# all_text = ''


# for d in div.find_all(recursive=False):
#     if d.name == 'table':
#         all_text = all_text + '\n' + convert_table(d)
#     elif d.find('table'):
#         all_text = all_text + '\n' + convert_table(d.find('table'))
#     else:
#         all_text = all_text + "\n" + d.get_text()


with open('cleartax_new.json', 'r') as file, open('cleartax.jsonl', 'w+') as file2:
    data = json.load(file)
    for d in data:
        if d['headline']:
            file2.write(json.dumps({
                'title': d['headline'].strip(),
                'text': d['data'].strip(),
            }, ensure_ascii=False)+'\n')
