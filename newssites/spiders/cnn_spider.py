from ..NewsSpider import NewsSpider
from newssites.items import NewssitesItem
from bs4 import BeautifulSoup


class CNNNewsSpider(NewsSpider):
    name = "cnn"
    #allowed_domains = ["edition.cnn.com", "money.cnn.com/"]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = NewssitesItem()
        item["tags"] = self.get_tags(response.url)
        if "edition.cnn.com" in response.url:
            item["title"] = response.xpath('.//h1[@class="pg-headline"]/text()').extract()[0]
            item["abstract"] = response.xpath('.//p[@class="zn-body__paragraph"]/text()').extract()[0]
            text = ""

            for paragraph in response.xpath('.//div[@class="zn-body__paragraph"]').extract():
                soup = BeautifulSoup(paragraph, 'html.parser').get_text() + "\n"
                if not any(x in soup.lower() for x in ["related:", "read:"]):
                    text += soup
            item["text"] = text
        yield item
