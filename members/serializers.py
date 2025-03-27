from rest_framework import serializers
from .models import Member, Contact, Testimony
from .custom_user_model import CustomUser
from .profile_model import Profile

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'middle_name': {'required': False},
            'office_address': {'required': False},
            'prayer_request': {'required': False}
        }

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True, 'error_messages': {'required': 'Name is required'}},
            'message': {'required': True, 'error_messages': {'required': 'Message is required'}},
            'subject': {'required': True, 'error_messages': {'required': 'Subject is required'}},
            'phone': {'required': True, 'error_messages': {'required': 'Phone number is required'}},
            'email': {'required': False}
        }

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('Phone number must contain only digits')
        return value

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('Message must be at least 10 characters long')
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'middle_name', 'last_name', 'email', 
                 'phone_number', 'country_code', 'gender', 'profile_complete']
        extra_kwargs = {
            'password': {'write_only': True},
            'middle_name': {'required': False},
            'email': {'required': False},
            'first_name': {'required': True, 'error_messages': {'required': 'First name is required'}},
            'last_name': {'required': True, 'error_messages': {'required': 'Last name is required'}},
            'username': {'required': True, 'error_messages': {'required': 'Username is required'}},
            'phone_number': {'required': True, 'error_messages': {'required': 'Phone number is required'}},
            'gender': {'required': True, 'error_messages': {'required': 'Gender is required'}}
        }

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Username must be at least 3 characters long')
        return value

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('Phone number must contain only digits')
        return value

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'visit_date', 'date_of_birth', 'house_address', 
                 'digital_address', 'occupation', 'church_information', 
                 'profile_image', 'fellowship', 'created_at', 'updated_at']
        read_only_fields = ['user', 'visit_date', 'created_at', 'updated_at']
        extra_kwargs = {
            'date_of_birth': {'required': True, 'error_messages': {'required': 'Date of birth is required'}},
            'house_address': {'required': True, 'error_messages': {'required': 'House address is required'}},
            'occupation': {'required': True, 'error_messages': {'required': 'Occupation is required'}},
            'digital_address': {'required': False},
            'church_information': {'required': False},
            'profile_image': {'required': False},
            'fellowship': {'required': False}
        }

    def validate_date_of_birth(self, value):
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 13:
            raise serializers.ValidationError('You must be at least 13 years old')
        return value

class TestimonySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Testimony
        fields = ['id', 'user', 'user_name', 'category', 'testimony', 'image', 'video', 'created_at']
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'category': {'required': True, 'error_messages': {'required': 'Category is required'}},
            'testimony': {'required': True, 'error_messages': {'required': 'Testimony content is required'}},
            'image': {'required': False},
            'video': {'required': False}
        }
    
    def get_user_name(self, obj):
        if obj.user:
            if obj.user.first_name and obj.user.last_name:
                return f"{obj.user.first_name} {obj.user.last_name}"
            return obj.user.username
        return "Anonymous"
        
    def validate_image(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:  # 5MB limit
                raise serializers.ValidationError('Image file too large. Size should not exceed 5MB.')
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError('Invalid file type. Only image files are allowed.')
        return value
        
    def validate_video(self, value):
        if value and len(value) > 100:  # Assuming video is stored as a URL/slug
            raise serializers.ValidationError('Video URL/slug is too long. Maximum 100 characters allowed.')
        return value