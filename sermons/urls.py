from rest_framework.routers import DefaultRouter
from .views import SermonViewset

router = DefaultRouter()
router.register("",SermonViewset,basename="sermon-view")

urlpatterns = router.urls