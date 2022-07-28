from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from books.models import Book
from .models import Cart


class CartAppTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(first_name="A", last_name='B', username='active_user',
                                              email='emailCD@gmail.com', password='12345', is_active=True)
        self.user2 = User.objects.create_user(first_name="C", last_name='D', username='not_active',
                                              email='emailHA@gmail.com', password='12345', is_active=False)
        login = self.client.post(reverse('login'), {"username": "active_user", "password": "12345"})
        token = login.data.get('short_token')

        self.header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}
        self.book = Book.objects.create(name="Harry Potter", price="700", author="JK Rowling",
                                        description="This is a story book", book_quantity=10)

    def create_cart(self):
        cart_data = {
            "book": self.book,
            "book_quantity": 1,
            "total_price": self.book.price,
            "user": self.user1
        }
        cart = Cart.objects.create(**cart_data)
        return cart

    def test_add_to_cart_api_pass(self):
        cart_data = {
            "book": self.book.id,
            "book_quantity": 1
        }

        expected_data = {'book': self.book.id, 'book_quantity': 1, 'user': self.user1.id, 'id': 1}

        response = self.client.post(reverse('add_to_cart'), cart_data, **self.header)
        self.assertEqual(response.data.get('status_code'), 200)
        self.assertEqual(response.data.get('message'), 'cart added')
        self.assertEqual(response.data.get('data'), expected_data)

    def test_add_to_cart_api_with_wrong_book_id_fail(self):
        cart_data = {
            "book": 1,
            "book_quantity": 1
        }

        response = self.client.post(reverse('add_to_cart'), cart_data, **self.header)
        self.assertEqual(response.data.get('status_code'), 400)

    def test_get_cart_api_pass(self):
        self.create_cart()
        response = self.client.get(reverse('get_cart'), **self.header)
        self.assertEqual(response.data.get('message'), 'cart fetched')
        self.assertEqual(response.data.get('status_code'), 200)

    def test_get_cart_api_fail(self):
        response = self.client.get(reverse('get_cart'), **self.header)
        self.assertEqual(response.data.get('status_code'), 400)

    # def test_update_cart_api_pass(self):  # id error
    #     cart = self.create_cart()
    #     print(cart.id)
    #     data = {
    #         "book_quantity": 2,
    #         "id": cart
    #     }
    #     response = self.client.patch(reverse('cart'), data, **self.header)
    #     print(response.data)
    #     # self.assertEqual(response.data.get('message'), 'cart fetched')
    #     # self.assertEqual(response.data.get('status_code'), 200)
