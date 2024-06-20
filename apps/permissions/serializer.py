from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.permissions.models import Category,Permission

class categorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','categoryname']

class permissionSerializer(ModelSerializer):
    class Meta:
        model=Permission
        fields=['id','permissionname']