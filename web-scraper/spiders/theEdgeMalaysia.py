import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin


class TheedgemalaysiaSpider(scrapy.Spider):
    name = "theEdgeMalaysia"
    allowed_domains = ["theedgemalaysia.com"]
    # start_urls = ["https://theedgemalaysia.com/news-search-results?keywords=Wipro"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.theedgemalaysia.com/news-search-results?keywords=Wipro",
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
        title = sel.css("div .NewsList_newsListItemHead__dg7eK::text").get()
        url = sel.css(".NewsList_newsListText__hstO7 a::attr(href)").get()
        baseUrl = "https://theedgemalaysia.com"
        yield scrapy.Request(
            url=baseUrl + url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
            ),
            callback=self.parse_another_page
        )
        # newsList = sel.css(".NewsList_newsListText__hstO7").getall()
        # for news in newsList:
        #     nodeLink = news.css("a ::attr(href)").get()
        #     newsLink = urljoin(baseUrl, nodeLink)
        #     yield sel.follow(newsLink, callback=self.parse_news)

    async def parse_another_page(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(1000) 
        content = ""
        try:
            content = await page.content()
        except Exception as error:
            print(error)
        sel = Selector(text = content)
        yield {
            "title" : sel.css(".news-detail_newsdetailsItemHead__zb6Ed span::text").get()
        }
        page.close()
            

    # def parse_news(self, response):
    #     yield{
    #         "title": response.css(".news-detail_newsdetailsItemHead__zb6Ed span::text").get(),
    #         "author": response.css(".news-detail_newsdetailsItemInfo__g9Hsi .news-detail_newsBy__6_pzA span:nth-child(2) a::text").get(),
    #         "date": response.css(".news-detail_newsdetailsItemInfo__g9Hsi .news-detail_newsInfo__dv0be span::text").get(),
    #         "content": response.css(".newsTextDataWrapInner p::text").getall()
    #     }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
