from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
import rest_framework
from testmongo.settings import *
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer
# Create your views here.

class UserCreate(APIView): 
    authentication_classes = ()
    permission_classes = () 
    serializer_class = UserSerializer

    def get(self,request):
        print(11111111111)
        test = User.objects.using(testmongo).get(pk=1)
        print(test)
        user = User(
            email='ss@gmail.com',
            username='ss',
        )
        user.save()
        Token.objects.create(user=user)
        return Response({
            'message': ''
            })