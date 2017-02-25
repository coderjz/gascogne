import re
import requests
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from SiteSelector import SiteSelector
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse
from IntermediateFile import IntermediateFile
from util import write_file

json_file = "data.json"
html_dir = os.path.join("output", "html")
inter_file = IntermediateFile()


def get_filename(site, title):
    return re.sub('[^a-zA-Z ]+', '', title) + "_" + \
           site.get_short_name() + ".html"


def get_html(recipe):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('main.html')
    return template.render(recipe)


def write_recipe_obj(recipe):
    inter_file.add_recipe(recipe)
    write_file(os.path.join(html_dir, recipe["filename"]), get_html(recipe))


def generate_from_url(url):
    user_agent = ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    headers = {'User-Agent': user_agent}

    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        site = SiteSelector().get_site(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = site.get_title(soup)
        fname = get_filename(site, title)
        obj = {
            "title": title,
            "ingredients": site.get_ingredients(soup),
            "directions": site.get_directions(soup),
            "url": url,
            "filename": fname,
            "date_retrieved": datetime.now().strftime("%Y-%m-%d")
        }
    write_recipe_obj(obj)


def generate_from_file(filename):
    obj = {
        "date_retrieved": datetime.now().strftime("%Y-%m-%d")
    }
    multi_line_behaviour = ["ingredients", "directions"]
    single_line_behaviour = ["url", "title"]
    all_keys = single_line_behaviour + multi_line_behaviour
    for k in single_line_behaviour:
        obj[k] = ""
    for k in multi_line_behaviour:
        obj[k] = []
    behaviour = ""

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            elif line.lower() in all_keys:
                behaviour = line.lower()
            else:
                if behaviour in single_line_behaviour:
                    obj[behaviour] = line
                    behaviour = ""
                elif behaviour in multi_line_behaviour:
                    obj[behaviour].append(line)

    for k in all_keys:
        if len(obj[k]) == 0:
            print("Error reading file.  No entry found for " + k)

    obj["filename"] = re.sub('[^a-zA-Z ]+', '', obj["title"]) + "_FILE.html"
    write_recipe_obj(obj)


# Read all JSON files and regenerate the HTML files
def regenerate_from_json():
    recipes = inter_file.get_contents()
    for r in recipes:
        write_file(os.path.join(html_dir, r["filename"]), get_html(r))


# Manage the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', default=None,
                    help='URL to retrieve recipe from.')
parser.add_argument('-f', '--file', default=None,
                    help='File to retrieve recipe from.')
parser.add_argument("--regen-json", dest='regen_json', action='store_true',
                    help='Regenerate all HTML files from json files')
parser.add_argument('-i', '--intermediate_file', default=None,
                    help='Location of the intermediate file to use')
parser.add_argument('-o', '--output_dir', default=None,
                    help='Location to output the HTML files')
parser.set_defaults(regen_json=False)
args = parser.parse_args()


if args.intermediate_file is not None:
    inter_file.file_path
if args.output_dir is not None:
    html_dir = os.path.normpath(args.output_dir)

if args.regen_json is not False:
    regenerate_from_json()
elif args.url is not None:
    generate_from_url(args.url)
elif args.file is not None:
    generate_from_file(args.file)
else:
    print("Must add valid arguments.  Exiting.")
    sys.exit()
