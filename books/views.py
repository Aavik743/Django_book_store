from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.exceptions import BadRequest
from common import logger
from common.jwt import token_required
from .models import Book
from .serializers import AddBookSerializer, BookSerializer
from accounts.models import User


class AddBookAPI(APIView):

    @swagger_auto_schema(request_body=AddBookSerializer, responses={200: "Success"})
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
            return Response({'message': 'Admin access required', 'status_code': 400})
        except BadRequest:
            logger.logging.error('Log Error Message')
            return Response({'message': 'something went wrong', 'status_code': 400})


class BookAPI(APIView):

    @method_decorator(cache_page(60 * 60))
    @method_decorator(token_required)
    def get(self, request, user_id, id=None):
        try:
            user = User.objects.filter(pk=user_id).first()
            if user.is_active:
                if id:
                    book = Book.objects.get(pk=id)
                    book_s = BookSerializer(book)
                    return Response({'message': 'Fetched book details', 'status_code': 200, 'data': book_s.data})
                all_books = Book.objects.all()
                book_s = BookSerializer(all_books, many=True)
                return Response({'message': 'fetched all books details', 'status_code': 200, 'data': book_s.data})
            return Response({'message': 'activate your account and login', 'status_code': 400})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})

    @swagger_auto_schema(request_body=BookSerializer, responses={200: "Success"})
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
            return Response({'message': 'Admin access required', 'status_code': 400})
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
            return Response({'message': 'Admin access required', 'status_code': 400})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class BookByPriceAPI(APIView):

    @method_decorator(cache_page(60 * 60))
    @method_decorator(token_required)
    def get(self, request, user_id, page):
        try:
            user = User.objects.filter(pk=user_id).first()
            if user:
                all_books = Book.objects.all().order_by('price').values()
                paginator = Paginator(all_books, 2)

                page_obj = paginator.get_page(page)

                data = []
                for kw in page_obj.object_list:
                    data.append({"name": kw.get('name'), "author": kw.get('author'), 'price': kw.get('price'),
                                 'book_quantity': kw.get('book_quantity')})
                payload = {
                    "page": {
                        "current page": page_obj.number,
                        "next page exists": page_obj.has_next(),
                        "previous page exists": page_obj.has_previous(),
                    },
                    "data": data
                }

                return Response({'message': 'fetched books details', 'status_code': 200, 'data': payload})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})
