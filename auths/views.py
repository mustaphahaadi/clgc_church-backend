from django.db.models import Q

# Create your views here.
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
import pyotp

from user.models import CustomUser
from .serializers import *
from utils.helpers import *

class GenerateOtp:
    @staticmethod
    def handler(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret,interval=86400)
        otp_code = totp.now()
        return {"secret":secret,"otp":otp_code}
    
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

class OtpVerification(APIView):
    permission_classes= (AllowAny,)
    @swagger_auto_schema(request_body=OtpSerializer)

    def post(self,request,*args,**kwars):
        serializer = OtpSerializer(data=request.data) # serialzier request

        if serializer.is_valid(raise_exception=True): # validate serialized data
            try:
                # get otp_code and email from request data
                otp_code = serializer.validated_data["otp"] 
                email = serializer.validated_data["email"]
                user = CustomUser.objects.get(Q(otp_code=otp_code) & Q(email=email))
                
                # Validate Otp
                is_valid_otp = pyotp.TOTP(user.secret,interval=86400)
                verify = is_valid_otp.verify(otp_code)

                if verify:
                    user.is_active = True # activate user"s account
                    user.save()
                    first_name = user.first_name

                    send_success_email(first_name,email)
                    return Response({"sucess":"otp verification successful"},status=status.HTTP_200_OK)
                
                return  Response({"error":"invalid otp code"},status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return  Response({"error":"user cannot be found"},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"Invalid request"},status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    seriailizers = ForgotPasswordSerializer

    @swagger_auto_schema(request_body=ForgotPasswordSerializer,responses={200:ForgotPasswordSerializer})
    def post(self,request,*args,**kwargs):
        serializer = self.seriailizers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]

            try:
                user = CustomUser.objects.get(email=email)
                otp_result = GenerateOtp.handler()

                secret = otp_result.get("secret")
                otp_code = otp_result.get("otp_code")

                user.activation_code = secret
                user.otp_code = otp_code
                user.save()
            except CustomUser.DoesNotExist:
                return Response({"error":"email cannot be found"},status=status.HTTP_400_BAD_REQUEST)

            send_otp(user.first_name,email,otp_code)    
            return Response({"success":"Reset Password is successful"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializers = ResetPasswordSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]

            try:
                user = CustomUser.objects.get(email=email)
                new_password = serializer.validated_data["new_password"]
                user.set_password(new_password)
                user.save()
            except CustomUser.DoesNotExist:
                return Response({"error":"email cannot be found"},status=status.HTTP_400_BAD_REQUEST)

            send_reset_password_success(user.first_name,email) 
            return Response({"success":"Reset Password is successful"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ReSendOtp(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(request_body=ResendOtpSerializer)

    def post(self,request,*args,**kwars):
        serializers = ResendOtpSerializer(data=request.data)

        # verify seriailzed data
        if serializers.is_valid(raise_exception=True):
            try:
                # get user using email
                email = serializers.validated_data["email"]

                otp_result = GenerateOtp.result()

                user = CustomUser.objects.get(email=email)

                user.otp_code = otp_result["otp_code"]
                user.secret = otp_result["secret"]
                
                first_name = user.full_name.split(" ")[0]
                send_otp(first_name,email, otp_result["otp_code"])
                
                user.save()
                return Response({"success":"Otp sent. Check your email"},status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return  Response({"error":"user cannot be found"},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error":"Invalid request"},status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(TokenBlacklistView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        pass