from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from user.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer


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
