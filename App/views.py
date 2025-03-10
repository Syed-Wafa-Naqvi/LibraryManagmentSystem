from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Book, Category, Author, Billing
from .serializers import BookSerializer, UserSerializer, CategorySerializer, AuthorSerializer
from django.db.models import Q
from datetime import datetime,date
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_book(request):
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')
    if not user_id or not book_id:
        return Response({'error': 'user_id and book_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    book = get_object_or_404(Book, pk=book_id)
    if book.book_status in ['Borrow', 'Reserve']:
        return Response({'error': 'Book is already reserved or borrowed'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, pk=user_id)
    book = get_object_or_404(Book, pk=book_id)
    book.book_status = "Reserve"
    book.save()
    return Response({'message': f'Book "{book.book_title}" has been reserved by {user.name}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request):
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')
    return_date = request.data.get('return_date')
    user = get_object_or_404(User, pk=user_id)
    book = get_object_or_404(Book, pk=book_id)
    if not user_id or not book_id:
        return Response({'error': 'user_id and book_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    if book.book_status in ['Borrow', 'Reserve']:
        return Response({'error': 'Book is already reserved or borrowed'}, status=status.HTTP_400_BAD)
    borrow_date = datetime.now().date()
    return_date = date.fromisoformat(return_date)
    total_cost = (return_date - borrow_date).days * book.price_perDay
    Billing.objects.create(borrowed_by=user, book=book, borrow_date=borrow_date, return_date=return_date, total_cost=total_cost)
    book.book_status = "Borrow"
    book.save()
    return Response({'message': f'Book "{book.book_title}" has been borrowed by {user.name} and price will be ${total_cost}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request):
    user_id = request.data.get('user_id')
    book_id = request.data.get('book_id')
    user = get_object_or_404(User, pk=user_id)
    book = get_object_or_404(Book, pk=book_id)
    if not user_id or not book_id:
        return Response({'error': 'user_id and book_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    billing = Billing.objects.filter(book=book, borrowed_by=user).first()
    if not billing:
        return Response({'error': 'Billing record not found'}, status=status.HTTP_404_NOT_FOUND)
    current_date = datetime.now().date()
    fine = 0 
    if billing.return_date < current_date:
        overdue_days = (current_date - billing.return_date).days
        fine = overdue_days * 0.5 
    billing.delete()
    book.book_status = "Available"
    book.save()
    if fine > 0:
        return Response({'message': f'Book "{book.book_title}" returned by {user.name}. You have to pay a fine of ${fine}.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': f'Book "{book.book_title}" returned by {user.name}.'}, status=status.HTTP_200_OK)    
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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