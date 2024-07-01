import scrapy


class GlobalbankingandfinanceSpider(scrapy.Spider):
    name = "globalBankingAndFinance"
    allowed_domains = ["www.globalbankingandfinance.com"]
    start_urls = ["https://www.globalbankingandfinance.com/?s=FPT+software"]

    def parse(self, response):
        articles = response.css("ul .mvp-blog-story-col a ::attr(href)").getall()
        availableLink = response.css(".pagination a::text").getall()
        currentPage = response.css(".pagination .current::text").get()
        for articleLink in articles:
            yield response.follow(articleLink, self.parse_article)

        if currentPage < availableLink[len(availableLink) - 1]:
            nextPageNumber = availableLink[len(availableLink) - 1]
            yield response.follow(
                "https://www.globalbankingandfinance.com/page/"
                + nextPageNumber
                + "/?s=FPT+software",
                self.parse,
            )

    def parse_article(self, response):
        contentsTag = response.css("#mvp-content-main p")
        contents = []
        for content in contentsTag:
            if content.css("span::text").get() != None:
                contents.append(content.css("span::text").get())
            if content.css("p::text").get() != None:
                contents.append(content.css("p::text").get())
            if content.css("em::text").get() != None:
                contents.append(content.css("em::text").get())
            if content.css("i::text").get() != None:
                contents.append(content.css("i::text").get())
            if content.css("strong::text").get() != None:
                contents.append(content.css("strong::text").get())

        yield {
            "url": response.request.url,
            "title": response.css(".mvp-post-title::text").get(),
            "author": response.css(".mvp-author-box-name a::text").get(),
            "content": contents,
        }
