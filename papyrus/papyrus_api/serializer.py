from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'date_joined'
            ]

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    # user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = [
            'id',
            'book',
            'user',
            'rating',
            'comment',
            'created'
            ]

    def validate_rating(self,value):
        if value > 10 or value < 0:
            raise serializers.ValidationError('Ratings must be between 0 - 10')
        return value

class BookSerializer(serializers.ModelSerializer):
    avgrating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'description',
            'reviews',
            'avgrating'
            ]


# class BookCreateSerializer(serializers.ModelSerializer):
#     class BookReviewsCreateSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = BookReview
#             fields = ['rating','comment']

#     reviews = BookReviewsCreateSerializer(many=True)

#     def create(self,validated_data):
#         bookreview_data = validated_data.pop('reviews')
#         book = Book.objects.all().create(**validated_data)

#         for review in bookreview_data:
#             BookReview.objects.create(book = book, **item)

#         return book

#     class Meta:
#         model = Book
#         fields=[
#             'title',
#             'author',
#             'description',
#             'reviews',
#         ]
#         extra_kwargs = (
#             'user': {'read_only': True}
#         )

