from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [ 'title', 'image', 'notes','user']



class Notesserializer(serializers.ModelSerializer):
    updated_on = serializers.DateTimeField(format="%d-%m-%y")
    created_on = serializers.DateTimeField(format="%d-%m-%y")

    class Meta:
        fields = ['id', 'title','notes','image','updated_on','created_on']
        model = Note




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}






