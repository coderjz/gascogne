import re
import requests
import os
import json
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from SiteSelector import SiteSelector
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse


def get_filename(site, title):
    return re.sub('[^a-zA-Z ]+', '', title) + "_" + site.get_short_name()


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


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', default=None,
                    help='URL to retrieve recipe from.')
args = parser.parse_args()

if args.url is not None:
    url = args.url
else:
    print("No URL Entered.  Exiting.")
    sys.exit()

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
        "directions": site.get_directions(soup),
        "url": url,
        "date_retrieved": datetime.now().strftime("%Y-%m-%d")
    }
    fname = get_filename(site, obj["title"])
    write_file(fname, json.dumps(obj), "json", os.path.join("output", "json"))
    write_file(fname, get_html(obj), "html", os.path.join("output", "html"))
