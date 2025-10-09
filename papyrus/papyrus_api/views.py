from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser,
    AllowAny,
)
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Book, Review
from .serializer import UserSerializer, BookSerializer, ReviewSerializer #BookCreateSerializer
from .filters import BookFilter, ReviewFilter
from .pagination import ReviewCPagination
from django_filters.rest_framework import DjangoFilterBackend #HasAuthorFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle


#USERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#BOOKS
# class BookInfoAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    throttle_scope = 'books'
    throttle_classes = [ScopedRateThrottle]
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

    @method_decorator(cache_page(60 * 15, key_prefix="book_list"), name="list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset()
    

    # pagination_class.pagesize = 2
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 10

    #optional overwrite
    #pagination_class.page_query_param = 'pagenum'

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return BookCreateSerializer
    #     return super().get_serializer_class()

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


#REVIEW
class ReviewViewSet(viewsets.ModelViewSet):
    throttle_scope = 'reviews'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ReviewFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ReviewCPagination

    #optional
    #paginantion_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
