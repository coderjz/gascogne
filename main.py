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

json_dir = os.path.join("output", "json")
html_dir = os.path.join("output", "html")


def get_filename(site, title):
    return re.sub('[^a-zA-Z ]+', '', title) + "_" + site.get_short_name()


def write_file(filename, contents, extension, dir):
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


def generate_from_url(url):
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
        write_file(fname, json.dumps(obj), "json", json_dir)
        write_file(fname, get_html(obj), "html", html_dir)


# Read all JSON files and regenerate the HTML files
def regenerate_from_json():
    for filename in os.listdir(json_dir):
        with open(os.path.join(json_dir, filename)) as data_file:
            data = json.load(data_file)
            fileNameNoExt = os.path.splitext(filename)[0]
            write_file(fileNameNoExt, get_html(data), "html", html_dir)


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', default=None,
                    help='URL to retrieve recipe from.')

# TODO: Need to make this not be an argument but just a single flag
parser.add_argument("--regen-json", dest='regen_json', action='store_true',
                    help='Regenerate all HTML files from json files')
parser.set_defaults(regen_json=False)
args = parser.parse_args()

if args.regen_json is not False:
    regenerate_from_json()
elif args.url is not None:
    url = args.url
    generate_from_url(url)
else:
    print("Must add valid arguments.  Exiting.")
    sys.exit()
