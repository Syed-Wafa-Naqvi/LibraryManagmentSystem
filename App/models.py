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