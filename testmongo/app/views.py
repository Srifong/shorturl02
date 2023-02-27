from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView,DestroyAPIView
from django.views import View
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
import rest_framework
import pandas as pd
import qrcode
from PIL import Image
from django.contrib.auth import authenticate
from rest_framework import status
from testmongo.settings import *
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer
from .models import Link,count,OfficeUser,Album,Story
from .serializer import LinkSerializer,UserSerializer,AlbumSerializer
from rest_framework.request import Request
from .cal import cal 
import json
import random  
import string  
from django.conf import settings
from datetime import datetime,date,timedelta

from random import choices
from string import ascii_letters
from django.conf import settings
import json
from collections import Counter

from django.urls import reverse_lazy
from django.conf import settings
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

############## create user #######################
class UserCreate(APIView): 
    authentication_classes = ()
    permission_classes = () 
    serializer_class = UserSerializer
    def post(self,request,*args, **kwargs):
        try:
            email_exists = User.objects.using(testmongo).filter(email=request.data['email']).exists()
            username_exists = User.objects.using(testmongo).filter(username=request.data['username']).exists()
            if email_exists:
                return Response({
                'message': 'email already applied'
                })
            if username_exists:
                return Response({
                'message': 'username already applied'
                })
            else:
                email=request.data['email']
                staff = OfficeUser.objects.using(testmongo).filter(email= email)
                if staff :
                    # เป็นพนักงาน
                    user = User(
                    email=request.data['email'],
                    username=request.data['username'],
                    is_staff = 1
                    )
                    user.set_password(request.data['password'])
                    user.save()
                    # สร้าง Album ให้เองตอนสมัคร
                    user_album = User.objects.using(testmongo).get(email=email)
                    id_album = user_album
                    album = Album(name_album = 'collection 1',create_by = id_album)
                    album.save()
                    Token.objects.using(testmongo).create(user=user)
                    call_cal = cal()
                    log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                    return Response({
                        'message': ''
                    })
                else:
                    user = User(
                    email=request.data['email'],
                    username=request.data['username'],
                    )
                    user.set_password(request.data['password'])
                    user.save()
                    # สร้าง Album ให้เองตอนสมัคร
                    user_album = User.objects.using(testmongo).get(email=email)
                    id_album = user_album
                    album = Album(name_album = 'collection 1',create_by = id_album)
                    album.save()
                    Token.objects.using(testmongo).create(user=user)
                    call_cal = cal()
                    log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                    return Response({
                        'message': '',
                    })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

############## Login User#######################
class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = authenticate(username=username, password=password)
            if user:
                sent_login = User.objects.using(testmongo).get(pk=user.pk)
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                "token": user.auth_token.key, # type: ignore
                "id": user.pk,
                "username": username ,
                "email": sent_login.email,
                "first_name" : sent_login.first_name,
                "lastname": sent_login.last_name,
                "is_staff" : sent_login.is_staff,
                "last_login": sent_login.last_login,
                "date_joined":sent_login.date_joined,
                }) 
            else:
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'Wrong Credentials',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

