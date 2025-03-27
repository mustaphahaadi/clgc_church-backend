from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from .models import Member, Contact, Testimony, CustomUser
from .profile_model import Profile
from .serializers import MemberSerializer, ContactSerializer, UserSerializer, ProfileSerializer, TestimonySerializer
from .forms import TestimonyForm
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Authentication Views
class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            with transaction.atomic():
                # Extract user data from request
                user_data = {
                    'first_name': request.data.get('firstName'),
                    'middle_name': request.data.get('middleName'),
                    'last_name': request.data.get('lastName'),
                    'username': request.data.get('username'),
                    'email': request.data.get('email'),
                    'phone_number': request.data.get('phoneNumber'),
                    'country_code': request.data.get('countryCode', '+233'),
                    'gender': request.data.get('gender'),
                }
                
                # Validate password
                password = request.data.get('password')
                if not password:
                    return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Create user with serializer
                serializer = UserSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()
                    user.set_password(password)
                    user.save()
                    
                    # Generate tokens
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        'user': serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'profileComplete': user.profile_complete
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'profileComplete': user.profile_complete
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Profile Views
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            user_serializer = UserSerializer(user)
            
            # Get profile if it exists
            try:
                profile = Profile.objects.get(user=user)
                profile_serializer = ProfileSerializer(profile)
                return Response({
                    'user': user_serializer.data,
                    'profile': profile_serializer.data,
                    'profileComplete': user.profile_complete
                }, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({
                    'user': user_serializer.data,
                    'profile': None,
                    'profileComplete': False
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileCompletionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        try:
            user = request.user
            
            # Create or update profile
            profile_data = {
                'date_of_birth': request.data.get('dateOfBirth'),
                'house_address': request.data.get('houseAddress'),
                'digital_address': request.data.get('digitalAddress'),
                'occupation': request.data.get('occupation'),
                'church_information': request.data.get('churchInformation'),
                'fellowship': request.data.get('fellowship'),
            }
            
            # Handle profile image
            if 'profileImage' in request.FILES:
                profile_data['profile_image'] = request.FILES['profileImage']
            
            # Get or create profile
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Update profile with serializer
            serializer = ProfileSerializer(profile, data=profile_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Update user's profile_complete status
                user.profile_complete = True
                user.save()
                
                # Return updated user data
                user_serializer = UserSerializer(user)
                return Response({
                    'user': user_serializer.data,
                    'profile': serializer.data,
                    'profileComplete': True
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        if Member.objects.filter(user=user).exists():
            return Response({'error': 'Member already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create new member
        member = Member.objects.create(user=user)
        
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)