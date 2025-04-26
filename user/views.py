from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *

from .models import CustomUser, Profile, Fellowship
from utils.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly,IsAdminOrSuperuser

class FellowViewset(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,IsAdminOrReadOnly,)
    serializer_class = FellowshipSerializer
    queryset = Fellowship.objects.all()

class GetMyFellowship(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_clas = FellowshipSerializer

    def get_profile(self,user):
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None

    def get_fellowship(self,id):
        try:
            return Fellowship.objects.get(id=id)
        except Fellowship.DoesNotExist:
            return None
        
    def get(self,request,*args,**kwargs):
        profile = self.get_profile(request.user)

        if profile == None:
            return Response({"error":"profile not found"},status=status.HTTP_400_BAD_REQUEST)
        
        fellowship = self.get_fellowship(profile.fellowship.id)
        if fellowship == None:
            return Response({"error":"fellowship cannot be found"},status=status.HTTP_400_BAD_REQUEST)
        
        data = FellowshipSerializer(fellowship).data
        return Response(data,status=status.HTTP_200_OK)
        
class JoinFellowShip(APIView):
    permission_classes = (IsAuthenticated,)
    serializers = JoinFellowshipSerializer

    @swagger_auto_schema(request_body=JoinFellowshipSerializer)
    def post(self,request,*args,**kwargs):
        serializer = self.serializers(data=request.data)

        # Add fellowship to user profile
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get("username")
            fellowship = serializer.validated_data.get("fellowship")
            username_object = CustomUser.objects.get(username=username)
            fellowship_object = Fellowship.objects.get(name=fellowship)

            profile = Profile.objects.get(user=username_object)
            profile.fellowship = fellowship_object
            profile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserView(ModelViewSet):
    permission_classes = (IsAdminOrSuperuser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UpdateUserDetailView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    def get_user(self,username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None
    @swagger_auto_schema(request_body=UserSerializer, responses={200: ProfileSerializer})
    def patch(self, request,username, *args, **kwargs):
        user = self.get_user(username=username)
        if user != None:
            serializer = self.serializer_class(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response({"error":"User cannot be found"},status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializers = ProfileSerializer
    
    def get_profile(self, user):
        try:
            # profile = get_object_or_404(Profile,user)
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None
    
    def get_fellowship(self,fellowship):
        try:
            return Fellowship.objects.get(id=fellowship)
        except Fellowship.DoesNotExist:
            return None
        
    @swagger_auto_schema(responses={200: ProfileSerializer})
    def get(self, request,*args, **kwargs):
        profile = self.get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not complete"}, status=status.HTTP_404_NOT_FOUND)
        
        fellowship = self.get_fellowship(fellowship=profile.fellowship.id)
        serializer = self.serializers(profile)
        # serializer.data["fellowships"] = fellowship
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
    