from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import  UserModelSerializer
from .models import User

@api_view(['GET'])
def check_email(request,email):

    user=User.objects.filter(email=email).first()
    if user:
        return Response({'emailtook':True},status=status.HTTP_200_OK)
    else:
        return Response({'emailtook':False},status=status.HTTP_200_OK)

@api_view(['GET'])
def check_username(request,username):

    user=User.objects.filter(username=username).first()
    if user:
        return Response({'usernametook':True},status=status.HTTP_200_OK)
    else:
        return Response({'usernametook':False},status=status.HTTP_200_OK)
    