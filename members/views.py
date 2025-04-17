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
from .permissions import IsOwnerOrReadOnly

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
    

@api_view(['POST'])
@permission_classes([AllowAny])
def create_testimony(request):
    if request.method == 'POST':
        # Add user to request data if authenticated
        data = request.data.copy()
        if request.user.is_authenticated:
            data['user'] = request.user.id
        
        serializer = TestimonySerializer(data=data)
        if serializer.is_valid():
            testimony = serializer.save()
            
            # Send email notification
            try:
                send_mail(
                    'New Testimony Submitted',
                    f'A new testimony has been submitted by {testimony.user.username if testimony.user else "Anonymous"}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass  # Don't fail if email sending fails
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_contact(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
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
                pass  # Don't fail if email sending fails
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_member(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Check if member already exists
        if CustomUser.objects.filter(user=user).exists():
            return Response({'error': 'Member already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create new member
        member = CustomUser.objects.create(user=user)
        
        serializer = UserSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)