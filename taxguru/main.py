import asyncio
import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Change this to your directory containing the XML files
xml_directory = 'xmls'


# Issue with updated_max which needs to be passed as a parameter
file_name = 'tax.json'


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
        res = requests.get(url, timeout=30)
        soup = BeautifulSoup(res.text, 'lxml')

        tables = soup.find_all('table')
        for table in tables:
            df = pd.read_html(table.prettify())[0]
            markdown_table = df.to_markdown(index=False)
            table.string = f'\n{markdown_table}\n'

        title = soup.find('h1').get_text() if soup.find(
            'h1') is not None else ""
        print(title)

        all_text = soup.find(class_='newsBoxPost margint-10').get_text()

        news_item = {
            'headline': title,
            'subheadline': '',
            'data': all_text,
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


async def scrape_page():
    i = 1

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Referer": "https://taxguru.in/filters/page/5/?cats=0&type=articles&court=0&pyear=0&pmonth&filters=Y"
    }

    while True:
        url = f"https://taxguru.in/filters/page/{i}/?cats=0&type=articles&court=0&pyear=0&pmonth&filters=Y"
        print(url)
        r = requests.get(url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.text)

        a_tags = [a.find('a').get('href') for a in soup.find_all(
            'h4', class_='newsBoxPostTitle')]

        print(len(a_tags))

        if len(a_tags) < 10:
            print('breaking')
            break

        tasks = []
        for a_tag in a_tags:
            task = get_data(a_tag)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        update_file(results)
        i += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_page())
