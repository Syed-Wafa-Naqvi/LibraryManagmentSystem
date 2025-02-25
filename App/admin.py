from django.contrib import admin
from App.models import User, Book, Category
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Category)


"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Book, Category
from .serializers import BookSerializer, UserSerializer, CategorySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user = request.user  # Assuming the user is authenticated

        if book.is_borrowed:
            return Response({"message": "Book is already borrowed."}, status=status.HTTP_400_BAD_REQUEST)
        
        book.borrow_by = user
        book.is_borrowed = True
        book.save()
        
        return Response({"message": "Book borrowed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        user = request.user  # Assuming the user is authenticated

        if not book.is_borrowed or book.borrow_by != user:
            return Response({"message": "Book is not borrowed by you."}, status=status.HTTP_400_BAD_REQUEST)
        
        book.borrow_by = None
        book.is_borrowed = False
        book.save()
        
        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
"""