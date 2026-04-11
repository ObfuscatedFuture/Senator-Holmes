import re

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, build_opener, urlretrieve, install_opener

def find_promises_page(homeurl):
    request = Request(homeurl)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15")
    with urlopen(request) as response:
        soup = BeautifulSoup(response, "html.parser")
        promise_heading = soup.body.find("h1", string=re.compile("Day One Promises"))

def scrape_promises_single_page(url):
    request = Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15")

    promises = []

    with urlopen(request) as response:
        soup = BeautifulSoup(response, "html.parser")

        promises_html = soup.body.select("ol")
        main_html = soup.body.select_one("header").find_next_sibling()
        for promise in promises_html:
            promises.append(promise.find("li").get_text())
        for promise in main_html.find_all("p"):
            promises.append(promise.get_text())

    return promises


