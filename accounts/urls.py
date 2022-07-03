from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegistrationAPI.as_view(), name='register'),
    path('activate/', views.ActivationAPI.as_view(), name='activate'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('forgot/', views.ForgotPasswordAPI.as_view(), name='forgot'),
    path('change/', views.ChangePasswordAPI.as_view(), name='change'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
]
