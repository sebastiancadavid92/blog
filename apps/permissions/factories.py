import factory
from .models import *


possible_values_category = ['AUTHOR','TEAM','AUTHENTICATED','PUBLIC']
possible_values_permission = ['READ_ONLY', 'READ_EDIT', 'NONE']
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        # Define una lista de valores posibles
  

    # Utiliza Sequence para asignar valores secuencialmente
    categoryname = factory.Sequence(lambda n: possible_values_category[n % len(possible_values_category)])

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
    permissionname = factory.Sequence(lambda n: possible_values_permission[n % len(possible_values_permission)])

class PermissionCategoryPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PermissionCategoryPost