from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from .models import User, Book ,Category
from .serializers import BookSerializer, UserSerializer,CategorySerializer
from django.utils.timezone import now

@api_view(['GET', 'POST'])
def users(request):
  if request.method == 'GET':
    seriliazer = UserSerializer(User.objects.all(), many = True)
    return Response(seriliazer.data)
  elif request.method == "POST":
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
  status=status.HTTP_201_CREATED
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
      return Response(UserSerializer(user).data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def book_list(request):
    if request.method == 'GET':
        serializer = BookSerializer(Book.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'GET':
        return Response(BookSerializer(book).data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class UserViewSet(viewsets.ModelViewSet):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer
  
# class BookViewSet(viewsets.ModelViewSet):
#   queryset = Book.objects.all()
#   serializer_class = BookSerializer
#   @action(detail=True, methods=['post'])
#   def borrow(self, request, pk=None):
#     book = self.get_object()
#     user = request.user
#     if book.is_borrowed:
#       return Response(
#         {"error": "This book is already borrowed."},
#           status=status.HTTP_400_BAD_REQUEST
#         )
#     book.borrow_by = user
#     book.is_borrowed = True
#     book.borrow_date = now()
#     book.save()
#     return Response(
#             {"message": f"Book '{book.book_title}'has been borrowed by {user.name}"},
#             status=status.HTTP_200_OK
#         )
#   @action(detail=True, methods=['post'])
#   def return_book(self, request, pk=None):
#     book = self.get_object()
#     user = request.user
#     if not book.is_borrowed or book.borrow_by != user:
#       return Response (
#         {"error":"This book was not borrowed by you already"},
#                 status=status.HTTP_400_BAD_REQUEST
#       )

#     book.borrow_by = None
#     book.is_borrowed = False
#     book.borrow_date = None
#     book.save()
#     return Response(
#             {"message": f"Book '{book.book_title}'has been returned by {user.name}"},
#             status=status.HTTP_200_OK
#         )
# class CategoryViewSet(viewsets.ModelViewSet):
#   queryset = Category.objects.all()
#   serializer_class = CategorySerializer

