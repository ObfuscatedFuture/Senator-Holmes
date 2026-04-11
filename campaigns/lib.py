import re

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlcleanup
from requests import get

def find_promises_page(homeurl):
    request = Request(homeurl)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15")
    return f"{homeurl}/issues"
    #
    # with urlopen(request) as response:
    #     soup = BeautifulSoup(response, "html.parser")
    #     promise_heading = soup.body.find("h1", string=re.compile("Day One Promises"))

def scrape_promise_single_page(url):
    """
    Scrapes a page with a single promise
    :param url:
    :return:
    """
    soup = construct_request(url)
    return map(lambda x: x.get_text(), soup.body.select("header + * p"))


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

def scrape_promises_linked_pages(overview):
    """
    Scrapes campaign websites where each campaign promise is on a separate page, all linked from a page listing out titles
    for those promises
    :param overview: URL of the issues/campaign promises overview
    :return:Complete list of strings each representing a campaign promise from the website
    """
    promises = []
    soup = construct_request(overview)

    promises_html = soup.body.select("header ~ * a")
    for link in promises_html:
        promises.append(scrape_promise_single_page(link['href']))

    return promises


def construct_request(url):
    request = Request(url)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15")
    response = urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    return soup