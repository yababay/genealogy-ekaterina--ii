#!/usr/bin/env python3

import re
import sys
import requests

from bs4 import BeautifulSoup

re_url = re.compile(r'https[^"]+')
re_key = re.compile(r'"[A-Z0-1]+"')

def main():
    with open('./src/lib/settings.json', 'r') as file:
        for line in file.readlines():
            if 'https' not in line:
                continue
            url = re.search(re_url, line)[0]
            key = re.search(re_key, line)[0]
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.select('#content p')
            weight = 0
            for p in content:
                weight += len(p.text)
            print(f'        {key}: {{"weight": {weight}, "link": "{url}"}}')

if __name__ == '__main__':
    main()
