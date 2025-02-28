from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Book, Category, Author
from .serializers import BookSerializer, UserSerializer, CategorySerializer, AuthorSerializer
from django.utils import timezone
from django.db.models import Q


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
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


@api_view(['GET', 'POST'])
def authors(request):
    if request.method == 'GET':
        serializer = AuthorSerializer(Author.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'GET':
        return Response(AuthorSerializer(author).data)
    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
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


@api_view(['PATCH'])
def update_book_status(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.book_status = request.data.get('book_status')
    book.save()
    return Response({'message': f'Book "{book.book_title}" status updated to {book.book_status}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_book_to_user(request):
    user = get_object_or_404(User, pk=request.data.get('user_id'))
    book = get_object_or_404(Book, pk=request.data.get('book_id'))
    user.books.add(book)
    return Response({'message': f'Book "{book.book_title}" added to {user.name}'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_book_from_user(request):
    user = get_object_or_404(User, pk=request.data.get('user_id'))
    book = get_object_or_404(Book, pk=request.data.get('book_id'))
    user.books.remove(book)
    return Response({'message': f'Book "{book.book_title}" removed from {user.name}'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        return Response(CategorySerializer(category).data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def search_data(request):
    query = request.GET.get('q', None)
    if not query:
        return Response({"error": "Invalid search"}, status=status.HTTP_400_BAD_REQUEST)
    books = Book.objects.filter(Q(book_title__icontains=query) | Q(ISBN__icontains=query))
    users = User.objects.filter(Q(name__icontains=query) | Q(name__icontains=query))
    categories = Category.objects.filter(Q(name__icontains=query))
    authors = Author.objects.filter(Q(author_name__icontains=query))
    books_data = BookSerializer(books, many=True).data
    users_data = UserSerializer(users, many=True).data
    categories_data = CategorySerializer(categories, many=True).data
    authors_data = AuthorSerializer(authors, many=True).data
    if not (books_data or users_data or categories_data or authors_data):
        return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"books": books_data,"users": users_data,"categories": categories_data,"authors": authors_data,}, status=status.HTTP_200_OK)