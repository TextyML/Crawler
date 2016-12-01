from ..NewsSpider import NewsSpider
from newssites.items import NewssitesItem
from bs4 import BeautifulSoup


class CNNSpider(NewsSpider):
    name = "cnn"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = NewssitesItem()
        item["tags"] = self.get_tags(response.url)

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
        text = ""

        for paragraph in response.xpath(pattern["paragraph"]).extract():
            soup = BeautifulSoup(paragraph, 'html.parser').get_text() + "\n"
            if not any(x in soup.lower() for x in ["related:", "read:"]):
                text += soup
        item["text"] = text

        yield item
