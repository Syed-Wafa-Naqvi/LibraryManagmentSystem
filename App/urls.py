from django.urls import path
from .views import (users, user_detail, book_list, book_detail, book_borrow, book_return,category_list, category_detail)
# from Project.urls import path
# from .views import UserViewSet, BookViewSet, CategoryViewSet

urlpatterns = [
path('users/', users, name='user-list'),
path('users/<int:pk>/', user_detail, name='user-detail'),
path('books/', book_list, name='book-list'),
path('books/<int:pk>/', book_detail, name='book-detail'),
path('books/<int:pk>/borrow/', book_borrow, name='book-borrow'),
path('books/<int:pk>/return/', book_return, name='book-return'),
path('categories/', category_list, name='category-list'),
path('categories/<int:pk>/', category_detail, name='category-detail'),

# path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
# path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
# path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
# path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail'),
# path('books/<int:pk>/borrow/', BookViewSet.as_view({'post': 'borrow'}), name='book-borrow'),
# path('books/<int:pk>/return/', BookViewSet.as_view({'post': 'return_book'}), name='book-return'),
# path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
# path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
]
