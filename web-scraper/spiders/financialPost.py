import scrapy
from scrapy.selector import Selector


class FinancialpostSpider(scrapy.Spider):
    name = "financialPost"
    allowed_domains = ["financialpost.com"]
    start_urls = ["https://financialpost.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.financialpost.com/search/?q=FPT+Sofware",
            meta=dict(
                playwright = True,
                playwright_include_page = True,  
            ),
            errback = self.errback,
            callback= self.parse
        )
    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(1000)
        content = ""
        try:
            content = await page.content()
        except Exception as error:
            print("An exception occured ", error)
        sel = Selector(text=content)
        yield{
            "title" : sel.css(".article-card__headline-clamp::text").get(),
            # "url": sel.css("h6 a::attr(href)").get()
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
