from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserView, ProfileView, FellowViewset,JoinFellowShip,UpdateUserDetailView

router = DefaultRouter()

router.register("users",UserView,basename="users-view")
router.register("fellowships",FellowViewset,basename="fellowship")

urlpatterns = [
    path("users/update/<str:username>/",UpdateUserDetailView.as_view(),name="update-specific-user-details"),
    path("profiles/",ProfileView.as_view(),name="profile-view"),
    path("join-fellowship", JoinFellowShip.as_view(), name="join-fellowship")
]

urlpatterns += router.urls