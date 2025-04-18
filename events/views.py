from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView ,RetrieveAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Events
from .serializers import EventSerializers
from utils.permissions import IsAdminOrReadOnly, IsAdminOrSuperuser
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class ListEventView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializers
    queryset = Events.objects.all()

class CreateEventView(APIView):
    permission_classes = (IsAuthenticated,IsAdminOrSuperuser,)
    serializer_class = EventSerializers
    parser_classes = (MultiPartParser,)
    
    @swagger_auto_schema(request_body=EventSerializers)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"error":"unable to create event"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveEventView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EventSerializers
    queryset = Events.objects.all()
    lookup_field = "pk"

class UpdateEventView(UpdateAPIView):
    permission_classes = (IsAuthenticated,IsAdminOrSuperuser,)
    serializer_class = EventSerializers
    queryset = Events.objects.all()

class DestroyEventView(DestroyAPIView):
    permission_classes = (IsAuthenticated,IsAdminOrSuperuser,)
    serializer_class = EventSerializers
    queryset = Events.objects.all()
    lookup_field = "pk"