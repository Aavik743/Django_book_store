from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from .models import User
from django.core.exceptions import BadRequest
from rest_framework.response import Response
from common.jwt import get_tokens_for_user, token_required, modified_token
from common.email import to_send_email


class RegistrationAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serialized_data = RegistrationSerializer(data=data)
            if not serialized_data.is_valid():
                raise Exception
            first_name = serialized_data.data.get('first_name')
            last_name = serialized_data.data.get('last_name')
            username = serialized_data.data.get('username')
            email = serialized_data.data.get('email')
            password = serialized_data.data.get('password')
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                            email=email, password=password, is_active=False)

            token = get_tokens_for_user(user).get('access token')
            short_token = modified_token(token)
            current_site = get_current_site(request).domain
            path = reverse('activate')
            url = 'http://' + current_site + path + '?token=' + short_token
            subject = 'Activation Link'
            message = f'Hi {username}, Click on the link to activate your account {url}'
            sender = 'fake.abhik@gmail.com'
            recipient = f'{email}'
            to_send_email(subject, message, sender, recipient)
            user.save()
            return Response({'Message': 'Activate your account', 'Status Code': 200,
                             'Token': token, 'Activation Link': url})
        except BadRequest:
            return Response({'Error': "Something went wrong", 'Status Code': 400})
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
                raise Exception
            user.is_active = True
            user.save()
            return Response({'Message': 'Account has been activated', 'Status Code': 200})
        except BadRequest:
            return Response({'Error': "Something went wrong", 'Status Code': 400})
