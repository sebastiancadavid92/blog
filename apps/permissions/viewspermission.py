
from rest_framework.generics import ListAPIView
from apps.permissions.serializer import permissionSerializer
from apps.permissions.models import Permission

class ListPermissions(ListAPIView):
    serializer_class=permissionSerializer
    queryset=Permission.objects.all()