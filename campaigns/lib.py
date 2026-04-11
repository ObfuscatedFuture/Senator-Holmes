import requests
from bs4 import BeautifulSoup


def find_promises_page(homeurl):
    return f"{homeurl}/issues"
    #
    # with urlopen(request) as response:
    #     soup = BeautifulSoup(response, "html.parser")
    #     promise_heading = soup.body.find("h1", string=re.compile("Day One Promises"))


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

        promises_html = soup.body.select("ol")
        main_html = soup.body.select_one("header").find_next_sibling()
        for promise in promises_html:
            promises.append(promise.find("li").get_text())
        for promise in main_html.find_all("p"):
            promises.append(promise.get_text())

        return promises

    def scrape_promises_linked_pages(self, overview):
        """
        Scrapes campaign websites where each campaign promise is on a separate page, all linked from a page listing out titles
        for those promises
        :param overview: URL of the issues/campaign promises overview
        :return:Complete list of strings each representing a campaign promise from the website
        """
        promises = []
        soup = self.construct_soup(overview)

        promises_html = soup.body.select("header + * a")
        for link in promises_html:
            promises.append(self.scrape_promise_single_page(link['href']))

        return promises
