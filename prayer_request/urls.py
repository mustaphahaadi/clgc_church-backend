from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrayerRequestView

router = DefaultRouter();
router.register("",PrayerRequestView,basename="prayer-request")

urlpatterns = [
    path("",include(router.urls)),
]