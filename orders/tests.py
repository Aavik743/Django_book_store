from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from books.models import Book
from carts.models import Cart
from .models import Order


class OrderAppTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(first_name="A", last_name='B', username='active_user',
                                              email='emailCD@gmail.com', password='12345', is_active=True)
        login = self.client.post(reverse('login'), {"username": "active_user", "password": "12345"})
        token = login.data.get('short_token')

        self.header = {"HTTP_AUTHORIZATION": token, "Content-Type": "application/json"}

        self.book = Book.objects.create(name="Harry Potter", price="700", author="JK Rowling",
                                        description="This is a story book", book_quantity=10)
        self.cart = Cart.objects.create(book=self.book, book_quantity=1, total_price=self.book.price, user=self.user1)

    def test_place_order_api_pass(self):
        order_data = {
            "cart": self.cart.id,
            "address": "city name"
        }

        response = self.client.post(reverse('checkout'), order_data, **self.header)
        self.assertEqual(response.data.get('message'), 'order has been placed by active_user')
        self.assertEqual(response.data.get('status_code'), 201)

    def test_place_order_api_fail(self):
        order_data = {
            "address": "city name"
        }

        response = self.client.post(reverse('checkout'), order_data, **self.header)
        self.assertEqual(response.data.get('status_code'), 400)

    def test_get_order_api_fail(self):
        response = self.client.get(reverse('get-orders'), **self.header)
        self.assertEqual(response.data.get('message'), "('Create order at first', 400)")
        self.assertEqual(response.data.get('status_code'), 400)

    def test_get_order_api_pass(self):
        order_data = {
            "cart": self.cart.id,
            "address": "city name",
            "book_quantity": self.cart.book_quantity,
            "total_price": self.cart.total_price,
            "book_id": self.book.id,
            "user_id": self.user1.id
        }

        self.client.post(reverse('checkout'), order_data, **self.header)
        response = self.client.get(reverse('get-orders'), **self.header)
        self.assertEqual(response.data.get('status_code'), 200)
        self.assertEqual(response.data.get('message'), 'cart fetched')

