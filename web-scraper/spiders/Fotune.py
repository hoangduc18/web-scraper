import scrapy
from scrapy.selector import Selector


class FotuneSpider(scrapy.Spider):
    name = "Fotune"
    allowed_domains = ["fortune.com"]
    # start_urls = ["https://www.fortune.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://fortune.com/advanced-search/?query=FPT+Corp",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
            ),
            errback=self.errback,
            callback=self.parse,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(3000)
        content = ""
        try:
            content = await page.content()
        except Exception as error:
            print(error)
        sel = Selector(text=content)
        links = sel.css("a::attr(href)").getall()

        yield{
            "link": links
        }
        # links = response.css(".queryly_item_row a:nth-child(1)::text").getall()
        # for link in links:
        #     yield response.follow(link, callback = self.parse_another_page)

    # async def parse_another_page(self, response):
    #     yield {
    #         "title" : response.css("h1::text").get(),
    #         "content": response.css(".article-content p::text").getall()
    #     }
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        
# import scrapy
#
# class FotuneSpider(scrapy.Spider):
#     name = "Fotune"
#     allowed_domains = ["fortune.com"]
#     start_urls = ["https://fortune.com/"]
#
#     def parse(self, response):
#         links = response.css(".queryly_item_row a::text").get()
#         for link in links:
#             yield response.follow(link, callback=self.parse_another_page)
#
#     def parse_another_page(self, response):
#         yield {
#             "title": response.css("h1::text").get(),
#             "content": response.css(".article-content p::text").getall()
#         }



