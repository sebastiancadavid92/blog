

# Create your views here.
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sessions.models import Session

@api_view(['POST'])

def login_view(request):
        
        if Session.objects.filter(session_key=request.session.session_key).first():
             return Response({'error':'user already logged in'},status=status.HTTP_400_BAD_REQUEST)
    
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
             return Response({'error':'you must provide both, a valid username and a valid password'},status=status.HTTP_404_NOT_FOUND)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message':'Sucessful login'},status=status.HTTP_200_OK)
        else:
            return Response({'error':'invalid credentials'},status=status.HTTP_404_NOT_FOUND)
        



@api_view(['GET'])
def logout_view(request):
    if not request.session.session_key:
         return Response({'error':'user is already logged out'},status=status.HTTP_400_BAD_REQUEST)
    logout(request)
    return Response({'message':'Successfull logout'},status=status.HTTP_200_OK)