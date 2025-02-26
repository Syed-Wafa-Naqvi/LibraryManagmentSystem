from rest_framework import serializers
from .models import Book, Category, User, Borrow, Reservation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = User
        fields = ['userid', 'user_password', 'name', 'address', 'phonenumber', 'books']
        
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'