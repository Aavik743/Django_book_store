from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.OrderAPI.as_view(), name='checkout'),
    path('get-orders/', views.GetOrderAPI.as_view(), name='get-orders'),
]
