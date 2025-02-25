from django.db import models
from django.utils.timezone import now

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=50, unique=True)
    user_password = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=220)
    phonenumber = models.CharField(max_length=15)
    def __str__(self):
        return self.userid
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Author(models.Model):
    author_name = models.CharField(max_length=255)
    def __str__(self):
        return self.author_name

class Book(models.Model):
    ISBN = models.CharField(max_length=13, unique=True)
    book_title = models.CharField(max_length=255)
    How_many_days = models.CharField(max_length=10)
    book_catogory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    borrow_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    is_borrowed = models.BooleanField(default=False)
    
    borrow_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.book_title

class BookTransaction(models.Model):
    ACTION_CHOICES = [
        ('BORROW', 'Borrow a book'),
        ('RETURN', 'Return a book'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (f"{self.user.userid}-{self.get_action_display()}-{self.book.book_title}")