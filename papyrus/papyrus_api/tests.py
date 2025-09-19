from django.test import TestCase
from .models import Review, User, Book
from django.urls import reverse

# Create your tests here.
class UserReviewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='a@b.com',password='temp')
        self.user2 = User.objects.create_user(username='user2', email='d@b.com',password='temp')

        self.book = Book.objects.create(title='Test Book', author='John Doe', description='Test description')

        Review.objects.create(book=self.book, user=self.user1, rating=8.5, comment="Great book")
        Review.objects.create(book=self.book, user=self.user2, rating=7.5, comment="Not bad")

    def test_user_review_endpoint_retrieves_only_authenticated_user_reviews(self):
        user = User.objects.get(username = 'user1')

        self.client.force_login(user)
        response = self.client.get(reverse('user-reviews-list'))

        assert response.status_code == 200
        data = response.json()
        print(data)