############ create URL ##################
class ShortenerCreateApiView(APIView):
    serializer_class = LinkSerializer
    def get(self, request, pk, *args, **kwargs):
        try:
            shortenerlinst = Link.objects.using(testmongo).get(pk = pk)
            link = Link.objects.using(testmongo).filter(name_album = 2)
            if (shortenerlinst.check_date == 1) and (datetime.now().strftime("%Y-%m-%d")> shortenerlinst.ex_date.strftime("%Y-%m-%d")):
                ex_date_no_play = 1
            else:
                ex_date_no_play = 0
            sum_count_day = 0
            sum_count_all = count.objects.using(testmongo).filter(Link_by__pk = shortenerlinst.pk)
            name_album = Album.objects.using(testmongo).get(pk=shortenerlinst.name_album)
            for i in sum_count_all:
                if i.DateURL.strftime("%d") == datetime.now().strftime("%d"):
                    sum_count_day = sum_count_day + 1
            data = {
                "id" : shortenerlinst.pk,
                "original_link": shortenerlinst.original_link,
                "shortened_link" : shortenerlinst.shortened_link,
                "date_now" : shortenerlinst.date_now.strftime("%d-%b-%y"),
                "ex_date":shortenerlinst.ex_date.strftime("%d-%b-%y"),
                "name_album" : str(name_album.name_album),
                "name_album_id" : str(shortenerlinst.name_album),
                "code": str(shortenerlinst.code),
                "sum_count_day" : sum_count_day ,
                "sum_count_all": len(sum_count_all),
                "key" : shortenerlinst.key,
                "check_date" : shortenerlinst.check_date,
                "today_dat" : datetime.now().strftime("%Y-%m-%d"),
                "ex_date_no_play" : ex_date_no_play
                
            }
            call_cal = cal()
            log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response(data)
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })


    def post(self, request, *args, **kwargs):
        try:
            # new_link=settings.HOST_URL+'/'+random_string
            user_id = request.user
            # call_cal = Book()
            # new_link = call_cal.randome()
            while True:
                random_string =''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                # random_string=''.join(choices(ascii_letters,k=6))
                new_link=settings.HOST_URL+'/api/url/'+random_string

                # new_link = f"http://127.0.0.1:8000/api/url/{random_string}"
                if not Link.objects.using(testmongo).filter(shortened_link=new_link).exists():
                    break

            if request.data.get('original_link'):
                album = request.data.get('name_album')
                date = datetime.now()
                key = 0
                name_album = None
                try:
                    name_album =Album.objects.using(testmongo).get(pk = album ,status_delete__in = [False])
                except Album.DoesNotExist:
                    album = Album(name_album = 'collection 1',create_by = user_id)
                    album.save()
                    name_album =Album.objects.using(testmongo).get(pk = album ,status_delete__in = [False])
                url = [{'ชื่อ url':request.data.get('original_link'),"ชื่อ album": name_album.name_album}]
                if request.data.get('key'):
                    key = request.data.get('key')
                    new_link = f"{new_link}{key}"
                    key_data = {"key" : key}
                    url.append(key_data)

                if request.data.get('check_date') == 0:
                    check_date = False
                    date_data = {"Ent Date" : 'No'}
                    url.append(date_data)

                print(request.data.get('check_date') == 1)
                if request.data.get('check_date') == 1:
                    check_date = True
                    date = request.data.get('ex_date')
                    print(date)
                    date_data = {"Ent Date" : date}
                    url.append(date_data)

                if request.data.get('name_album'):
                    img = qrcode.make(f'{new_link}qrcode')
                    buf = io.BytesIO()
                    img.save(buf,"PNG")
                    buf.seek(0)
                    uploaded_file = InMemoryUploadedFile(
                        buf, None,  f'{user_id}{random_string}qr.png', "image/png", buf.getbuffer().nbytes, None
                    )
                    try:
                        target_path = '/images/' + f'{user_id}{random_string}qr.png'
                        path = storage.save(target_path,uploaded_file)
                        return storage.url(path)
                    except Exception as e:
                        print('')
                # img.save(f'{user_id}{random_string}qr.png')
                # shutil.move(f"D:/test/ShortURL/ShortURL/{user_id}{random_string}qr.png",f"D:/test/ShortURL/img/{user_id}{random_string}qr.png")
                savecount = Link.objects.using(testmongo).create(
                    original_link= request.data.get('original_link'),
                    shortened_link = new_link, 
                    number_random = random_string,
                    create_by=user_id,
                    ex_date = date,
                    name_album = album,
                    key = key,
                    check_date = check_date,
                    code = f'{user_id}{random_string}qr.png',
                    name_qr = f'{new_link}qrcode'

                )
                savecount.save()
                data1 = {
                    'message': 'Created Successfully',
                    'original_link' : request.data.get('original_link'),
                    'short_URL': new_link,
                    'ex_date' : date,
                    'key' : key,
                    'check_date' : check_date,
                    'code' : f'{user_id}{random_string}qr.png'
                }
                call_cal = cal()
                id_shorturl = Link.objects.using(testmongo).get(shortened_link=new_link)
                story = call_cal.story(request.user,'สร้าง url',url,id_shorturl.pk)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(data1)
        except Exception as error:
            print("error", error)
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class Redirector(View):
    def get(self,request,shortener_link,*args, **kwargs):
        try:
            try:
                qr = Link.objects.using(testmongo).get(name_qr = f"https://pythonshorturl.herokuapp.com/api/url/{shortener_link}")
                print( f"https://pythonshorturl.herokuapp.com/api/url/{shortener_link}",111111111111111111111111111111111111111)
                if qr.check_date == 0 and qr.status_delete == 0:
                    call_cal = cal()
                    log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],'', request.method)
                    CountShortUrl = count(CountShort= qr.shortened_link,Link_by=Link(id=qr.pk),Countqr= True)
                    CountShortUrl.save()
                    return redirect(qr.original_link)
                elif qr.check_date == 1 and qr.status_delete == 0:
                    if datetime.now().strftime("%Y-%m-%d")< qr.ex_date.strftime("%Y-%m-%d") :
                        call_cal = cal()
                        log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],'', request.method)
                        CountShortUrl = count(CountShort= qr.shortened_link,Link_by=Link(id=qr.pk),Countqr= True)
                        CountShortUrl.save()
                        return redirect(qr.original_link)
                    else:
                        call_cal = cal()
                        log_api = call_cal.log_api(request.path,'หมดเวลาแล้ว',request.META['HTTP_USER_AGENT'],'', request.method)
                        return Response({
                        'message': 'หมดเวลาแล้ว'})
            except Link.DoesNotExist:
                a = f"https://pythonshorturl.herokuapp.com/api/url/{shortener_link}"
                redirect_link = Link.objects.using(testmongo).get(shortened_link=a)
                if redirect_link.check_date == 1 and redirect_link.status_delete == 0 :
                    if datetime.now().strftime("%Y-%m-%d")< redirect_link.ex_date.strftime("%Y-%m-%d") :
                        call_cal = cal()
                        log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],'', request.method)
                        CountShortUrl = count(CountShort= a,Link_by=Link(id=redirect_link.pk))
                        CountShortUrl.save()
                        return redirect(redirect_link.original_link)
                    else:
                        call_cal = cal()
                        log_api = call_cal.log_api(request.path,'หมดเวลาแล้ว',request.META['HTTP_USER_AGENT'],'', request.method)
                        return Response({
                            'message': 'หมดเวลาแล้ว'
                        }, status=status.HTTP_400_BAD_REQUEST)
                elif redirect_link.check_date == 0 and redirect_link.status_delete == 0 :
                    call_cal = cal()
                    log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],'', request.method)
                    CountShortUrl = count(CountShort= a,Link_by=Link(id=redirect_link.pk))
                    CountShortUrl.save()
                    return redirect(redirect_link.original_link)
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],'', request.method)
            return Response({
                'message': ''
            },)

