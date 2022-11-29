import requests
import lxml
import json

import wget
from bs4 import BeautifulSoup as BS


def load_links():
    for n in range(266):
        url = f"https://www.edimdoma.ru/retsepty/tags/400-prostye-retsepty-na-kazhdyy-den?page={n}"
        session = requests.Session()
        session.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
        }

        response = session.get(url)
        print(response)
        with open(f'index{n}.html', "w", encoding='utf-8') as file:
            file.write(response.text)


def parse_page_links():
    for n in range(266):
        try:
            with open(f'index{n}.html', "r") as file:
                page = file.read()

            sp = BS(page, 'lxml')

            links_box = sp.find('div', class_='card-container').find_all('article', class_='card')
            dict_links = {}
            for item in links_box:
                link = f"{'https://www.edimdoma.ru/retsepty/tags/400-prostye-retsepty-na-kazhdyy-den'}{item.find_next('a').get('href')}"
                title = item.find_next('img').get('alt')
                url = item.find_next('img').get('src')

                if title not in dict_links:
                    print(title)
                    wget.download(url=url)
                    dict_links[title] = link

                with open(f'page.json', "a") as f:
                    json.dump(dict_links, f, indent=4, ensure_ascii=False)

        except Exception as ex:
            print(ex, "NOT DATA", sep='\n')
        finally:
            print(n)


if __name__ == '__main__':
    load_links()
    parse_page_links()
