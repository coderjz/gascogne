# Handles the intermediate file representation
import json
import os
from util import write_file

class IntermediateFile:
    def __init__(self):
        self.filePath = "data.json"

    def get_contents(self):
        if not os.path.isfile(self.filePath):
            return []

        with open(self.filePath) as data_file:
            return json.load(data_file)

    # Adds a new recipe to our intermediate file
    # If the recipe already exists (based on filename), update the content
    def add_recipe(self, new_recipe):
        recipes = self.get_contents()
        recipes = [r for r in recipes if r["filename"] != new_recipe["filename"]]
        recipes.append(new_recipe)

        write_file(self.filePath, json.dumps(recipes))
