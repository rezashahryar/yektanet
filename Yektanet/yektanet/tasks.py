from __future__ import absolute_import, unicode_literals

import json
from requests import post
from celery import shared_task

URL = "http://localhost:6801/schedule.json"

@shared_task
def add(x,y):
    return x + y

@shared_task
def call_spider():
    try:
       response = post(URL, data={
           'project': 'crawlers',
           'spider': 'quote',
       })
    except:
       return
    json_data = json.loads(response.content)

    print(json_data)
    
@shared_task
def call_bama_spider():
    try:
       response = post(URL, data={
           'project': 'default',
           'spider': 'bama',
       })
    except:
       return
    json_data = json.loads(response.content)
    print(json_data)
    
@shared_task
def call_divar_spider():
    try:
       response = post(URL, data={
           'project': 'default',
           'spider': 'divar',
       })
    except:
       return
    json_data = json.loads(response.content)
    print(json_data)
    
@shared_task
def call_sheypoor_spider():
    try:
       response = post(URL, data={
           'project': 'default',
           'spider': 'sheypoor',
       })
    except:
       return
    json_data = json.loads(response.content)
    print(json_data)