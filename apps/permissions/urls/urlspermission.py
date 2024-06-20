from django.urls import path
from apps.permissions.viewspermission import ListPermissions


urlpatterns = [path('',ListPermissions.as_view(),name='listpermission')]