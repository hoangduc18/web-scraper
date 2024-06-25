import scrapy
from urllib.parse import urljoin

class TheedgemalaysiaSpider(scrapy.Spider):
    name = "theEdgeMalaysia"
    allowed_domains = ["theedgemalaysia.com"]
    start_urls = ["https://theedgemalaysia.com/news-search-results?keywords=Wipro"]

    def start_requests(self):
        yield scrapy.Request(
            url = "https://theedgemalaysia.com/news-search-results?keywords=Wipro",
            meta = {
                "playwright": True
            }
        )

    def parse(self, response):
        baseUrl = "theedgeMalaysia.com"
        newsList = response.css(".NewsList_newsListText__hstO7").getall()
        for news in newsList:
            nodeLink = news.css("a ::attr(href)").get()
            newsLink = urljoin(baseUrl, nodeLink)
            yield response.follow(newsLink, callback=self.parse_news)



    def parse_news(self, response):
        yield{
            "title": response.css(".news-detail_newsdetailsItemHead__zb6Ed span::text").get(),
            "author": response.css(".news-detail_newsdetailsItemInfo__g9Hsi .news-detail_newsBy__6_pzA span:nth-child(2) a::text").get(),
            "date": response.css(".news-detail_newsdetailsItemInfo__g9Hsi .news-detail_newsInfo__dv0be span::text").get(),
            "content": response.css(".newsTextDataWrapInner p::text").getall()
        }

