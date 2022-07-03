from rest_framework import serializers
from .models import User


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
        ]

    def create(self, validated_data):
        user = User.objects.create_user(first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'], username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user


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
