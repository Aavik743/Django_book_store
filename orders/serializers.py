from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'cart',
            'address'
        ]

    def create(self, validated_data):
        cart = validated_data.get('cart')

        update_data = {'total_price': cart.total_price, "user_id": cart.user.id, "book_id": cart.book.id,
                       "cart_id": cart.id, "book_quantity": cart.book_quantity}

        validated_data.update(update_data)

        self.Meta.model.objects.create(**validated_data)

        # cart.delete()

        return validated_data


class GetOrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    cart_id = serializers.IntegerField()
    book_quantity = serializers.IntegerField()
    total_price = serializers.FloatField()
    address = serializers.CharField()

    class Meta:
        model = Order
        fields = [
            'user_id',
            'book_id',
            'cart_id',
            'book_quantity',
            'total_price',
            'address'
        ]
