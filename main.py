import requests
from bs4 import BeautifulSoup
from SiteSelector import SiteSelector


url = 'https://www.food52.com/recipes/25530-joanne-chang-s-hot-and-sour-soup'
user_agent = ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
headers = {'User-Agent': user_agent}


response = requests.get(url, headers=headers)
if(response.status_code == 200):

    site = SiteSelector().get_site(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    obj = {
        "title": site.get_title(soup),
        "ingredients": site.get_ingredients(soup),
        "directions": site.get_directions(soup)
    }
    print(obj)
