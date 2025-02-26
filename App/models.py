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
    book_catogory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    borrow_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    total_copies = models.IntegerField(null=True, blank=True)
    avaliable_copies_in_inventory = models.IntegerField(default=1)
    def copies(self, *args, **kwargs):
        try:
            if self.availaavaliable_copies_in_inventoryble_copies > self.total_copies:
                self.avaliable_copies_in_inventory = self.total_copies
            super().copies(args,*kwargs)
        except  Exception  as e:
            print("Error... You did some mistake")
    is_borrowed = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.book_title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default="Pending")
    def __str__(self):
        return f"{self.user.username} Reserved {self.book.book_title}"