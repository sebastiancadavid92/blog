from django.urls import path
from apps.permissions.viewscategory import ListCategories


urlpatterns = [path('',ListCategories.as_view(),name='listcategories')]