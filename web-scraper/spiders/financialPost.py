import scrapy


class FinancialpostSpider(scrapy.Spider):
    name = "financialPost"
    allowed_domains = ["financialpost.com"]
    start_urls = ["https://financialpost.com/"]

    def parse(self, response):
        pass
