from apps.posts.serializer import CreationPostModelSerializer,PermissionModelSerializer,CategoryModelSerializer,PermissionCategoryPostModelSerializer
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,decorators
from django.db import transaction
from .models import Post
from .permissionclass import PostPermissionRead, PostPermissionEdit
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
# Create your views here.
class PostCreateAPIView(CreateAPIView):
    serializer_class=CreationPostModelSerializer
    permission_classes=[IsAuthenticated]
    def post(self,request):
        with transaction.atomic():
            author=request.user
            
            serializerblog=self.serializer_class(data=request.data)
            if serializerblog.is_valid():
                blog,permission=serializerblog.save(author=author)
                
                categories=[{'categoryname':i} for i in permission]
                permissions=[{'permissionname':permission[i]} for i in permission]
                serializerpermission=PermissionModelSerializer(data=permissions, many=True)
                serializercategory=CategoryModelSerializer(data=categories, many=True)
            
                if not serializercategory.is_valid():
                    transaction.set_rollback(True)
                    return Response(serializercategory.errors,status=status.HTTP_400_BAD_REQUEST)
                if not serializerpermission.is_valid():
                    transaction.set_rollback(True)
                    return Response(serializerpermission.errors,status=status.HTTP_400_BAD_REQUEST)

                categories=serializercategory.save()
                permissions=serializerpermission.save()
                data = [{'post':blog.id, 'category':categories[i][0].id,'permission':permissions[i][0].id} for i in range(0,len(categories))]
                sesrializercategorypostpermission=PermissionCategoryPostModelSerializer(data=data, many=True)
             
                if not sesrializercategorypostpermission.is_valid():
                     transaction.set_rollback(True)
                     return Response(serializerpermission.errors,status=status.HTTP_400_BAD_REQUEST)
                sesrializercategorypostpermission.save()
                data2=self.serializer_class(blog)
                return Response(data2.data,status=status.HTTP_201_CREATED)
            return Response(serializerblog.errors,status=status.HTTP_400_BAD_REQUEST)

class PostGetDeleteAPIView(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericAPIView):
    serializer_class:CreationPostModelSerializer
    queryset=Post.objects.all()
    
    @decorators.permission_classes([PostPermissionEdit])
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)
    
    @decorators.permission_classes([PostPermissionRead])
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @decorators.permission_classes([PostPermissionEdit])
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
	