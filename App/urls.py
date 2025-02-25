from django.urls import path

from .CategoryViewSet import CategoryViewSet
from .views import BookViewSet, UserViewSet

urlpatterns = [
path('users/',UserViewSet.as_view({'get':'list','post':"create"}),name='user_list'),
path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
path('books/<int:pk>/',BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail')
]