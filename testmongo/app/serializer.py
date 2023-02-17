from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from .models import Link,count,OfficeUser,Album,test
from django.http import HttpResponse
from rest_framework import serializers
from django.contrib.auth.models import User

class testSerializer(ModelSerializer):
    class Meta:
        model=test
        # fields= ('original_link','name_album',)
        fields='__all__'

class LinkSerializer(ModelSerializer):
    class Meta:
        model=Link
        # fields= ('original_link','name_album',)
        fields='__all__'


class CountSerializer(ModelSerializer):
    class Meta:
        model=count
        fields='__all__'

class AlbumSerializer(ModelSerializer):
    class Meta:
        model=Album
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username =serializers.CharField(max_length=45)
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

