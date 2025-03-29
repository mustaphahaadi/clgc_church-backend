from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path("login/",LoginView.as_view(),name="login-view"),
    path("register/",RegisterView.as_view(),name="register-view"),
    path("refresh/",TokenRefreshView.as_view(),name="refresh-token"),
    path("profile/",ProfileView.as_view(),name="profile-view"),
]