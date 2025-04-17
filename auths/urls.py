from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView ,TokenVerifyView
from .views import *

urlpatterns = [
    path("login/",LoginView.as_view(),name="login-view"),
    path("register/",RegisterView.as_view(),name="register-view"),
    path("refresh/",TokenRefreshView.as_view(),name="refresh-token"),  
    path("verify/",TokenVerifyView.as_view(),name="token-verification"),
    path("otp/verification/",OtpVerification.as_view(),name="otp-verification"),
    path("otp/resend/",ReSendOtp .as_view(),name="otp-resend"), 
    path("logout/",LogoutView.as_view(),name="logout-view"),
]