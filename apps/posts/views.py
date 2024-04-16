from apps.posts.serializer import CreationPostModelSerializer,PermissionModelSerializer,CategoryModelSerializer,PermissionCategoryPostModelSerializer
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status,decorators

from .models import Post
from .permissionclass import PostPermissionRead, PostPermissionEdit
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
# Create your views here.

class PostCreateListAPIView(CreateAPIView):

    serializer_class=CreationPostModelSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request):
        author=request.user
        serializerblog=self.serializer_class(data=request.data, context={'author':author})
        if serializerblog.is_valid():
            blog=serializerblog.save()
            data=self.serializer_class(blog)
            if len(serializerblog.errors)==0:
                return Response(data.data,status=status.HTTP_201_CREATED) 
        return Response(serializerblog.errors,status=status.HTTP_400_BAD_REQUEST)



class PostGetDeleteUpdateAPIView(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericAPIView): 
    serializer_class=CreationPostModelSerializer
    queryset=Post.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [PostPermissionRead()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [PostPermissionEdit()]
        return False

     
    def patch(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        return super().update(request, *args, **kwargs)
    
 
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
 
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
	