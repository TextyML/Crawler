from ..NewsSpider import NewsSpider
from bs4 import BeautifulSoup


class DailyExpressSpider(NewsSpider):
    name = "dailyexpress"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.get_links(self.name)

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = self.get_item(response.url)

        pattern = {
                "title": "//meta[@property='og:title']/@content",
                "abstract": "//meta[@property='og:description']/@content",
                "paragraph": "//div[@data-type='article-body']/*/section[@class='text-description']/p"
        }

        item["title"] = response.xpath(pattern["title"]).extract()[0]
        item["abstract"] = response.xpath(pattern["abstract"]).extract()[0]
        item["text"] = self.clean_text(extracted=response.xpath(pattern["paragraph"]).extract(),
                                       extract_tags=['em'],
                                       illegal_tags=None,
                                       illegal_words=['●'])

        yield item
