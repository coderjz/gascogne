import Sites
from urllib.parse import urlparse
# Selects the appropriate class for the recipe and returns that object


class SiteSelector:
    def __init__(self):
        self.sites = [Sites.Food52()]

    def _does_domain_match(self, url, domain):
        url_domain = urlparse(url).netloc
        return url_domain == domain or url_domain.endswith("." + domain)

    def get_site(self, url):
        matches = [site for site in self.sites
                   if self._does_domain_match(url, site.get_domain())]
        if len(matches) == 1:
            return matches[0]
        else:
            raise Exception("Found " + len(matches) + " matches." +
                            "Expected 1 match.  For URL " + url)
