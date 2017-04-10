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
        return [(elem.select_one(quantity).get_text() + " " +
                elem.select_one(name).get_text())
                for elem in soup.select("li[itemprop=ingredients]")]

    def get_directions(self, soup):
        return [elem.get_text()
                for elem in soup.select("li[itemprop=recipeInstructions]")]


class FoodNetwork:
    def get_domain(self):
        return "foodnetwork.com"

    def get_short_name(self):
        return "FNET"

    def get_title(self, soup):
        return soup.select_one(".o-AssetTitle__a-Headline").get_text()

    def get_ingredients(self, soup):
        return [elem.get_text()
                for elem in soup.select(".o-Ingredients__a-ListItemText")]

    def get_directions(self, soup):
        invalid_direction = "Watch how to make this recipe."
        return [elem.get_text()
                for elem in soup.select(".o-Method__m-Body p")
                if elem.get_text().strip() != invalid_direction]


class BBCGoodFood:
    def get_domain(self):
        return "bbcgoodfood.com"

    def get_short_name(self):
        return "BBCGOOD"

    def get_title(self, soup):
        return soup.select_one(".recipe-header__title").get_text()

    def get_ingredients(self, soup):
        return [" ".join((a.string or "") for a in e.contents)
                for e in soup.find_all("li",
                                       {"class": "ingredients-list__item"})]

    def get_directions(self, soup):
        return [elem.get_text().strip()
                for elem in soup.select(".method__item p")]


class SmittenKitchen:
    def get_domain(self):
        return "smittenkitchen.com"

    def get_short_name(self):
        return "SK"

    def get_title(self, soup):
        return soup.select_one(".jetpack-recipe-title").get_text()

    def get_ingredients(self, soup):
        return [i.get_text() for i in soup.select(".jetpack-recipe-ingredient")]

    def get_directions(self, soup):
        #First direction is properly under a class element
        dir1 = soup.select_one(".jetpack-recipe-directions").get_text()

        #All other directions are direct children of the root, not under <html>
        dir2 = [elem.get_text() for elem in
                soup.findChildren("p", recursive=False)
                if elem.get_text().strip() != ""]

        dir2.insert(0, dir1)
        return dir2
