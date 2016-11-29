from scrapy.contrib.spiders import CrawlSpider
from newssites.items import NewssitesItem
from bs4 import BeautifulSoup


class CNNNewsSpider(CrawlSpider):
    name = "cnnnews"
    allowed_domains = ["edition.cnn.com"]
    start_urls = [
        "http://edition.cnn.com/2016/11/28/politics/wisconsin-recount/index.html"
    ]

    def parse(self, response):
        self.log("Scraping: " + response.url)

        item = NewssitesItem()
        item["title"] = response.xpath('.//h1[@class="pg-headline"]/text()').extract()[0]
        item["abstract"] = response.xpath('.//p[@class="zn-body__paragraph"]/text()').extract()[0]
        text = ""

        for paragraph in response.xpath('.//div[@class="zn-body__paragraph"]').extract():
            text += BeautifulSoup(paragraph, 'html.parser').get_text() + "\n"
        item["text"] = text
        yield item
