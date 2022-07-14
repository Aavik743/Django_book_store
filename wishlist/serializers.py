from rest_framework import serializers
from .models import Wishlist


class AddToWishlist(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = [
            'book',
            'user'
        ]
