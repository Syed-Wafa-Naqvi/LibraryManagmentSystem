from App.models import Category
from App.serializers import CategorySerializer


from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer