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

    def find_tag(self, soup, tag):
        if soup.find(tag):
            return True
        return

    def extract_tag(self, soup, tag):
        pass

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
