from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.users.models import User
from .models import User,Team
import re
from datetime import date
from django.db import IntegrityError



class UserModelSerializer(ModelSerializer):
    passwordconfirmation = serializers.CharField(write_only=True,required=True)
    team=serializers.CharField(write_only=True,required=False,default='DEFAULT')
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','birthdate','is_admin','passwordconfirmation','password','team']
        
    def to_representation(self, instance):
        data= super().to_representation(instance)
        data.pop('password')
        data['team']=instance.team.team_name
        data['team was created']=self.validated_data['was_created']
        return data
   
    
    def namesvalidation(self,name):
       if not name:
           return True
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
    
    def validate_birthdate(self,value):
        if value is None:
            return None
        if value> date.today():
            raise serializers.ValidationError(['the birthday you provided is not allowed'])
        return value

    def validate(self,data):
        super().validate(data)
        password=data.get('password')
        passwordconfirmation= data.get('passwordconfirmation',None)
        if password is None:
            raise serializers.ValidationError('a password has to be provided')
        if password!=passwordconfirmation:
            raise serializers.ValidationError({'password':['password and passwordconfirmation dont match']})
        return data   



    def create(self,validated_data):
        validated_data.pop('passwordconfirmation')
        team,was_created=Team.objects.get_or_create(team_name=validated_data.pop('team'))
        user=User.objects.create(**validated_data,team=team)
        self.validated_data['was_created']=was_created
        user.save()
        return user
       

        
    

  


