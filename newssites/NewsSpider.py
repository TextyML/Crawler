from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider
from newssites.items import NewssitesItem
import json


class NewsSpider(CrawlSpider):
    downloadList = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def get_item(self, url):
        item = NewssitesItem()
        item["tags"] = self.get_tags(url)
        item["url"] = self.get_url(url)
        return item

    def get_tags(self, url):
        for downloadLink in self.downloadList:
            if downloadLink[0] == url:
                return downloadLink[1]

    def find_tags(self, soup, tags):
        if soup.find(tags):
            return True
        return False

    def find_words(self, soup, words):
        if any(x in soup.get_text().lower() for x in words):
            return True
        return False

    def extract_tags(self, soup, tags):
        for tag in tags:
            [s.extract() for s in soup(tag)]
        return soup

    def clean_text(self, extracted, extract_tags, illegal_tags, illegal_words):
        text = ""
        for paragraph in extracted:
            soup = BeautifulSoup(paragraph, 'html.parser')
            garbage = False

            if extract_tags is not None:
                soup = self.extract_tags(soup, extract_tags)
            if illegal_tags is not None:
                garbage |= self.find_tags(soup, illegal_tags)
            if illegal_words is not None:
                garbage |= self.find_words(soup, illegal_words)

            if not garbage:
                text += soup.get_text() + "\n"

        return text

    def get_url(self, url):
        for downloadLink in self.downloadList:
            if downloadLink[0] == url:
                return downloadLink[0]

    def get_links(self, siteName):
        with open("download.txt") as dl:
            downloadlist = json.load(dl)

        linklist = [site["links"] for site in downloadlist if site["name"] == siteName][0]
        self.downloadList = [[link["url"], link["tags"]] for link in linklist]
        self.start_urls = [row[0] for row in self.downloadList]
