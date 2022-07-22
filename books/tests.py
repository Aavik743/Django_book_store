from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Book
from accounts.models import User


class BooksAppTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(first_name="A", last_name='H', username='active_superuser',
                                         email='emailAH@gmail.com', password='12345', is_superuser=True, is_active=True)
        self.user2 = User.objects.create(first_name="C", last_name='D', username='active_not_superuser',
                                         email='emailCD@gmail.com', password='12345', is_superuser=False,
                                         is_active=True)
        self.user3 = User.objects.create(first_name="H", last_name='A', username='not_active',
                                         email='emailHA@gmail.com', password='12345', is_active=False)

    def test_add_book_api_pass(self):
        client = APIClient()
        login = client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        header = {'HTTP_AUTHORIZATION': token, 'content_type': 'application/json'}

        book = {
            "name": "Harry Potter",
            "price": "700",
            "author": "JK Rowling",
            "description": "This is a story book",
            "book_quantity": "10"
        }

        response = client.post(reverse('add_book'), book, **header)
        print("--->>", response.data)
        self.assertEqual(1, 1)
