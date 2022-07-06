from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from books.models import Book
from common import logger
from common.jwt import token_required
from .models import Cart
from .serializers import AddToCartSerializer, GetCartSerializer


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
                cart = Cart.objects.filter(book_id=book_id).first()

                Cart.add_to_cart_validation(user, book, cart, book_quantity)

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
        try:
            user = User.objects.filter(pk=user_id).first()

            if user:
                data_ = Cart.update_cart_validation(user, request)
                data = {'book quantity in cart': data_}

                return Response({'message': 'cart updated', 'status_code': 200, 'data': data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})

    @method_decorator(token_required)
    def delete(self, request, user_id):
        try:
            user = User.objects.filter(pk=user_id).first()

            if user:
                cart = Cart.objects.filter(user=user).first()
                book = Book.objects.filter(pk=cart.book_id).first()
                
                book.book_quantity += cart.book_quantity

                cart.delete()
                book.save()

                return Response({'message': 'cart removed', 'status_code': 200})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})