from rest_framework import serializers
from members.profile_model import Profile
from user.models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'house_address', 'digital_address',
            'occupation', 'church_information', 'profile_image',
            'fellowship', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'email', 'created_at', 'updated_at']
    
    def get_username(self, obj):
        return obj.user.username if obj.user else None
    
    def get_email(self, obj):
        return obj.user.email if obj.user else None
    
    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else None
    
    def validate_date_of_birth(self, value):
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 13:
            raise serializers.ValidationError('You must be at least 13 years old')
        return value