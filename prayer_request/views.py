from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PrayerRequest
from .serializers import PrayerRequestSerializer
from utils.permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class PrayerRequestListView(ListAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PrayerRequestSerializer
    queryset = PrayerRequest.objects.all()

class PrayerRequestRetrieveView(RetrieveAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PrayerRequestSerializer
    queryset = PrayerRequest.objects.all()
    lookup_field = "pk"

class PrayerRequestUpdateView(UpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PrayerRequestSerializer
    queryset = PrayerRequest.objects.all()
    lookup_field = "pk"

class PrayerRequestDeleteView(DestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PrayerRequestSerializer
    queryset = PrayerRequest.objects.all()
    lookup_field = "pk"

class MyPrayerRequests(APIView):
    permission_classes = (IsAuthenticated,)
    serializers = PrayerRequestSerializer

    def get(self,request,*args,**kwargs):
        query = PrayerRequest.objects.filter(author=request.user)
        if query != []:
            serializer_data = self.serializers(query,many=True).data
            return Response(serializer_data,status=200)
        
        return Response({"data":[]},status=200)
    
class CreatePrayerRequests(APIView):
    permission_classes = (IsAuthenticated,)
    serializers = PrayerRequestSerializer

    @swagger_auto_schema(request_body=PrayerRequestSerializer)
    def post(self,request,*args,**kwargs):
        serializer = self.serializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = PrayerRequest(
                author=request.user
            )
            data.save(**serializer.validated_data)

            return Response({"success":"Prayer Request created successfully"},status=200)
        return Response({"error":"Prayer Request created failed"},status=500)

