import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class CampaignScraper:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'})

    def construct_soup(self, url):
        return BeautifulSoup(self.session.get(url).content, "html.parser")

    def scrape_promise_single_page(self, url):
        """
        Scrapes a page with a single promise
        :param url:
        :return:
        """
        soup = self.construct_soup(url)
        return "\n".join(map(lambda x: x.get_text(), soup.body.select("header + * p")))


    def scrape_promises_single_page(self, url):
        soup = self.construct_soup(url)
        promises = []

        list_html = soup.body.select("header + * ol,header + * ul")
        if len(list_html) > 0:      # If the structure was li, don't add extraneous promises
            for promise in list_html:
                for x in promise.find_all("li"):
                    promises.append(x.get_text())
            return promises

        p_html = soup.body.select("header + * p")
        for promise in p_html:
            promises.append(promise.get_text())

        return promises

    def scrape_promises_linked_pages(self, overview):
        """
        Scrapes campaign websites where each campaign promise is on a separate page, all linked from a page listing out titles
        for those promises

        :param overview: URL of the issues/campaign promises overview
        :return: Complete list of strings each representing a campaign promise from the website.
        Empty list if this is an invalid way to get promises (the website does not display the information this way)
        """
        promises = []
        soup = self.construct_soup(overview)

        promises_html = soup.body.select("header + * a")
        overview_hostname = urlparse(overview).hostname
        if len(promises_html) < 5:
            return []
        for link in promises_html:
            if urlparse(link['href']).hostname != overview_hostname:
                continue
            subpage_link = self.scrape_promise_single_page(link['href'])
            promises.append(subpage_link)

        return promises

    def try_and_print_promises(self, url):
        senator = self.scrape_promises_linked_pages(url)
        if len(senator) == 0:
             senator = self.scrape_promises_single_page(url)
        for x in senator: print(x)
        print("\n")