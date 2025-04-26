from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .serializers import *
from utils.permissions import IsOwnerOrReadOnly

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Testimony Views
class TestimonyViewSet(viewsets.ModelViewSet):
    queryset = Testimony.objects.all()
    serializer_class = TestimonySerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]  # Allow anyone to view testimonies
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserTestimoniesView(APIView):
    permission_classes= (IsAuthenticated,IsOwnerOrReadOnly)
    serializers = TestimonySerializer

    def get_testimony(self, user):
        # find his/her testimony
        try:
            return Testimony.objects.filter(user=user)
        except Profile.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200:TestimonySerializer})
    def get(self,request,*args,**kwargs):
        testimony = self.get_testimony(request.user)
        if testimony == None:
            return Response([], status=status.HTTP_200_OK)
        
        serializer = self.serializers(testimony,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ContactUsView(APIView):
    permission_classes = (AllowAny,)
    serializer = ContactSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Send email notification
            try:
                send_mail(
                    f'New Contact Form Submission: {contact.subject}',
                    f'Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\n\nMessage:\n{contact.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
                
                # Send confirmation to user if email provided
                if contact.email:
                    send_mail(
                        'Thank you for contacting City of Light Global Church',
                        'We have received your message and will get back to you soon.',
                        settings.DEFAULT_FROM_EMAIL,
                        [contact.email],
                        fail_silently=True,
                    )
            except Exception:
                return Response({"error":"mail not found"},status=status.HTTP_400_BAD_REQUEST)  # Don't fail if email sending fails
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
