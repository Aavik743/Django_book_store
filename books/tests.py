from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Book
from accounts.models import User


def create_book():
    book = {
        "name": "Harry Potter",
        "price": "700",
        "author": "JK Rowling",
        "description": "This is a story book",
        "book_quantity": "10"
    }
    return Book.objects.create(**book)


class BooksAppTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_superuser(first_name="A", last_name='H', username='active_superuser',
                                                   email='emailAH@gmail.com', password='12345', is_superuser=True,
                                                   is_active=True)
        self.user2 = User.objects.create_user(first_name="C", last_name='D', username='active_not_superuser',
                                              email='emailCD@gmail.com', password='12345', is_active=True)
        self.user3 = User.objects.create_user(first_name="H", last_name='A', username='not_active',
                                              email='emailHA@gmail.com', password='12345', is_active=False)

    def test_add_book_api_pass(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}

        book = {
            "name": "Harry Potter",
            "price": "700",
            "author": "JK Rowling",
            "description": "This is a story book",
            "book_quantity": "10"
        }

        response = self.client.post(reverse('add_book'), book, **header)
        self.assertEqual(response.data.get('message'), 'book added')
        self.assertEqual(response.data.get('status_code'), 200)

    def test_add_book_api_fail(self):
        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}

        book = {
            "name": "Harry Potter II",
            "price": "700",
            "author": "JK Rowling",
            "description": "This is a story book",
            "book_quantity": "10"
        }

        response = self.client.post(reverse('add_book'), book, **header)
        self.assertEqual(response.data.get('message'), 'Admin access required')
        self.assertEqual(response.data.get('status_code'), 400)

    def test_get_all_book_api_pass(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}

        response = self.client.get(reverse('book'), **header)
        self.assertEqual(response.data.get('message'), 'fetched all books details')
        self.assertEqual(response.data.get('status_code'), 200)

    def test_get_book_by_id_api_pass(self):
        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book = create_book()

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.get(reverse('book_by_id', kwargs={"id": book.id}), **header)
        self.assertEqual(response.data.get('status_code'), 200)

    def test_get_book_by_id_api_fail(self):
        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book_id = 5

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.get(reverse('book_by_id', kwargs={"id": book_id}), **header)
        self.assertEqual(response.data.get('message'),  'Book matching query does not exist.')
        self.assertEqual(response.data.get('status_code'), 400)

    def test_patch_book_by_id_api_pass(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book = create_book()

        data = {
            "name": "Updated Book"
        }

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.patch(reverse('book_by_id', kwargs={"id": book.id}), data, **header)
        self.assertEqual(response.data.get('data').get('name'), 'Updated Book')
        self.assertEqual(response.data.get('message'), 'book details updated')

    def test_patch_book_by_id_api_fail_not_superuser(self):
        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book_id = 1

        data = {
                "name": "Updated Book"
            }

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.patch(reverse('book_by_id', kwargs={"id": book_id}), data, **header)
        self.assertEqual(response.data.get('message'), 'Admin access required')
        self.assertEqual(response.data.get('status_code'), 400)

    def test_patch_book_by_id_api_fail_wrong_book_id(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book_id = 5

        data = {
                "name": "Updated Book"
            }

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.patch(reverse('book_by_id', kwargs={"id": book_id}), data, **header)
        self.assertEqual(response.data.get('message'), 'Book matching query does not exist.')
        self.assertEqual(response.data.get('status_code'), 400)

    def test_delete_book_by_id_api_pass(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book = create_book()

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.delete(reverse('book_by_id', kwargs={"id": book.id}), **header)
        self.assertEqual(response.data.get('status_code'), 200)
        self.assertEqual(response.data.get('message'), 'book deleted')

    def test_delete_book_by_id_not_superuser_fail(self):
        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book = create_book()

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.delete(reverse('book_by_id', kwargs={"id": book.id}), **header)
        self.assertEqual(response.data.get('message'), 'Admin access required')
        self.assertEqual(response.data.get('status_code'), 400)

    def test_delete_book_by_id_wrong_book_id_fail(self):
        login = self.client.post(reverse('login'), {"username": "active_superuser", "password": "12345"})
        token = login.data.get('short_token')

        book_id = 1

        header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        response = self.client.delete(reverse('book_by_id', kwargs={"id": book_id}), **header)
        self.assertEqual(response.data.get('message'), 'Book matching query does not exist.')
        self.assertEqual(response.data.get('status_code'), 400)
