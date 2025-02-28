from django.urls import path
from .views import (users, user_detail,authors,author_detail, book_list, book_detail, category_list, category_detail, search_data,update_book_status, add_book_to_user, remove_book_from_user)

urlpatterns = [
  path('users/', users, name='user-list'),
  path('users/<int:pk>/', user_detail, name='user-detail'),
  path('authors/', authors, name='author-list'),
  path('authors/<int:pk>/', author_detail, name='author-detail'),
  path('books/', book_list, name='book-list'),
  path('books/<int:pk>/', book_detail, name='book-detail'),
  path('categories/', category_list, name='category-list'),
  path('categories/<int:pk>/', category_detail, name='category-detail'),
  path('search/', search_data, name='search_data'),
  path('update/<int:pk>/', update_book_status, name='update_book_status'),
  path('add/<int:pk>/', add_book_to_user, name='add_book_to_user'),
  path('remove/<int:pk>/', remove_book_from_user, name='remove_book_from_user')
]

