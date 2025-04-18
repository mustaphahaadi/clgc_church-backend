from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, FellowshipSerializer

from .models import CustomUser, Profile, Fellowship
from utils.permissions import IsAdminOrReadOnly

class FellowViewset(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)
    serializer_class = FellowshipSerializer
    queryset = Fellowship.objects.all()

class UserView(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()



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
            return Response({"error": "Profile not complete"}, status=status.HTTP_404_NOT_FOUND)
        
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
    