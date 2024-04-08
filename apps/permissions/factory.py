import factory
from .models import *

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

class PermissionCategoryPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission_Category_Post