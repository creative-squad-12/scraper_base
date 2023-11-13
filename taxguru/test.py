

import json
import re

if __name__ == '__main__':
    with open('tax.json', 'r') as file:
        c = 0
        data = json.load(file)
        for d in data:
            # Check for non english characters
            pattern = r'^[\s\w\d\?><;,\{\}\[\]\-_\+=!@\#\$%^&\*\|\']*$'
            non_english_pattern = re.compile(pattern=pattern)

            non_english_characters = non_english_pattern.findall(d['headline'])
            if non_english_characters:
                print(d['headline'])
                c += 1
                continue
        print(c)
