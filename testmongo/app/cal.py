import random  
import string  
from datetime import datetime
# from .models import Link as  เป็นชื่อ
from .models import Link,log,Story
from django.conf import settings
from django.contrib.auth.models import User
from testmongo.settings import *
class cal:
    def __init__(self):
        pass

    def randome(self):
        while True:
            random_string =''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # random_string=''.join(choices(ascii_letters,k=6))
            new_link=settings.HOST_URL+'/api/url/'+random_string

            # new_link = f"http://127.0.0.1:8000/api/url/{random_string}"
            if not Link.objects.filter(shortened_link=new_link).exists():
                break
        return new_link

    def log_api(self,path,error,device,data,method):
        log_api = {
            'log_error_api_api_path' : path,
            'log_error_api_api_error' : error,
            'log_error_api_client_device': device,
            'log_error_api_client_data' : data,
            'log_error_api_method' : method,
            'log_error_api_datenow' : datetime.now(),
            }
        log.objects.using(testmongo).create(**log_api)
        return 1
    
    def story(self,createby,name,data,id_short_url):
        story = {
            'create_by' : createby,
            'namepath' : name,
            'data' : data,
            'date' : datetime.now(),
            'short_url_by' : Link(id=id_short_url),
        }
        Story.objects.using(testmongo).create(**story)
        return 1

