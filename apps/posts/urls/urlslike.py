
from django.urls import path
from apps.posts.views import ListLikeAPIView


urlpatterns = [path('',ListLikeAPIView.as_view(),name='listlikes')]