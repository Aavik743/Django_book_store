from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from books.models import Book
from common import logger, custom_exceptions
from common.jwt import token_required
from .models import Cart
from .serializers import AddToCartSerializer, GetCartSerializer
from rest_framework import status


class AddToCartAPI(APIView):

    @method_decorator(token_required)
    def post(self, request, user_id):
        try:
            data = request.data.copy()
            data.update({'user': user_id})

            cart_serializer = AddToCartSerializer(data=data)
            cart_serializer.is_valid(raise_exception=True)
            cart_serializer.save()

            return Response({'message': 'cart added', 'status_code': 200, 'data': cart_serializer.data},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)


class CartAPI(APIView):

    @method_decorator(cache_page(60 * 60))
    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            if user_id:
                cart = Cart.objects.filter(user__id=user_id, ordered=False)

                if not cart:
                    raise custom_exceptions.CartDoesNotExist('Add to cart at first', 400)
                if cart:
                    cart_serializer = GetCartSerializer(cart, many=True)

                    return Response({'message': 'cart fetched', 'status_code': 200, 'data': cart_serializer.data},
                                    status=status.HTTP_200_OK)

        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class UpdateCartAPI(APIView):

    @method_decorator(token_required)
    def patch(self, request, user_id):
        try:
            data = request.data.copy()
            data.update({'user': user_id})
            pk = data.pop('id')
            cart = Cart.objects.get(pk=pk)
            serializer = AddToCartSerializer(cart, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'message': 'cart updated', 'status_code': 200, 'data': serializer.data},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(token_required)
    def delete(self, request, user_id):
        try:
            user = User.objects.filter(pk=user_id).first()

            if not user:
                raise custom_exceptions.UserDoesNotExist('User does not exist', 400)
            if user:
                cart = Cart.objects.filter(user=user, book_id=request.data).first()
                book = Book.objects.filter(pk=cart.book_id).first()

                book.book_quantity += cart.book_quantity

                cart.delete()
                book.save()

                return Response({'message': 'cart removed', 'status_code': 200})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})
