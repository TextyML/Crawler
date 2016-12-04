from ..NewsSpider import NewsSpider
from bs4 import BeautifulSoup


class HuffingtonSpider(NewsSpider):
    name = "huffington"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = self.get_item(response.url)

        pattern = {
                "title": "//h1[@class='headline__title']/text()",
                "abstract": "//meta[@property='og:description']/@content",
                "paragraph": "//div[contains(@class,'entry__body')]/div[contains(@class,'text')]/p"
        }

        item["title"] = response.xpath(pattern["title"]).extract()[0]
        item["abstract"] = response.xpath(pattern["abstract"]).extract()[0]
        item["text"] = self.clean_text(extracted=response.xpath(pattern["paragraph"]).extract(),
                                       extract_tags=None,
                                       illegal_tags=['em'],
                                       illegal_words=None)

        yield item
