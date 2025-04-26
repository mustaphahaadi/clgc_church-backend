from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("users",UserView,basename="users-view")
router.register("fellowships",FellowViewset,basename="fellowship")

urlpatterns = [
    path("fellowships/my/",GetMyFellowship.as_view(),name="get-my-fellowship"),
    path("users/update/<str:username>/",UpdateUserDetailView.as_view(),name="update-specific-user-details"),
    path("profiles/",ProfileView.as_view(),name="profile-view"),
    path("join-fellowship", JoinFellowShip.as_view(), name="join-fellowship")
]

urlpatterns += router.urls