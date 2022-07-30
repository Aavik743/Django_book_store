from django.contrib.auth import logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import BadRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common import logger
from common.email import Mail
from common.jwt import get_tokens_for_user, token_required, modified_token
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer, ForgotPasswordSerializer


class RegistrationAPI(APIView):

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user).get('access_token')
                short_token = modified_token(token)

                current_site = get_current_site(request).domain
                path = reverse('activate')
                url = 'http://' + current_site + path + '?token=' + short_token

                Mail.register_user(data={'email': user.email, 'username': user.username, 'url': url})
                data_ = {'Activation Link': url, 'token': token, 'short_token': short_token}
                logger.logging.info('User account registered')
                return Response({'message': 'activate your account', 'status_code': 200, 'data': data_})
        except BadRequest as e:
            logger.logging.error(e)
            return Response({'message': 'Something went wrong', 'status_code': 400}, status=400)


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
            return Response({'message': f'{user.username} your account has been activated', 'Status Code': 200})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'Error': "Something went wrong", 'Status Code': 400})


class LoginAPI(APIView):

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: "Success"})
    def post(self, request):
        try:
            serialized_data = LoginSerializer(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                user = serialized_data.get_user(serialized_data.data)
                check_user = authenticate(username=serialized_data.data.get('username'),
                                          password=serialized_data.data.get('password'))

                if not check_user:
                    return Response({'message': 'invalid credentials'}, status=401)
                token = get_tokens_for_user(check_user).get('access_token')
                short_token = modified_token(token)
                logger.logging.info('User signed in')
                return Response({'Message': f'{user.username} is now logged in', 'status_code': 200, 'token': token,
                                 'short_token': short_token})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'Error': "Something went wrong", 'status_code': 400})


class ForgotPasswordAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serialized_data = ForgotPasswordSerializer(data=data)
            if serialized_data.is_valid():
                user = serialized_data.get_user(serialized_data.data)
                if not user:
                    return Response({'message': 'Improper email', 'status_code': 400})
                token = get_tokens_for_user(user).get('access token')
                short_token = modified_token(token)
                current_site = get_current_site(request).domain
                path = reverse('change')
                url = 'http://' + current_site + path + '?token=' + short_token
                Mail.forgot_password(user, url)
                logger.logging.info('Password reset link sent')
                return Response({'message': 'Reset your password', 'status_code': 200,
                                 'Token': token, 'Forgot Password Link': url})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'message': "Something went wrong", 'status_code': 400})


class ChangePasswordAPI(APIView):
    @method_decorator(token_required)
    def put(self, request, user_id):
        try:
            data = request.data
            user = User.objects.get(pk=user_id)
            if user.check_password(data.get('old_password')):
                user.set_password(data.get('new_password'))
                user.save()
                logger.logging.info('password changed')
                return Response({"message": f"{user.username} your password is changed", "status_code": 200})
            return Response({"message": "old password does not match", "status_code": 200})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'message': 'something went wrong', 'status_code': 400})


class LogoutAPI(APIView):
    def get(self, request):
        logout(request)
        logger.logging.info('User logged out')
        return Response({'Message': 'You have been logged out', 'Status Code': 200})
