from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from common import logger
from common.jwt import token_required
from .models import Book
from .serializers import AddBookSerializer, BookSerializer
from accounts.models import User


class AddBookAPI(APIView):

    @method_decorator(token_required)
    def post(self, request, user_id):
        try:
            superuser = Book.validate_superuser(user_id)
            if superuser:
                data = request.data
                book_s = AddBookSerializer(data=data)
                book_s.is_valid(raise_exception=True)
                book_s.save()
                return Response({'message': 'book added', 'status_code': 200, 'data': book_s.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class BookAPI(APIView):

    @method_decorator(token_required)
    def get(self, request, user_id, id):
        try:
            user = User.objects.filter(pk=user_id).first()
            if user:
                if id:
                    book = Book.objects.get(pk=id)
                    book_s = BookSerializer(book)
                    return Response({'message': 'Fetched book details', 'status_code': 200, 'data': book_s.data})
                all_books = Book.objects.all()
                book_s = BookSerializer(all_books, many=True)
                return Response({'message': 'fetched all books details', 'status_code': 200, 'data': book_s.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})

    @method_decorator(token_required)
    def patch(self, request, user_id, id):
        try:
            superuser = Book.validate_superuser(user_id)
            if superuser:
                book = Book.objects.get(pk=id)
                if book:
                    book_s = BookSerializer(book, request.data, partial=True)
                    book_s.is_valid(raise_exception=True)
                    book_s.save()
                    return Response({'message': 'book details updated', 'status_code': 200, 'data': book_s.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})

    @method_decorator(token_required)
    def delete(self, request, user_id, id):
        try:
            superuser = Book.validate_superuser(user_id)
            if superuser:
                book = Book.objects.get(pk=id)
                if book:
                    book.delete()
                    return Response({'message': 'book deleted', 'status_code': 200})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


# class WishlistAPI(APIView):
#
#     @method_decorator(token_required)
#     def post(self, request, user_id, id):
#         try:
#             user = User.objects.filter(pk=user_id).first()
#             if user:
#                 if id:
#                     book = Book.objects.get(pk=id)
#                     book.is_on_wishlist = True
#                     book.save()
#                     data = {'book_id': id, 'user_id': user_id}
#                     return {'message': 'book added to wishlist', 'data': data, 'status_code': 200}
#         except Exception as e:
#             logger.logging.error('Log Error Message')
#             return Response({'message': str(e), 'status_code': 400})

