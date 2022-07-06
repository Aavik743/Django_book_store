from rest_framework import serializers
from .models import Cart


class AddToCartSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    book_quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = [
            'book_id',
            'book_quantity',
        ]


class GetCartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    book_quantity = serializers.IntegerField()
    total_price = serializers.FloatField()

    class Meta:
        model = Cart
        fields = [
            'user_id',
            'book_id',
            'book_quantity',
            'total_price',
        ]

