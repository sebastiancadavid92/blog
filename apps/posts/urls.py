from rest_framework.routers import DefaultRouter

from apps.posts.views import PostCreateAPIView

from django.urls import path

urlpatterns = [
    path('',PostCreateAPIView.as_view(),name='postcreation'),
]

