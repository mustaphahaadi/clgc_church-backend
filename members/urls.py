from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'testimonies', views.TestimonyViewSet)

urlpatterns = [
    # Contact form endpoint
    path('contacts/', views.ContactUsView.as_view(), name='create_contact'),
    path("my/testimonies/",views.UserTestimoniesView.as_view(),name="my-testimonies"),

    
    # Include router URLs
    path('', include(router.urls)),
]