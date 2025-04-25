from rest_framework import serializers

from .models import CustomUser, Profile,Fellowship

class FellowshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fellowship
        fields = "__all__"

class JoinFellowshipSerializer(serializers.Serializer):
    username = serializers.CharField()
    fellowship = serializers.CharField()

    class Meta:
        fields = [
            "username","fellowship"
        ]
    
    def validate_username(self,value):
        # check if user exists
        if CustomUser.objects.filter(username=value).exists():
            user = CustomUser.objects.get(username=value)
        else:
            serializers.ValidationError("user cannot be found")
            

        # check if user profile exists
        try:
            if Profile.objects.filter(user=user).exists():
                return value
        except:
            serializers.ValidationError("profile cannot be found")
        

    def validate_fellowship(self,value):
        try:
            if Fellowship.objects.filter(name=value):
                return value;
        except:
            serializers.ValidationError("fellowship cannot be found")

        
    
class UserSerializer(serializers.ModelSerializer):
    profileComplete = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = [
            "username","email","first_name","middle_name","last_name","telephone","profileComplete","role",
            "last_login","gender"
        ]

    def get_profileComplete(self,obj):
        return obj.profile_complete

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    fellowship_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'house_address', 'digital_address',
            "martial_status","born_again",
            'occupation', 'church_information', 'profile_image',
            'fellowship', 'created_at', 'updated_at',"fellowship_name"
        ]
        read_only_fields = ['id', 'username', 'email', 'created_at', 'updated_at',"fellowship_name"]

        extra_kwargs = {
            'date_of_birth': {'required': True, 'error_messages': {'required': 'Date of birth is required'}},
            'house_address': {'required': True, 'error_messages': {'required': 'House address is required'}},
            'occupation': {'required': True, 'error_messages': {'required': 'Occupation is required'}},
            'digital_address': {'required': False},
            'church_information': {'required': False},
            'profile_image': {'required': False},
            'fellowship': {'required': False}
        }
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None
    
    def get_email(self, obj):
        return obj.user.email if obj.user else None
    
    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else None
    
    def get_fellowship_name(self, obj):
        return obj.fellowship.name if obj.fellowship else None
    
    def validate_date_of_birth(self, value):
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 13:
            raise serializers.ValidationError('You must be at least 13 years old')
        return value