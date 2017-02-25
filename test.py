from unittest import TestCase
from main import create_parser, run_main
import os
import shutil


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
    def tearDown(self):
        if(os.path.isfile("data.json")):
            os.remove("data.json")
        if(os.path.isdir("output")):
            shutil.rmtree("output")
        if(os.path.isfile("data.json.bak")):
            os.rename("data.json.bak", "data.json")
        if(os.path.isdir("outputbak")):
            os.rename("outputbak", "output")

    def _num_files_in_dir(self, dir):
        return len([name for name in os.listdir(dir) if
                    os.path.isfile(os.path.join(dir, name))])

    def _get_file_length(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return len(file.read())

    def test_download_default_URL(self):
        url = 'https://food52.com/recipes/9743-roasted-carrot-soup'
        args = self.parser.parse_args(['-u', url])
        run_main(args)

        data_file = 'data.json'
        html_file = 'output/html/Roasted CarrotSoup_F52.html'
        html_dir = 'output/html'
        self.assertTrue(os.path.isfile(data_file))
        self.assertTrue(os.path.isfile(html_file))
        self.assertEqual(1, self._num_files_in_dir(html_dir))
        self.assertEqual(1602, self._get_file_length(data_file))
        self.assertEqual(4740, self._get_file_length(html_file))
