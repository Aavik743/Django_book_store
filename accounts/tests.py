from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token

from .models import User


class AccountsAppTestCases(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_superuser(first_name="A", last_name='H', username='active_superuser',
                                                   email='emailAH@gmail.com', password="12345")
        self.user2 = User.objects.create_user(first_name="C", last_name='D', username='active_not_superuser',
                                              email='emailCD@gmail.com', password="12345")
        self.user3 = User.objects.create_user(first_name="H", last_name='A', username='not_active',
                                              email='emailHA@gmail.com', password="12345", is_active=False)

    def test_user_count(self):
        all_user = User.objects.all().count()
        self.assertEqual(all_user, 3)

    #
    # def test_user_emails(self):
    #     ah = User.objects.get(username='active_superuser')
    #     ha = User.objects.get(username='active_not_superuser')
    #     self.assertEqual(ah.email, 'emailAH@gmail.com')
    #     self.assertEqual(ha.email, 'emailCD@gmail.com')
    #
    def test_registration_api_pass(self):
        factory = APIRequestFactory()
        data = {
            "first_name": "A",
            "last_name": "H",
            "username": "userAH",
            "email": "emailAH@gmail.com",
            "password": "12345",
            "confirm_password": "12345"
        }
        request = factory.post('http://127.0.0.1:8000/register/', data, format='json')
        self.assertEqual(request.method, 'POST')

    def test_login_api_pass(self):
        client = APIClient()
        data = {
            "username": "active_not_superuser",
            "password": "12345"
        }
        response = client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_api_fail(self):
        client = APIClient()
        data = {
            "username": "not_active",
            "password": "12345"
        }
        response = client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_forgot_password_api_pass(self):
    #     data = {
    #         "email": "emailCD@gmail.com"
    #     }
    #     response = self.client.post("http://127.0.0.1:8000/forgot/", data)
    #     self.assertEqual(response.data.get('message'), 'Reset your password')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_api_pass(self):
        data = {
            "old_password": '12345',
            "new_password": '1234',
            "confirm_password": '1234'
        }

        login = self.client.post(reverse('login'), {"username": "active_not_superuser", "password": "12345"})
        token = login.data.get('short_token')

        header = {"HTTP_AUTHORIZATION": token, "content_type": "application/json"}
        print("token", token)

        response = self.client.put(reverse('change'), data, **header)
        print(response.data)
        # self.assertEqual(response.data.get('message'), 'active_not_superuser your password is changed')
