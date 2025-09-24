from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class ReviewCPagination(CursorPagination):
    page_size = 5
    #ordering = 'book'