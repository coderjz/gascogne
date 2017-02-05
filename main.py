import hashlib
import requests
import os
import json
from bs4 import BeautifulSoup
from SiteSelector import SiteSelector


def write_file(url, contents, extension, dir="output"):
    """ Writes a file with the contents and extension passed.
     The file name is taken as the MD5 hash of our URL
     This will give us unique file names for each URL we fetch from """
    if not os.path.exists(dir):
        os.makedirs(dir)

    filename = dir + hashlib.md5(url.encode('utf-8')).hexdigest()
    if extension:
        filename += "." + extension

    with open(os.path.join(dir, filename), "w", encoding="utf-8") as file:
        file.write(contents)

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
    print(hashlib.md5(url.encode('utf-8')).hexdigest())
    write_file(url, json.dumps(obj), "json")
