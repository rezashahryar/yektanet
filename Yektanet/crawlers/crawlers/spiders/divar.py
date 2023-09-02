import os
import json
import random
import scrapy

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from yektanet import models


class DivarSpider(scrapy.Spider):
    name = "divar"
    start_urls = [
        'https://api.divar.ir/v8/web-search/iran/vehicles?page=1'
    ]
    allowed_domains = ['divar.ir', 'api.divar.ir']
    # headers = {
    #     'Accept': 'application/json',
    #     "Authorization" : "Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDk5MTAzOTEzNzkiLCJpc3MiOiJhdXRoIiwidmVyaWZpZWRfdGltZSI6MTY5MzAzMDEyMiwiaWF0IjoxNjkzMDMwMTIyLCJleHAiOjE2OTQzMjYxMjIsInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6IjM2NDdiZDZlLWI1ZTEtNDhhMC1hZGQ3LTYyZjE2ZmMwMmYzNyJ9.e3VRhXmfqOo_y7_FQlKYfwwIlDwhvrcNmoeLVhOatTQ"
    # }
    custom_settings = dict(
      DOWNLOAD_DELAY = (30 + 30) / 2 * 60,
      RANDOMIZE_DOWNLOAD_DELAY = True
    )
    global got_nums
    
    def __init__(self, *args, **kwargs):
        self.got_nums = 0
        self.car_nums = 0
        self.saturation = random.randint(35,60)
        
    def start_requests(self):
        for page in range(1,3):
            if self.got_nums <= self.saturation:
                url = f'https://api.divar.ir/v8/web-search/iran/vehicles?page={page}'
                
                yield scrapy.Request(url, callback=self.parse)

        print(f"CAR NUMBERS : {self.car_nums}")
        print(f"GOT NUMBERS : {self.got_nums}")
        
    async def parse(self, response):
        json_response = json.loads(response.body.decode("UTF-8"))
        cars = json_response["web_widgets"]["post_list"]

        auth_code = await models.AuthCode.objects.afirst()
        self.headers = {
            'Accept': 'application/json',
            "Authorization" : f"Basic {auth_code.code}"
        }
        
        for car in cars :
            car_token = car["data"]["action"]["payload"]["token"]
            
            if self.got_nums <= self.saturation :
                self.got_nums = int(self.got_nums) + 1
                contact_url = f"https://api.divar.ir/v8/postcontact/web/contact_info/{car_token}"
                yield scrapy.Request(contact_url, callback=self.parse_contact, headers=self.headers,meta={"code": car_token})
        
        print(f"GOT NUMBERS : {self.got_nums}")
        
    async def parse_contact(self, response):
        json_response = json.loads(response.body.decode("UTF-8"))
        try :
            contact = json_response["widget_list"][0]["data"]["value"]
            car_code = response.meta["code"]
           
            car, created = await models.Car.objects.aget_or_create(source="divar",code=car_code)
         
            res = {"Message" : "Repeated Record"}
            
            if created :
                self.car_nums = int(self.car_nums) + 1
                
                if contact:
                    await models.Phone.objects.acreate(phone=contact,car=car)
                res = {
                    car_code : {
                        "phones": contact
                    }
                }
            
            yield res
            
        except :
            print("LOGIN FIRST")
            yield {"phone":f"INVALID , {self.car_nums} , {self.got_nums}"}
