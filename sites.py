# This file contains a class for each different site we can pull recipes from.
# The class/site to use is selected based on the get_domain function.


class Food52:
    def get_domain(self):
        return "food52.com"

    def get_short_name(self):
        return "F52"

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


class FoodNetwork:
    def get_domain(self):
        return "foodnetwork.com"

    def get_short_name(self):
        return "FNET"

    def get_title(self, soup):
        return soup.select_one(".o-AssetTitle__a-Headline").get_text()

    def get_ingredients(self, soup):
        return [elem.get_text().strip()
                for elem in soup.select(".o-Ingredients__a-ListItemText")]

    def get_directions(self, soup):
        invalid_direction = "Watch how to make this recipe."
        return [elem.get_text().strip()
                for elem in soup.select(".o-Method__m-Body p")
                if elem.get_text().strip() != invalid_direction]


class BBCGoodFood:
    def get_domain(self):
        return "bbcgoodfood.com"

    def get_short_name(self):
        return "BBCGOOD"

    def get_title(self, soup):
        return soup.select_one(".recipe-header__title").get_text().strip()

    def get_ingredients(self, soup):
        ing = [" ".join((a.string or "").strip() for a in e.contents).strip()
               for e in soup.find_all("li", {"class": "ingredients-list__item"})
               ]

        # TODO: Make this replace, strip() call, other character substitutio
        # be part of a dedicated "cleaning" method used by the parent of this.
        return [i.replace(" ,", ",") for i in ing]

    def get_directions(self, soup):
        return [elem.get_text().strip()
                for elem in soup.select(".method__item p")]
