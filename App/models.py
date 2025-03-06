from django.db import models
# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(TimeStampModel):
    author_name = models.CharField(max_length=255)

    def __str__(self):
        return self.author_name


class Book(TimeStampModel):
    isbn = models.CharField(max_length=13, default="")
    book_title = models.CharField(max_length=255)
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publish_date = models.DateField()
    book_status = models.CharField(max_length=20, default="Available" , choices=[('Available', 'Available'),('Borrow', 'Borrow'),('Reserve', 'Reserve'),('Return', 'Return')])
    users = models.ManyToManyField('User', related_name="reserved_books", blank=True)
    price_perDay = models.FloatField()
    description = models.TextField()
    borrow_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="borrowed_by", blank=True)

    def __str__(self):
        return self.book_title

class Billing(TimeStampModel):
    borrowed_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name="billing")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name="billing")
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    total_cost = models.FloatField()

    def __str__(self):
        return f"{self.borrowed_by} by {self.book}"


class User(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    books = models.ManyToManyField(Book, related_name="readers", blank=True)

    def __str__(self):
        return self.name