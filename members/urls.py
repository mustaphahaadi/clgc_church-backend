from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'testimonies', views.TestimonyViewSet)

urlpatterns = [
    # Authentication endpoints
    # path('auth/signup/', views.SignupView.as_view(), name='signup'),
    # path('auth/login/', views.LoginView.as_view(), name='login'),
    
    # Profile endpoints
    path('user/complete-profile/', views.ProfileCompletionView.as_view(), name='profile-completion'),
    path('user/profile/', views.ProfileView.as_view(), name='user-profile'),
    
    # Contact form endpoint
    path('contacts/', views.create_contact, name='create_contact'),
    
    # Member registration
    path('members/', views.create_member, name='create_member'),
    
    # Include router URLs
    path('', include(router.urls)),
]