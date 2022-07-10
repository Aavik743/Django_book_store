from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.jwt import token_required
from .models import Order
from .serializers import OrderSerializer, GetOrderSerializer
from common import logger, custom_exceptions


class OrderAPI(APIView):  # cart.delete not working

    @method_decorator(token_required)
    def post(self, request, user_id):  # cart_id, address
        try:
            data = request.data.copy()
            data.update({'user': user_id})

            order_serializer = OrderSerializer(data=data)
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()

            return Response({'message': f'order has been placed by user id {user_id}', "status_code": 201,
                             "data": order_serializer.data})
        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})


class GetOrderAPI(APIView):

    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            if user_id:
                order = Order.objects.filter(user__id=user_id)

                if not order:
                    raise custom_exceptions.CartDoesNotExist('Create order at first', 400)
                if order:
                    cart_serializer = GetOrderSerializer(order, many=True)

                    return Response({'message': 'cart fetched', 'status_code': 200, 'data': cart_serializer.data},
                                    status=status.HTTP_200_OK)

        except Exception as e:
            logger.logging.error('Log Error Message')
            return Response({'message': str(e), 'status_code': 400})
