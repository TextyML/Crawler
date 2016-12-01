from scrapy.spiders import CrawlSpider
import json


class NewsSpider(CrawlSpider):
    downloadList = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def get_tags(self, url):
        for downloadLink in self.downloadList:
            if downloadLink[0] == url:
                return downloadLink[1]

    def get_links(self, siteName):
        with open("download.json") as dl:
            downloadlist = json.load(dl)

        linklist = [site["links"] for site in downloadlist if site["name"] == siteName][0]
        self.downloadList = [[link["url"], link["tags"]] for link in linklist[:7]]
        self.start_urls = [row[0] for row in self.downloadList]
