import requests
from bs4 import BeautifulSoup


def get_title(soup):
    return soup.select_one("h1.article-header-title").get_text()


def get_ingredients(soup):
    return [(elem.select_one(".recipe-list-quantity").get_text().strip() + " " +
            elem.select_one(".recipe-list-item-name").get_text().strip())
            .strip() for elem in soup.select("li[itemprop=ingredients]")]


def get_directions(soup):
    return [elem.get_text().strip()
            for elem in soup.select("li[itemprop=recipeInstructions]")]


url = 'https://food52.com/recipes/25530-joanne-chang-s-hot-and-sour-soup'
user_agent = ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
headers = {'User-Agent': user_agent}


response = requests.get(url, headers=headers)
if(response.status_code == 200):
    soup = BeautifulSoup(response.text, 'html.parser')
    obj = {
        "title": get_title(soup),
        "ingredients": get_ingredients(soup),
        "directions": get_directions(soup)
    }
