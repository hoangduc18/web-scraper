import scrapy
# from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["e.vnexpress.net"]
    # start_urls = ["https://e.vnexpress.net/search/q/FPT"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://e.vnexpress.net/search/q/FPT",
            meta=dict(
                playwright = True,
                playwright_include_page = True,  
            ),
            errback = self.errback,
            callback= self.parse
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        # load_button = page.locator("#vnexpress_folder_load_more")
        # while load_button != None:
        #     load_button.click()
        #     page.wait_for_selector("#vnexpress_folder_load_more")
        #     load_button = page.locator("#vnexpress_folder_load_more")
        page.set_default_timeout(1000)
        try:
            while button := page.locator("#vnexpress_folder_load_more"):
                await button.click()
        except:
            pass
            print("failedddddddddd")

        content = await page.content()
        sel = Selector(text=content)


        articles = sel.css(".item_news")
        for article in articles:
            relative_url = article.css("h4 a::attr(href)").get()
            yield response.follow(relative_url, callback=self.parse_article_page)

    def parse_article_page(self, response):
        yield {
            "Title": response.css(
                ".main_fck_detail .block_title_detail h1::text"
            ).get(),
            "Author": response.css(".main_fck_detail .author a::text").get(),
            "Content": response.css(".main_fck_detail .fck_detail p::text").getall(),
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
