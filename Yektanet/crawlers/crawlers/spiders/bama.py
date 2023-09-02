import os
import json
import scrapy
from scrapy.utils.log import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from yektanet import models


class BamaSpider(scrapy.Spider):
    name = 'bama'
    allowed_domains = ['bama.ir']
    start_urls = ['https://bama.ir/cad/api/search?pageIndex=1']

    def parse(self, response, **kwargs):        
        for page in range(1,8):
            url = f"https://bama.ir/cad/api/search?pageIndex={page}"
            yield scrapy.Request(url=url , callback=self.parse_code)

    def parse_code(self, response,**kwargs):
        cars = json.loads(response.text)
        print("-" * 90)
        print(cars)
        for car in cars['data']['ads']:
            try:
                if car['detail'] != None:
                    car_code = car['detail']['code']
                    dealer_phone_url = f"https://bama.ir/cad/api/detail/{car_code}/phone"
                    yield scrapy.Request(url=dealer_phone_url, callback=self.parse_phone, meta={"code": car_code})
            except Exception as e:
                logger.critical(e)
        
    async def parse_phone(self, response, **kwargs):
        phones = json.loads(response.text)
        car_code = response.meta["code"]
        
        car, created = await models.Car.objects.aget_or_create(source="bama",code=car_code)
        
        res = {"Message" : "Repeated Record"}
        
        if created :
            phone = phones["data"]["mobile"]
            mobile = phones["data"]["mobile"]
            
            final_phone = []
            
            if phone:
                for num in phone:
                    final_phone.append(num)
            
            if mobile:
                for num in mobile:
                    final_phone.append(num)
            
            final_phone = list(set(final_phone))
            
            res = { 
                car_code : {
                    "phones" : final_phone,
                }
            }
            
            if final_phone :
                for phone in final_phone:
                    phone = await models.Phone.objects.acreate(phone=phone,car=car)
            
        yield res