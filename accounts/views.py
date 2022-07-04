from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import BadRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from common.email import to_send_email, Mail
from common import logger
from common.jwt import get_tokens_for_user, token_required, modified_token
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer, ForgotPasswordSerializer, ChangePasswordSerializer


class RegistrationAPI(APIView):

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = get_tokens_for_user(user).get('access token')
                short_token = modified_token(token)

                current_site = get_current_site(request).domain
                path = reverse('activate')
                url = 'http://' + current_site + path + '?token=' + short_token

                Mail.register_user(data={'email': user.email, 'username': user.username, 'url': url})
                data_ = {'Activation Link': url, 'token': token, 'short_token': short_token}
                logger.logging.info('User account registered')
                return Response({'message': 'activate your account', 'status_code': 200, 'data': data_})
        except Exception as e:
            logger.logging.error(e)
            return Response({'message': str(e), 'status_code': 400}, status=400)

        # {
        # "first_name": "f_name1",
        # "last_name": "l_name1",
        # "username": "username1",
        # "email": "email1@gmail.com",
        # "password": "12345",
        # "confirm_password": "12345"
        # }


class ActivationAPI(APIView):

    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                raise Exception('The account is already activated')
            user.is_active = True
            user.save()
            logger.logging.info('User account activated')
            return Response({'Message': f'{user.username} your account has been activated', 'Status Code': 200})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'Error': "Something went wrong", 'Status Code': 400})


class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serialized_data = LoginSerializer(data=data)
            if serialized_data.is_valid():
                user = serialized_data.get_user(serialized_data.data)
                if not user:
                    return Response({'Error': 'Improper username', 'Status Code': 400})
                if user.password == serialized_data.data['password']:
                    return Response({'Error': 'Improper password', 'Status Code': 400})
                if not user.is_active:
                    return Response({'Error': 'Please activate your account first', 'Status Code': 400})
                login(request, user)
                token = get_tokens_for_user(user).get('access token')
                short_token = modified_token(token)
                logger.logging.info('User signed in')
                return Response({'Message': f'{user.username} is now logged in', 'Status Code': 200, 'token': token,
                                 'short token': short_token})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'Error': "Something went wrong", 'Status Code': 400})


class ForgotPasswordAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serialized_data = ForgotPasswordSerializer(data=data)
            if serialized_data.is_valid():
                user = serialized_data.get_user(serialized_data.data)
                if not user:
                    return Response({'Error': 'Improper email', 'Status Code': 400})
                token = get_tokens_for_user(user).get('access token')
                short_token = modified_token(token)
                current_site = get_current_site(request).domain
                path = reverse('change')
                url = 'http://' + current_site + path + '?token=' + short_token
                subject = 'Forgot Password Link'
                message = f'Hi {user.username}, ' \
                          f'Click on the link to reset your password ' \
                          f'{url}'
                sender = 'fake.abhik@gmail.com'
                recipient = f'{user.email}'
                to_send_email(subject, message, sender, recipient)
                logger.logging.info('Password reset link sent')
                return Response({'Message': 'Reset your password', 'Status Code': 200,
                                 'Token': token, 'Forgot Password Link': url})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'Error': "Something went wrong", 'Status Code': 400})


class ChangePasswordAPI(APIView):
    @method_decorator(token_required)
    def put(self, request, user_id):
        try:
            data = request.data
            serialized_data = ChangePasswordSerializer(data=data)
            if serialized_data.is_valid():
                old_password = serialized_data.data.get('old_password')
                new_password = serialized_data.data.get('new_password')
                confirm_password = serialized_data.data.get('confirm_password')
                user = User.objects.get(pk=user_id)
                if old_password != user.password:
                    return Response({'Error': 'Improper Old Password', 'Code': 400})
                if new_password != confirm_password:
                    return Response({'Error': 'New passwords does not match', 'Code': 400})
                user.password = new_password
                user.save()
                logger.logging.info('password changed')
                return Response({'Message': f'{user.username} your password is changed', 'Code': 200})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'Error': str(e), 'Status Code': 400})
        # {
        #     "old_password": 12345,
        #     "new_password": 12345,
        #     "confirm_password": 12345
        # }


class LogoutAPI(APIView):
    def get(self, request):
        logout(request)
        logger.logging.info('User logged out')
        return Response({'Message': 'You have been logged out', 'Status Code': 200})
