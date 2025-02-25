from rest_framework import serializers
from .models import Book, Category, User, BookTransaction

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
                    "borrow_date": obj.borrow_date.strftime( ) 
                }
            return None
        
class UserSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = User
        fields = ['userid', 'user_password', 'name', 'address', 'phonenumber', 'books']
        
class BookActionSeriliazer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[('BORROW', 'Borrow a book'), ('RETURN', 'Return a book')])
  