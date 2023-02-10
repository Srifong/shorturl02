from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from django.http import HttpResponse
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username =serializers.CharField(max_length=45)
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}
