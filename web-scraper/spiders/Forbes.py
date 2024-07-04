import scrapy
from scrapy.selector import Selector

class ForbesSpider(scrapy.Spider):
    name = "Forbes"
    allowed_domains = ["www.forbes.com"]
    # start_urls = ["https://www.forbes.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.forbes.com/search/?q=FPT",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
            ),
            errback=self.errback,
            callback=self.parse,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(1000)
        content = ""
        try:
            content = await page.content()
        except Exception as error:
            print(error)
        sel = Selector(text=content)
        links = sel.css("div .CardArticle_link__AgXDI::attr(href)").getall()

        for link in links:
            yield response.follow(link, callback = self.parse_another_page)

    async def parse_another_page(self, response):
        # page = response.meta["playwright_page"]
        # page.set_default_timeout(1000)
        # content = ""
        # try:
        #     content = await page.content()
        # except Exception as error:
        #     print(error)
        # sel = Selector(text = content)
        yield {
            "title" : response.css("h1::text").get(),
            "content": response.css(".article-body-container p::text").getall()
        }
        # page.close()
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
