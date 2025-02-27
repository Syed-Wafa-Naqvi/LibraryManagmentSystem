from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from .models import User, Book ,Category,Reservation,Author,Borrow,Search
from .serializers import BookSerializer, UserSerializer,CategorySerializer, BorrowSerializer,ReservationSerializer
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

@api_view(['POST'])
def book_borrow(request,pk):
    userid = request.data.get('userid')
    isbn = request.data.get('ISBN')
    if not userid or not isbn:
        return Response({'error': 'User ID and ISBN are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, userid=userid)
    book = get_object_or_404(Book, ISBN=isbn)
    if book.is_borrowed:
        return Response({'error': 'This book is already borrowed'}, status=status.HTTP_400_BAD_REQUEST)
    borrow_entry = Borrow.objects.create(user=user, book=book, borrow_date=timezone.now())
    book.is_borrowed = True
    book.save()
    return Response({'message': f'Book "{book.book_title}" borrowed by {user.userid}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def book_return(request,pk):
    userid = request.data.get('userid')
    isbn = request.data.get('ISBN')
    if not userid or not isbn:
        return Response({'error': 'User ID and ISBN are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, userid=userid)
    book = get_object_or_404(Book, ISBN=isbn)
    if not book.is_borrowed:
        return Response({'error': 'This book is not currently borrowed'}, status=status.HTTP_400_BAD_REQUEST)
    borrow_entry = Borrow.objects.filter(user=user, book=book, return_date__isnull=True).first()
    if not borrow_entry:
        return Response({'error': 'This book was not borrowed by you'}, status=status.HTTP_400_BAD_REQUEST)
    borrow_entry.return_date = timezone.now()
    borrow_entry.save()
    book.is_borrowed = False
    book.save()
    return Response({'message': f'Book "{book.book_title}" returned successfully'}, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def book_reservation(request):
    userid = request.data.get('userid')
    isbn = request.data.get('ISBN')
    if not userid or not isbn:
        return Response({'error': 'User ID and ISBN are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, userid=userid)
    book = get_object_or_404(Book, ISBN=isbn)
    if not book.is_borrowed:
        return Response({'error': 'This book is  currently borrowed borrowed and cannot be reserve'}, status=status.HTTP_400_BAD_REQUEST)
    existing_reservation = Reservation.objects.filter(user=user, book=book, status="Pending")
    if existing_reservation:
        return Response({'error': 'The book is already reserved'}, status=status.HTTP_400_BAD_REQUEST)
    reservation = Reservation.objects.create(user=user, book=book,reservation_date= timezone.now(),status= "Pending"    )    
    return Response({'message':f'Book "{book.book_title}" has been reserved succesfully'}, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def reservation_list(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)
@api_view(['GET', 'PUT', 'DELETE'])
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
def search_data(request):
    query = request.GET.get('q', None)
    if not query:
        return Response({"error": "Invalid search"}, status=status.HTTP_400_BAD_REQUEST)
    books = Book.objects.filter(Q(book_title__icontains=query) | Q(ISBN__icontains=query))
    users = User.objects.filter(Q(userid__icontains=query) | Q(name__icontains=query))
    categories = Category.objects.filter(Q(name__icontains=query))
    authors = Author.objects.filter(Q(author_name__icontains=query))
    books_data = BookSerializer(books, many=True).data
    users_data = UserSerializer(users, many=True).data
    categories_data = CategorySerializer(categories, many=True).data
    authors_data = [{"id": author.id, "author_name": author.author_name} for author in authors]
    if not (books_data or users_data or categories_data or authors_data):
        return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"books": books_data,"users": users_data,"categories": categories_data,"authors": authors_data,}, status=status.HTTP_200_OK)