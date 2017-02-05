import re
import requests
import os
import json
from bs4 import BeautifulSoup
from SiteSelector import SiteSelector
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_filename(site, url):
    url = url.rsplit("/", 1)[-1]
    if(url.endswith(".html")):
        url = url[:-5]
    return re.sub('[^a-zA-Z ]+', '', url) + "_" + site.get_short_name()


def write_file(filename, contents, extension, dir="output"):
    if extension:
        filename += "." + extension

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(os.path.join(dir, filename), "w", encoding="utf-8") as file:
        file.write(contents)


def get_html(recipe):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('main.html')
    return template.render(recipe)


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
    fname = get_filename(site, url)
    write_file(fname, json.dumps(obj), "json", os.path.join("output", "json"))
    write_file(fname, get_html(obj), "html", os.path.join("output", "html"))
