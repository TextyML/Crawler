from ..NewsSpider import NewsSpider
from newssites.items import NewssitesItem
from bs4 import BeautifulSoup


class BBCSpider(NewsSpider):
    name = "bbc"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = NewssitesItem()
        item["tags"] = self.get_tags(response.url)

        pattern = {
                "title": "//meta[@property='og:title']/@content",
                "abstract": "//meta[@property='og:description']/@content",
                "paragraph": "//div[contains(@class, 'story-body')]/*/p | //div[contains(@class, 'story-body')]/p"
        }

        item["title"] = response.xpath(pattern["title"]).extract()[0]
        item["abstract"] = response.xpath(pattern["abstract"]).extract()[0]
        text = ""

        for paragraph in response.xpath(pattern["paragraph"]).extract():
            soup = BeautifulSoup(paragraph)
            [s.extract() for s in soup('i')]
            text += soup.get_text() + "\n"
        item["text"] = text

        yield item
