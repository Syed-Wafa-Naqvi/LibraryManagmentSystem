from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User, Book ,Category
from .serializers import BookSerializer, UserSerializer,CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
class BookViewSet(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  @action(detail=True, methods=['post'])
  def borrow(self, request, pk=None):
    book = self.get_object()
    user = request.user
    


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer

