from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from books.models import Book


class WishlistTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(first_name="A", last_name='B', username='active_user',
                                              email='emailCD@gmail.com', password='12345', is_active=True)
        login = self.client.post(reverse('login'), {"username": "active_user", "password": "12345"})
        token = login.data.get('short_token')

        self.header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}

        self.book = Book.objects.create(name="Harry Potter", price="700", author="JK Rowling",
                                        description="This is a story book", book_quantity=10)

    def test_add_to_wishlist_fail(self):
        wishlist_data = {"book_id": self.book.id, "user_id": self.user1.id}

        response = self.client.post(reverse('wishlist'), wishlist_data, **self.header)
        self.assertEqual(response.data.get('status_code'), 400)

    def test_get_the_wishlist_fail(self):
        wishlist_data = {"book": self.book.id}

        self.client.post(reverse('wishlist'), wishlist_data, **self.header)
        response = self.client.get(reverse('wishlist'), wishlist_data, **self.header)
        self.assertEqual(response.data.get('status_code'), 400)