class ShortenerListAPIView(ListAPIView):
    def get(self, request,  *args, **kwargs):
        try:
            result = []
            sum_all = 0
            shortenerlinst = Link.objects.using(testmongo).filter(create_by_id__username= request.user,status_delete__in = [False])
            if len(shortenerlinst) != 0:
                for i in shortenerlinst:
                    resultcount = count.objects.using(testmongo).filter(Link_by_id__in = [i.pk])
                    sum_all  = sum_all + len(resultcount)
                    if (i.check_date == 1) and (datetime.now().strftime("%Y-%m-%d")> i.ex_date.strftime("%Y-%m-%d")):
                        ex_date_no_play = 1
                    else:
                        ex_date_no_play = 0
                    data = {
                        "id" : i.pk,
                        "original_link": i.original_link,
                        "shortened_link" : i.shortened_link,
                        "number_of_clicks" : len(resultcount),
                        "date_now" : i.date_now.strftime("%d-%b-%y"),
                        "ex_date":i.ex_date.strftime("%d-%b-%y"),
                        "name_album" : str(i.name_album),
                        "check_date" : i.check_date,
                        "ex_date_no_play" : ex_date_no_play
                    }
                    result.append(data)
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(result)
            else:
                print("no url")
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                'message': ''
            })
        except Exception as error:
            print("error",error)
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class SumurlListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            result= []
            sum_all = 0
            datenow = datetime.now()
            datenow = datenow.strftime("%d")
            sumday = 0
            shortenerlinst = Link.objects.using(testmongo).filter(create_by_id__username = request.user,status_delete__in = [False])
            for i in shortenerlinst:
                resultcount = count.objects.using(testmongo).filter(Link_by__pk = i.pk)
                for i in resultcount:
                    if datenow ==i.DateURL.strftime("%d"):
                        sumday = sumday+1
                sum_all  = sum_all + len(resultcount)
            data1 = {
                "title" : 'Clicks Today',
                "sum" : sumday,
                "icon" : 'mdi-cursor-default-click-outline'
            }
            result.append(data1)
            data2 = {
                "title" : 'All Clicks',
                "sum" : sum_all,
                "icon" : 'mdi-cursor-default-click'
            }
            result.append(data2)
            data3 = {
                "title" : 'All URL',
                "sum" : len(shortenerlinst),
                "icon" : 'mdi-link-variant'
            }
            result.append(data3)
            call_cal = cal()
            log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response(result)
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class ShortenerUpdateApiView(APIView):
    serializer_class = LinkSerializer
    def put(self, request,pk = None,*args, **kwargs ):
        try:
            if pk != None:
                UpdateLink = Link.objects.using(testmongo).get(pk=pk)
                update = []
                call_cal = cal()

                UpdateLink.original_link = request.data.get('original_link') 
                key = request.data.get('key')
                number_random = UpdateLink.number_random
                new = f'{settings.HOST_URL}/api/url/{number_random}'
                new_short_link = f"{new}{key}"
                UpdateLink.shortened_link = new_short_link 
                UpdateLink.key = key
                # UpdateLink.name_qr = f'{request.user}{number_random}{key}qr'
                # img = qrcode.make(new_short_link)
                # buf = io.BytesIO()
                # img.save(buf,"PNG")
                # buf.seek(0)
                # uploaded_file = InMemoryUploadedFile(
                #     buf, None,  f'{UpdateLink.code}', "image/png", buf.getbuffer().nbytes, None
                # )
                # try:
                #     target_path = '/images/' + f'{UpdateLink.code}'
                #     path = storage.save(target_path,uploaded_file)
                #     return storage.url(path)
                # except Exception as e:
                #     print('')
                if request.data.get('check_date') == 0:
                    UpdateLink.check_date = False
                print( request.data.get('check_date'),33333333333333)
                if request.data.get('check_date') == 1:
                    print(11111111111111122222222222)
                    UpdateLink.check_date = True
                    UpdateLink.ex_date= request.data.get('ex_date')

                name=request.data.get('name_album')
                UpdateLink.name_album = name
                UpdateLink.save()
                
                data = {
                    "ชื่อ url" : request.data.get('original_link'),
                    "key" : request.data.get('key'),
                    "ชื่อ Album" : UpdateLink.name_album
                    }
                update.append(data)


                call_cal = cal()
                story = call_cal.story(request.user,'update url',update,pk)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                'message': 'update url successfully'
                })
            else:
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                'message': ''
                })
        except Exception as error:
            print(error,"error")
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class ShortenerDeleteApiView(DestroyAPIView):
    def delete(self, request, pk = None, format=None ,*args, **kwargs):
        try:
            if pk != None:
                DeleteLink =  Link.objects.using(testmongo).get(pk=pk)
                DeleteLink.status_delete = True
                DeleteLink.save()
                # location = f"D:/test/ShortURL/img/"
                # path = os.path.join(location, file)
                # os.remove(path)
                # DeleteLink.delete()
                # try:
                #     target_path = '/images/' + f'{DeleteLink.code}'
                #     path = storage.delete(target_path)
                #     return storage.url(path)
                # except Exception as e:
                #     print("")
                # delete_count = count.objects.filter(CountShort=DeleteLink.shortened_link)
                # for i in delete_count:
                #     Deletecount =  count.objects.get(pk=i.pk)
                #     Deletecount.delete()
                call_cal = cal()
                story = call_cal.story(request.user,'delete url',DeleteLink.original_link,DeleteLink.shortened_link)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                'message': 'Deleted Successfully'
                })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class AlbumListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            result = []
            name_Album = Album.objects.using(testmongo).filter(create_by_id__username = request.user,status_delete__in = [False])
            if len(name_Album):
                for i in name_Album:
                    data = {
                        "id" : i.pk,
                        "name_Album": i.name_album,
                        "create_by" : i.create_by.username
                    }
                    result.append(data)
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(result)     
            else:
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                    'message': ''
                })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

    def post(self,request, *args, **kwargs):
        try:
            data = request.data
            if data:
                sefrializer = AlbumSerializer(data=data)
                sefrializer.is_valid(raise_exception=True)
                sefrializer.save()
                response = Response()
                response.data = {
                    'message': 'Created Album Successfully',
                    'data': sefrializer.data
                }
                update = {
                    "name" : request.data.get('name_album')
                }
                call_cal = cal()
                # story = call_cal.story(request.user,'create Album',update)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return response
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

    def put(self,request,pk=None, *args, **kwargs):
        try:
            if pk:
                UpdateAlbum = Album.objects.using(testmongo).get(pk=pk)
                serializer = AlbumSerializer(instance=UpdateAlbum,data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response = Response()
                response.data = {
                    'message': 'Updated Album Successfully',
                    'data': serializer.data
                }
                call_cal = cal()
                # story = call_cal.story(request.user,'update Album',UpdateAlbum.name_album)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return response
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

    def delete(self, request, pk = None, format=None):
        try:
            if pk:
                DeleteAlbum =  Album.objects.using(testmongo).get(pk=pk)
                DeleteAlbum.status_delete = True
                DeleteAlbum.save()
                DeleteAlbunLink = Link.objects.using(testmongo).filter(name_album = DeleteAlbum.pk)
                for i in DeleteAlbunLink:
                    delete_link = Link.objects.using(testmongo).get(pk=i.pk)
                    delete_link.status_delete = True 
                    delete_link.save()
                    # delete_count = count.objects.filter(CountShort=i.shortened_link)
                    # for i in delete_count:
                    #     deletecount = count.objects.get(pk=i.pk)
                    #     deletecount.delete()
                    # delete.delete()
                # DeleteAlbum.delete()
                
                call_cal = cal()
                # story = call_cal.story(request.user,'delete Album',DeleteAlbum.name_album)
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                    'message': 'Deleted Successfully'
                })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })

