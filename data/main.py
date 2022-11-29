import requests
import lxml
import json
import csv
import wget
from bs4 import BeautifulSoup as BS


def load_links():
    for n in range(232, 266):
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
        print(n)


def parse_page_links():
    for n in range(266):  # 266
        try:
            with open(f'index{n}.html', "r") as file:
                page = file.read()

            sp = BS(page, 'lxml')

            links_box = sp.find('div', class_='card-container').find_all('article', class_='card')
            dict_links = {}
            for i, item in enumerate(links_box):
                link = f"{'https://www.edimdoma.ru'}{item.find_next('a').get('href')}"
                title = item.find_next('img').get('alt')
                url = item.find_next('img').get('src')
                # wget.download(url=url)

                if title not in dict_links:
                    print(title)
                    dict_links[title] = (link, url)
            with open(f'page{n}.json', "w", encoding="utf-8") as f:
                json.dump(dict_links, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex, "NOT DATA", sep='\n')
        finally:
            print(n)


def repice():
    for n in range(1):
        try:
            with open(f'page{n}.json', "r") as file:
                dict_page = json.load(file)
            titles = []
            steps = []
            list3 = []
            dict_all_reciept = dict(zip(titles, (zip(steps, list3))))
            for k, v in dict_page.items():
                url = v[0]
                session = requests.Session()
                session.headers = {
                    "Accept-Encoding": "gzip, deflate, br",
                    "accept": "*/*",
                    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"
                }

                response = session.get(url)

                soup = BS(response.text, 'lxml')
                title = soup.find('h1', class_="recipe-header__name").text
                titles.append(title)
                print(title)
                print('\n')
                ingridients = soup.find('div', id='recipe_ingredients_block').find_all('span', class_='recipe_ingredient_title')

                for item in ingridients:
                    product = item.get_text()
                    print(product)

                print('\n')
                print('Рецепт пошагово:')
                print('\n')
                step_by_step = soup.find_all('div', class_="plain-text recipe_step_text")

                for s in step_by_step:
                    d = s.find_next('div').text
                    list3.append(d)
                    print(d)

        except Exception as ex:
            print(ex)
        finally:
            print(n)


if __name__ == '__main__':
    # load_links()
    # parse_page_links()
    repice()
