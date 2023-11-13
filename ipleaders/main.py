import asyncio
import json

import requests
from bs4 import BeautifulSoup

file_name = 'ipleaders.json'


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
    elements = soup.find(class_='td-post-content').children if soup.find(
        class_='td-post-content') is not None else []
    text = ""
    for e in elements:
        if not hasattr(e, 'get'):  # Check if it's a NavigableString
            continue
        if e.get('id') is None:
            text = text + "\n" + e.get_text()

    news_item = {
        'headline': title,
        'subheadline': '',
        'data': text,
    }

    return news_item


async def main():
    i = 484
    url = "https://blog.ipleaders.in/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=12.5"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI5NzQ3NTMiLCJhcCI6IjEwOTk5OTM5ODQiLCJpZCI6IjU0MmMzNDcyN2EzOWYxMmQiLCJ0ciI6IjlhYjMzNDAwMTYwOGUwMWJjYTVmMGQ3NzNlNmVjNzAwIiwidGkiOjE2OTM5MjkwMDM3MDl9fQ==",
        "traceparent": "00-9ab334001608e01bca5f0d773e6ec700-542c34727a39f12d-01",
        "tracestate": "2974753@nr=0-1-2974753-1099993984-542c34727a39f12d----1693929003709",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "X-NewRelic-ID": "Vg8AVVFWCxABVFhbDgYDUFQF",
        "X-Requested-With": "XMLHttpRequest"
    }
    while True:
        payload = {
            "action": "td_ajax_block",
            "td_atts": '{"custom_title":"","limit":"20","ajax_pagination":"infinite","block_type":"td_block_5","separator":"","custom_url":"","block_template_id":"","m3_tl":"","post_ids":"","category_id":"","taxonomies":"","category_ids":"","in_all_terms":"","tag_slug":"","autors_id":"","installed_post_types":"","include_cf_posts":"","exclude_cf_posts":"","sort":"","linked_posts":"","favourite_only":"","offset":"","open_in_new_window":"","show_modified_date":"","time_ago":"","time_ago_add_txt":"ago","time_ago_txt_pos":"","el_class":"","td_ajax_filter_type":"","td_ajax_filter_ids":"","td_filter_default_txt":"All","td_ajax_preloading":"","f_header_font_header":"","f_header_font_title":"Block header","f_header_font_settings":"","f_header_font_family":"","f_header_font_size":"","f_header_font_line_height":"","f_header_font_style":"","f_header_font_weight":"","f_header_font_transform":"","f_header_font_spacing":"","f_header_":"","f_ajax_font_title":"Ajax categories","f_ajax_font_settings":"","f_ajax_font_family":"","f_ajax_font_size":"","f_ajax_font_line_height":"","f_ajax_font_style":"","f_ajax_font_weight":"","f_ajax_font_transform":"","f_ajax_font_spacing":"","f_ajax_":"","f_more_font_title":"Load more button","f_more_font_settings":"","f_more_font_family":"","f_more_font_size":"","f_more_font_line_height":"","f_more_font_style":"","f_more_font_weight":"","f_more_font_transform":"","f_more_font_spacing":"","f_more_":"","m3f_title_font_header":"","m3f_title_font_title":"Article title","m3f_title_font_settings":"","m3f_title_font_family":"","m3f_title_font_size":"","m3f_title_font_line_height":"","m3f_title_font_style":"","m3f_title_font_weight":"","m3f_title_font_transform":"","m3f_title_font_spacing":"","m3f_title_":"","m3f_cat_font_title":"Article category tag","m3f_cat_font_settings":"","m3f_cat_font_family":"","m3f_cat_font_size":"","m3f_cat_font_line_height":"","m3f_cat_font_style":"","m3f_cat_font_weight":"","m3f_cat_font_transform":"","m3f_cat_font_spacing":"","m3f_cat_":"","m3f_meta_font_title":"Article meta info","m3f_meta_font_settings":"","m3f_meta_font_family":"","m3f_meta_font_size":"","m3f_meta_font_line_height":"","m3f_meta_font_style":"","m3f_meta_font_weight":"","m3f_meta_font_transform":"","m3f_meta_font_spacing":"","m3f_meta_":"","ajax_pagination_next_prev_swipe":"","ajax_pagination_infinite_stop":"","css":"","tdc_css":"","td_column_number":2,"header_color":"","color_preset":"","border_top":"","class":"tdi_6","tdc_css_class":"tdi_6","tdc_css_class_style":"tdi_6_rand_style"}',
            "td_block_id": "tdi_6",
            "td_column_number": 2,
            "td_current_page": i,
            "block_type": "td_block_5",
            "td_filter_value": "",
            "td_user_action": "",
            "td_magic_token": "83d6e89144"
        }

        # url_acts = f"https://blog.ipleaders.in/category/law-notes/law-of-torts-complete-reading-material/page/{i}/"
        response = requests.post(url, data=payload, headers=headers)
        soup = BeautifulSoup(json.loads(response.text)['td_data'])

        elements = [element.find('a').get('href')
                    for element in soup.find_all('h3', 'entry-title')]
        print(i, len(elements))

        tasks = []
        for element in elements:
            data = get_data(element)
            tasks.append(data)

        data_list = await asyncio.gather(*tasks)
        update_file(data_list)

        if (len(elements) < 20):
            break
        i += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
