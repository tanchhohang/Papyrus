import django_filters
from .models import Book
from rest_framework import filters


# class HasAuthorFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self,request,queryset,view):
#         return queryset.filter()


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title':['exact','contains'],
            'author': ['exact', 'contains'],
        }