from django.db import models
# Create your models here.


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(AbstractBaseModel):
    author_name = models.CharField(max_length=255)

    def __str__(self):
        return self.author_name


class Book(AbstractBaseModel):
    ISBN = models.CharField(max_length=13, default="")
    book_title = models.CharField(max_length=255)
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publish_date = models.DateField()
    book_status = models.CharField(max_length=20, default="Available" , choices=[('Available', 'Available'),('Borrow', 'Borrow'),('Reserve', 'Reserve'),('Return', 'Return')])
    users = models.ManyToManyField('User', related_name="borrowed_books", blank=True)
    description = models.TextField()

    def __str__(self):
        return self.book_title


class User(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    books = models.ManyToManyField(Book, related_name="readers", blank=True)

    def __str__(self):
        return self.name


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.name} searched {self.description}"