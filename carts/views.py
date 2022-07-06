import json

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from common import logger
from common.jwt import token_required
from .models import Cart
from .serializers import AddToCartSerializer, GetCartSerializer, UpdateCartSerializer
from accounts.models import User
from books.models import Book


class AddToCartAPI(APIView):

    @method_decorator(token_required)
    def post(self, request, user_id):
        try:
            user = User.objects.filter(pk=user_id).first()
            if user:
                cart_serializer = AddToCartSerializer(data=request.data)
                cart_serializer.is_valid()
                book_quantity = cart_serializer.validated_data.get('book_quantity')
                book_id = cart_serializer.validated_data.get('book_id')
                book = Book.objects.get(pk=book_id)
                if book:
                    if book.book_quantity >= book_quantity:
                        cart = Cart.objects.filter(book_id=book_id).first()
                        if cart:
                            cart.book_quantity += book_quantity
                            book.book_quantity -= book_quantity
                            cart.total_price = cart.book_quantity * book.price
                            cart.save()
                            book.save()
                            return Response(
                                {'message': 'cart updated', 'status_code': 200, 'data': cart_serializer.data})
                        book.book_quantity -= book_quantity
                        total_price = book.price * book_quantity

                        cart = Cart.objects.create(user=user, book=book,
                                                   book_quantity=book_quantity, total_price=total_price)
                        cart.save()
                        book.save()
                        return Response({'message': 'cart added', 'status_code': 200, 'data': cart_serializer.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class CartAPI(APIView):

    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            user = User.objects.filter(pk=user_id).first()
            if user:
                cart = Cart.objects.filter(user=user)
                if cart:
                    cart_serializer = GetCartSerializer(cart, many=True)
                    return Response({'message': 'cart fetched', 'status_code': 200, 'data': cart_serializer.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class UpdateCartAPI(APIView):

    @method_decorator(token_required)
    def patch(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
        if user:
            cart = Cart.objects.filter(user=user).first()
            book = Book.objects.filter(pk=cart.book_id).first()
            if book:
                if cart:
                    # cart_serializer = UpdateCartSerializer(cart)
                    # book_quantity = cart_serializer.data.get('book_quantity')
                    book_quantity = int(request.data.get('book_quantity'))

                    print('cart book q', cart.book_quantity)
                    print('input book q', book_quantity)

                    if cart.book_quantity > book_quantity:
                        count = cart.book_quantity - book_quantity

                        book.book_quantity += count

                    if cart.book_quantity < book_quantity:
                        count = book_quantity - cart.book_quantity

                        book.book_quantity -= count

                    cart.book_quantity = book_quantity
                    cart.save()
                    book.save()
                    data = {'book quantity in cart': cart.book_quantity}
                    return Response({'message': 'cart updated', 'status_code': 200, 'data': data})

    @method_decorator(token_required)
    def delete(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
        if user:
            cart = Cart.objects.filter(user=user).first()
            book = Book.objects.filter(pk=cart.book_id).first()
            book.book_quantity += cart.book_quantity
            cart.delete()
            book.save()
            return Response({'message': 'cart removed', 'status_code': 200})
