from rest_framework.routers import DefaultRouter

from apps.users.views import LoginView,LogoutView,RegisterView
from apps.users.api_views import check_email,check_username


from django.urls import path

urlpatterns = [
path('login/',LoginView,name='login'),
path('logout/',LogoutView,name='logout'),
path('register/',RegisterView, name='register'),
path('api/checkemail/<str:email>/',check_email, name='checkemail'),
path('api/checkusername/<str:username>/',check_username, name='checkusername')]


