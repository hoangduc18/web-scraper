import scrapy


class InsuranceedgeSpider(scrapy.Spider):
    name = "InsuranceEdge"
    allowed_domains = ["insurance-edge.net"]
    start_urls = ["https://insurance-edge.net/?s=samsung"]

    def parse(self, response):
        links = response.css("h3 a::attr(href)").getall()
        for link in links:
            yield response.follow(link, self.parse_article) 

    def parse_article(self, response):
        contentsTag = response.css(".entry-content")
        contents = []
        for content in contentsTag:
            if content.css("div p::text").get() != None:
                contents.append(content.css("div p::text").get())
            if content.css("div p em::text").get() != None:
                contents.append(content.css("div p em::text").get())
            if content.css("div p strong::text").get() != None:
                contents.append(content.css("div p strong::text").get())
            # if content.css("i::text").get() != None:
            #     contents.append(content.css("i::text").get())
            # if content.css("strong::text").get() != None:
            #     contents.append(content.css("strong::text").get())
        yield{
            "title": response.css("h1::text").get(),
            "author": response.css(".entry-meta-author a::text").get(),
            "content": contents
        }
