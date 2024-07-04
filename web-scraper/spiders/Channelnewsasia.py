import scrapy
from scrapy.selector import Selector


class ChannelnewsasiaSpider(scrapy.Spider):
    name = "Channelnewsasia"
    allowed_domains = ["www.channelnewsasia.com"]
    start_urls = ["https://www.channelnewsasia.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.channelnewsasia.com/search?q=FPT+sofware",
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
            "title" : sel.css("h6 a::text").get(),
            "url": sel.css("h6 a::attr(href)").get()
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
