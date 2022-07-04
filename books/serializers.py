from rest_framework import serializers
from .models import Book


class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'name',
            'price',
            'author',
            'description',
            'image_field',
            'book_quantity'
        ]
        required_field = ['name', 'price', 'author', 'book_quantity']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'price',  'book_quantity', 'description', 'image_field']
