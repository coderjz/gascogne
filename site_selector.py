# Selects the appropriate class for the recipe and returns that object
import sites
from urllib.parse import urlparse


class SiteSelector:
    def __init__(self):
        self.sites = [sites.Food52(), sites.FoodNetwork(), sites.BBCGoodFood(),
                      sites.SmittenKitchen()]

    def _does_domain_match(self, url, domain):
        url_domain = urlparse(url).netloc
        return url_domain == domain or url_domain.endswith("." + domain)

    def get_site(self, url):
        matches = [site for site in self.sites
                   if self._does_domain_match(url, site.get_domain())]
        if len(matches) == 1:
            return matches[0]
        else:
            raise Exception("Found " + str(len(matches)) +
                            " sites that support the URL.  Can only download" +
                            " the recipe if exactly 1 site supports the URL." +
                            " URL: " + url)
