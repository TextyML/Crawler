from ..NewsSpider import NewsSpider
from bs4 import BeautifulSoup


class GuardianSpider(NewsSpider):
    name = "guardian"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = self.get_item(response.url)

        pattern = {
                "title": "//meta[@property='og:title']/@content",
                "abstract": "//meta[@property='og:description']/@content",
                "paragraph": "//div[contains(@class,'content__article-body')]/p"
        }

        item["title"] = response.xpath(pattern["title"]).extract()[0]
        item["abstract"] = response.xpath(pattern["abstract"]).extract()[0]
        text = ""

        for paragraph in response.xpath(pattern["paragraph"]).extract():
            soup = BeautifulSoup(paragraph)
            text += soup.get_text() + "\n"
        item["text"] = text

        yield item