class AlbumSearch(APIView):
    def get(self, request,pk, *args, **kwargs):
        try:
            result = []
            link = Link.objects.using(testmongo).filter(create_by_id__username = request.user,status_delete__in = [False],name_album__in = [pk])
            if link:
                for i in link:
                    if (i.check_date == 1) and (datetime.now().strftime("%Y-%m-%d")> i.ex_date.strftime("%Y-%m-%d")):
                        ex_date_no_play = 1
                    else:
                        ex_date_no_play = 0
                    resultcount = count.objects.using(testmongo).filter(CountShort = i.shortened_link)
                    data = {
                        "id" : i.pk,
                        "original_link": i.original_link,
                        "shortened_link" : i.shortened_link,
                        "number_of_clicks" : len(resultcount),
                        "date_now" : i.date_now.strftime("%d-%b-%y"),
                        "ex_date":i.ex_date.strftime("%d-%b-%y"),
                        "name_album" : str(i.name_album),
                        "ex_date_no_play" : ex_date_no_play
                    }
                    result.append(data)
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(result)
            else:
                return Response({
                'message': ''
                })  
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })   

######### filter count with day to dashboard #########
class CountShortenerListAPIView(ListAPIView):
    def get(self,request, datestart,dateend,*args, **kwargs):
        try:
            link_count = Link.objects.using(testmongo).filter(create_by_id__username = request.user,status_delete__in = [False])
            all_date_pd = pd.date_range(start = datestart,end=dateend, freq='D') 
            if link_count:
                day_save = []
                a_count_all = []
                a_count_qr = []
                a_count_link = []
                a_save_sum_qr = [0]*(len(all_date_pd))
                a_save_sum_link = [0]*(len(all_date_pd))
                if link_count:
                    for i in link_count:
                        count_all = count.objects.using(testmongo).filter( DateURL__range=[datestart,dateend],Link_by_id__in = [i.pk])
                        if count_all:
                            for j in count_all:
                                if j.Countqr == False:
                                    a_count_link.append(j.DateURL.strftime("%d/%m/%Y"))
                                elif j.Countqr == True:
                                    a_count_qr.append(j.DateURL.strftime("%d/%m/%Y"))
                a_count_link = Counter(a_count_link) #  นับรวม
                # print(a_count_link['16/02/2023'])
                a_count_link = a_count_link.items() # แยกส่วน
                a_count_qr = Counter(a_count_qr) #  นับรวม
                # print(a_count_link['16/02/2023'])
                a_count_qr = a_count_qr.items() # แยกส่วน
                for k in range(len(all_date_pd)):
                    a_count_all.append(all_date_pd[k].strftime("%d/%m/%Y"))
                    for z in a_count_link:
                        if all_date_pd[k].strftime("%d/%m/%Y") == z[0]:
                            a_save_sum_link[k] = z[1]
                    for a in a_count_qr:
                        if all_date_pd[k].strftime("%d/%m/%Y") == a[0]:
                            a_save_sum_qr [k] = a[1]
                    
                data ={
                    "day" : a_count_all,
                    # "count_day": len(a_count_all),
                    "count_link":a_save_sum_link,
                    "count_qr":a_save_sum_qr
                }
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(data)       
            # date_link = []
            # date_qr = []
            # for i in link_count:
            #     for i in all_date_pd:
            #         get_count = coount_of_link = count.objects.filter(Link_by__pk = link_count[i].pk,DateURL__range=[datestart,dateend],Countqr = 0 )
            # if link_count:
            #     i = 0
            #     for i in range(len(link_count)):
            #         a_l = count.objects.using(testmongo).filter(Link_by_id__pk = link_count[i].pk,DateURL__range__in=([datestart,dateend]) )
            #         check_error = len(a_l)
            #         for j in range(len(a_l)):
            #             day_save.append(a_l[j].DateURL.strftime("%d/%m/%Y"))
            #         day_save.sort()
            #     a =Counter(day_save) #ทำให้นับเป็นกลุ่ม
            #     n = a.items() # เป็นการแยก
            #     day = []
            #     count_day = []
            #     for j in n:
            #         day.append(j[0])
            #         count_day.append(j[1])
            #     data ={
            #         "day" : day,
            #         "count_day": count_day
            #     }
            else:
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                'message': 'ไม่มีการ click'
            })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })   

