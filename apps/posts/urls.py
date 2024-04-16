from rest_framework.routers import DefaultRouter

from apps.posts.views import PostCreateAPIView, PostGetDeleteUpdateAPIView

from django.urls import path

urlpatterns = [
    path('',PostCreateAPIView.as_view(),name='postcreation'),
    path('<pk>/',PostGetDeleteUpdateAPIView.as_view(),name='getdeletepost')
]

