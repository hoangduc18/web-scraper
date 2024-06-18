import scrapy


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["e.vnexpress.net"]
    start_urls = ["https://e.vnexpress.net/search/q/FPT"]

    def parse(self, response):
        articles = response.css(".item_news")
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
        pass
