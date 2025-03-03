from django.urls import path
from .views import (users, user_detail,authors,author_detail, book_list, book_detail, category_list, category_detail, search_data,reserve_book, borrow_book,return_book)

urlpatterns = [
  path('users/', users, name='user-list'),
  path('users/<int:pk>/', user_detail, name='user-detail'),
  path('authors/', authors, name='author-list'),
  path('authors/<int:pk>/', author_detail, name='author-detail'),
  path('books/', book_list, name='book-list'),
  path('books/<int:pk>/', book_detail, name='book-detail'),
  path('categories/', category_list, name='category-list'),
  path('categories/<int:pk>/', category_detail, name='category-detail'),
  path('reserve/', reserve_book, name='reserve_book'),
  path('borrow/', borrow_book, name='borrow_book'),
  path('return/', return_book, name='return_book'),
  path('search/', search_data, name='search_data')
]

