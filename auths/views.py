from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from user.models import CustomUser
from members.profile_model import Profile
from .serializers import RegisterSerializer, LoginSerializer
from .profile_serializer import ProfileSerializer


# Register View
class RegisterView(APIView):
    # grant permission to all
    permission_classes = (AllowAny,) # allows make sure to bring the comma
    serializers = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self,request,*args,**kwargs):
        serializer = self.serializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data.pop("confirm_password")
            
            serializer.save(**serializer.validated_data)
            return Response(serializer.validated_data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializers = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer,)
    def post(self,request,*args,**kwargs):
        serializer = self.serializers(data=request.data)
        data = serializer.validate(request.data)
        if serializer.is_valid(raise_exception=True) and data:
            
            return Response(data,status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors,status=status.HTTP_401_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers = ProfileSerializer
    
    def get_profile(self, user):
        try:
            # profile = get_object_or_404(Profile,user)
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None
    
    @swagger_auto_schema(responses={200: ProfileSerializer})
    def get(self, request,*args, **kwargs):
        profile = self.get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializers(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=ProfileSerializer, responses={200: ProfileSerializer})
    def put(self, request, *args, **kwargs):
        profile = self.get_profile(request.user)
        if not profile:
            # Create a new profile if it doesn't exist
            profile = Profile.objects.create(user=request.user)
        
        serializer = self.serializers(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=ProfileSerializer, responses={200: ProfileSerializer})
    def patch(self, request, *args, **kwargs):
        profile = self.get_profile(request.user)
        if not profile:
            # Create a new profile if it doesn't exist
            profile = Profile.objects.create(user=request.user)
        
        serializer = self.serializers(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProfileSerializer, responses={201: ProfileSerializer})
    def post(self, request, *args, **kwargs):
        # Check if profile already exists
        profile = self.get_profile(request.user)
        if profile:
            return Response(
                {"error": "Profile already exists. Use PUT or PATCH to update."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new profile
        serializer = self.serializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)