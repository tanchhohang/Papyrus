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