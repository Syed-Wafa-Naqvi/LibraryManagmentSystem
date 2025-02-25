from rest_framework import serializers
from .models import Book, Category, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        def get_borrower_details(self, obj):
            if obj.is_borrowed and obj.borrow_by:
                return {
                    "userid": obj.borrow_by.userid,
                    "name": obj.borrow_by.name,
                    "address": obj.borrow_by.address,
                    "phonenumber": obj.borrow_by.phonenumber,
                    "borrow_date": obj.borrow_date.strftime( ) 
                    if obj.borrow_date 
                    else None
                }
            return None
        
class UserSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = User
        fields = ['userid', 'user_password', 'name', 'address', 'phonenumber', 'books']
  