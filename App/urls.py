from django.urls import path
from .views import (users, user_detail, book_list, book_detail, book_borrow, book_return,category_list, category_detail, book_reservation, reservation_list, reservation_detail)

urlpatterns = [
path('users/', users, name='user-list'),
path('users/<int:pk>/', user_detail, name='user-detail'),
path('books/', book_list, name='book-list'),
path('books/<int:pk>/', book_detail, name='book-detail'),
path('books/<int:pk>/borrow/', book_borrow, name='book-borrow'),
path('books/<int:pk>/return/', book_return, name='book-return'),
path('categories/', category_list, name='category-list'),
path('categories/<int:pk>/', category_detail, name='category-detail'),
path('reservations/reserve/', book_reservation, name='book-reservation'),
path('reservations/', reservation_list, name='reservation-list'),
path('reservations/<int:pk>/', reservation_detail, name='reservation-detail'),
]
