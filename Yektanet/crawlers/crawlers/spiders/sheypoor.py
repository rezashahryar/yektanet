import os
import json

import scrapy

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from yektanet import models

class SheypoorSpider(scrapy.Spider):
    name = "sheypoor"
    allowed_domains = ["www.sheypoor.com"]
    start_urls = ["https://www.sheypoor.com"]
    custom_settings = dict(
    DOWNLOADER_MIDDLEWARES = {
         'crawlers.middlewares.ProxyMiddleware': 350,
         'scrapy_random_fake_ua.middleware.RandomUserAgentMiddleware': 400,
         'crawlers.middlewares.CrawlersDownloaderMiddleware': 543,
         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
         'scrapy.spidermiddlewares.referer.RefererMiddleware': 80,
         'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
         # 'scrapy_proxies.RandomProxy': 100,
         'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
         # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 120,
         # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 130,
         'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
         'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 900,
      },
      DOWNLOAD_DELAY = 5,
      DOWNLOAD_TIMEOUT = 50,
      RANDOMIZE_DOWNLOAD_DELAY = True,
      USER_AGENT = 'Opera/8.83 (Windows NT 5.01; sl-SI) Presto/2.11.280 Version/12.00'

   )


    def parse(self, response):
        for page in range(1, 5):
            url = f"https://www.sheypoor.com/api/v10.0.0/search/iran/car?brandInSlug=43969&c=43627&p={page}&f=1692694651.426077"
            yield scrapy.Request(url=url, callback=self.parse_car)
    
    def parse_car(self, response):
        res = json.loads(response.body)
        cars = res["data"]
        
        for car in cars:
            try:
                car_code = car["id"]
                if len(car_code) == 9:
                    phone_url = f"https://www.sheypoor.com/api/v10.0.0/listings/{car_code}/number"
                    yield scrapy.Request(url=phone_url, callback=self.parse_phone, meta={"car_code":car_code})
            except:
                pass

    async def parse_phone(self, response):
        res = json.loads(response.body)
        
        car_code = response.meta["car_code"]
        
        car, created = await models.Car.objects.aget_or_create(source="sheypoor",code=car_code)
        
        res = {"Message" : "Repeated Record"}
        
        if created :                
            phone = res["data"]["attributes"]["phoneNumber"]
            if phone:
                await models.Phone.objects.acreate(phone=phone,car=car)
                res = {
                    car_code : {
                        "phones": phone
                    }
                }
            
            yield res
