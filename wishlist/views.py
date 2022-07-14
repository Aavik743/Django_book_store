from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from books.models import Book
from common import logger, custom_exceptions
from common.jwt import token_required
from .models import Wishlist
from .serializers import WishlistSerializer


class AddToWishlistAPI(APIView):

    @method_decorator(token_required)
    def post(self, request, user_id):
        try:
            data = request.data.copy()
            data.update({'user': user_id})

            wishlist_serializer = WishlistSerializer(data=data)
            wishlist_serializer.is_valid(raise_exception=True)
            print(wishlist_serializer.data.get('book'))
            book = Wishlist.objects.get(book=wishlist_serializer.data.get('book'))
            if book:
                raise custom_exceptions.BookAlreadyExists('book already exists in your wishlist', 400)
            wishlist_serializer.save()

            return Response({'message': 'book added to wishlist', 'status_code': 200, 'data': wishlist_serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            if user_id:
                wishlist = Wishlist.objects.filter(user__id=user_id)

                if not wishlist:
                    raise custom_exceptions.CartDoesNotExist('Add to wishlist at first', 400)
                if wishlist:
                    wishlist_serializer = WishlistSerializer(wishlist, many=True)

                    return Response({'message': 'cart fetched', 'status_code': 200, 'data': wishlist_serializer.data},
                                    status=status.HTTP_200_OK)

        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})
