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
            'date'
            ]

    def validate_rating(self,value):
        if value > 10 or value < 0:
            raise serializers.ValidationError('Ratings must be between 0 - 10')
        return value

class BookSerializer(serializers.ModelSerializer):
    avgrating = serializers.FloatField(read_only=True)
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'description',
            'avgrating'
            ]

class BookInfoSerializer(serializers.Serializer):
    books = BookSerializer(many=True)
    count = serializers.IntegerField()

