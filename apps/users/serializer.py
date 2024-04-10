from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.users.models import User
from .models import User
import re
from datetime import date
from django.db import IntegrityError

class UserModelSerializer(ModelSerializer):
    passwordconfirmation = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','birthdate','is_admin','passwordconfirmation','password']

    def namesvalidation(self,name):
       p = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚüÜ\s]+$'
       if not re.match(p,name):
            return False
       return True

    def validate_first_name(self,value):
        if not self.namesvalidation(value):
            raise serializers.ValidationError(['Name have special caracters, thats not allowed'])
        return value
    
    def validate_last_name(self,value):
        if not self.namesvalidation(value):
            raise serializers.ValidationError({'last_name':['Name have special caracters, thats not allowed']})
        return value
    
    def validate_birthday(self,value):
        if value> date.today:
            raise serializers.ValidationError(['the birthday you provided is not allowed'])
    

    def validate(self,data):
        super().validate(data)
        password=data.get('password')
        passwordconfirmation= data.get('passwordconfirmation',None)
        if password is None:
            raise serializers.ValidationError('a password has to be provided')
        if password!=passwordconfirmation:
            raise serializers.ValidationError({'password':['password and passwordconfirmation dont match']})
        return data   

## update 
##create


    def create(self,validated_data):
        validated_data.pop('passwordconfirmation')
        user=User.objects.create(**validated_data)
        return user
       

        
    

  


