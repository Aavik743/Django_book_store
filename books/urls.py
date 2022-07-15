from django.urls import path

from . import views

urlpatterns = [
    path('addbook/', views.AddBookAPI.as_view(), name='add_book'),
    path('book/', views.BookAPI.as_view(), name='book'),
    path('book/<str:id>/', views.BookAPI.as_view(), name='book_by_id'),
    path('book-by-price/<str:page>', views.BookByPriceAPI.as_view(), name='book_by_price'),
]
