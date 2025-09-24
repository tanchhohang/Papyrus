import django_filters
from .models import Book, Review
from rest_framework import filters


# class HasAuthorFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self,request,queryset,view):
#         return queryset.filter()


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title':['iexact','icontains'],
            'author': ['exact', 'contains'],
        }

class ReviewFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date__date")
    class Meta:
        model = Review
        fields = {
            'rating':['exact','lt','gt'],
            'date': ['lt','gt','exact']
        }        