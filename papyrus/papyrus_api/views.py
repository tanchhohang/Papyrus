from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from django.contrib.auth.models import User
from .models import Book, Review
from .serializer import UserSerializer, BookSerializer, ReviewSerializer, BookInfoSerializer

#USERS

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# class UserListAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetailAPIView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_url_kwarg = 'user_id'

#BOOKS
class BookInfoAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


