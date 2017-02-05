# This file contains a class for each different site we can pull recipes from.
# The class/site to use is selected based on the get_domain function.


class Food52:
    def get_domain(self):
            return "food52.com"

    def get_title(self, soup):
        return soup.select_one("h1.article-header-title").get_text()

    def get_ingredients(self, soup):
        quantity = ".recipe-list-quantity"
        name = ".recipe-list-item-name"
        return [(elem.select_one(quantity).get_text().strip() + " " +
                elem.select_one(name).get_text().strip()).strip()
                for elem in soup.select("li[itemprop=ingredients]")]

    def get_directions(self, soup):
        return [elem.get_text().strip()
                for elem in soup.select("li[itemprop=recipeInstructions]")]
