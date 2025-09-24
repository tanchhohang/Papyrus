from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny,
)
from django.contrib.auth.models import User
from .models import Book, Review
from .serializer import UserSerializer, BookSerializer, ReviewSerializer
from .filters import BookFilter, ReviewFilter
from .pagination import ReviewCPagination
from django_filters.rest_framework import DjangoFilterBackend #HasAuthorFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


#USERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#BOOKS
# class BookInfoAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.order_by('pk')
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

    # pagination_class.pagesize = 2
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 10

    #optional overwrite
    #pagination_class.page_query_param = 'pagenum'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


#REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ReviewFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ReviewCPagination

    #optional
    #paginantion_class = None

    def get_queryset(self):
        qs= super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
    
    # @action(
    #     detail=False,
    #     methods=['GET'], 
    #     url_path='user-reviews',
    #     )
    # def user_reviews(self,request):
    #     reviews = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(reviews, many=True)
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    

# class UserReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
