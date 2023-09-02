import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quote"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']
    
    def parse(self, response, **kwargs):        
        for page in range(1,11):
            url = f"https://quotes.toscrape.com/page/{page}/"
            
            yield scrapy.Request(url = url , callback = self.parse_quotes)
            
    def parse_quotes(self, response, **kwargs):
        quotes = response.xpath('.//div[@class="quote"]')
        
        for quote in quotes:
            text = quote.xpath('.//span[@class="text"]/text()').get()
            author = quote.xpath('.//small/text()').get()
            
            yield {
                "text" : text,
                "author" : author
            }