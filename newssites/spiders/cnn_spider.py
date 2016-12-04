from ..NewsSpider import NewsSpider
from bs4 import BeautifulSoup


class CNNSpider(NewsSpider):
    name = "cnn"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = self.get_item(response.url)

        extractor = {
            "title": "//meta[@property=\"og:title\"]/@content",
            "abstract": "//meta[@property=\"og:description\"]/@content",
            "edition": {
                "paragraph": ".//div[@class=\"zn-body__paragraph\"]"
            },
            "money": {
                "paragraph": ".//div[@id=\"storytext\"]/p"
            }
        }

        if "edition.cnn.com" in response.url:
            pattern = extractor["edition"]
        else:
            pattern = extractor["money"]

        item["title"] = response.xpath(extractor["title"]).extract()[0]
        item["abstract"] = response.xpath(extractor["abstract"]).extract()[0]
        item["text"] = self.clean_text(extracted=response.xpath(pattern["paragraph"]).extract(),
                                       extract_tags=None,
                                       illegal_tags=['em'],
                                       illegal_words=["related:", "read:"])

        yield item
