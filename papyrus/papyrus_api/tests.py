from .models import Review, User, Book
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class BookAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin',password='adminpass')
        self.normal_user = User.objects.create_user(username='user1',email='user@g.com',password='userpass')
        self.book = Book.objects.create(
            title ='Test Book',
            author = 'TestAuthor',
            description = 'Test Description'
        )

        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_get_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_unauthorized_update_book(self):
        data = {"title": "Updated Title"}
        response = self.client.put(self.book_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_book(self):
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admins_can_delete_product(self):
        # test normal user cannot delete
        self.client.login(username='user1',password='userpass')
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

        #test admin user can delete
        self.client.login(username='admin',password='adminpass')
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_get_all_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_book(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'description': 'New Description'
        }
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')

    def test_normal_user_cannot_create_book(self):
        self.client.login(username='user1', password='userpass')
        data = {
            'title': 'Unauthorized Book',
            'author': 'Unauthorized Author',
            'description': 'Should not be created'
        }
        response = self.client.post(self.book_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_book(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'title': 'Updated Title',
            'author': 'TestAuthor',
            'description': 'Updated Description'
        }
        response = self.client.put(self.book_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db() 
        self.assertEqual(self.book.title, 'Updated Title')
    
    def test_search_books_by_title(self):
        Book.objects.create(
            title='Test Book', 
            author='Test', 
            description='Test'
            )
        response = self.client.get(self.book_list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.book_list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.book = Book.objects.create(
            title='Review Test Book',
            author='Review Author',
            description='Book for testing reviews'
        )
        self.review_list_url = reverse('review-list')

    def test_create_review_requires_authentication(self):
        data = {
            'book': self.book.pk,
            'rating': 8.1,
            'comment': 'Good book'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_review(self):
        self.client.login(username='user1', password='pass1')
        data = {
            'book': self.book.pk,
            'rating': 9.7,
            'comment': 'Excellent book'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.user1)

    def test_user_can_only_see_their_reviews(self):
        Review.objects.create(book=self.book, user=self.user1, rating=8, comment='User1 review')
        Review.objects.create(book=self.book, user=self.user2, rating=6, comment='User2 review')
        
        self.client.login(username='user1', password='pass1')
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['comment'], 'User1 review')

    def test_rating_validation_too_high(self):
        self.client.login(username='user1', password='pass1')
        data = {
            'book': self.book.pk,
            'rating': 12,
            'comment': 'Good book'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_rating_validation_negative(self):
        self.client.login(username='user1', password='pass1')
        data = {
            'book': self.book.pk,
            'rating': -1,
            'comment': 'Good book'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_rating_accepted(self):
        self.client.login(username='user1', password='pass1')
        data = {
            'book': self.book.pk,
            'rating': 7.8,
            'comment': 'Great book'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], '7.8')


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass'
        )
        self.user_list_url = reverse('user-list')

    def test_get_user_list(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)