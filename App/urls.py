from django.urls import path
from .views import users, user_detail, book_list, book_detail, book_borrow, book_return, category_list, category_detail




urlpatterns = [
path('users/', users, name='user-list'),
path('users/<int:pk>/', user_detail, name='user-detail'),

# path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
# path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
# path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
# path('books/<int:pk>/',BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail')
]