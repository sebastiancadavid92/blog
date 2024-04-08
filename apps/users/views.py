

# Create your views here.
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def login_view(request):
        username = request.data.get('username')
        password = request.data.get('password')
        import pdb; pdb.set_trace()
        if not username or not password:
             return Response({'error':'you must provide both, a valid username and a valid password'},status=status.HTTP_404_NOT_FOUND)
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return Response({'hola':'hola mundo'},status=status.HTTP_200_OK)
        else:
            # Return an 'invalid login' error message.
            return Response({'error':'invalid credentials'},status=status.HTTP_404_NOT_FOUND)


def logout_view(request):
    logout(request)
    # Redirect to a login page, home page, or any other page
    return Response({'hola':'hola mundo'})