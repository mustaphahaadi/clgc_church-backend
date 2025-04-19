from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path("",PrayerRequestListView.as_view(),name="list-prayer-requests"),
    path("create/",CreatePrayerRequests.as_view(),name="create-prayer-request"),
    path("delete/<int:pk>/",PrayerRequestDeleteView.as_view(),name="delete-prayer-request"),
    path("<int:pk>/",PrayerRequestRetrieveView.as_view(),name="retrieve-prayer-request"),
    path("update/<int:pk>/",PrayerRequestUpdateView.as_view(),name="update-prayer-request"),
    path("my/",MyPrayerRequests.as_view(),name="my-prayer-requests")
]