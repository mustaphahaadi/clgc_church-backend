from django.urls import path
from .views import *


urlpatterns = [
    path("", ListEventView.as_view(),name="List-events"),
    path("create/",CreateEventView.as_view(),name="create-events"),
    path("<int:pk>/",RetrieveEventView.as_view(),name="retrieve-events"),
    path("update/",UpdateEventView.as_view(),name="update-events"),
    path("<int:pk>/",RetrieveEventView.as_view(),name="retrieve-events"),
    path("<int:pk>/delete/",DestroyEventView.as_view(),name="detroy-events"),
]