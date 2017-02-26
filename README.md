# gascogne

## Introduction
Fetch recipes from other websites and store in HTML files.
This tool was built as I tend to use a lot of recipes from online websites and want an easy way to reference/archive them.  Tried copying them into Evernote, but realized it should be straightforward to parse the HTML content and download to a local file.

Supported sites are now in the file (more to be added soon!) https://github.com/coderjz/gascogne/blob/master/sites.py

## Usage
python main.py -u _URL_
* Downloads the recipe from the given URL and saves it to a file in the directory <application>/output/html
* Use the -o option to specify a different output directory

python main.py -f _FILE_
* Reads the recipe from a file and saves it as an HTML file with the same content as if downloaded from a URL.  Use this for sites that don't support automatic HTML downloading.
* For an example file, see: https://github.com/coderjz/gascogne/blob/master/testfiles/recipe.txt
