from django.core.exceptions import BadRequest
from django.db import models
from rest_framework.response import Response

from accounts.models import User
from common import logger


class Book(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    price = models.FloatField(blank=False)
    author = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=100)
    image_field = models.FileField(upload_to='images/', null=True, default=None)
    book_quantity = models.IntegerField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def validate_superuser(user_id):
        user = User.objects.get(pk=user_id)
        if user.is_superuser:
            return user

    @staticmethod
    def check_if_book_exists(validated_data):
        try:
            book_name = validated_data['name']
            book = Book.objects.filter(name=book_name).first()
            if book:
                book.book_quantity += int(validated_data['book_quantity'])
                return book
            return None
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'error': "something went wrong", 'status code': 400})
