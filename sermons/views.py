from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser

from .models import Sermon
from .serializers import SermonSerializer
from .permissions import IsAdminOrReadOnly

class SermonViewset(ModelViewSet):
    parser_classes = (MultiPartParser,FormParser)
    permission_classes = (IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer