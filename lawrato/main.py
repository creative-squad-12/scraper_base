import asyncio
import json
import xml.etree.ElementTree as ET

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
                for loc in loc_tags if not any(substring in loc.text.strip() for substring in ['lawyers', '/advocate-'])]
    return urls


# Issue with updated_max which needs to be passed as a parameter
file_name = 'lawrato.json'


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
        title = soup.find('h1').get_text() if soup.find(
            'h1') is not None else ""
        print(title)
        data = soup.find(class_='content').get_text() if soup.find(
            class_='content') is not None else ""

        tag = soup.find_all(class_='container')[3].get_text() if soup.find_all(
            class_='container') is not None else ""

        news_item = {
            'headline': title,
            'subheadline': '',
            'data': data,
            'tag': tag,
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

    for i in range(0, len(urls), 30):
        batch = urls[i:i + 30]
        batch_result = await process_batch(batch)
        update_file(batch_result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
