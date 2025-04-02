from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'testimonies', views.TestimonyViewSet)

urlpatterns = [
    # Contact form endpoint
    path('contacts/', views.create_contact, name='create_contact'),

    
    # Include router URLs
    path('', include(router.urls)),
]