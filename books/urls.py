from django.urls import path

from . import views

urlpatterns = [
    path('addbook/', views.AddBookAPI.as_view(), name='add_book'),
    path('book/', views.GetBookAPI.as_view(), name='book'),
    path('book/<str:id>/', views.GetBookAPI.as_view(), name='book_by_id'),
]
