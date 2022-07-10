from rest_framework import serializers
from .models import Cart


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'book',
            'book_quantity',
            'user',
            'id'
        ]

    def create(self, validated_data):
        book = validated_data.get('book')
        book_quantity = validated_data.get('book_quantity')

        if book.book_quantity < book_quantity:
            raise Exception('book out of stock')
        book.book_quantity -= book_quantity
        book.save()
        total_price = book.price * book_quantity

        validated_data.update({'total_price': total_price})

        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        book = instance.book
        book_quantity = validated_data.get('book_quantity')

        if book_quantity > book.book_quantity:
            raise Exception('reduce books')

        if instance.book_quantity > book_quantity:
            count = instance.book_quantity - book_quantity

            book.book_quantity += count

        if instance.book_quantity < book_quantity:
            count = book_quantity - instance.book_quantity

            book.book_quantity -= count

        instance.book_quantity = book_quantity
        instance.total_price = book.price * book_quantity

        book.save()
        instance.save()
        return instance


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
