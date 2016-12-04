from ..NewsSpider import NewsSpider
from bs4 import BeautifulSoup


class BBCSpider(NewsSpider):
    name = "bbc"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = self.get_item(response.url)

        pattern = {
            "title": "//meta[@property='og:title']/@content",
            "abstract": "//meta[@property='og:description']/@content",
            "paragraph": "//div[contains(@class, 'story-body')]/*/p | //div[contains(@class, 'story-body')]/p"
        }

        item["title"] = response.xpath(pattern["title"]).extract()[0].replace(' - BBC News', '')
        item["abstract"] = response.xpath(pattern["abstract"]).extract()[0]
        item["text"] = self.clean_text(extracted=response.xpath(pattern["paragraph"]).extract(),
                                       extract_tags=None,
                                       illegal_tags=['i'],
                                       illegal_words=["follow me on Twitter"])

        yield item
