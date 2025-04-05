from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.validators import ValidationError
from user.models import CustomUser


class LoginSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    username_field = "username"

    class Meta:
        model = CustomUser
        fields = [
            "username","password"
        ]
    
    def validate(self, attrs):
        username = attrs.get("username")
        try:
            user = CustomUser.objects.get(username=username)

        except CustomUser.DoesNotExist:
            raise ValidationError({"error":"Invalid credentials"})
        
        if user.last_login == None:
            user.is_active = True
            user.save()

        
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['user'] = {
            "username":user.username,
            "first_name":user.first_name,
            "middle_name":user.middle_name,
            "last_name":user.last_name,
            "telephone":user.telephone,
            "profileComplete":user.profile_complete,
            "email":user.email
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "username",
            "telephone",
            "country_code",
            "password",
            "confirm_password",
        ]

        # write_only_fields = [
        #     "password","confirm_password"
        # ]
    
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise ValidationError({"password":"Password does not match"})
        
        return super().validate(attrs)
    
    def save(self, **kwargs):
        user = CustomUser.objects.create_user(
            **kwargs
        )
        return True
class OtpSerializer(serializers.Serializer):
    otp  = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        fields = [
            "email",
            "otp"
        ]

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = [
            "email"
        ]

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    class Meta:
        fields = [
            "email","new_password","confirm_password"
        ]
        pass
    
    def validate(self, attrs):
        email = attrs.get("email")
        user = CustomUser.object.get(email=email)
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            return ValidationError("error","passwords do not match")
        
        if new_password == user.check_password(new_password):
            return ValidationError("error","new password must not be same as old password")
        return super().validate(attrs)

class ResendOtpSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    class Meta:
        fields = [
            "email",
        ]

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    class Meta:
        fields = [
            "refresh",
        ]