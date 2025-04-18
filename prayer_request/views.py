from rest_framework.viewsets import ModelViewSet
from .models import PrayerRequest
from .serializers import PrayerRequestSerializer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.
class PrayerRequestView(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PrayerRequestSerializer
    queryset = PrayerRequest.objects.all()

