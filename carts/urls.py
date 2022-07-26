from django.urls import path

from . import views

urlpatterns = [
    path('addcart/', views.AddToCartAPI.as_view(), name='add_to_cart'),
    path('getcart/', views.CartAPI.as_view(), name='get_cart'),
    path('cart/>', views.UpdateCartAPI.as_view(), name='cart'),
]
