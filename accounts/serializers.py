from rest_framework import serializers
from .models import User
from common.jwt import get_tokens_for_user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',
        ]
        required_fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password'
        ]

        extra_kwargs = {'first_name': {'write_only': True},
                        'last_name': {'write_only': True},
                        'username': {'write_only': True},
                        'email': {'write_only': True},
                        'password': {'write_only': True},
                        'confirm_password': {'write_only': True}
                        }

    # def get_token(self, obj):
    #     print(obj)
    #     token = get_tokens_for_user(obj).get('access token')
    #     print(token)
    #     return token

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
        required_fields = fields

    def get_user(self, validated_data):
        username = validated_data['username']
        user = User.objects.get(username=username)
        return user


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def get_user(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']
        required_fields = fields
