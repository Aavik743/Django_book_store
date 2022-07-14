from django.urls import path

from . import views

urlpatterns = [
    path('wishlist/', views.AddToWishlistAPI.as_view(), name='add_to_wishlist'),
]
