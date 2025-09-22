from rest_framework import viewsets, filters
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny,
)
from django.contrib.auth.models import User
from .models import Book, Review
from .serializer import UserSerializer, BookSerializer, ReviewSerializer
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend #HasAuthorFilterBackend

#USERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#BOOKS
# class BookInfoAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
        #HasAuthorFilterBackend,
        ]
    search_fields= ['title', 'author']
    ordering_fields = ['title', 'author']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


#REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

class UserReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
