import asyncio
import json
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

file_name = 'scc.json'


def update_file(data_list):
    existing_data = []

    with open(file_name, 'r', encoding='utf-8') as json_file:
        existing_data = json.load(json_file)

    # Combine existing data with new data
    combined_data = existing_data + data_list

    # Write the combined data back to the JSON file
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, ensure_ascii=False, indent=4)


async def get_data(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.find('h1', class_='entry-title').get_text() if soup.find(
        'h1', class_='entry-title') is not None else ""
    print(title)

    div = soup.find(class_='entry-content')

    sup_tags = soup.find_all('sup')
    tables = soup.find_all('tables')

    for sup in sup_tags:
        sup.string = f"[{sup.string}]"

    for table in tables:
        df = pd.read_html(table.prettify())[0]
        markdown_table = df.to_markdown(index=False)
        table.string = markdown_table

    news_item = {}
    if div:
        if div.find('div', class_=''):
            all_text = div.find('div', class_='').get_text()

            ref = [p.get_text() for p in soup.find(
                class_='entry-content').find_all('p', recursive=False)]

            all_text = all_text + "\n".join(ref)

            news_item = {
                'headline': title,
                'subheadline': '',
                'data': all_text,
            }
        else:
            all_text = ''
            for d in div.find_all(recursive=False):
                clasess = d.get('class', [])
                if any(class_name in clasess for class_name in ["jp-relatedposts", "sharedaddy", "twitter-share"]):
                    continue
                all_text = all_text + '\n' + d.get_text()
            news_item = {
                'headline': title,
                'subheadline': '',
                'data': div,
            }

    return news_item


async def main(url):
    i = 0

    while True:
        url_acts = f"{url}page/{i}/"
        response = requests.get(url_acts, timeout=30)
        soup = BeautifulSoup(response.text)

        elements = [element.find('a').get('href')
                    for element in soup.find_all('h2', 'entry-title')]
        print(url, i, len(elements))

        tasks = []
        for element in elements:
            data = get_data(element)
            tasks.append(data)

        data_list = await asyncio.gather(*tasks)
        print(data_list)
        update_file(data_list)

        if len(elements) < 20:
            print(f'Breaking for at {i}')
            break

        i += 1


urls = [

    'https://www.scconline.com/blog/post/category/op-ed/legal-analysis/',
    'https://www.scconline.com/blog/post/category/op-ed/scc-journal-section/',
    'https://www.scconline.com/blog/post/category/op-ed/practical-lawyer-archives/',



    'https://www.scconline.com/blog/post/category/experts_corner/',

    'https://www.scconline.com/blog/post/category/casebriefs/',

    'https://www.scconline.com/post/category/legislationupdates/',

    'https://www.scconline.com/blog/post/category/law-made-easy/'
]

# urls = ['https://www.scconline.com/blog/post/category/casebriefs/']


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for url in urls:
        loop.run_until_complete(main(url))