class StoryAPIView(ListAPIView):
    def get(self,request,pk, *args, **kwargs):
        try:
            result = []

            story = Story.objects.using(testmongo).filter(short_url_by_id=pk)
            for i in story:
                # if i.date.strftime("%d/%m/%Y") == datetime.now().strftime("%d/%m/%Y"):
                date = i.date.strftime("%d/%m/%Y") 
                data = {
                    'name' : i.namepath,
                    'data' : i.data,
                    'date' : date,
                }
                result.append(data)
            return Response(result)
        except Exception as error:
            return Response({
                'message': ''
            })

class AlbumListURLAPIView(APIView):
       def get(self, request, *args, **kwargs):
        try:
            result = []
            de = {
                "id" : '',
                "name_Album": 'All Collection',
            }
            result.append(de)
            name_Album = Album.objects.using(testmongo).filter(create_by_id__username = request.user,status_delete__in = [False])
            if len(name_Album):
                for i in name_Album:
                    data = {
                        "id" : i.pk,
                        "name_Album": i.name_album,
                    }
                    result.append(data)
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response(result)     
            else:
                call_cal = cal()
                log_api = call_cal.log_api(request.path,'',request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
                return Response({
                    'message': ''
                })
        except Exception as error:
            call_cal = cal()
            log_api = call_cal.log_api(request.path,error,request.META['HTTP_USER_AGENT'],json.dumps(request.data), request.method)
            return Response({
                'message': ''
            })           
