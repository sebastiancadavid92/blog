

from rest_framework.generics import ListAPIView
from apps.permissions.serializer import categorySerializer
from apps.permissions.models import Category


class ListCategories(ListAPIView):
    serializer_class=categorySerializer
    queryset=Category.objects.all()