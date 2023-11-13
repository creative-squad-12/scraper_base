import asyncio
import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Change this to your directory containing the XML files
xml_directory = 'xmls'


def extract_urls_from_xml(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')  # Parse the XML using BeautifulSoup
        loc_tags = soup.find_all('loc')  # Find all <loc> tags
        # Extract the URLs and remove leading/trailing spaces
        urls = [loc.text.strip()
                for loc in loc_tags]
    return urls


# Issue with updated_max which needs to be passed as a parameter
file_name = 'cleartax.json'


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
    try:
        print(url)
        res = requests.get(url, timeout=30)
        soup = BeautifulSoup(res.text, 'lxml')
        print(soup)

        tables = soup.find_all('table')
        for table in tables:
            df = pd.read_html(table.prettify())[0]
            markdown_table = df.to_markdown(index=False)
            table.string = f'\n{markdown_table}\n'

        title = soup.find('h1').get_text() if soup.find(
            'h1') is not None else ""
        print(title)

        all_text = soup.find(
            class_='styles__MainLayout-sc-aoq1me-1').find('div', class_='').get_text()
        if all_text:
            sentences = re.split(r'\n{3,}', all_text)[0]

        news_item = {
            'headline': title,
            'subheadline': '',
            'data': sentences,
            # 'tag': tag,
        }

        return news_item
    except Exception as e:
        print(f"{e} for {url}")
        return {
            'headline': '',
            'subheadline': '',
            'data': '',
            'tag': '',
        }


async def process_batch(batch):
    tasks = []
    for element in batch:
        data = get_data(element)
        tasks.append(data)
    return await asyncio.gather(*tasks)


async def main():
    # xml_files = [f for f in os.listdir(xml_directory) if f.endswith('.xml')]
    xml_files = ['download.xml']
    urls = []

    for xml_file in xml_files:
        urls.extend(extract_urls_from_xml(xml_file))

    with open('urls.txt', 'r') as file:
        read_urls = file.readlines()
        read_urls = [u.strip() for u in read_urls]
        urls = [u.strip() for u in urls]

        a = set(urls) - set(read_urls)
        a = list(a)

        for i in range(0, len(a), 10):
            batch = a[i:i + 10]
            batch_result = await process_batch(batch)
            update_file(batch_result)


async def get_data_news(url):
    try:
        res = requests.get(url, timeout=30)
        soup = BeautifulSoup(res.text, 'lxml')
        title = soup.find('h1').get_text() if soup.find(
            'h1') is not None else ""
        print(title)

        div = soup.find(class_='content').find_all('p')
        all_text = "\n".join([p.get_text() for p in div])

        # tag = soup.find_all(class_='container')[3].get_text() if soup.find_all(
        #     class_='container') is not None else ""

        news_item = {
            'headline': title,
            'subheadline': '',
            'data': all_text,
            # 'tag': tag,
        }

        return news_item

    except Exception as e:
        print(f"{e} for {url}")
        return {
            'headline': '',
            'subheadline': '',
            'data': '',
            'tag': '',
        }


async def scrape_news_page(url):
    i = 1
    while True:
        print(url + f'page/{i}')
        r = requests.get(url + f'page/{i}')
        print(r.status_code)
        soup = BeautifulSoup(r.text)

        a_tags = [a.find('a').get('href') for a in soup.find_all(
            'article', class_='layout-list-alternative')]

        print(len(a_tags))

        if len(a_tags) < 10:
            print('breaking')
            break

        tasks = []
        for a_tag in a_tags:
            task = get_data_news(a_tag)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        update_file(results)
        i += 1


async def main_news():
    urls = ['https://news.cleartax.in/category/cleartax-explains/',
            'https://news.cleartax.in/category/tech/',
            'https://news.cleartax.in/category/tax-talks/']

    for url in urls:
        await scrape_news_page(url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
