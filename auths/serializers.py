from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.validators import ValidationError
from user.models import CustomUser
from .profile_serializer import ProfileSerializer

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
            raise ValidationError({"error":"User does not exist"})
        
        if user.last_login == None:
            user.is_active = True
            user.save()

        
        data = super().validate(attrs)
        print(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['username'] = user.username
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
    


