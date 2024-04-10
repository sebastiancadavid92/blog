

# Create your views here.
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from .serializer import  UserModelSerializer
from django.contrib.sessions.models import Session
from rest_framework.permissions import AllowAny
@api_view(['POST'])
def LoginView(request):
        
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
@permission_classes([IsAuthenticated])
def LogoutView(request):
    logout(request)
    return Response({'message':'Successfull logout'},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterView(request):
    if request.user.is_authenticated:
         return Response({'error':'authenticated users cant register users'},status=status.HTTP_403_FORBIDDEN)
    serializer=UserModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

     
     