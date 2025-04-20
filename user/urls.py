from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserView, ProfileView, FellowViewset,JoinFellowShip

router = DefaultRouter()

router.register("users",UserView,basename="users-view")
router.register("fellowships",FellowViewset,basename="fellowship")

urlpatterns = [
    path("profiles/",ProfileView.as_view(),name="profile-view"),
    path("join-fellowship", JoinFellowShip.as_view(), name="join-fellowship")
]

urlpatterns += router.urls