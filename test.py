# Allow long lines for test file
# pylama:ignore=E501

from unittest import TestCase
from main import create_parser, run_main, clean_recipe_object
import os
import shutil
from intermediate_file import IntermediateFile


class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    Source: http://dustinrcollins.com/testing-python-command-line-apps
    """
    @classmethod
    def setUpClass(cls):
        cls.parser = create_parser()


class MainTestCase(CommandLineTestCase):
    # Move the default outputs to a temporary "backup" folder
    def setUp(self):
        if(os.path.isfile("data.json")):
            os.rename("data.json", "data.json.bak")
        if(os.path.isdir("output")):
            os.rename("output", "outputbak")

    # Move the "backup" folder back to the default outputs
    # Remove temp folders (do it here in case test fails!)
    def tearDown(self):
        if(os.path.isfile("data.json")):
            os.remove("data.json")
        if(os.path.isdir("output")):
            shutil.rmtree("output")
        if(os.path.isfile("data.json.bak")):
            os.rename("data.json.bak", "data.json")
        if(os.path.isdir("outputbak")):
            os.rename("outputbak", "output")

        if(os.path.isdir("tmp_zz")):
            shutil.rmtree("tmp_zz")

    def _num_files_in_dir(self, dir):
        return len([name for name in os.listdir(dir) if
                    os.path.isfile(os.path.join(dir, name))])

    def test_download_default_URL(self):
        url = 'https://food52.com/recipes/9743-roasted-carrot-soup'
        args = self.parser.parse_args(['-u', url])
        run_main(self.parser, args)

        data_file = 'data.json'
        html_file = 'output/html/Roasted CarrotSoup_F52.html'
        html_dir = 'output/html'
        self.assertTrue(os.path.isfile(data_file))
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(1, self._num_files_in_dir(html_dir))

        url = 'https://food52.com/recipes/64163-roasted-veggie-ciabatta-sandwich-gluten-free'
        args = self.parser.parse_args(['-u', url])
        run_main(self.parser, args)

        html_file = 'output/html/Roasted Veggie Ciabatta Sandwich  GlutenFree_F52.html'
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(2, self._num_files_in_dir(html_dir))

    def test_download_different_intermediate_file(self):
        url = 'https://food52.com/recipes/9743-roasted-carrot-soup'
        args = self.parser.parse_args(['-u', url, "-i", "tmp_zz/data2.json"])
        run_main(self.parser, args)

        data_file = 'tmp_zz/data2.json'
        html_file = 'output/html/Roasted CarrotSoup_F52.html'
        html_dir = 'output/html'
        self.assertTrue(os.path.isfile(data_file))
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(1, self._num_files_in_dir(html_dir))

        url = 'https://food52.com/recipes/64163-roasted-veggie-ciabatta-sandwich-gluten-free'
        args = self.parser.parse_args(['-u', url, "-i", "tmp_zz/data2.json"])
        run_main(self.parser, args)

        html_file = 'output/html/Roasted Veggie Ciabatta Sandwich  GlutenFree_F52.html'
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(2, self._num_files_in_dir(html_dir))

        self.assertFalse(os.path.isfile("data.json"))

    def test_download_different_output_directory(self):
        url = 'https://food52.com/recipes/9743-roasted-carrot-soup'
        args = self.parser.parse_args(['-u', url, "-o", "output/html2"])
        run_main(self.parser, args)

        data_file = 'data.json'
        html_file = 'output/html2/Roasted CarrotSoup_F52.html'
        html_dir = 'output/html2'
        self.assertTrue(os.path.isfile(data_file))
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(1, self._num_files_in_dir(html_dir))

        url = 'https://food52.com/recipes/64163-roasted-veggie-ciabatta-sandwich-gluten-free'
        args = self.parser.parse_args(['-u', url, "-o", "output/html2"])
        run_main(self.parser, args)

        html_file = 'output/html2/Roasted Veggie Ciabatta Sandwich  GlutenFree_F52.html'
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(2, self._num_files_in_dir(html_dir))

    def test_download_and_regen_json(self):
        # These urls already tested
        url = 'https://food52.com/recipes/9743-roasted-carrot-soup'
        args = self.parser.parse_args(['-u', url])
        run_main(self.parser, args)

        url = 'https://food52.com/recipes/64163-roasted-veggie-ciabatta-sandwich-gluten-free'
        args = self.parser.parse_args(['-u', url])
        run_main(self.parser, args)

        shutil.rmtree("output")

        args = self.parser.parse_args(["--regen-json"])
        run_main(self.parser, args)

        html_file = 'output/html/Roasted Veggie Ciabatta Sandwich  GlutenFree_F52.html'
        html_dir = 'output/html'
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(2, self._num_files_in_dir(html_dir))

        # Test regen json with different output directory
        args = self.parser.parse_args(['--regen-json', "-o", "output/html2"])
        run_main(self.parser, args)

        html_file = 'output/html2/Roasted Veggie Ciabatta Sandwich  GlutenFree_F52.html'
        html_dir = 'output/html2'
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(2, self._num_files_in_dir(html_dir))

        shutil.rmtree(html_dir)

    def test_add_from_file(self):
        filename = "testfiles/recipe.txt"
        html_dir = 'output/html'
        html_file = 'output/html/Big crumb coffee cake_FILE.html'
        data_file = 'data.json'
        args = self.parser.parse_args(["-f", filename])
        run_main(self.parser, args)

        # Get the content from the file created from main...
        inter_file = IntermediateFile()
        inter_file.file_path = data_file
        recipe_obj = inter_file.get_contents()[0]

        self.assertEqual(1, self._num_files_in_dir(html_dir))
        self.assertEqual("https://smittenkitchen.com/2008/02/big-crumb-coffee-cake/",
                         recipe_obj["url"])
        self.assertEqual("Big crumb coffee cake",
                         recipe_obj["title"])
        self.assertEqual(21, len(recipe_obj["ingredients"]))
        self.assertEqual(5, len(recipe_obj["directions"]))
        self.assertTrue(os.path.isfile(html_file))

    def test_clean_recipe_obj(self):
        obj = {
            "title": " Title",
            "ingredients": ["Ingredient 1", "Ingredient 2  ",
                            "  Ingredient  3 "],
            "directions":  ["  Direction ,  chop  ,  eat  ,  1 "],
            "url": "fake",
            "filename": "fake",
            "date_retrieved": "fake",
            "note": "   C is for cookie.. and cookie is for me  "
        }

        clean_recipe_object(obj)

        self.assertEqual(obj["title"], "Title")
        self.assertEqual(obj["ingredients"][0], "Ingredient 1")
        self.assertEqual(obj["ingredients"][1], "Ingredient 2")
        self.assertEqual(obj["ingredients"][2], "Ingredient 3")
        self.assertEqual(obj["directions"][0], "Direction, chop, eat, 1")
        self.assertEqual(obj["note"], "C is for cookie.. and cookie is for me")
