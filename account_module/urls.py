from django.urls import path
from .views import (RegisterView, LoginView, VerifyOTPView,
                     ResendOTPView, LogoutView, ForgotPasswordView, ResetPasswordView)
app_name = 'account_module'
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('verify/',VerifyOTPView.as_view(),name='verify_otp'),
    path('resend-otp/',ResendOTPView.as_view(),name='resend_otp'),
    path('forgot-password/',ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset_password'),
    path('logout/',LogoutView.as_view(),name='logout'),
]