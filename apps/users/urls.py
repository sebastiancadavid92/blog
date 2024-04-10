from rest_framework.routers import DefaultRouter

from apps.users.views import LoginView,LogoutView,RegisterView


from django.urls import path

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('logout/',LogoutView,name='logout'),
    path('register/',RegisterView, name='register')]
